import { createAuthClient } from "better-auth/react";

// Create the Better Auth client with JWT configuration
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  // JWT plugin would be configured here if needed
  // Currently using default session management with JWT tokens
});

export const { signIn, signOut, useSession } = authClient;