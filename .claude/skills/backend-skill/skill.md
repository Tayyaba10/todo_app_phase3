---
name: backend-skill
description: Build backend systems by generating API routes, handling requests and responses, and connecting to databases.
---

# Backend Skill

## Instructions

1. **Route Generation**
   - Define RESTful API endpoints
   - Use clear and consistent URL patterns
   - Separate routes by resource
   - Support CRUD operations

2. **Request Handling**
   - Parse request body, params, and headers
   - Validate incoming data
   - Handle authentication and authorization
   - Manage middleware and dependencies

3. **Response Handling**
   - Return standardized JSON responses
   - Use proper HTTP status codes
   - Handle success and error responses
   - Implement global error handling

4. **Database Connection**
   - Configure database connection securely
   - Use ORM or query builders
   - Manage connection lifecycle
   - Handle transactions safely

## Best Practices
- Follow REST or API-first design
- Keep controllers thin and logic reusable
- Validate input at boundaries
- Use environment variables for secrets
- Handle errors gracefully
- Log important backend events

## Example Structure

### Route Definition
```python
@app.get("/tasks")
def get_tasks():
    return fetch_all_tasks()
