---
description: "Task list for Todo App Backend API implementation"
---

# Tasks: Todo App Phase-II Backend API & Database

**Input**: Design documents from `/specs/1-todo-api-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `tests/` at repository root
- Paths shown below assume web app structure based on plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure per implementation plan
- [x] T002 Initialize Python project with FastAPI, SQLModel, PyJWT dependencies in requirements.txt
- [x] T003 [P] Configure environment variables management in backend/src/core/config.py
- [x] T004 [P] Create .env.example file with required environment variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Setup database connection and session management in backend/src/core/database.py
- [x] T006 [P] Implement JWT verification utility in backend/src/utils/jwt_utils.py
- [x] T007 [P] Create authentication dependency in backend/src/api/deps.py
- [x] T008 Create base model in backend/src/models/__init__.py
- [x] T009 Configure error handling and HTTP exception responses in backend/src/core/exceptions.py
- [x] T010 Setup main application in backend/src/main.py with proper configuration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create a new task (Priority: P1) 🎯 MVP

**Goal**: Allow authenticated users to create new tasks that are associated with their account

**Independent Test**: User can make a POST request to /api/tasks with a valid JWT token and task data, and the task is created and stored in the database with the correct user association

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T011 [P] [US1] Contract test for POST /api/tasks endpoint in tests/contract/test_tasks_api.py
- [x] T012 [P] [US1] Integration test for task creation flow in tests/integration/test_task_creation.py

### Implementation for User Story 1

- [x] T013 [P] [US1] Create Task model in backend/src/models/task.py
- [x] T014 [P] [US1] Create User model in backend/src/models/user.py
- [x] T015 [US1] Implement TaskService in backend/src/services/task_service.py (depends on T013, T014)
- [x] T016 [US1] Implement POST /api/tasks endpoint in backend/src/api/routes/tasks.py
- [x] T017 [US1] Add request/response validation schemas in backend/src/api/schemas/task.py
- [x] T018 [US1] Add logging for task creation operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View user's own tasks (Priority: P1)

**Goal**: Allow authenticated users to view all their tasks while ensuring they only see tasks that belong to them

**Independent Test**: User can make a GET request to /api/tasks with a valid JWT token and only receives tasks associated with their account

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T019 [P] [US2] Contract test for GET /api/tasks endpoint in tests/contract/test_tasks_api.py
- [x] T020 [P] [US2] Integration test for task listing flow in tests/integration/test_task_listing.py

### Implementation for User Story 2

- [x] T021 [P] [US2] Enhance TaskService to include user filtering in backend/src/services/task_service.py
- [x] T022 [US2] Implement GET /api/tasks endpoint in backend/src/api/routes/tasks.py
- [x] T023 [US2] Add validation to ensure user can only access their own tasks
- [x] T024 [US2] Add response schema for task listing in backend/src/api/schemas/task.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update and manage individual tasks (Priority: P2)

**Goal**: Allow authenticated users to update, delete, and mark tasks as complete while ensuring they can only modify tasks that belong to them

**Independent Test**: User can make GET, PUT, DELETE, and PATCH requests to /api/tasks/{id} with a valid JWT token and operations only succeed for tasks belonging to the authenticated user

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T025 [P] [US3] Contract test for GET /api/tasks/{id} endpoint in tests/contract/test_tasks_api.py
- [x] T026 [P] [US3] Contract test for PUT /api/tasks/{id} endpoint in tests/contract/test_tasks_api.py
- [x] T027 [P] [US3] Contract test for DELETE /api/tasks/{id} endpoint in tests/contract/test_tasks_api.py
- [x] T028 [P] [US3] Contract test for PATCH /api/tasks/{id}/complete endpoint in tests/contract/test_tasks_api.py

### Implementation for User Story 3

- [x] T029 [P] [US3] Enhance TaskService with update, delete, and toggle completion methods in backend/src/services/task_service.py
- [x] T030 [US3] Implement GET /api/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [x] T031 [US3] Implement PUT /api/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [x] T032 [US3] Implement DELETE /api/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [x] T033 [US3] Implement PATCH /api/tasks/{id}/complete endpoint in backend/src/api/routes/tasks.py
- [x] T034 [US3] Add validation to ensure user can only modify their own tasks
- [x] T035 [US3] Add response schemas for individual task operations in backend/src/api/schemas/task.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T036 [P] Documentation updates in docs/backend_api.md
- [x] T037 Code cleanup and refactoring across all modules
- [x] T038 Performance optimization for database queries
- [x] T039 [P] Additional unit tests in tests/unit/
- [x] T040 Security hardening and input validation
- [x] T041 Run quickstart validation to ensure all endpoints work correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /api/tasks endpoint in tests/contract/test_tasks_api.py"
Task: "Integration test for task creation flow in tests/integration/test_task_creation.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in backend/src/models/task.py"
Task: "Create User model in backend/src/models/user.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence