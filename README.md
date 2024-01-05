### NOTES BACKEND SERVER

#### Prequsites
- Postgres (Preferebly v16)
- A postgre user with Create permission
- Python (Preferebly v3.11)

#### Setup
**Postgres**  
- Run *psql postgres* from terminal, this will connect with postgres with user postgre

- Switch user by *SET ROLE \<user>* 
- Create Database *CREATE DATABASE \<database_name>;*

- Next need to put this database info in django config. Check Python Setup for more details.

**Python Setup**
- Git clone This report
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
- Install all the requirements file, Go to backend folder and run below command
    ```
        pip install -r requirements.txt
    ```
- From backend folder run migrations, this will generate the tables and schema on setupped database
    ```
        python manage.py migrate
    ```

**Run Server**
- From backend run server, this will start the server on desired port
    ```
        python manage.py runserver <Port>
    ```