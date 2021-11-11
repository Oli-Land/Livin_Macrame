import unittest

from werkzeug.wrappers import response
from main import create_app
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["FLASK_ENV"] = "testing"

class TestCourses(unittest.TestCase):
    def setUp(self):        
        self.app = create_app()
        self.client = self.app.test_client()

    def test_course_index(self):
        response = self.client.get("/courses/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Course Index</h1>', response.data)

    def test_create_bad_course(self):
        response = self.client.post("/courses/", data={"course_name": ""})
        self.assertEqual(response.status_code, 400)

    def test_create_good_course(self):
        response = self.client.post("/courses/", data={"course_name": "testcourse"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["course_name"], "testcourse")
        self.client.delete(f"/courses/{response.get_json()['course_id']}/")

    def test_delete_course(self):
        response1 = self.client.post("/courses/", data={"course_name": "testcourse"})
        id = response1.get_json()["course_id"]
        
        response2 = self.client.delete(f"/courses/{id}/")
        self.assertEqual(response2.status_code, 200)

    def test_update_course(self):
        response1 = self.client.post("/courses/", data={"course_name": "testcourse"})
        id = response1.get_json()["course_id"]
        
        response2 = self.client.put(f"/courses/{id}/", json={"course_name": "newtestcourse"})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.get_json()["course_name"], "newtestcourse")
        
        self.client.delete(f"/courses/{id}/")