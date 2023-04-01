![](https://github.com/PUM-05/backend/actions/workflows/django.yml/badge.svg)
![](https://github.com/PUM-05/backend/actions/workflows/style.yml/badge.svg)
![](https://github.com/PUM-05/backend/actions/workflows/sonar.yml/badge.svg)


# Backend readme
Contains instructions for setting up and running the backend part of the Personalkollen project.

# Setup

## Requirements
- Python 3.10 (or later)
- Git
- Pip

## Backend setup
> Note:
> If using Windows make sure you change occurences of "/" to "\\" (or use bash terminal),
> also you may need to change occurences of "python3" to "python".

- Git clone the repository to your local machine.
- Navigate to the project folder in your terminal.
- Create a virtual environmnent and activate it (for MacOS/Linux):
```
python3 -m venv .venv
source .venv/bin/activate
```
- Create a virtual environmnent and activate it (for Windows):
```
python3 -m venv .venv
source .venv/Scripts/activate
```

- Install requirements:
```
pip install -r requirements/requirements.txt
```

- Setup local database:
```
python3 src/manage.py migrate
```

- Run tests to make sure it works correctly (no errors should occur):
```
python3 src/manage.py test api
```

## Deploy static files from frontend
> Note:
> This additionally requires that Node.js and npm are installed.

- Pull the main branch of both repositories.
- Build frontend:
```
npm run build
```
- Delete everything in `backend/src/static/`
- Move/Copy the files from `frontend/frontend-friends/build` into `backend/src/static/`


## Starting the server
- Run the server:
```
python3 src/manage.py runserver
```


# API
## Authentication
### Login
Logs in the user with the given credentials.
The password field is not required, since some users may not have a password.
An empty password filed will be treaded the same as if no password field was given.

Request:
``` http
POST /api/login/

{
    "username": "<username>",
    "password": "<password>"
}
```
Success:
``` http
Status: 200 (OK)
Set-Cookie: sessionid=...
```
Wrong credentials:
``` http
Status: 401 (Unauthorized)
```

### Logout
Logs out the currently logged in user.

Request:
``` http
POST /api/logout/
Cookie: sessionid=...
```
Success response:
``` http
Status: 200 (OK)
```

### Check
Checks if the user is logged in or not.

Request:
``` http
GET /api/check/
Cookie: sessionid=...
```
Response if logged in:
``` http
Status: 200 (OK)
```
Response if not logged in:
``` http
Status: 401 (Unauthorized)
```

## Cases
### Get cases
Returns all cases sorted chronologically that matches the given query parameters.

Query parameters:
- `id: int` (Not jet implemented)
- `index-start: int` (Not jet implemented)
- `index-end: int` (Not jet implemented)
- `category_id: int` (Not jet implemented)

Request:
``` http
GET /api/cases/
```

Success response:
``` http
Status: 200 (OK)

[
    {
        "id": 1,
        "notes": "Example notes 1",
        "medium": "phone",
        "created_at": "yyyy-mm-ddThh:mm:ssZ",
        "updated_at": "yyyy-mm-ddThh:mm:ssZ",
    },
    {
        "id": 2,
        "notes": "Example notes 2",
        "medium": "email",
        "created_at": "yyyy-mm-ddThh:mm:ssZ",
        "updated_at": "yyyy-mm-ddThh:mm:ssZ",
    },
]
```

### Create case
Creates a new case.
All fields are optional and will be set to empty values if not specified.

Request:
``` http
POST /api/cases/

{
    "notes": "Example notes 1",
    "medium": "phone",
}
```
Success response:
``` http
Status: 201 (Created)
```

### Update case
Updates the case with the given id.
Fields that are not specified will not be updated.
If a filed is specified but with an empty value it will be set to an empty value.

Request:
``` http
PATCH /api/cases/<id>/

{
    "notes": "Example notes 1",
    "medium": "phone",
}
```
Success response:
``` http
Status: 204 (No Content)
```

### Delete case
Deletes the case with the given id.

Request:
``` http
DELETE /api/cases/<id>/
```

Success response:
``` http
Status: 204 (No Content)
```

### Get categories
Returns all categories.

Request:
``` http
GET /api/categories/
```

Success response:
``` http
Status: 200 (OK)

(The response format is not yet finalized)
```
