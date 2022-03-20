import unittest
import os
from models.projects import Project
from main import create_app, db

class TestProjects(unittest.TestCase):
    #Runs before the tests
    @classmethod
    def setUp(cls):
        if os.environ.get("FLASK_ENV") != "testing":
            raise EnvironmentError("FLASK_ENV is not testing")
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        db.create_all()

        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])

    #runs after all the tests, removes the tables and stops the app
    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    #POST method in projects
    def test_post_project(self):
        #register and login a user
        response = self.client.post('/users/signup', data={
            'email': 'tester@example.com',
            'name': 'tester',
            'password': '1234567'
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/users/login', data={
            'email': 'tester@example.com',
            'name': 'tester',
            'password': '1234567'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        #creating the data for the project
        project_data = {
            "project_name": "test_project",
            "description": "test_description",
            "price": "567" 
            
        }

        response = self.client.post("projects/",data = project_data)
        project = self.client.get("projects/")
        self.assertIsNotNone(project)
        self.assertIn("unittest_name", str(project.data))


    # test the GET method in /projects/ returns all the projects
    def test_get_all_projects(self):
        response = self.client.get("/projects/")
        
        #check the OK status
        self.assertEqual(response.status_code, 200)
        #Check that we receive a string in the html response
        self.assertIn("projects", str(response.data))
