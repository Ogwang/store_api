# Store List API

The api enables you to create/ register a user within the application.

## Usage
- [Running the application](#starting-the-application)
- [Live Application](#live-application)
- [API Documentation](#api-documentation)
- [Users](#users)
- [Stores](#stores)
- [Store Items](#storeitems)
- [Generating Dummy Data](#generating-dummy-data)
- [Running tests](#running-tests)


## Starting the application
In order to run the application set the environment
variable below.
```
Windows
set FLASK_APP=run.py

Unix
export FLASK_APP=run.py
```
Then run the command below to start the application.
```
flask run
```

## Live Application
This API is hosted [here](http://#.herokuapp.com) on [heroku](heroku.com)

## API Documentation

The api documentation is hosted as the homepage
of the application.

## Users

### User registration.
Send a `POST` request to `v1/auth/register` endpoint with the payload in
`Json`

An example would be
```
{
  "email": "do@gmail.com",
  "password": "987654321"
}
```

The email value must be a valid email format and the password must be
four characters and above.
If the email is invalid or empty and the password is empty or less than
four character, the response `status` will be `failed` with the `message`
`Missing or wrong email format or password is less than four characters`
and a `status code` of `202`

As shown below:
```
{
    "message": "Missing or wrong email format or password",
    "status": "failed"
}
```

If the user already exists then they wont be registered again, the
following response will be returned.
```
{
    "message": "Failed, User already exists, Please sign In",
    "status": "failed"
}
```

If the request is successful and the user has been registered the
response below is returned. With an auth token
```
{
    "auth_token": "eyB0eXAiOiJKV1QiLCJhbGciOiKIUzI1NiJ9.eyBleHAiOjE1MDM0ODQ5OTYsImlhdCI6KFUwMzM5ODU4Niwic3ViIjo1fQ.KV6IEOohdo_xrz9__UeugIlir0qtJdKbEzBtLgqjt5A",
    "message": "Successfully registered",
    "status": "success"
}
```

### User Login
The user is able to login by send sending a `POST` request to
`v1/auth/login` with the json payload below.
```
{
  "email": "do@gmail.com",
  "password": "987654321"
}
```

If the request is successful the following response is returned:
```
{
    "auth_token": "eyB0eXAiOiJKV1QiLCJhbGciOiKIUzI1NiJ9.eyBleHAiOjE1MDM0ODQ5OTYsImlhdCI6KFUwMzM5ODU4Niwic3ViIjo1fQ.KV6IEOohdo_xrz9__UeugIlir0qtJdKbEzBtLgqjt5A",
    "message": "Successfully logged In",
    "status": "success"
}
```

Otherwise if the email is invalid, user with the email does not exist or
the password length is incorrect or less than four characters, the
following response is returned.
```
{
    "message": "Missing or wrong email format or password is less than four characters",
    "status": "failed"
}
```

### User Logout
The api also enables a user to logout. The `auth/logout` endpoint
provides this functionality.
The `POST` request to the endpoint must have an `Authorization`
header containing the auth token, otherwise the user wont be logged out.

Example of the Authorization header
```
Authorization Bearer <token>
```

If the operation is successful, the response below will be returned.
```
{
    "message": "Successfully logged out",
    "status": "success"
}
```

If the token has expired this will be returned.

```
{
    "message": "Signature expired, Please sign in again",
    "status": "failed"
}
```

For an invalid token
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}

```

Without an Authorization header
```
{
    "message": "Provide an authorization header",
    "status": "failed"
}
```

## Stores
The user is also able to create and get back a list of their stores.

### Create Store
Below is an example of a request to create a store. **name** is a
required attribute. An auth token must be attached in the Authorization
header
```
{
  "name": "Uchumi"
}
```

The following response will be returned
```
{
    "createdAt": "Thur, 16 May 2019 10:14:52 GMT",
    "id": 2,
    "modifiedAt": "Thur, 16 May 2019 10:14:52 GMT",
    "name": "Uchumi",
    "status": "success"
}
```

### Get user`s Stores
Below is an example of a *get* request endpoint to get the users stores.
An auth token must be attached in the Authorization
header. The results returned are paginated.
```
v1/storelists
```

### Get a user store by Id
You can also get a store by its id by using the
this endpoint and replacing the store_id with an existing store Id.
```
v1/storelists/<store_id>
```
The following response will be returned.
```
{
    "store": {
        "createdAt": "2019-05-16T19:56:07.942974",
        "id": 3,
        "modifiedAt": "2019-05-16T19:56:07.942974",
        "name": "Travel"
    },
    "status": "success"
}
```

### Edit a store
You can also edit the store name by sending a `PUT` request to
this endpoint with a Json payload having the name attribute
```
v1/storelists/<store_id>
```

Payload
```
{
  "name": "Cooking"
}
```

### Delete a Store
A store can also be deleted by sending a `Delete`
request with the store Id as shown below.
```
v1/storelists/<store_id>
```

## StoreItems
You can also add, edit, update and delete items
in a Store.

### Get Items from a Store
Get all the items contained in the store by
specifying the Store Id. The results returned
paginated.

```
v1/storelists/<store_id>/items
```

### Get an Item from the Store
You can also get an item from the Store by specifying
the item Id and Store Id as shown in the endpoint
below.
```
v1/storelists/<store_id>/items/<item_id>
```

### Add item to store
Send a Json payload with the item name and/or
description to this endpoint by specifying the
Store Id.
```
v1/storelists/<store_id>/items
```
Example Json payload
```
{
  "name": "unga",
  "description": "sample description"
}
```

### Edit an Item in the Store
An item can be edited by sending a `PUT` request
with a Json payload with a name and/or description.
Specifying the Store Id and Item Id as shown in the
endpoint below.
```
v1/storelists/<store_id>/items/<item_id>
```

### Delete an Item from the Store
To delete an item from a Store, send a `DELETE`
request specifying a Store Id and Item Id as shown
below:
```
v1/storelists/<store_id>/items/<item_id>
```

## Generating dummy data
You can also generate dummy data to test out the
different API endpoints.
All you have to do is run this command

```
python manage.py dummy
```

A `user` with an email address of `example@example.com`
and password `7654321` is created. And also `100`
Stores and `1000` Store Items are created
and items linked to the different Stores.

## Running tests
Before running the application tests, update your env variables
```
export  APP_SETTINGS=app.config.TestingConfig
export DATABASE_URL_TEST=<postgres database url>
```

### Running tests without coverage
You can now run the tests from the terminal
```
python manage.py test
```

### Running tests with coverage
You can also run tests with coverage by running this command in the terminal
```
nosetests --with-coverage --cover-package=app
```
