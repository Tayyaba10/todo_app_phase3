# Data Model: Todo App Phase-II Backend API & Database

## Task Entity
- **id**: Integer (Primary Key, Auto-increment)
- **title**: String (Required, Max length: 255)
- **description**: String (Optional, Max length: 1000)
- **completed**: Boolean (Default: False)
- **created_at**: DateTime (Default: Current timestamp)
- **updated_at**: DateTime (Default: Current timestamp, Updates on modification)
- **user_id**: Integer (Foreign Key to User, Required)

## User Entity
- **id**: Integer (Primary Key, Auto-increment)
- **email**: String (Required, Unique, Max length: 255)
- **name**: String (Optional, Max length: 255)
- **created_at**: DateTime (Default: Current timestamp)
- **updated_at**: DateTime (Default: Current timestamp, Updates on modification)

## Relationships
- **User to Tasks**: One-to-Many (One user can have many tasks)
- **Task to User**: Many-to-One (Many tasks belong to one user)

## Validation Rules
- Task title must not be empty
- Task title must be less than 256 characters
- Task description must be less than 1001 characters
- User email must be valid email format
- User email must be unique

## State Transitions
- Task completion state can transition from False to True or True to False via PATCH /api/tasks/{id}/complete endpoint