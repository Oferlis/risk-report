import json
import unittest
from PublishPackageVersion import app, load_data, save_data


class TestPublishPackageAPI(unittest.TestCase):

    def setUp(self):
        # Create a test client for the app
        self.app = app.test_client()
        self.app.testing = True

        # Initial sample data for testing
        self.sample_data = [
            {'PackageManager': 'Nuget',
             'PackageName': 'Test',
             'PackageVersion': ['1.0.0']},
            {'PackageManager': 'NPM',
             'PackageName': 'Test2',
             'PackageVersion': ['1.2.0', '1.4.0', '2.0.0']},
        ]

        # Save initial sample data to the data.json file
        save_data(self.sample_data)

    def tearDown(self):
        # Reset the data file to the initial state after each test
        save_data(self.sample_data)

    def test_get_all_data(self):
        response = self.app.get('/api/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), len(self.sample_data))

    def test_create_data(self):
        new_data = {"PackageName": "Test_add",
                    "PackageManager": "pip", "PackageVersion": "1.1.3"}
        response = self.app.post('/api/', json=new_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Data created successfully')

        # Check if the new data is present in the saved data
        saved_data = load_data()
        self.assertTrue(new_data in saved_data)

    def test_create_duplicated_data(self):
        new_data = {"PackageName": "Test_dup",
                    "PackageManager": "pip", "PackageVersion": "1.1.3"}
        response = self.app.post('/api/', json=new_data)
        self.assertEqual(response.status_code, 201)

        new_data = {"PackageName": "Test_dup",
                    "PackageManager": "pip", "PackageVersion": "1.1.3"}
        response = self.app.post('/api/', json=new_data)
        self.assertEqual(response.status_code, 409)

        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Package already exists')

        # Check if the new data is present in the saved data
        saved_data = load_data()
        self.assertTrue(new_data in saved_data)

    def test_create_data_with_invalid_payload(self):
        # Invalid payload with missing 'PackageName' field
        new_data = {"PackageManager": "wrong_name", "PackageVersion": 28}
        response = self.app.post('/api/', json=new_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Invalid data')

    def test_get_specific_package(self):
        response = self.app.get('/api/data/Nuget/Test/')
        print(response)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, load_data()[0])

    def test_get_wrong_sepcific_package(self):
        response = self.app.get('/api/data/wrong_package/Test2/')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Package not found')

    def test_get_next_version(self):
        response = self.app.get('/api/data/NPM/Test2/1.2.0/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, ['1.4.0', '2.0.0'])

    def test_get_next_version_failure(self):
        # try to get next version where none exist, should reutrn 404 status
        response = self.app.get('/api/data/NPM/Test2/2.0.0/')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Next versions not found')


if __name__ == '__main__':
    unittest.main()
