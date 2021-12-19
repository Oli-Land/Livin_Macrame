from main import db
from flask import Blueprint
import os

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("create")
def create_db():
    """ Creates tables in the database based on the models. """
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    """ Drops tables in the database """
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted!")

@db_commands.cli.command("seed")
def seed_db():
    from models.projects import Project
    from faker import Faker
    faker = Faker()

    for i in range(10):
        project = Project(faker.catch_phrase())
        db.session.add(project)

    db.session.commit()
    print("Tables seeded!")

@db_commands.cli.command("reset")
def reset_db():
    """ Drops, creates and seeds tables """

    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted!")

    db.create_all()
    print("Tables created!")

    from models.projects import Project
    from faker import Faker
    from random import randint
    faker = Faker()

    for i in range(10):
        project = Project()
        project.project_name = faker.catch_phrase()
        project.description = faker.catch_phrase()
        project.price = randint(1,500)
        db.session.add(project)

    db.session.commit()
    print("Tables seeded!")

@db_commands.cli.command("dump")
def dump_db():

    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")

    os.system(f" pg_dump {db_name} -U {db_user} > db_dump.txt")