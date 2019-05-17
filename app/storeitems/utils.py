from flask import jsonify, make_response, request, url_for
from app import app
from functools import wraps
from app.models import User, StoreItem


def store_required(f):
    """
    Decorator to ensure that a valid store id is sent in the url path parameters
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        store_id_ = request.view_args['store_id']
        try:
            int(store_id_)
        except ValueError:
            return response('failed', 'Provide a valid Store Id', 401)
        return f(*args, **kwargs)

    return decorated_function


def response(status, message, status_code):
    """
    Make an http response helper
    :param status: Status message
    :param message: Response Message
    :param status_code: Http response code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code


def response_with_store_item(status, item, status_code):
    """
    Http response for response with a store item.
    :param status: Status Message
    :param item: StoreItem
    :param status_code: Http Status Code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'item': item.json()
    })), status_code


def response_with_pagination(items, previous, nex, count):
    """
    Get the Store items with the result paginated
    :param items: Items within the Store
    :param previous: Url to previous page if it exists
    :param nex: Url to next page if it exists
    :param count: Pagination total
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': 'success',
        'previous': previous,
        'next': nex,
        'count': count,
        'items': items
    })), 200


def get_user_store(current_user, store_id):
    """
    Query the user to find and return the store specified by the store Id
    :param store_id: Store Id
    :param current_user: User
    :return:
    """
    user_store = User.get_by_id(current_user.id).stores.filter_by(id=store_id).first()
    return user_store


def get_paginated_items(store, store_id, page, q):
    """
    Get the items from the store and then paginate the results.
    Items can also be search when the query parameter is set.
    Construct the previous and next urls.
    :param q: Query parameter
    :param store: Store
    :param store_id: Store Id
    :param page: Page number
    :return:
    """

    if q:
        pagination = StoreItem.query.filter(StoreItem.name.like("%" + q.lower().strip() + "%")) \
            .order_by(StoreItem.create_at.desc()) \
            .filter_by(store_id=store_id) \
            .paginate(page=page, per_page=app.config['STORE_AND_ITEMS_PER_PAGE'], error_out=False)
    else:
        pagination = store.items.order_by(StoreItem.create_at.desc()).paginate(page=page, per_page=app.config[
            'STORE_AND_ITEMS_PER_PAGE'], error_out=False)

    previous = None
    if pagination.has_prev:
        if q:
            previous = url_for('items.get_items', q=q, store_id=store_id, page=page - 1, _external=True)
        else:
            previous = url_for('items.get_items', store_id=store_id, page=page - 1, _external=True)
    nex = None
    if pagination.has_next:
        if q:
            nex = url_for('items.get_items', q=q, store_id=store_id, page=page + 1, _external=True)
        else:
            nex = url_for('items.get_items', store_id=store_id, page=page + 1, _external=True)
    return pagination.items, nex, pagination, previous
