from flask import make_response, jsonify, url_for
from app import app
from app.models import Store


def response_for_user_store(user_store):
    """
    Return the response for when a single store when requested by the user.
    :param user_store:
    :return:
    """
    return make_response(jsonify({
        'status': 'success',
        'store': user_store
    }))


def response_for_created_store(user_store, status_code):
    """
    Method returning the response when a store has been successfully created.
    :param status_code:
    :param user_store: Store
    :return: Http Response
    """
    return make_response(jsonify({
        'status': 'success',
        'id': user_store.id,
        'name': user_store.name,
        'createdAt': user_store.create_at,
        'modifiedAt': user_store.modified_at
    })), status_code


def response(status, message, code):
    """
    Helper method to make a http response
    :param status: Status message
    :param message: Response message
    :param code: Response status code
    :return: Http Response
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), code


def get_user_store_json_list(user_stores):
    """
    Make json objects of the user stores and add them to a list.
    :param user_stores: Store
    :return:
    """
    stores = []
    for user_store in user_stores:
        stores.append(user_store.json())
    return stores


def response_with_pagination(stores, previous, nex, count):
    """
    Make a http response for StoreList get requests.
    :param count: Pagination Total
    :param nex: Next page Url if it exists
    :param previous: Previous page Url if it exists
    :param stores: Store
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': 'success',
        'previous': previous,
        'next': nex,
        'count': count,
        'stores': stores
    })), 200


def paginate_stores(user_id, page, q, user):
    """
    Get a user by Id, then get hold of their stores and also paginate the results.
    There is also an option to search for a store name if the query param is set.
    Generate previous and next pagination urls
    :param q: Query parameter
    :param user_id: User Id
    :param user: Current User
    :param page: Page number
    :return: Pagination next url, previous url and the user stores.
    """
    if q:
        pagination = Store.query.filter(Store.name.like("%" + q.lower().strip() + "%")).filter_by(user_id=user_id) \
            .paginate(page=page, per_page=app.config['STORE_AND_ITEMS_PER_PAGE'], error_out=False)
    else:
        pagination = user.stores.paginate(page=page, per_page=app.config['STORE_AND_ITEMS_PER_PAGE'],
                                           error_out=False)
    previous = None
    if pagination.has_prev:
        if q:
            previous = url_for('store.storelist', q=q, page=page - 1, _external=True)
        else:
            previous = url_for('store.storelist', page=page - 1, _external=True)
    nex = None
    if pagination.has_next:
        if q:
            nex = url_for('store.storelist', q=q, page=page + 1, _external=True)
        else:
            nex = url_for('store.storelist', page=page + 1, _external=True)
    items = pagination.items
    return items, nex, pagination, previous
