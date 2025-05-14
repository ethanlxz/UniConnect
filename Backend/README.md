Hi, Welcome to the Uniconnect's Backend Manual

=============
api/otp/send
=============

Payload :
{
	"email" : ""
}

generates a otp and send to the email specified in the payload, otp is viable within 10 minutes after called


=============
api/otp/resend
=============

Payload :
{
	"email" : ""
}

regenerates a new otp, deletes the old otp and send to the email specified in the payload


=============
api/otp/verify
=============

Payload :
{
	"email" : "",
	"code": ""
}

verify the otp code, if otp code is older than 10 minutes, it won't work


====================
api/student/register
====================

Payload :
{
	"id" : "",
	"username": "",
	"email" : "",
	"name": "",
	"password" : "",
	"contact_num": ""
}

Allow creation of new student with student id, username, email, full name, password and contact numbers


====================
api/lecturer/register
====================

Payload :
{
	"id" : "",
	"username": "",
	"email" : "",
	"name": "",
	"password" : "",
	"contact_num": ""
}

Allow creation of new lecturer with lecturer id, username, email, full name, password and contact numbers


==================
api/student/login
==================

Payload :
{
	"username": "",
	"password" : ""
}

Verify credentials (username and password) to authenticate and grant access to registered students.

On success (example):
{
    "message": "Login successful",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NzMxNjgyMywiaWF0IjoxNzQ3MjMwNDIzLCJqdGkiOiJjOTE3YjM1N2YyYWI0MmY2YWJhODk2NDU3MjU5NThiNyIsInVzZXJfaWQiOjF9.iAmKzs8ZqgNwgDrlFwNG39JWLroc0MTS5taz7j1KVFQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MjMyMjIzLCJpYXQiOjE3NDcyMzA0MjMsImp0aSI6ImFmZGRkOTFiODY3ZTQ0OWQ4NzcyNGI2N2ViMzNjYjQ3IiwidXNlcl9pZCI6MX0.9pT1LWpOKWF9j1V7JO9V3uPt7iFkfe3RZXAZIFzdTx4"
}


==================
api/lecturer/login
==================

Payload :
{
	"username": "",
	"password" : ""
}

Verify credentials (username and password) to authenticate and grant access to registered lecturers.

On success (example) :

{
    "message": "Login successful",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NzMxNjgyMywiaWF0IjoxNzQ3MjMwNDIzLCJqdGkiOiJjOTE3YjM1N2YyYWI0MmY2YWJhODk2NDU3MjU5NThiNyIsInVzZXJfaWQiOjF9.iAmKzs8ZqgNwgDrlFwNG39JWLroc0MTS5taz7j1KVFQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3MjMyMjIzLCJpYXQiOjE3NDcyMzA0MjMsImp0aSI6ImFmZGRkOTFiODY3ZTQ0OWQ4NzcyNGI2N2ViMzNjYjQ3IiwidXNlcl9pZCI6MX0.9pT1LWpOKWF9j1V7JO9V3uPt7iFkfe3RZXAZIFzdTx4"
}