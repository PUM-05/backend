![](https://github.com/PUM-05/backend/actions/workflows/django.yml/badge.svg)
![](https://github.com/PUM-05/backend/actions/workflows/style.yml/badge.svg)
![](https://github.com/PUM-05/backend/actions/workflows/sonar.yml/badge.svg)


# Backend readme
Contains instructions for setting up and running the backend part of the Personalkollen project.



# Requirements
- Python 3.10 (or later)
- Git
- Pip

# Setup
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

# Starting the server
- Run the server:
```
python3 src/manage.py runserver
```
