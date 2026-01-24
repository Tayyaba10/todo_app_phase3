# Research: Todo App Authentication Implementation

## Decision: Better Auth Configuration with JWT Plugin
**Rationale**: Better Auth provides a complete authentication solution that can be configured to issue JWT tokens, meeting the requirement for JWT-only authentication without sessions. It integrates well with Next.js and provides both frontend and backend components.
**Alternatives considered**:
- Self-built JWT system: More complex, requires more security considerations
- NextAuth.js: Another solid option but Better Auth was specified in requirements
- Clerk: Proprietary solution that doesn't fit the open-source approach

## Decision: JWT Payload Design
**Rationale**: JWT tokens will contain essential user identity claims (user_id, email) with expiration timestamp to ensure security. This matches the requirement for verifiable user identity in tokens.
**Payload structure**:
- `sub`: user_id (subject identifier)
- `email`: user's email address
- `exp`: expiration timestamp
- `iat`: issued at timestamp
- `jti`: JWT ID for potential revocation (future extension)

## Decision: Frontend Token Storage Strategy
**Rationale**: Storing JWT tokens in localStorage provides persistent authentication across browser sessions while being accessible to JavaScript for API requests. sessionStorage is an alternative for more sensitive applications.
**Security consideration**: XSS attacks could potentially access localStorage, but this is mitigated by proper input validation and sanitization.

## Decision: Backend JWT Verification Strategy
**Rationale**: Using python-jose library for JWT verification provides robust cryptographic validation against the shared secret (BETTER_AUTH_SECRET). This ensures tokens are properly signed and not tampered with.
**Verification steps**:
- Verify signature using shared secret
- Check expiration timestamp
- Extract user identity claims

## Decision: API Request Attachment Method
**Rationale**: Attaching JWT tokens as Bearer tokens in the Authorization header is the standard practice for JWT authentication and is well-supported by both frontend and backend frameworks.

## Decision: Error Handling Approach
**Rationale**: Proper error handling for authentication failures ensures users get appropriate feedback and security is maintained. HTTP 401 responses for invalid/missing tokens is the standard approach.

## Decision: Environment Variable Management
**Rationale**: Using environment variables (BETTER_AUTH_SECRET, BETTER_AUTH_URL) keeps sensitive configuration separate from code and allows for different configurations across environments (development, staging, production).