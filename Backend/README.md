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


