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
- __Request__
  ``` http
  POST /api/login/
  ```
  ``` json
  {
    "username": "<username>",
    "password": "<password>"
  }
  ```
- __Response__\
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
- __Request__:
  ``` http
  POST /api/logout/
  Cookie: sessionid=...
  ```
- __Response__:
    ``` http
    Status: 200 (OK)
    ```

### Check
Checks if the user is logged in or not.
- __Request__:
  ``` http
  GET /api/check/
  Cookie: sessionid=...
  ```
- __Response__:\
    If logged in:
    ``` http
    Status: 200 (OK)
    ```
    If not logged in:
    ``` http
    Status: 401 (Unauthorized)
    ```

## Cases
### Get cases
Gets all cases.
- __Request__:
    ``` http
    GET /api/cases/
    ```
    Query parameters:
    - (Not jet implemented)

- __Response__:
    ``` http
    Status: 200 (OK)
    ```
    ``` json
    [
        {
            "id": 1,
            "notes": "Example notes 1",
            "medium": "phone",
            "created_at": "yyyy-mm-ddThh:mm:ssZ",
            "updated_at": "yyyy-mm-ddThh:mm:ssZ",
            ...
        },
        {
            "id": 2,
            "notes": "Example notes 2",
            "medium": "email",
            "created_at": "yyyy-mm-ddThh:mm:ssZ",
            "updated_at": "yyyy-mm-ddThh:mm:ssZ",
            ...
        },
        ...
    ]
    ```

### Create case
Creates a new case.
Fields that are not specified will be set to default values.
- __Request__:
    ``` http
    POST /api/cases/
    ```
    ``` json
    {
        "notes": "Example notes 1",
        "medium": "phone",
        ...
    }
    ```
- __Response__:
    ``` http
    Status: 201 (Created)
    ```

### Update case
Updates the case with the given id.
Fields that are not specified will not be updated.
- __Request__:
    ``` http
    PATCH /api/cases/<id>/
    ```
    ``` json
    {
        "notes": "Example notes 1",
        "medium": "phone",
        ...
    }
    ```
- __Response__:
    ``` http
    Status: 204 (No Content)
    ```
