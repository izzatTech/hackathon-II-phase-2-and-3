# Data Model for Todo Application Evolution

## Core Entities

### User
- **Description**: Represents an authenticated person using the system, uniquely identified and secured through authentication mechanisms
- **Fields**:
  - id: Unique identifier (UUID/string)
  - email: User's email address (string, required, unique)
  - username: User's chosen display name (string, required, unique)
  - hashed_password: Securely hashed password (string, required)
  - created_at: Timestamp of account creation (datetime, required)
  - updated_at: Timestamp of last update (datetime, required)
  - is_active: Account status flag (boolean, default: true)

### Task
- **Description**: Represents a user's activity or to-do item with properties like title, description, status (complete/incomplete), creation date, and due date
- **Fields**:
  - id: Unique identifier (UUID/string)
  - title: Task title (string, required)
  - description: Detailed task description (string, optional)
  - status: Task completion status (enum: pending, in_progress, completed)
  - user_id: Reference to the owning user (foreign key to User.id, required)
  - created_at: Timestamp of task creation (datetime, required)
  - updated_at: Timestamp of last update (datetime, required)
  - due_date: Optional deadline for the task (datetime, optional)
  - priority: Task priority level (enum: low, medium, high, critical, default: medium)

### Session
- **Description**: Represents a temporary authenticated connection between a user and the system
- **Fields**:
  - id: Unique identifier (UUID/string)
  - user_id: Reference to the authenticated user (foreign key to User.id, required)
  - token: Session authentication token (string, required, unique)
  - expires_at: Expiration timestamp (datetime, required)
  - created_at: Timestamp of session creation (datetime, required)
  - ip_address: IP address of the session (string, optional)
  - user_agent: Browser/device information (string, optional)

### Conversation
- **Description**: Represents a session of natural language interactions between a user and the AI assistant
- **Fields**:
  - id: Unique identifier (UUID/string)
  - user_id: Reference to the user (foreign key to User.id, required)
  - title: Conversation title/description (string, optional)
  - created_at: Timestamp of conversation start (datetime, required)
  - updated_at: Timestamp of last activity (datetime, required)
  - is_active: Whether the conversation is ongoing (boolean, default: true)

### Message
- **Description**: Individual messages within a conversation between user and AI
- **Fields**:
  - id: Unique identifier (UUID/string)
  - conversation_id: Reference to the parent conversation (foreign key to Conversation.id, required)
  - sender_type: Who sent the message (enum: user, ai_assistant, system)
  - content: The actual message content (string, required)
  - created_at: Timestamp of message creation (datetime, required)
  - metadata: Additional data about the message (JSON, optional)

### Event
- **Description**: Represents significant system actions (task creation, update, deletion) that trigger downstream processing
- **Fields**:
  - id: Unique identifier (UUID/string)
  - event_type: Type of event (enum: task_created, task_updated, task_deleted, task_completed, user_signed_up)
  - entity_id: ID of the affected entity (string, required)
  - entity_type: Type of the affected entity (enum: task, user, conversation)
  - payload: Event data (JSON, required)
  - created_at: Timestamp of event occurrence (datetime, required)
  - processed: Whether the event has been processed (boolean, default: false)

## Relationships

- **User → Task**: One-to-many (one user can have many tasks)
- **User → Session**: One-to-many (one user can have multiple sessions)
- **User → Conversation**: One-to-many (one user can have multiple conversations)
- **Conversation → Message**: One-to-many (one conversation can have many messages)
- **User → Event**: One-to-many (events can be related to a user)
- **Task → Event**: One-to-many (events can be related to a task)

## Validation Rules

### User Validation
- Email must be in valid format
- Username must be 3-30 characters, alphanumeric with underscores/hyphens only
- Password must meet minimum strength requirements (configurable)

### Task Validation
- Title must be 1-200 characters
- Description must be 0-2000 characters
- Due date cannot be in the past
- Status values restricted to allowed enum values
- User_id must reference an existing user

### Session Validation
- Token must be unique across all sessions
- Expires_at must be in the future
- User_id must reference an existing user

### Conversation Validation
- User_id must reference an existing user

## Indexes

- User.email (unique)
- User.username (unique)
- Session.token (unique)
- Task.user_id (index for performance)
- Task.created_at (index for chronological queries)
- Event.created_at (index for chronological processing)
- Event.processed (index for event processing queries)
- Message.conversation_id (index for conversation retrieval)