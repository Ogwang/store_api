from tests.base import BaseTestCase
import unittest
import json


class TestStoreBluePrint(BaseTestCase):
    def test_creating_a_store(self):
        """
        Test that a user can add a store
        :return:
        """
        with self.client:
            self.create_store(self.get_user_token())

    def test_name_attribute_is_set_in_store_creation_request(self):
        """
        Test that the name attribute is present in the json request.
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/storelists/',
                headers=dict(Authorization='Bearer ' + self.get_user_token()),
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'], 'failed')
            self.assertTrue(data['message'], 'Missing name attribute')

    def test_store_post_content_type_is_json(self):
        """
        Test that the request content type is application/json
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/storelists/',
                headers=dict(Authorization='Bearer ' + self.get_user_token()),
                data=json.dumps(dict(name='Travel'))
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 202)
            self.assertTrue(data['status'], 'failed')
            self.assertTrue(data['message'], 'Content-type must be json')

    def test_user_can_get_list_of_stores(self):
        """
        Test that a user gets back a list of their stores or an empty dictionary if they do not have any yet
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/storelists/',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['stores'], list)
            self.assertEqual(len(data['stores']), 0)
            self.assertEqual(data['count'], 0)
            self.assertIsInstance(data['count'], int)
            self.assertEqual(data['previous'], None)
            self.assertEqual(data['next'], None)

    def test_request_for_a_store_has_integer_id(self):
        """
        Test that only integer store Ids are allowed
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/storelists/dsfgsdsg',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Store Id')

    def test_store_by_id_is_returned_on_get_request(self):
        """
        Test that a user store is returned when a specific Id is specified
        :return:
        """
        with self.client:
            token = self.get_user_token()
            # Create a Store
            response = self.client.post(
                'v1/storelists/',
                data=json.dumps(dict(name='Travel')),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            # Test Store creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['name'], 'Travel')
            response = self.client.get(
                'v1/storelists/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['store']['name'] == 'travel')
            self.assertIsInstance(data['store'], dict)
            self.assertTrue(response.content_type == 'application/json')

    def test_no_store_returned_by_given_id(self):
        """
        Test there is no store/no store returned with given Id
        :return:
        """
        with self.client:
            token = self.get_user_token()

            response = self.client.get(
                'v1/storelists/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(response.content_type == 'application/json')

    def test_deletion_handles_no_store_found_by_id(self):
        """
        Show tha a 404 response is returned when an un existing store is being deleted.
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/storelists/1',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Store resource cannot be found')
            self.assertTrue(response.content_type == 'application/json')

    def test_request_for_deleting_store_has_integer_id(self):
        """
        Test that only integer store Ids are allowed
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/storelists/dsfgsdsg',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Store Id')

    def test_store_is_updated(self):
        """
        Test that the Store details(name) is updated
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            # Create a Store
            response = self.client.post(
                'v1/storelists/',
                data=json.dumps(dict(name='Travel')),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            # Test Store creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['name'], 'Travel')
            # Update the store name
            res = self.client.put(
                'v1/storelists/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(name='Adventure')),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['name'] == 'Adventure')
            self.assertEqual(data['id'], 1)

    def test_id_of_store_to_be_edited_does_not_exist(self):
        """
        Test the store to be updated does not exist.
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            # Update the store name
            res = self.client.put(
                'v1/storelists/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(name='Adventure')),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 404)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'The Store with Id 1 does not exist')

    def test_id_of_store_to_be_edited_is_invalid(self):
        """
        Test the store id is invalid.
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            # Update the store name
            res = self.client.put(
                'v1/storelists/storeid',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(name='Adventure')),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Please provide a valid Store Id')

    def test_content_type_for_editing_store_is_json(self):
        """
        Test that the content type used for the request is application/json
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/storelists/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(name='Adventure'))
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 202)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Content-type must be json')

    def test_required_name_attribute_is_in_the_request_payload_and_has_a_value(self):
        """
        Test that the required attribute(name) exists and has value in the request payload
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/storelists/1',
                headers=dict(Authorization='Bearer ' + token),
                data=json.dumps(dict(name='')),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No attribute or value was specified, nothing was changed')

    def test_store_is_deleted(self):
        """
        Test that a Store is deleted successfully
        :return:
        """
        with self.client:
            # Get an auth token
            token = self.get_user_token()
            response = self.client.post(
                'v1/storelists/',
                data=json.dumps(dict(name='Travel')),
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            # Test Store creation
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['status'], 'success')
            self.assertTrue(data['name'], 'Travel')
            # Delete the created Store
            res = self.client.delete(
                'v1/storelists/1',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Store Deleted successfully')
            self.assertTrue(res.content_type == 'application/json')

    def test_400_bad_requests(self):
        """
        Test for Bad requests - 400s
        :return:
        """
        with self.client:
            token = self.get_user_token()
            res = self.client.put(
                'v1/storelists/1',
                headers=dict(Authorization='Bearer ' + token),
                content_type='application/json'
            )
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 400)
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Bad Request')

    def test_stores_returned_when_searched(self):
        """
        Test Stores are returned when a query search q is present in the url
        Also test that the next page pagination string is 'http://localhost/storelists/1/items/?page=2'
        and previous is none
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_stores(token)
            response = self.client.get(
                'v1/storelists/?q=T',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['stores'], list, 'Items must be a list')
            self.assertEqual(len(data['stores']), 3)
            self.assertEqual(data['stores'][0]['id'], 1)
            self.assertEqual(data['count'], 6)
            self.assertEqual(data['next'], 'http://localhost/v1/storelists/?q=T&page=2')
            self.assertEqual(data['previous'], None)
            self.assertEqual(response.status_code, 200)

    def test_stores_returned_when_searched_2(self):
        """
        Test Stores are returned when a query search q is present in the url
        Also test that the next page pagination string is None
        and previous is 'http://localhost/storelists/1/items/?page=1'
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_stores(token)
            response = self.client.get(
                'v1/storelists/?q=T&page=2',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['stores'], list, 'Items must be a list')
            self.assertEqual(len(data['stores']), 3)
            self.assertEqual(data['stores'][0]['id'], 4)
            self.assertEqual(data['count'], 6)
            self.assertEqual(data['next'], None)
            self.assertEqual(data['previous'], 'http://localhost/v1/storelists/?q=T&page=1')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
