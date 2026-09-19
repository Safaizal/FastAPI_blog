# Day 10

## Key Setup and Dependencies

* Password Hashing: Uses Argon2 via pwdlib for modern, secure password storage . This is chosen over BCrypt for better resistance to GPU cracking attacks.
* JWT Management: Utilizes the PyJWT library for creating and verifying tokens .
* Configuration: Implements pydantic-settings to manage environment variables securely, preventing sensitive data exposure in logs or code .

## Backend Implementation

* Database Updates: Added a password_hash field to the user model , ensuring no plain-text passwords are ever saved.
* Schema Security: Introduced distinct UserPublic and UserPrivate response schemas  to ensure sensitive fields like emails are not exposed in public-facing API responses.
* Auth Utilities: Created oauth2_scheme and helper functions for hashing, verifying passwords, and handling JWT encoding/decoding .
Endpoints: Implemented:
    Registration
Login (/api/users/token)
    A current user endpoint (/me) to validate sessions .

## Frontend and UI Integration

* Templates: Created register.html and login.html pages with client-side form validation .
* State Management: Developed an auth.js module  to manage JWT tokens in localStorage and update the navbar UI dynamically based on the user's logged-in status.

 -> Note: While the authentication infrastructure is now complete, the video specifies that authorization (protecting routes and checking ownership for editing/deleting posts) is the focus of the next tutorial .
