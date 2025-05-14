
#📡 UniConnect Backend API Documentation

🔢 OTP Endpoints
1. Send OTP
Endpoint: POST /api/otp/send
Payload:

```json
{
  "email": "user@example.com"
}
```
Response:

Generates an OTP and sends it to the email (valid for 10 minutes).

2. Resend OTP
Endpoint: POST /api/otp/resend
Payload:

```json
{
  "email": "user@example.com"
}
```

Response:

Regenerates a new OTP (invalidates the old one) and sends it.

3. Verify OTP
Endpoint: POST /api/otp/verify
Payload:

```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

Response:

Validates the OTP (fails if older than 10 minutes).

🎓 Student Endpoints
1. Register Student
Endpoint: POST /api/student/register
Payload:

```json
{
  "id": "STU001",
  "username": "student1",
  "email": "student@example.com",
  "name": "John Doe",
  "password": "securepassword123",
  "contact_num": "+1234567890"
}
```


2. Student Login
Endpoint: POST /api/student/login
Payload:

```json
{
  "username": "student1",
  "password": "securepassword123"
}
```


Success Response:

```json
{
  "message": "Login successful",
  "refresh": "eyJhbGci...",
  "access": "eyJhbGci..."
}
```

👨‍🏫 Lecturer Endpoints
1. Register Lecturer
Endpoint: POST /api/lecturer/register
Payload:

```json
{
  "id": "LEC001",
  "username": "lecturer1",
  "email": "lecturer@example.com",
  "name": "Dr. Smith",
  "password": "securepassword123",
  "contact_num": "+9876543210"
}
```


2. Lecturer Login
Endpoint: POST /api/lecturer/login
Payload:

```json
{
  "username": "lecturer1",
  "password": "securepassword123"
}
```

Success Response:

```json
{
  "message": "Login successful",
  "refresh": "eyJhbGci...",
  "access": "eyJhbGci..."
}
```