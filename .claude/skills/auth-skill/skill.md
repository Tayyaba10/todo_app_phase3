---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Signup**
   - Validate email and password
   - Hash passwords securely before storage
   - Store user credentials in database
   - Prevent duplicate accounts

2. **User Signin**
   - Verify user credentials
   - Compare hashed passwords
   - Handle invalid login attempts
   - Return authentication response

3. **Password Security**
   - Use strong hashing algorithms (bcrypt / argon2)
   - Apply salt automatically
   - Never store plain-text passwords
   - Enforce password strength rules

4. **JWT Authentication**
   - Generate access tokens on successful login
   - Sign tokens with secret key
   - Include user ID and expiry
   - Verify tokens on protected routes

5. **Better Auth Integration**
   - Use Better Auth secret from environment variables
   - Connect frontend and backend auth flow
   - Handle token refresh and logout
   - Ensure secure cookie or header-based auth

## Best Practices
- Store secrets in `.env` files
- Use HTTPS in production
- Set token expiration times
- Protect sensitive routes with middleware
- Return consistent auth error messages
- Follow OWASP authentication guidelines

## Example Structure

### Signup
```python
@app.post("/auth/signup")
def signup(user: UserCreate):
    hashed_password = hash_password(user.password)
    save_user(user.email, hashed_password)
    return {"message": "User created successfully"}
