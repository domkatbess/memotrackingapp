"""Shared test fixtures: async SQLite database, session with rollback, and httpx test client."""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB

from app.models.base import Base

# ---------------------------------------------------------------------------
# Register SQLite-compatible compilation for PostgreSQL-specific types
# ---------------------------------------------------------------------------

@compiles(PG_UUID, "sqlite")
def compile_pg_uuid_for_sqlite(type_, compiler, **kw):
    """Render PostgreSQL UUID as VARCHAR(36) on SQLite."""
    return "VARCHAR(36)"


@compiles(PG_JSONB, "sqlite")
def compile_pg_jsonb_for_sqlite(type_, compiler, **kw):
    """Render PostgreSQL JSONB as JSON on SQLite."""
    return "JSON"


# ---------------------------------------------------------------------------
# Test database engine (SQLite async via aiosqlite)
# ---------------------------------------------------------------------------
TEST_DATABASE_URL = "sqlite+aiosqlite://"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

TestSessionFactory = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ---------------------------------------------------------------------------
# Session-scoped: create / drop all tables once per test session
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
async def _create_tables():
    """Create all tables at the start of the test session and drop them at the end."""
    # Import all models so Base.metadata knows about every table
    import app.models  # noqa: F401

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


# ---------------------------------------------------------------------------
# Per-test: provide an async session wrapped in a SAVEPOINT that is rolled back
# ---------------------------------------------------------------------------
@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async session that rolls back all changes after each test.

    Uses a nested transaction (SAVEPOINT) so that the test can call
    ``session.commit()`` without actually persisting data.
    """
    async with test_engine.connect() as connection:
        transaction = await connection.begin()
        session = AsyncSession(bind=connection, expire_on_commit=False)

        # Start a SAVEPOINT so that session.commit() inside the test
        # only commits to the savepoint, not the outer transaction.
        nested = await connection.begin_nested()

        @event.listens_for(session.sync_session, "after_transaction_end")
        def _restart_savepoint(sess, trans):
            """Re-open a SAVEPOINT after the previous one ends."""
            if trans.nested and not trans._parent.nested:
                sess.begin_nested()

        yield session

        await session.close()
        await transaction.rollback()


# ---------------------------------------------------------------------------
# Per-test: httpx AsyncClient wired to the FastAPI app with session override
# ---------------------------------------------------------------------------
@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provide an httpx AsyncClient whose requests use the test database session."""
    from app.core.database import get_session
    from app.main import create_app

    app = create_app()

    # Override the get_session dependency so all requests use the test session
    async def _override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = _override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
