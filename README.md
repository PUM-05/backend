![](https://github.com/PUM-05/backend/actions/workflows/django.yml/badge.svg)
![](https://github.com/PUM-05/backend/actions/workflows/style.yml/badge.svg)
![](https://github.com/PUM-05/backend/actions/workflows/sonar.yml/badge.svg)

__Table of Contents__
- [Setup](#setup)
  * [Requirements](#requirements)
  * [Backend Setup (MacOS/Linux)](#backend-setup-macoslinux)
  * [Backend Setup (Windows 10/11)](#backend-setup-windows-1011)
  * [Deploy static files from frontend](#deploy-static-files-from-frontend)
  * [Starting the server](#starting-the-server)
- [API](#api)
  * [Authentication](#authentication)
    + [Login](#login)
    + [Logout](#logout)
    + [Check](#check)
  * [Cases](#cases)
    + [Get cases](#get-cases)
    + [Create case](#create-case)
    + [Update case](#update-case)
    + [Delete case](#delete-case)
    + [Get categories](#get-categories)

# Setup

## Requirements
- Python 3.10 (or later)
- Git
- Pip

## Backend Setup (MacOS/Linux)
- Git clone the repository to your local machine.
- Navigate to the project folder in your terminal.
- Create a virtual environmnent and activate it:
```
python3 -m venv .venv
source .venv/bin/activate
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

- Create a super user, and make sure to follow the instructions in the command line (the email is not required):
```
python3 src/manage.py createsuperuser
```

## Backend Setup (Windows 10/11)

- Git clone the repository to your local machine.
- Navigate to the project folder in your Windows terminal.
- Create a virtual environmnent:
```
python -m venv .venv
```

- If needed, add permissions to load scripts in PowerShell (tested on Windows 11):
```
Set-ExecutionPolicy -ExecutionPolicy AllSigned
```

- Activate the environment:
```
.venv\Scripts\activate
```

- Install requirements:
```
pip install -r requirements\requirements.txt
```

- Setup local database:
```
python src\manage.py migrate
```

- Run tests to make sure it works correctly (no errors should occur):
```
python src\manage.py test api
```

- Create a super user, and make sure to follow the instructions in the command line (the email is not required):
```
python src\manage.py createsuperuser
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
The password field is not always required, since some users may not have a password.
An empty password field will be treaded the same as if no password field was given.

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
Status: 204 (No Content)
Set-Cookie: sessionid=...
```
The username was valid, but a password is also required and wasn't provided in the request:
``` http
Status: 403 (Forbidden)
```
Wrong username or password:
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
Status: 204 (No Content)
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
Status: 204 (No Content)
```
Response if not logged in:
``` http
Status: 401 (Unauthorized)
```

## Cases
### Get cases
Returns a list with all cases sorted chronologically (latest at top) that match the given query parameters.
A request without parameters returns the latest 100 cases.

Query parameters:
- `id: int`
- `time-start: DateTime`
- `time-end: DateTime`
- `category-id: int`
- `medium: string`
- `per-page: int (default 100, set to 0 to disable pages)`
- `page: int (default 1)`

Request:
``` http
GET /api/case/
GET /api/case/<query>
```

Example:
``` http
GET /api/case/category-id=2&medium=phone&per-page=20&page=3
```

Success response:
``` http
Status: 200 (OK)
{
  "result_count": 1,
  "has_more": false,
  "cases": [
    {
        "id": 1,
        "notes": "Example notes 1",
        "medium": "phone",
        "customer_time": "PdDThhHmmMssS",
        "additional_time": "PdDThhHmmMssS",
        "form_fill_time": "PdDThhHmmMssS",
        "created_at": "yyyy-mm-ddThh:mm:ssZ",
        "updated_at": "yyyy-mm-ddThh:mm:ssZ",
        "category_id": 1,
    },
  ]
}
```

### Create case
Creates a new case.
All fields are optional and will be set to empty values if not specified.

Request:
``` http
POST /api/case/

{
    "notes": "Example notes 1",
    "medium": "phone",
    "customer_time": 0,
    "additional_time": 0,
    "form_fill_time": 0,
    "category_id": 1,
}
```
Success response:
``` http
Status: 201 (Created)
```

### Update case
Updates the case with the given id.
Fields that are not specified will not be updated.
If a field is specified but with an empty value it will be set to an empty value.

Request:
``` http
PATCH /api/case/<id>/

{
    "notes": "Example notes 1",
    "medium": "phone",
    "customer_time": 0,
    "additional_time": 0,
    "form_fill_time": 0,
    "category_id": 1,
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
DELETE /api/case/<id>/
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

[
    {
        "id": 1,
        "name": "Konto",
        "subcategories": [
            {"id": 2, "name": "Skapa nytt konto"},
            {"id": 3, "name": "Ta bort konto"}
        ]
    }, 
    {  
        "id": 4,
        "name": "Annat",
        "subcategories": []
    }
]
```
