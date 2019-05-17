from tests.base import BaseTestCase
import unittest
import json


class TestStoreItem(BaseTestCase):
    def test_item_post_request_content_type(self):
        """
        Test that the correct response is returned if the request payload content type is not application/json
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/storelists/1/items/',
                data=json.dumps(dict(name='food')),
                content_type='application/javascript',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Content-type must be application/json')
            self.assertEqual(response.status_code, 401)

    def test_item_put_request_content_type(self):
        """
        Test that the correct response is returned if the request payload content type is not application/json
        :return:
        """
        with self.client:
            response = self.client.put(
                'v1/storelists/1/items/1/',
                data=json.dumps(dict(name='food')),
                content_type='application/javascript',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Content-type must be application/json')
            self.assertEqual(response.status_code, 401)

    def test_store_id_is_invalid_in_request(self):
        """
        Test that the store Id is invalid
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/storelists/id/items/',
                data=json.dumps(dict(name='Food')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide a valid Store Id')
            self.assertEqual(response.status_code, 401)

    def test_store_id_is_invalid_in_put_request(self):
        """
        Test that the store Id is invalid
        :return:
        """
        with self.client:
            response = self.client.put(
                'v1/storelists/id/items/1/',
                data=json.dumps(dict(name='Food')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide a valid Store Id')
            self.assertEqual(response.status_code, 401)

    def test_name_attribute_is_missing_in_request(self):
        with self.client:
            response = self.client.post(
                'v1/storelists/1/items/',
                data=json.dumps(dict(description='')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No name or value attribute found')
            self.assertEqual(response.status_code, 401)

    def test_name_attribute_is_missing_in_put_request(self):
        """
        Test name attribute is missing
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_store(token)
            self.create_item(token)
            response = self.client.put(
                'v1/storelists/1/items/1/',
                data=json.dumps(dict(description='')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No name or value attribute found')
            self.assertEqual(response.status_code, 401)

    def test_name_attribute_has_no_value_in_request(self):
        with self.client:
            response = self.client.post(
                'v1/storelists/1/items/',
                data=json.dumps(dict(name='')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'No name or value attribute found')
            self.assertEqual(response.status_code, 401)

    def test_correct_response_when_user_has_no_store_with_specified_id_post_request(self):
        """
        Test that a user does not have a Store specified by that Id
        :return:
        """
        with self.client:
            response = self.client.post(
                'v1/storelists/1/items/',
                data=json.dumps(dict(name='food')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'User has no Store with Id 1')
            self.assertEqual(response.status_code, 202)

    def test_correct_response_when_user_has_no_store_with_specified_id_get_request(self):
        """
        Test that a user does not have a Store specified by that Id
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/storelists/1/items/',
                data=json.dumps(dict(name='food')),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Store not found')
            self.assertEqual(response.status_code, 404)

    def test_an_item_has_been_successfully_saved(self):
        """
        Test a Store Item has been successfully stored.
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_store(token)
            self.create_item(token)

    def test_items_are_returned(self):
        """
        Test Store Items are returned and the items are in a list
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_store(token)
            self.create_item(token)
            response = self.client.get(
                'v1/storelists/1/items/',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['items'], list, 'Items must be a list')
            self.assertEqual(len(data['items']), 1)
            self.assertEqual(data['count'], 1)
            self.assertEqual(data['next'], None)
            self.assertEqual(data['previous'], None)
            self.assertEqual(response.status_code, 200)

    def test_items_returned_when_searched(self):
        """
        Test Store Items are returned when a query search q is present in the url
        Also test that the next page pagination string is 'http://localhostv1/storelists/1/items/?page=2'
        and previous is none
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_store(token)
            self.create_items(token)
            response = self.client.get(
                'v1/storelists/1/items/?q=f',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['items'], list, 'Items must be a list')
            self.assertEqual(len(data['items']), 3)
            self.assertEqual(data['items'][0]['storeId'], 1)
            self.assertEqual(data['items'][0]['id'], 6)
            self.assertEqual(data['count'], 6)
            self.assertEqual(data['next'], 'http://localhost/v1/storelists/1/items/?q=f&page=2')
            self.assertEqual(data['previous'], None)
            self.assertEqual(response.status_code, 200)

    def test_items_returned_when_searched_2(self):
        """
        Test Store Items are returned when a query search q is present in the url
        Also test that the next page pagination is none and previous 'http://localhostv1/storelists/1/items/?page=1'
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_store(token)
            self.create_items(token)
            response = self.client.get(
                'v1/storelists/1/items/?q=f&page=2',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['items'], list, 'Items must be a list')
            self.assertEqual(len(data['items']), 3)
            self.assertEqual(data['items'][0]['storeId'], 1)
            self.assertEqual(data['items'][0]['id'], 3)
            self.assertEqual(data['count'], 6)
            self.assertEqual(data['next'], None)
            self.assertEqual(data['previous'], 'http://localhost/v1/storelists/1/items/?q=f&page=1')
            self.assertEqual(response.status_code, 200)

    def test_empty_item_list_is_returned_when_no_items_in_store(self):
        """
        Test empty items list is returned when the store is empty
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_store(token)
            response = self.client.get(
                'v1/storelists/1/items/',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

    def test_item_is_returned_successfully_get_request(self):
        """
        Test an item is returned on a get request
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_store(token)
            self.create_item(token)
            response = self.client.get(
                'v1/storelists/1/items/1/',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(data['item']['id'], 1)
            self.assertTrue(data['item']['name'] == 'food')
            self.assertEqual(response.status_code, 200)

    def test_item_to_be_returned_on_get_request_does_not_exist(self):
        """
        Test that the item to be returned on a get request does not exist.
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_store(token)
            response = self.client.get(
                'v1/storelists/1/items/1/',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Item not found')
            self.assertEqual(response.status_code, 404)

    def test_invalid_item_id_get_one_item_request(self):
        """
        Test that an invalid item Id has been sent to get an item
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/storelists/1/items/dsfdgfghjg/',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide a valid item Id')
            self.assertEqual(response.status_code, 202)

    def test_no_store_on_get_item_request(self):
        """
        Test there is no Store specified by that Id when getting an item by Id
        :return:
        """
        with self.client:
            response = self.client.get(
                'v1/storelists/1/items/1/',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'User has no Store with Id 1')
            self.assertEqual(response.status_code, 404)

    def test_invalid_item_id_delete_request(self):
        """
        Test that an invalid item Id has been sent.
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/storelists/1/items/dsfdgfghjg/',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Provide a valid item Id')
            self.assertEqual(response.status_code, 202)

    def test_no_store_delete_request(self):
        """
        Test there is no Store specified by that Id
        :return:
        """
        with self.client:
            response = self.client.delete(
                'v1/storelists/1/items/1/',
                headers=dict(Authorization='Bearer ' + self.get_user_token())
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'User has no Store with Id 1')
            self.assertEqual(response.status_code, 202)

    def test_item_is_deleted_successfully(self):
        with self.client:
            token = self.get_user_token()
            self.create_store(token)
            self.create_item(token)
            response = self.client.delete(
                'v1/storelists/1/items/1/',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully deleted the item from store with Id 1')
            self.assertEqual(response.status_code, 200)

    def create_item(self, token):
        """
        Create an item into a store
        :param token:
        :return:
        """
        response = self.client.post(
            'v1/storelists/1/items/',
            data=json.dumps(dict(name='food', description='Enjoying the good life')),
            content_type='application/json',
            headers=dict(Authorization='Bearer ' + token)
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertEqual(data['item']['id'], 1)
        self.assertTrue(data['item']['name'] == 'food')
        self.assertTrue(data['item']['description'] == 'Enjoying the good life')
        self.assertEqual(response.status_code, 200)

    def create_items(self, token):
        """
        Create an item into a store
        :param token:
        :return:
        """
        items = [
            {'name': 'food', 'description': 'Enjoying the good life'},
            {'name': 'fod', 'description': 'Enjoying the good life'},
            {'name': 'foood', 'description': 'Enjoying the good life'},
            {'name': 'foda', 'description': 'Enjoying the good life'},
            {'name': 'fd', 'description': 'Enjoying the good life'},
            {'name': 'foodad', 'description': 'Enjoying the good life'},
        ]
        for item in items:
            response = self.client.post(
                'v1/storelists/1/items/',
                data=json.dumps(dict(name=item['name'], description=item['description'])),
                content_type='application/json',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['item']['name'] == item['name'])
            self.assertTrue(data['item']['description'] == item['description'])
            self.assertEqual(response.status_code, 200)

    def test_item_to_be_deleted_does_not_exist(self):
        """
        Test that the item to be deleted does not exist.
        :return:
        """
        with self.client:
            token = self.get_user_token()
            self.create_store(token)
            response = self.client.delete(
                'v1/storelists/1/items/1/',
                headers=dict(Authorization='Bearer ' + token)
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'failed')
            self.assertTrue(data['message'] == 'Item not found')
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
