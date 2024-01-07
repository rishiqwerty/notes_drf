### NOTES BACKEND SERVER

#### Reason for Choosing Django:  
- I have been coding in Python for very long time, I found Django to be the go-to web framework for Python.
- Project setup is pretty easy.
- Django ORM is efficient and easy to use.
- Django Rest Framework library makes API creation quick.

#### Prerequisites
- Postgres (Preferably v16)
- A postgre user with Create permission
- Python (Preferably v3.11)

#### Setup
**Postgres**  
- Run *psql postgres* from the terminal, this will connect with postgres with user postgre

- Switch user by *SET ROLE \<user>* 
- Create Database *CREATE DATABASE \<database_name>;*

- Next need to put this database info in Django config. Check Python Setup for more details.

**Python Setup**
- Git clone This repo
    ```
        git clone https://github.com/rishiqwerty/notes_drf.git
    ```
- Create a new virtual environment
    ```
        python3 -m venv <env_name>
    ```
- Go inside backend folder and create .env
- Inside this file store this
    ```
        SECRET_KEY = <Add secure key>
        # DB Config
        NAME =  <DB name which we created during Postgres setup>
        USER = '<user>'
        PASSWORD = '<User password>'
        HOST = '<Host>'
        PORT = '<Port>'
    ```
- Now Run the environment
    ```
        workon <venv>
    ```
- Install all the requirements files, Go to the backend folder and run the below command
    ```
        pip install -r requirements.txt
    ```
- From the backend folder run migrations, this will generate the tables and schema on set upped database
    ```
        python manage.py migrate
    ```

**Run Server**
- From backend run server, this will start the server on the desired port.  
    ```
        python manage.py runserver <Port>
    ```
- Now, the Server can be accessible at localhost:\<port>

**Testing**
- From the backend with python virtual env being active run the following command.  
Authentication app tests
    ```
        python manage.py test authentication.tests
    ``` 
    Notes app tests  
    ```
        python manage.py test notes.tests
    ``` 

**Extras**
- Added one more script to deactivate shared notes which were shared for a limited duration of time. This is supposed to be run regularly as a cron
Run it from the backend folder
    ```
        python deactivate_shared_notes.py
    ```
