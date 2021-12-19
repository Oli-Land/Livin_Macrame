# Livin' Macrame
A webapp for display of macrame projects


## Application stack:

The app runs on `Flask`, using a `PostgreSQL` database via `Psycopg2` and `SQLAlchemy`. Serialization is courtesy of `Marshmallow`, templating from `Jinja2`, migrations from `Flask-Migrate` with `Alembic`, and sessions via `Flask-Login`.

Image upload and storage is handled with `boto3`, accessing an S3 bucket.


## Dependencies:
* Python 3
* PostgreSQL
* virtualenv
* pip

## Setup:

The instructions for Ubuntu 20:

### Update repositories:

```sudo apt-get update```

### Clone GitHub repository: 

```git clone https://github.com/Oli-Land/Livin_Macrame.git ```

### Install python virtual environment: 

```sudo apt-get install python3-venv```

### Install pip: 

```python -m pip install --upgrade pip```


### CREATE VENV:
```bash
# /Livin_Macrame/
python3 -m venv venv
```

### ACTIVATE VENV
```bash
# /Livin_Macrame/
source venv/bin/activate
```

### INSTALL DEPENDENCIES
```bash
# /Livin_Macrame/
pip install -r requirements.txt
```

### CREATE DATABASE AND USER
```SQL
psql postgres

>> CREATE DATABASE <db_name_here>;
>> CREATE USER <user_name_here> WITH PASSWORD '<password_here>';
>> GRANT ALL PRIVILEGES ON DATABASE <db_name_here> TO <user_name_here>;
>> \q
```

### CREATE S3 BUCKET WITH IAM POLICY
The user needs to have programmatic access to the bucket to perform `GetObject`, `PutObject` and `DeleteObject` actions.

### SET ENVIRONMENT VARIABLES. 
Add a `.env` file to the `/Livin_Macrame/`:
```bash
DB_USER = # value from above
DB_PASS = # value from above
DB_NAME = # value from above
DB_DOMAIN = "localhost:5432"
SECRET_KEY = # dealer's choice - a long random string is most secure
AWS_ACCESS_KEY_ID= # value from AWS
AWS_SECRET_ACCESS_KEY=# value from AWS
AWS_S3_BUCKET=# value from AWS
```

### TERMINAL COMMANDS

Terminal commands for the app must be executed from the `/Livin_Macrame/FlaskApp/` directory. Currently available commands are:

`flask db-custom drop` -> drops all tables

`flask db-custom create` -> creates all tables

`flask db-custom seed` -> seeds the projects table

`flask db-custom seed` -> seeds the projects table

`flask db-custom dump` -> dumps all tables from the database into a text file called db_dump.txt (Ensure the postgres role which created the database has superuser privileges)


### RUN APP 
```bash
# /Livin_Macrame/FlaskApp/
flask run
``` 
