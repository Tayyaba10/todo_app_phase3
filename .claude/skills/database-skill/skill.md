---
name: database-skill
description: Design and manage databases including table creation, schema design, and migrations.
---

# Database Skill

## Instructions

1. **Schema Design**
   - Identify entities and relationships
   - Normalize data to reduce redundancy
   - Define primary and foreign keys
   - Choose appropriate data types

2. **Create Tables**
   - Write SQL or ORM-based table definitions
   - Apply constraints (NOT NULL, UNIQUE)
   - Use indexes for frequently queried fields
   - Follow consistent naming conventions

3. **Migrations**
   - Create versioned migration files
   - Apply incremental schema changes
   - Support rollback strategies
   - Keep migrations idempotent

4. **Relationships**
   - One-to-one, one-to-many, many-to-many
   - Enforce referential integrity
   - Use cascading rules carefully

## Best Practices
- Design schema before writing code
- Use migrations instead of manual DB changes
- Avoid over-indexing
- Keep tables small and focused
- Back up database before migrations
- Document schema changes clearly

## Example Structure

### Table Creation (SQL)
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
