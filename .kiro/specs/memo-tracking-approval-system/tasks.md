# Implementation Plan: Memo Tracking and Approval System

## Overview

This plan implements the Memo Tracking and Approval System in three phases: Phase 1 (Core Backend without AWS), Phase 2 (AWS Integration), and Phase 3 (React Native for Web Frontend). Each task builds incrementally on previous work. All external services use abstraction interfaces (ABCs) with local/mock implementations first, then AWS adapters. The backend uses Python with FastAPI, PostgreSQL, and Hypothesis for property-based testing.

## Tasks

- [x] 1. Set up project structure, configuration, and database foundation
  - [x] 1.1 Initialize FastAPI project with directory structure and dependencies
    - Create project root with `app/` package containing: `api/`, `core/`, `models/`, `schemas/`, `services/`, `engines/`, `interfaces/`, `adapters/`, `tests/`
    - Set up `pyproject.toml` or `requirements.txt` with: fastapi, uvicorn, sqlalchemy[asyncio], asyncpg, alembic, pydantic, python-jose, hypothesis, pytest, pytest-asyncio, httpx, factory-boy
    - Create `app/core/config.py` with Pydantic Settings for database URL, JWT secret, CORS origins, file upload limits, feature toggle defaults
    - Create `app/main.py` with FastAPI app instance, CORS middleware, and exception handlers
    - _Requirements: 14.1, 14.2, 14.4_

  - [x] 1.2 Create SQLAlchemy models and Alembic migrations for all database tables
    - Define SQLAlchemy async models for: `users`, `face_profiles`, `speaker_profiles`, `memo_categories`, `approval_titles`, `roles`, `role_permissions`, `approval_title_roles`, `approval_workflows`, `approval_stages`, `memos`, `memo_attachments`, `memo_approval_snapshots`, `approval_actions`, `audit_logs`, `notifications`, `feature_toggles`
    - Set up all indexes, unique constraints, and foreign key relationships as specified in the design
    - Configure Alembic for async migrations and create initial migration
    - Enforce audit_logs table immutability (no UPDATE/DELETE at application level)
    - _Requirements: 9.5, 14.1_

  - [x] 1.3 Set up test infrastructure and database fixtures
    - Configure pytest with pytest-asyncio for async test support
    - Create test database setup with transaction rollback per test
    - Set up Factory Boy factories for all models
    - Configure Hypothesis settings (max_examples=100)
    - Create shared test utilities and fixtures (test client, authenticated sessions, seed data)
    - _Requirements: 14.1_

- [ ] 2. Implement service abstraction interfaces and local/mock implementations
  - [ ] 2.1 Define all service abstraction interfaces (ABCs)
    - Create `app/interfaces/storage_interface.py` — StorageInterface with upload_file, download_file, delete_file, get_file_url
    - Create `app/interfaces/face_recognition_interface.py` — FaceRecognitionInterface with detect_faces, index_face, compare_faces, search_faces_by_image, delete_faces
    - Create `app/interfaces/voice_transcription_interface.py` — VoiceTranscriptionInterface with transcribe_audio
    - Create `app/interfaces/voice_command_interface.py` — VoiceCommandInterface with parse_command
    - Create `app/interfaces/text_to_speech_interface.py` — TextToSpeechInterface with synthesize_speech
    - Create `app/interfaces/notification_interface.py` — NotificationInterface with send_email
    - Include all dataclasses: FaceMatch, TranscriptionResult, CommandIntent, EmailMessage
    - _Requirements: 15.7_

  - [ ] 2.2 Implement local/mock adapters for all interfaces
    - Create `app/adapters/local/` with: LocalStorageAdapter (filesystem-based), MockFaceRecognitionAdapter, MockVoiceTranscriptionAdapter, MockVoiceCommandAdapter, MockTextToSpeechAdapter, MockNotificationAdapter (log-based)
    - Each mock returns deterministic, configurable responses for testing
    - Create dependency injection setup in `app/core/dependencies.py` to wire interfaces to local adapters
    - _Requirements: 15.7_

- [ ] 3. Implement RBAC, roles, permissions, and approval titles
  - [ ] 3.1 Implement role and permission management service
    - Create `app/services/role_service.py` with CRUD for roles and role_permissions
    - Seed system roles on startup: Superuser, Administrator, Submitter, Approver
    - Implement permission checking logic that resolves user → approval_title → roles → permissions
    - Create Pydantic schemas for role creation, update, and response
    - _Requirements: 11.1, 11.2, 11.5_

  - [ ] 3.2 Implement approval title management service
    - Create `app/services/approval_title_service.py` with CRUD for approval_titles
    - Implement role assignment to approval titles (approval_title_roles)
    - Enforce unique approval title names
    - Enforce each user belongs to exactly one approval title
    - Create Pydantic schemas for approval title creation, update, and response
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [ ] 3.3 Implement RBAC middleware and permission decorators
    - Create `app/core/auth.py` with JWT token creation, validation, and refresh
    - Create `app/core/rbac.py` with permission-checking dependency that resolves permissions from user's approval_title → roles → permissions
    - Implement `require_permission(permission_string)` FastAPI dependency
    - Implement `require_role(role_name)` FastAPI dependency for Superuser-only endpoints
    - Ensure permission changes propagate immediately (no caching of stale permissions)
    - _Requirements: 11.1, 11.3, 11.4, 11.6, 11.7_

  - [ ] 3.4 Create API routes for roles and approval titles
    - Create `app/api/roles.py` with POST/GET/PATCH endpoints for roles
    - Create `app/api/approval_titles.py` with POST/GET/PATCH/DELETE endpoints for approval titles
    - Wire routes to services with RBAC enforcement (Admin only)
    - _Requirements: 4.1, 11.5_

  - [ ]* 3.5 Write property tests for RBAC and approval titles
    - **Property 9: Each approver belongs to exactly one approval title**
    - **Validates: Requirements 4.4**
    - **Property 10: Permission changes propagate immediately**
    - **Validates: Requirements 4.5, 11.6**
    - **Property 19: RBAC enforcement on all endpoints**
    - **Validates: Requirements 11.1, 11.3, 11.4, 11.7, 18.1, 18.2**


- [ ] 4. Implement audit logging service
  - [ ] 4.1 Create audit logging service and middleware
    - Create `app/services/audit_service.py` with `log_action(actor_id, action_type, target_entity_type, target_entity_id, description, metadata)` method
    - Ensure all required fields are captured: actor identity, action type, target entity, timestamp, description
    - Implement as a reusable dependency injectable into any service
    - Ensure audit log writes never block business operations (log errors to application log if audit write fails)
    - _Requirements: 9.1, 9.2, 9.3_

  - [ ] 4.2 Create audit log query API endpoint
    - Create `app/api/audit_logs.py` with GET endpoint supporting filters: actor, action_type, target_entity, date_range
    - Return paginated results
    - Enforce Admin-only access via RBAC
    - Enforce immutability — no UPDATE or DELETE endpoints
    - _Requirements: 9.4, 9.5_

  - [ ]* 4.3 Write property tests for audit logging
    - **Property 4: Comprehensive audit logging with required fields**
    - **Validates: Requirements 1.6, 5.6, 8.5, 9.1, 9.2, 9.3, 10.6, 18.6, 18.7, 19.8**
    - **Property 17: Audit log immutability**
    - **Validates: Requirements 9.5**

- [ ] 5. Implement feature toggles
  - [ ] 5.1 Create feature toggle service and middleware
    - Create `app/services/feature_toggle_service.py` with get_toggle, update_toggle, is_enabled methods
    - Seed default toggles on startup (e.g., `document_upload` defaults to enabled)
    - Create `app/core/feature_toggle.py` with `require_feature(toggle_key)` FastAPI dependency that returns 422 FEATURE_DISABLED when toggle is off
    - _Requirements: 8.1, 8.2, 8.3_

  - [ ] 5.2 Create feature toggle API endpoints
    - Create `app/api/feature_toggles.py` with GET (list all) and PATCH (update state) endpoints
    - Enforce Admin-only access
    - Log toggle state changes to audit log
    - _Requirements: 8.4, 8.5_

  - [ ]* 5.3 Write property test for feature toggles
    - **Property 16: Feature toggle controls endpoint access**
    - **Validates: Requirements 8.2, 8.3, 17.1, 17.3**

- [ ] 6. Checkpoint — Verify foundation
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement memo category management
  - [ ] 7.1 Create memo category service
    - Create `app/services/memo_category_service.py` with create, read, update, deactivate methods
    - Enforce unique category names
    - Require name and description on creation
    - Prevent new memos from being assigned to deactivated categories
    - Allow existing in-progress memos under deactivated categories to continue processing
    - Log all category changes to audit log
    - Create Pydantic schemas for category creation, update, and response
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ] 7.2 Create memo category API endpoints
    - Create `app/api/memo_categories.py` with POST, GET (list), GET (detail), PATCH, POST deactivate endpoints
    - Enforce Admin-only access for create/update/deactivate, Authenticated for read
    - _Requirements: 2.1_

  - [ ]* 7.3 Write property tests for memo categories
    - **Property 5: Category name uniqueness and required fields**
    - **Validates: Requirements 2.2, 2.3**
    - **Property 6: Deactivated category blocks new memos but allows existing memo processing**
    - **Validates: Requirements 2.4, 2.5**

- [ ] 8. Implement configurable approval workflows
  - [ ] 8.1 Create workflow engine service
    - Create `app/engines/workflow_engine.py` implementing the WorkflowEngine class from the design
    - Implement configure_workflow: create/update approval workflow with ordered stages for a category
    - Validate each stage references a valid, existing approval title
    - Enforce unique stage_order within a workflow
    - Implement workflow versioning — increment version on each modification
    - Allow reorder, add, remove of stages
    - Prevent submission if workflow has zero stages
    - Log workflow changes to audit log
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [ ] 8.2 Create workflow API endpoints
    - Create `app/api/approval_workflows.py` with GET and PUT endpoints under `/memo-categories/{id}/workflow`
    - Enforce Admin-only access
    - _Requirements: 3.1, 3.5_

  - [ ]* 8.3 Write property tests for approval workflows
    - **Property 7: Workflow stage ordering and title validation**
    - **Validates: Requirements 3.1, 3.3**
    - **Property 8: Workflow changes do not affect in-progress memos**
    - **Validates: Requirements 3.4**

- [ ] 9. Implement memo CRUD and submission
  - [ ] 9.1 Create memo service
    - Create `app/services/memo_service.py` with create, read, update, submit, search methods
    - Validate all mandatory fields on creation: title, body, category_id, priority
    - Return field-level errors for invalid/missing fields
    - Generate unique tracking numbers on submission
    - On submit: snapshot the current workflow stages into `memo_approval_snapshots`, set workflow_version, route to stage 1
    - Reject submission if category is deactivated or workflow has no stages
    - Only allow updates to memos in draft or revision_requested status
    - Log memo creation and submission to audit log
    - Create Pydantic schemas for memo creation, update, submission, and response
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [ ] 9.2 Create memo API endpoints
    - Create `app/api/memos.py` with POST (create), GET (search/filter), GET (detail), PATCH (update), POST submit, GET history endpoints
    - Implement search with filters: category, tracking_number, title, submitter, status, priority, date_range
    - Return paginated results sorted by submission date descending by default
    - Support combining multiple filters in a single query
    - Restrict results to memos the user is authorized to view based on role
    - Enforce Submitter role for create/update/submit, Authenticated for read/search
    - _Requirements: 1.1, 1.4, 12.1, 12.2, 12.3, 12.4, 12.5_

  - [ ]* 9.3 Write property tests for memo validation and submission
    - **Property 1: Memo validation accepts complete payloads and rejects incomplete ones with field-level errors**
    - **Validates: Requirements 1.2, 1.5**
    - **Property 2: Tracking number uniqueness**
    - **Validates: Requirements 1.3**
    - **Property 3: Memo submission routes to first stage or rejects if no stages**
    - **Validates: Requirements 1.4, 3.6**

  - [ ]* 9.4 Write property tests for memo search and filtering
    - **Property 20: Search results match all specified filter criteria and are sorted**
    - **Validates: Requirements 12.1, 12.2, 12.3, 12.4**
    - **Property 21: Data visibility restricted by user role**
    - **Validates: Requirements 12.5, 13.5**

- [ ] 10. Implement memo approval processing
  - [ ] 10.1 Implement approval, rejection, and revision actions in workflow engine
    - Implement `approve()`: advance memo to next stage or mark Approved at final stage, record completion timestamp
    - Implement `reject()`: set status to Rejected, store rejection reason
    - Implement `request_revision()`: set status to revision_requested, store revision comments
    - Implement `get_current_stage()`: return current stage info and assigned approver
    - Validate approver is assigned to the current stage's approval title
    - Use memo_approval_snapshots (not live workflow) for in-progress memos
    - Handle idempotency — approving an already-approved memo returns current state
    - Log all approval actions to audit log
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [ ] 10.2 Create approval API endpoints
    - Create `app/api/approvals.py` with GET pending, POST approve, POST reject, POST request-revision endpoints
    - Enforce Approver role and validate the user is the assigned approver for the current stage
    - _Requirements: 5.1, 5.2, 5.4, 5.5_

  - [ ]* 10.3 Write property tests for approval processing
    - **Property 11: Approval advances memo to next stage or marks as Approved at final stage**
    - **Validates: Requirements 5.2, 5.3**
    - **Property 12: Rejection sets status and records reason**
    - **Validates: Requirements 5.4**
    - **Property 13: Revision request returns memo to submitter with comments**
    - **Validates: Requirements 5.5**

- [ ] 11. Implement notification engine
  - [ ] 11.1 Create notification engine and service
    - Create `app/engines/notification_engine.py` implementing the NotificationEngine class from the design
    - Implement notify_approver, notify_submitter_approved, notify_submitter_rejected, notify_submitter_revision
    - Create in-app notifications (database records) and dispatch email via NotificationInterface
    - Log notification events to audit log
    - _Requirements: 5.1, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

  - [ ] 11.2 Wire notifications into workflow engine
    - Trigger notify_approver when memo advances to a new stage
    - Trigger notify_submitter_approved when memo reaches final approval
    - Trigger notify_submitter_rejected on rejection
    - Trigger notify_submitter_revision on revision request
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [ ] 11.3 Create notification API endpoints
    - Create `app/api/notifications.py` with GET (list user's notifications) and PATCH (mark as read) endpoints
    - Enforce Authenticated access
    - _Requirements: 10.5_

  - [ ]* 11.4 Write property test for notifications
    - **Property 18: Notifications dispatched to correct party with relevant details**
    - **Validates: Requirements 5.1, 10.1, 10.2, 10.3, 10.4**

- [ ] 12. Implement document upload with feature toggle
  - [ ] 12.1 Create file upload service
    - Create `app/services/attachment_service.py` with upload, list, download methods
    - Validate file size against configurable maximum
    - Validate file MIME type against configurable allowlist
    - Return descriptive errors identifying whether issue is file size, file type, or both
    - Store files via StorageInterface (local adapter in Phase 1)
    - Gate all attachment endpoints behind `document_upload` feature toggle
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_

  - [ ] 12.2 Create attachment API endpoints
    - Create `app/api/attachments.py` with POST upload and GET list endpoints under `/memos/{id}/attachments`
    - Apply feature toggle dependency
    - Enforce Submitter (owner) for upload, Authenticated for list
    - _Requirements: 17.1, 17.3_

  - [ ]* 12.3 Write property test for file upload validation
    - **Property 23: File upload validation enforces size and type constraints**
    - **Validates: Requirements 17.2, 17.4, 17.5**

- [ ] 13. Implement user management and superuser-only registration
  - [ ] 13.1 Create user management service
    - Create `app/services/user_service.py` with register, list, get, update, deactivate, reactivate methods
    - Validate required fields on registration: full_name, email, department, designation, role
    - Prevent Superuser role from being assigned via registration API
    - Seed initial Superuser account on system startup
    - Log all user management actions to audit log
    - Create Pydantic schemas for user registration, update, and response
    - _Requirements: 18.1, 18.2, 18.3, 18.5, 18.6, 18.7_

  - [ ] 13.2 Create user management API endpoints
    - Create `app/api/users.py` with POST register, GET list, GET detail, PATCH update, POST deactivate, POST reactivate endpoints
    - Enforce Superuser-only access for all user management endpoints
    - _Requirements: 18.1, 18.2, 18.7_

  - [ ]* 13.3 Write property test for user registration
    - **Property 24: User registration validation and Superuser role protection**
    - **Validates: Requirements 18.3, 18.5**

- [ ] 14. Implement dashboard and reporting
  - [ ] 14.1 Create dashboard service
    - Create `app/services/dashboard_service.py` with methods for: total memos by status, memos by category, average approval time per category, pending approvals per stage
    - Compute statistics from live memo data (no separate stats table — ensures accuracy)
    - Implement report generation with filters: date_range, category, status
    - Restrict data visibility based on user role
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

  - [ ] 14.2 Create dashboard and reporting API endpoints
    - Create `app/api/dashboard.py` with GET stats, GET pending-by-stage, GET reports endpoints
    - Enforce Admin-only access
    - _Requirements: 13.1, 13.2, 13.4_

  - [ ]* 14.3 Write property test for dashboard statistics
    - **Property 22: Dashboard statistics match actual memo data**
    - **Validates: Requirements 13.1, 13.4**

- [ ] 15. Implement error handling and API documentation
  - [ ] 15.1 Implement consistent error handling
    - Create `app/core/exceptions.py` with domain exceptions: ValidationError, WorkflowError, BiometricEnrollmentError, AWSServiceError, FeatureDisabledError
    - Create `app/core/exception_handlers.py` with FastAPI exception handlers mapping domain exceptions to the standard error response format from the design
    - Ensure validation errors return all invalid fields (batch, not first-only)
    - Ensure idempotent approval actions return current state rather than errors
    - _Requirements: 1.5, 14.1_

  - [ ] 15.2 Verify OpenAPI documentation and CORS
    - Ensure all endpoints are documented in auto-generated OpenAPI spec
    - Verify CORS middleware is configured with allowed origins from config
    - _Requirements: 14.3, 14.4_

- [ ] 16. Checkpoint — Phase 1 complete (Core Backend)
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 17. Implement biometric engine and enrollment (Phase 2 — AWS Integration)
  - [ ] 17.1 Implement biometric engine
    - Create `app/engines/biometric_engine.py` implementing the BiometricEngine class from the design
    - Implement enroll_face: validate face detection, require minimum 3 images, index faces via FaceRecognitionInterface
    - Implement enroll_voice: validate audio quality, require minimum 3 samples, store via StorageInterface
    - Implement verify_face: compare live image against stored Face_Profile
    - Implement verify_voice: transcribe audio and compare against Speaker_Profile
    - Implement authenticate: face first, then voice; reject immediately if face fails without attempting voice
    - Implement reset_profiles: clear both face and voice profiles (Superuser action)
    - Implement account lockout: track failed attempts, lock after 5 consecutive failures within 15 minutes, notify Superuser
    - Log all biometric events to audit log
    - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7, 19.8, 19.9, 20.1, 20.2, 20.3, 20.4, 20.5, 20.6, 20.7_

  - [ ] 17.2 Create biometric enrollment and auth API endpoints
    - Create `app/api/auth.py` with POST login, POST refresh, POST logout endpoints
    - Create enrollment endpoints under `/users/{id}/`: POST face-enrollment, POST voice-enrollment, POST biometric-reset, GET enrollment-status
    - Enforce Superuser-only access for enrollment and reset endpoints
    - _Requirements: 19.1, 19.9, 20.1, 20.2, 20.7_

  - [ ]* 17.3 Write property tests for biometric engine
    - **Property 15: Biometric enrollment requires minimum sample counts**
    - **Validates: Requirements 6.6, 20.1, 20.2**
    - **Property 25: Biometric login requires both face and voice in sequence**
    - **Validates: Requirements 19.1, 19.3, 19.4, 19.5, 19.6**
    - **Property 26: Account lockout after consecutive failed attempts**
    - **Validates: Requirements 19.7**
    - **Property 27: Biometric sample quality validation**
    - **Validates: Requirements 20.3, 20.4**

- [ ] 18. Implement voice engine
  - [ ] 18.1 Implement voice engine service
    - Create `app/engines/voice_engine.py` implementing the VoiceEngine class from the design
    - Implement transcribe_memo_content: verify speaker identity first, then transcribe audio
    - Implement parse_retrieval_command: verify speaker, transcribe, parse intent via VoiceCommandInterface, return structured query
    - Implement read_memo_aloud: convert memo text to speech via TextToSpeechInterface
    - Reject all voice commands if speaker verification fails
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.3, 7.4, 7.5_

  - [ ] 18.2 Create voice and speaker profile API endpoints
    - Create `app/api/voice.py` with POST transcribe, POST retrieve, POST read-memo endpoints
    - Create speaker profile endpoints under `/users/{id}/`: POST speaker-profile, PUT speaker-profile
    - Enforce Authenticated access for voice endpoints, Superuser for speaker profile management
    - Require minimum 3 voice samples for speaker profile enrollment
    - _Requirements: 6.1, 6.5, 6.6, 7.1_

  - [ ]* 18.3 Write property test for voice engine
    - **Property 14: Speaker verification gates all voice commands**
    - **Validates: Requirements 6.2, 6.3, 7.1, 7.2**

- [ ] 19. Implement AWS service adapters
  - [ ] 19.1 Implement AWS S3 storage adapter
    - Create `app/adapters/aws/s3_storage_adapter.py` implementing StorageInterface using boto3
    - Implement upload_file, download_file, delete_file, get_file_url (pre-signed URLs)
    - Wrap all calls in try/except, log failures, raise AWSServiceError with descriptive message
    - _Requirements: 15.1, 15.7, 15.8_

  - [ ] 19.2 Implement AWS Rekognition face recognition adapter
    - Create `app/adapters/aws/rekognition_adapter.py` implementing FaceRecognitionInterface using boto3
    - Implement detect_faces, index_face, compare_faces, search_faces_by_image, delete_faces
    - Wrap all calls in try/except, log failures, raise AWSServiceError
    - _Requirements: 15.3, 15.7, 15.8_

  - [ ] 19.3 Implement AWS Transcribe voice transcription adapter
    - Create `app/adapters/aws/transcribe_adapter.py` implementing VoiceTranscriptionInterface using boto3
    - Implement transcribe_audio
    - Wrap all calls in try/except, log failures, raise AWSServiceError
    - _Requirements: 15.4, 15.7, 15.8_

  - [ ] 19.4 Implement AWS Lex voice command adapter
    - Create `app/adapters/aws/lex_adapter.py` implementing VoiceCommandInterface using boto3
    - Implement parse_command for memo retrieval intents
    - Wrap all calls in try/except, log failures, raise AWSServiceError
    - _Requirements: 15.5, 15.7, 15.8_

  - [ ] 19.5 Implement AWS Polly text-to-speech adapter
    - Create `app/adapters/aws/polly_adapter.py` implementing TextToSpeechInterface using boto3
    - Implement synthesize_speech
    - Wrap all calls in try/except, log failures, raise AWSServiceError
    - _Requirements: 15.6, 15.7, 15.8_

  - [ ] 19.6 Implement AWS SES notification adapter
    - Create `app/adapters/aws/ses_adapter.py` implementing NotificationInterface using boto3
    - Implement send_email
    - Wrap all calls in try/except, log failures, raise AWSServiceError
    - _Requirements: 15.2, 15.7, 15.8_

  - [ ] 19.7 Update dependency injection to support AWS adapter selection
    - Update `app/core/dependencies.py` to select local or AWS adapters based on configuration
    - Add AWS free-tier usage logging and threshold warnings
    - _Requirements: 15.7, 15.9_

  - [ ]* 19.8 Write property test for AWS error handling
    - **Property 28: AWS service failure produces logged error and descriptive response**
    - **Validates: Requirements 15.8**

- [ ] 20. Checkpoint — Phase 2 complete (AWS Integration)
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 21. Implement React Native for Web frontend (Phase 3)
  - [ ] 21.1 Initialize React Native for Web project and navigation
    - Set up React Native for Web project with Expo or react-native-web
    - Configure navigation (React Navigation) with responsive layout: sidebar for desktop, bottom tabs for mobile
    - Set up API client module for communicating with the backend REST API
    - Configure authentication context and token management
    - _Requirements: 16.1, 16.4, 16.5_

  - [ ] 21.2 Implement biometric login screen
    - Create login screen with face capture (camera access) and voice capture (microphone access)
    - Implement two-step flow: face capture → voice phrase prompt
    - Display appropriate error messages for face/voice verification failures and account lockout
    - Store session token on successful login
    - _Requirements: 16.3, 19.1, 19.5, 19.6_

  - [ ] 21.3 Implement memo creation and editing screens
    - Create memo form with fields: title, body, category (dropdown), priority (dropdown)
    - Implement voice input button for dictating memo content (microphone access)
    - Implement file attachment upload (when feature toggle is enabled)
    - Implement draft save and submit actions
    - Responsive layout for 320px to 1920px screen widths
    - _Requirements: 1.1, 6.1, 16.2, 16.3, 16.6, 17.1_

  - [ ] 21.4 Implement memo list, search, and detail screens
    - Create memo list with search/filter controls: category, status, priority, date range, tracking number, title
    - Implement paginated results display
    - Create memo detail screen showing all fields, approval history, and attachments
    - Implement voice-activated memo retrieval control
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 16.3, 16.6_

  - [ ] 21.5 Implement approval workflow screens
    - Create pending approvals list for approvers
    - Create approval action screen with approve, reject (with reason), and request revision (with comments) actions
    - Display memo details and approval history on the action screen
    - _Requirements: 5.1, 5.2, 5.4, 5.5, 16.3_

  - [ ] 21.6 Implement admin screens (categories, workflows, titles, roles, users, toggles)
    - Create category management screen (CRUD + deactivate)
    - Create workflow configuration screen (add/remove/reorder stages)
    - Create approval title management screen (CRUD + role assignment)
    - Create role management screen (CRUD + permission assignment)
    - Create user management screen (register, list, deactivate/reactivate)
    - Create feature toggle management screen
    - _Requirements: 2.1, 3.1, 3.5, 4.1, 8.4, 11.5, 18.1, 18.7_

  - [ ] 21.7 Implement dashboard and reporting screen
    - Create real-time dashboard with: total memos by status, memos by category, average approval time, pending per stage
    - Create report generation interface with date range, category, and status filters
    - Auto-refresh dashboard data
    - _Requirements: 13.1, 13.2, 13.4, 16.3_

  - [ ] 21.8 Implement notifications screen
    - Create notifications list showing in-app notifications
    - Implement mark-as-read functionality
    - Display notification badges/counts in navigation
    - _Requirements: 10.5, 16.3_

  - [ ] 21.9 Implement audit log viewer screen
    - Create audit log viewer with filters: actor, action type, target entity, date range
    - Display paginated results
    - Admin-only access
    - _Requirements: 9.4, 16.3_

- [ ] 22. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at phase boundaries
- Property tests validate universal correctness properties from the design document using Hypothesis (min 100 examples each)
- Unit tests validate specific examples and edge cases
- Phase 1 (tasks 1–16) delivers a fully functional backend with local/mock adapters
- Phase 2 (tasks 17–20) adds AWS service integrations
- Phase 3 (tasks 21–22) builds the React Native for Web frontend
- All external services use abstraction interfaces — AWS adapters are swapped in via dependency injection configuration
