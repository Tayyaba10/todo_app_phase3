# Data Model: Todo App Authentication & Identity

## JWT Token Structure

### JWT Claims
- **sub** (Subject): Unique user identifier (user_id)
- **email** (Email): User's email address
- **exp** (Expiration Time): Unix timestamp when token expires
- **iat** (Issued At): Unix timestamp when token was issued
- **jti** (JWT ID): Optional unique identifier for token (for potential revocation)

### JWT Validation Rules
- Token must have valid signature matching BETTER_AUTH_SECRET
- Token must not be expired (current time < exp)
- Token must have been issued (iat present and reasonable)
- Subject (sub) must be present and non-empty

## User Identity Claims

### Required Claims
- **user_id**: String/Number representing unique user identifier
- **email**: String representing user's email address
- **exp**: Numeric timestamp for token expiration

### Optional Claims
- **name**: User's display name (may be provided by Better Auth)
- **roles**: Array of roles for future authorization (not used in current scope)

## Token Lifecycle

### Issuance
1. User successfully authenticates via Better Auth
2. Better Auth generates JWT with user identity claims
3. JWT is returned to frontend client
4. Frontend stores JWT securely

### Usage
1. Frontend retrieves JWT from storage
2. JWT is attached to API requests as Bearer token in Authorization header
3. Backend validates JWT signature and expiration
4. User identity is extracted from validated token

### Expiration
1. Token expires after configured time period
2. Backend rejects requests with expired tokens (HTTP 401)
3. Frontend detects 401 responses and redirects to login
4. User must re-authenticate to obtain new token

## API Security Requirements

### Protected Endpoints
- All endpoints that access user data require valid JWT
- JWT must be present in Authorization header
- JWT must be properly formatted (Bearer token)
- JWT must pass signature verification
- JWT must not be expired

### Identity Verification
- User identity must be extracted from JWT, not client input
- Backend must validate JWT signature using BETTER_AUTH_SECRET
- User-specific data access must be filtered by extracted user_id