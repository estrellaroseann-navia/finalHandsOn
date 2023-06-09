import unittest
import warnings
from flask import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["API TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), """
    Hundredrows DATABASE User Details (CRUD)

    SELECT OPERATION
    [1] Create User Detail/s
    [2] Retrieve User Detail/s
    [3] Update User Detail/s
    [4] Delete User Detail/s
    [E] Exit
    """)
        
    
    def test_user_details(self):
        response = self.app.get("/user_details")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("rogers" in response.data.decode())

    def test_get_user_details_by_id(self):
        response = self.app.get("/user_details/21")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("miller" in response.data.decode())

    def test_get_user_details_by_id_not_found(self):
        response = self.app.get(f"/user_details/101")
        self.assertEqual(response.status_code, 404) 

    def test_create_user_details(self):
        data = {
            "id": "101",
            "first_name": "breee",
            "last_name": "zenders",
            "gender": "female",
            "password": "bree12kjfofjwefwo"
        }
        response = self.app.post("/user_details", json = data)
        self.assertEqual(response.status_code, 201)

    def test_update_user_details(self):
        data = {
            "id": "102",
            "first_name": "breana",
            "last_name": "zanders",
            "gender": "female",
            "password": "fjowfjwoefjowefij"
        }
        response = self.app.put("/user_details/92", json = data)
        self.assertEqual(response.status_code, 201)

    def test_update_user_details_not_found(self):
        data = {
            "id": "105",
            "first_name": "trina",
            "last_name": "alver",
            "gender": "female",
            "password": "jwoewif"
        }
        response = self.app.put("/user_details/92", json = data)
        self.assertEqual(response.status_code, 201)
    
    def test_delete_customer(self):
        response = self.app.delete("/user_details/45")
        self.assertEqual(response.status_code, 200)

    def test_delete_customer_not_found(self):
        response = self.app.delete("/user_details/137")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, "User details with ID 137 does not exist!")

if __name__ == "__main__":
    unittest.main()