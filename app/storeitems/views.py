from flask import Blueprint, request, abort
from app.auth.utils import token_required
from app.storeitems.utils import store_required, response, get_user_store, response_with_store_item, \
    response_with_pagination, get_paginated_items
from sqlalchemy import exc
from app.models import StoreItem

storeitems = Blueprint('items', __name__)


@storeitems.route('/storelists/<store_id>/items/', methods=['GET'])
@token_required
@store_required
def get_items(current_user, store_id):
    """
    A user`s items belonging to a Store specified by the store_id are returned if the Store Id
    is valid and belongs to the user.
    An empty item list is returned if the store has no items.
    :param current_user: User
    :param store_id: Store Id
    :return: List of Items
    """
    # Get the user Store
    store = get_user_store(current_user, store_id)
    if store is None:
        return response('failed', 'Store not found', 404)

    # Get items in the store
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', None, type=str)
    items, nex, pagination, previous = get_paginated_items(store, store_id, page, q)

    # Make a list of items
    if items:
        result = []
        for item in items:
            result.append(item.json())
        return response_with_pagination(result, previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)


@storeitems.route('/storelists/<store_id>/items/<item_id>/', methods=['GET'])
@token_required
@store_required
def get_item(current_user, store_id, item_id):
    """
    An item can be returned from the Store if the item and Store exist and below to the user.
    The Store and Item Ids must be valid.
    :param current_user: User
    :param store_id: Store Id
    :param item_id: Item Id
    :return:
    """
    # Check item id is an integer
    try:
        int(item_id)
    except ValueError:
        return response('failed', 'Provide a valid item Id', 202)

    # Get the user Store
    store = get_user_store(current_user, store_id)
    if store is None:
        return response('failed', 'User has no Store with Id ' + store_id, 404)

    # Delete the item from the store
    item = store.items.filter_by(id=item_id).first()
    if not item:
        abort(404)
    return response_with_store_item('success', item, 200)


@storeitems.route('/storelists/<store_id>/items/', methods=['POST'])
@token_required
@store_required
def post(current_user, store_id):
    """
    Storing an item into a Store
    :param current_user: User
    :param store_id: Store Id
    :return: Http Response
    """
    if not request.content_type == 'application/json':
        return response('failed', 'Content-type must be application/json', 401)

    data = request.get_json()
    item_name = data.get('name')
    if not item_name:
        return response('failed', 'No name or value attribute found', 401)

    # Get the user Store
    store = get_user_store(current_user, store_id)
    if store is None:
        return response('failed', 'User has no Store with Id ' + store_id, 202)

    # Save the Store Item into the Database
    item = StoreItem(item_name.lower(), data.get('description', None), store.id)
    item.save()
    return response_with_store_item('success', item, 200)


@storeitems.route('/storelists/<store_id>/items/<item_id>/', methods=['PUT'])
@token_required
@store_required
def edit_item(current_user, store_id, item_id):
    """
    Edit an item with a valid Id. The request content-type must be json and also the Store
    in which the item belongs must be among the user`s Stores.
    The name of the item must be present in the payload but the description is optional.
    :param current_user: User
    :param store_id: Store Id
    :param item_id: Item Id
    :return: Response of Edit Item
    """
    if not request.content_type == 'application/json':
        return response('failed', 'Content-type must be application/json', 401)

    try:
        int(item_id)
    except ValueError:
        return response('failed', 'Provide a valid item Id', 202)

    # Get the user Store
    store = get_user_store(current_user, store_id)
    if store is None:
        return response('failed', 'User has no Store with Id ' + store_id, 202)

    # Get the item
    item = store.items.filter_by(id=item_id).first()
    if not item:
        abort(404)

    # Check for Json data
    request_json_data = request.get_json()
    item_new_name = request_json_data.get('name')
    item_new_description = request_json_data.get('description', None)

    if not request_json_data:
        return response('failed', 'No attributes specified in the request', 401)

    if not item_new_name:
        return response('failed', 'No name or value attribute found', 401)

    # Update the item record
    item.update(item_new_name, item_new_description)
    return response_with_store_item('success', item, 200)


@storeitems.route('/storelists/<store_id>/items/<item_id>/', methods=['DELETE'])
@token_required
@store_required
def delete(current_user, store_id, item_id):
    """
    Delete an item from the user's Store.
    :param current_user: User
    :param store_id: Store Id
    :param item_id: Item Id
    :return: Http Response
    """
    # Check item id is an integer
    try:
        int(item_id)
    except ValueError:
        return response('failed', 'Provide a valid item Id', 202)

    # Get the user Store
    store = get_user_store(current_user, store_id)
    if store is None:
        return response('failed', 'User has no Store with Id ' + store_id, 202)

    # Delete the item from the store
    item = store.items.filter_by(id=item_id).first()
    if not item:
        abort(404)
    item.delete()
    return response('success', 'Successfully deleted the item from store with Id ' + store_id, 200)


@storeitems.errorhandler(404)
def item_not_found(e):
    """
    Custom response to 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'Item not found', 404)


@storeitems.errorhandler(400)
def bad_method(e):
    """
    Custom response to 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad request', 400)
