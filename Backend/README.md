
# 📡 UniConnect Backend API Documentation

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
1. Student Profile
Endpoint: GET /api/student/profile/student1/
Payload:

Success Response:

```json
{
  "username": "student1",
  "email": "student@example.com",
  "name": "John Doe",
  "contact_num": "0123456789",
  "gender": "Male",
  "major": "Undeclared",
  "photo": "http://127.0.0.1:8000/default.jpg",
  "bio": "Bio loading… please wait.",
  "instagram_id": "@student1"
}
```

Endpoint: PATCH /api/student/profile/student1/
Payload:

```json
{
  "email": "student@example.com",
  "name": "John Doe",
  "contact_num": "0123456789",
  "gender": "M",
  "major": "Diploma in IT",
  "bio": "Bio loading… please wait.",
  "instagram_id": "@student1"
}
```

Success Response:

```json
{
  "username": "student1",
  "email": "student@example.com",
  "name": "John Doe",
  "contact_num": "0123456789",
  "gender": "Male",
  "major": "Diploma in IT",
  "photo": "http://127.0.0.1:8000/default.jpg",
  "bio": "Bio loading… please wait.",
  "instagram_link": "@student1"
}
```

2. Register Student
Endpoint: POST /api/student/register/
Payload:

```json
{
  "id": "STU001",
  "username": "student1",
  "email": "student@example.com",
  "name": "John Doe",
  "password": "securepassword123",
  "contact_num": "+1234567890",
  "gender": "M",
  "major": "Diploma in IT",
  "bio": "Bio loading… please wait.",
  "instagram_id": "@ethanlaw"
}
```


3. Student Login
Endpoint: POST /api/student/login/
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
1. Lecturer Profile
Endpoint: GET /api/lecturer/profile/LEC001/
Payload:

Success Response:

```json
{
  "username": "lecturer1",
  "email": "lecturer@example.com",
  "name": "Dr. Smith",
  "contact_num": "+9876543210",
  "major": "Degree in IT",
  "photo": "http://127.0.0.1:8000/default.jpg"
}
```

Endpoint: PATCH /api/lecturer/profile/LEC001/
Payload:

```json
{
  "email": "lecturer@example.com",
  "name": "Dr. Smith",
  "contact_num": "+9876543210",
  "major": "Degree in IT"
}
```

Success Response:

```json
{
  "username": "lecturer1",
  "email": "lecturer@example.com",
  "name": "Dr. Smith",
  "contact_num": "+9876543210",
  "major": "Degree in IT",
  "photo": "http://127.0.0.1:8000/default.jpg"
}
```

2. Register Lecturer
Endpoint: POST /api/lecturer/register/
Payload:

```json
{
  "id": "LEC001",
  "username": "lecturer1",
  "email": "lecturer@example.com",
  "name": "Dr. Smith",
  "password": "securepassword123",
  "contact_num": "+9876543210",
  "major": "Degree in IT"
}
```


3. Lecturer Login
Endpoint: POST /api/lecturer/login/
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

Class
1. Create Class
Endpoint: POST /classing/create/
Payload:

```json
{
  "username": "lecturer1",
  "name": "ClassName1",
  "max_students": 60,
  "group": 10,
  "min_group_members": 6
}
```

Success Response:

```json
{
    "name": "ClassName1",
    "code": "ClassCode1",
    "max_students": 60,
    "group": 10,
    "min_group_members": 6,
    "created_groups": 10
}
```

2. Join Class
Endpoint: POST /classing/join/
Payload:

```json
{
  "username": "student1",
  "code": "ClassCode1"
}
```

Success Response:

```json
{
    "detail": "student1 successfully joined class 'ClassName1'."
}
```

3. Edit Class
Endpoint: PUT /classing/edit/
Payload:

```json
{
  "username": "lecturer1",
  "code": "ClassCode1",
  "name": "ClassName2"
}
```

Success Response:

```json
{
    "detail": "Class name updated successfully."
}
```

4. Delete Class
Endpoint: DELETE /classing/delete/
Payload:

```json
{
  "username": "lecturer1",
  "code": "ClassCode1"
}
```

Success Response:

```json
{
    "detail": "Class deleted successfully."
}
```

5. Remove Student from Class
Endpoint: POST /classing/removeStudent/
Payload:

```json
{
  "username": "lecturer1",
  "code": "ClassCode1",
  "student_username": "student1"
}
```

Success Response:

```json
{
    "detail": "Student removed successfully."
}
```

6. LecturerClassList
Endpoint: POST /classing/lecturer/classes/
Payload:

```json
{
  "username": "lecturer1"
}
```

Success Response:

```json
[
    {
        "id": 1,
        "name": "ClassName1",
        "code": "ClassCode1"
    },
    {
        "id": 5,
        "name": "ClassName2",
        "code": "ClassCode2"
    },
    {
        "id": 7,
        "name": "ClassName3",
        "code": "ClassCode3"
    }
]
```

7. StudentClassList
Endpoint: POST /classing/student/classes/
Payload:

```json
{
  "username": "student1"
}
```

Success Response:

```json
[
    {
        "id": 1,
        "name": "ClassName1",
        "code": "ClassCode1"
    },
    {
        "id": 5,
        "name": "ClassName2",
        "code": "ClassCode2"
    },
    {
        "id": 7,
        "name": "ClassName3",
        "code": "ClassCode3"
    }
]
```

8. Class Detail
Endpoint: GET /classing/detail/?class_id=8

Success Response:

```json
{
    "class_id": 8,
    "name": "ClassName1",
    "code": "ClassCode1",
    "max_students": 60,
    "current_student_count": 2,
    "group": 4,
    "min_group_members": 3,
    "lecturer": {
        "id": 2,
        "username": "Lecturer1",
        "name": "LecturerName1",
        "email": "Lecturer1@gmail.com",
        "contact_num": "01267895"
    },
    "students": [
        {
            "id": 2,
            "username": "Student1",
            "name": "StudentName1",
            "email": "Student1@gamil.com",
            "contact_num": "01234567"
        },
        {
            "id": 3,
            "username": "Student2",
            "name": "StudentName2",
            "email": "Student2@gmail.com",
            "contact_num": "01289765"
        }
    ]
}
```

9. Leave Class
Endpoint: POST /classing/leave/
Payload:

```json
{
  "code": "nMAU8t",
  "username": "adammm"
}
```

Success Response:

```json
{
    "detail": "Successfully left the class."
}
```

10. Student Detail in Class
Endpoint: GET /classing/studentDetail/?class_code=aHvlFz

Success Response:

```json
{
    "students": [
        {
            "id": 1,
            "username": "ysss",
            "name": "ys",
            "email": "ys@gmail.com",
            "contact_num": "01234567",
            "group_type": "temporary"
        },
        {
            "id": 2,
            "username": "ethan",
            "name": "ethanlxz",
            "email": "ethan@gmail.com",
            "contact_num": "012378624",
            "group_type": "temporary"
        },
        {
            "id": 3,
            "username": "xyyy",
            "name": "xy",
            "email": "xy@gmail.com",
            "contact_num": "0127386283",
            "group_type": "temporary"
        },
        {
            "id": 4,
            "username": "alexxx",
            "name": "alex",
            "email": "alex@gmail.com",
            "contact_num": "0173827683",
            "group_type": "temporary"
        },
        {
            "id": 5,
            "username": "adammm",
            "name": "adam",
            "email": "adam@gmail.com",
            "contact_num": "017836382",
            "group_type": "no group"
        }
    ]
}
```

Grouping
1. Send Request
Endpoint: POST /grouping/send/
Payload:

```json
{
  "class_code": "CS101",
  "sender_username": "alice123",
  "receiver_username": "bob456"
}
```

Success Response:

```json
{
    "detail": "Group request sent."
}
```

2. Respond Request
Endpoint: POST /grouping/respond/
Payload:

```json
{
  "request_id": 7,
  "class_code": "CS101",
  "current_username": "ysss",
  "action": true
}
```

Success Response:

```json
{
    "detail": "Request accepted. Students added to sender’s temporary group.",
    "temp_group_id": 6
}
```

```json
{
  "request_id": 7,
  "class_code": "CS101",
  "current_username": "ysss",
  "action": false
}
```

Success Response:

```json
{
    "detail": "Request declined."
}
```

3. Request List
Endpoint: GET /grouping/requests?username=susannn&class_code=nMAU8t
Payload:

Success Response:

```json
[
    {
        "request_id": 19,
        "sender_username": "alexxx"
    },
    {
        "request_id": 20,
        "sender_username": "raelll"
    }
]
```

4. Group List
Endpoint: GET /grouping/list/?class_id=4
Payload:

Success Response:

```json
{
    "class_code": "nMAU8t",
    "class_name": "AI",
    "min_group_members": 3,
    "max_groups_allowed": 4,
    "final_groups": [
        {
            "group_type": "finalized",
            "group_label": "Finalized Group 1",
            "id": 1,
            "members": [
                "ys",
                "ethanlxz",
                "xy",
                "adam"
            ],
            "member_count": 4,
            "is_finalized": true
        }
    ],
    "temporary_groups": [
        {
            "group_type": "temporary",
            "group_label": "Temp Group 1",
            "id": 6,
            "leader": "alexxx",
            "members": [
                "rael",
                "alex",
                "susan",
                null
            ],
            "member_count": 3,
            "is_finalized": false
        }
    ]
}
```

5. Student myGroups View
Endpoint: GET /grouping/myGroups/?username=ysss
Payload:

Success Response:

```json
{
    "groups": [
        {
            "group_id": 6,
            "class_code": "mvd7Vk",
            "class_name": "FYP",
            "members": [
                "ys",
                "ethanlxz",
                "xy",
                "alex"
            ],
            "leader": "ysss",
            "group_type": "finalized"
        },
        {
            "group_id": 1,
            "class_code": "DTcXDr",
            "class_name": "AI",
            "members": [
                "ys",
                "ethanlxz",
                "xy",
                "alex"
            ],
            "leader": "ysss",
            "group_type": "temporary"
        }
    ]
}
```

6. Leave Group
Endpoint: POST /grouping/leave/
Payload:

```json
{
  "username": "susannnn",
  "class_code": "HLHYCP",
  "group_id": 5,
  "group_type": "temporary"
}
```

Success Response:

```json
{
    "detail": "Student successfully left the temporary group."
}
```

7. FinalizeTemporaryGroup
Endpoint: POST /grouping/finalTG/
Payload:

```json
{
  "username": "ethan",
  "class_code": "HLHYCP",
  "temp_group_id": 4
}
```

Success Response:

```json
{
    "detail": "Group finalized."
}
```

8. Change Group Leader
Endpoint: POST /grouping/changeLeader/
Payload:

```json
{
  "username": "alexxx",
  "class_code": "HLHYCP",
  "temp_group_id": 7,
  "new_leader_username": "raelll",
  "new_leader_name": "rael"
}
```

Success Response:

```json
{
  "detail": "Leader changed successfully.",
  "new_leader": "raelll (rael)"
}
```

8. DefinalizeTemporaryGroup
Endpoint: POST /grouping/definalTG/
Payload:

```json
{
  "username": "ethan",
  "class_code": "HLHYCP",
  "temp_group_id": 4
}
```

Success Response:

```json
{
    "detail": "Group definalized."
}
```

9. ConvertToExistingGroup
Endpoint: POST /grouping/api/convert-to-group/
Description: Converts a finalized temporary group into an existing group by transferring all members and leader, then deletes the temporary group.

Payload:

```json
{
  "username": "student123",
  "class_code": "CS101",
  "temp_group_id": 1,
  "target_group_id": 5
}
```

Success Response:

```json
{
  "detail": "Group converted successfully.",
}
```

10. Remove Member from Temporary Group
Endpoint: POST /grouping/removeMember/
Payload:

```json
{
  "username": "ethan",
  "member_username": "adammm",
  "class_code": "HLHYCP",
  "temp_group_id": 4
}
```

Success Response:

```json
{
    "detail": "adammm has been removed from the group."
}
```

11. SendJoinRequest
Endpoint: POST /grouping/sendJoinRequest/
Payload:

```json
{
  "sender_username": "xyyy",
  "target_username": "ethan",
  "class_code": "HLHYCP"
}
```

Success Response:

```json
{
    "detail": "Join request sent to leader ysss."
}
```

11. RespondJoinRequest
Endpoint: POST /grouping/respondJoinRequest/
Payload:

```json
{
  "request_id": 1,
  "class_code": "izi897",
  "leader_username": "ethan",
  "action": true
}
```

Success Response:

```json
{
    "detail": "Join request sent to leader ysss."
}
```

12. Join Request List
Endpoint: GET /grouping/joinRequests?leader_username=ysss&class_code=izi897
Payload:

Success Response:

```json
[
    {
        "request_id": 2,
        "sender_username": "alexxx"
    }
]
```