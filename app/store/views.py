from flask import Blueprint, request, abort
from app.auth.utils import token_required
from app.store.utils import response, response_for_created_store, response_for_user_store, response_with_pagination, \
    get_user_store_json_list, paginate_stores
from app.models import User, Store

# Initialize blueprint
store = Blueprint('store', __name__)


@store.route('/storelists/', methods=['GET'])
@token_required
def storelist(current_user):
    """
    Return all the stores owned by the user or limit them to 10.
    Return an empty stores object if user has no stores
    :param current_user:
    :return:
    """
    user = User.get_by_id(current_user.id)
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', None, type=str)

    items, nex, pagination, previous = paginate_stores(current_user.id, page, q, user)

    if items:
        return response_with_pagination(get_user_store_json_list(items), previous, nex, pagination.total)
    return response_with_pagination([], previous, nex, 0)


@store.route('/storelists/', methods=['POST'])
@token_required
def create_storelist(current_user):
    """
    Create a Store from the sent json data.
    :param current_user: Current User
    :return:
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        if name:
            user_store = Store(name.lower(), current_user.id)
            user_store.save()
            return response_for_created_store(user_store, 201)
        return response('failed', 'Missing name attribute', 400)
    return response('failed', 'Content-type must be json', 202)


@store.route('/storelists/<store_id>', methods=['GET'])
@token_required
def get_store(current_user, store_id):
    """
    Return a user store with the supplied user Id.
    :param current_user: User
    :param store_id: Store Id
    :return:
    """
    try:
        int(store_id)
    except ValueError:
        return response('failed', 'Please provide a valid Store Id', 400)
    else:
        user_store = User.get_by_id(current_user.id).stores.filter_by(id=store_id).first()
        if user_store:
            return response_for_user_store(user_store.json())
        return response('failed', "Store not found", 404)


@store.route('/storelists/<store_id>', methods=['PUT'])
@token_required
def edit_store(current_user, store_id):
    """
    Validate the store Id. Also check for the name attribute in the json payload.
    If the name exists update the store with the new name.
    :param current_user: Current User
    :param store_id: Store Id
    :return: Http Json response
    """
    if request.content_type == 'application/json':
        data = request.get_json()
        name = data.get('name')
        if name:
            try:
                int(store_id)
            except ValueError:
                return response('failed', 'Please provide a valid Store Id', 400)
            user_store = User.get_by_id(current_user.id).stores.filter_by(id=store_id).first()
            if user_store:
                user_store.update(name)
                return response_for_created_store(user_store, 201)
            return response('failed', 'The Store with Id ' + store_id + ' does not exist', 404)
        return response('failed', 'No attribute or value was specified, nothing was changed', 400)
    return response('failed', 'Content-type must be json', 202)


@store.route('/storelists/<store_id>', methods=['DELETE'])
@token_required
def delete_store(current_user, store_id):
    """
    Deleting a User Store from the database if it exists.
    :param current_user:
    :param store_id:
    :return:
    """
    try:
        int(store_id)
    except ValueError:
        return response('failed', 'Please provide a valid Store Id', 400)
    user_store = User.get_by_id(current_user.id).stores.filter_by(id=store_id).first()
    if not user_store:
        abort(404)
    user_store.delete()
    return response('success', 'Store Deleted successfully', 200)


@store.errorhandler(404)
def handle_404_error(e):
    """
    Return a custom message for 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'Store resource cannot be found', 404)


@store.errorhandler(400)
def handle_400_errors(e):
    """
    Return a custom response for 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad Request', 400)
