![](https://github.com/PUM-05/backend/actions/workflows/django.yml/badge.svg)
![](https://github.com/PUM-05/backend/actions/workflows/style.yml/badge.svg)
![](https://github.com/PUM-05/backend/actions/workflows/sonar.yml/badge.svg)


# Backend readme
Contains instructions for setting up and running the backend part of the Personalkollen project.



# Requirements
- Python 3.10 (or later)
- Git
- Pip

# Setup (MacOS/Linux)

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

# Setup (Windows 10/11)

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

Activate the environment:
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

# Deploy static files from frontend
> Note:
> This additionally requires that Node.js and npm are installed.

- Pull the main branch of both repositories.
- Build frontend:
```
npm run build
```
- Delete everything in `backend/src/static/`
- Move/Copy the files from `frontend/frontend-friends/build` into `backend/src/static/`


# Starting the server
- Run the server:
```
python3 src/manage.py runserver
```
