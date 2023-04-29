This project provides an API for managing user accounts, recipes and ingredients, built with Django and Django Rest Framework. Users can register, login, and logout using Django token authentication. The API allows users to view, create, update, and delete their own recipes and ingredients, as well as view recipes uploaded by other users. Users can also leave reviews for recipes, which include a rating and a comment.

# Installation

1.  Clone this repository:


- `git clone https://github.com/kirantyefun/cupofjoe.git`
- `cd cupofjoe/backend` 

## Backend

2.  Create a virtual environment and activate it:


`python -m venv env
source env/bin/activate` 

3.  Install dependencies:

`pip install -r requirements.txt` 

4.  Migrate the database:


`python manage.py migrate` 

5.  Create a superuser account:


`python manage.py createsuperuser` 

6.  Start the development server:


`python manage.py runserver` 

## Usage/API documentation:

### Authentication

To authenticate with the API, send a POST request to `/api/v1/users/login/` with the user's username and password in the request body:

`{
  "username": "johndoe@example.com",
  "password": "password123"
}` 

The API will respond with a token:

jsonCopy code

`{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}` 

Include the access token in subsequent requests by including an `Authorization` header with the value `Token <access_token>`:

`Authorization: Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` 

### User API

#### Register

To register a new user, send a POST request to `/api/v1/users/register/` with the user's username, email, and password in the request body:

`{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "password123"
}` 

The API will respond with the new user's username and email:

`{
  "username": "johndoe",
  "email": "johndoe@example.com"
}` 

#### Login

To login, send a POST request to `/api/token/` with the user's username and password in the request body (see Authentication):

jsonCopy code

`{
  "username": "johndoe",
  "password": "password123"
}` 

The API will respond with a token (see Authentication).

#### Logout

To logout, send a POST request to `/api/v1/users/logout/` with the user's access token in authorization Header

The API will respond with a status of 204 No Content.

#### Endpoint: `/users/my-orders/`
-   GET: Returns a list of order made by current user. This endpoint can be accessed only by someone with valid authentication token.

### Cafe API

#### Endpoint: `/cafes/`

Methods:

-   GET: Returns a list of cafes with their details and menu items. This endpoint can be accessed by anyone without authentication.
-   POST: Allows an authenticated user to register their cafe. The request body should include the details of the cafe to be registered.

#### Endpoint: `/cafes/{id}/`

Methods:

-   GET: Returns the details of a specific cafe with its menu items. This endpoint can be accessed by anyone without authentication.
-   PUT: Allows the cafe owner to update the details of their cafe. The request body should include the updated details of the cafe.
-   PATCH: Allows the cafe owner to update some of the details of their cafe. The request body should include the updated details of the cafe.
-   DELETE: Allows the cafe owner to delete their cafe. 


#### Endpoint: `/cafes/{id}/place-order/`

Methods:

-   POST: Allows an authenticated user to place an order for a cafe. The request body should include the details of the order including the id of item, the quantity, and any additional instructions.

#### Endpoint: `/cafes/{id}/view-orders/`

Methods:

-   GET: Returns a list of all orders placed for a specific cafe. This endpoint can only be accessed by the cafe owner.

#### Endpoint: `/menu-items/`

Methods:

-   GET: Returns a list of all menu items for the authenticated user's cafe. This endpoint can only be accessed by a cafe owner.
-   POST: Allows a cafe owner to add a new menu item to their cafe's menu. The request body should include the details of the new menu item.

#### Endpoint: `/menu-items/{id}/`

Methods:

-   PUT: Allows the cafe owner to update the details of a menu item. The request body should include the updated details of the menu item.
-   PATCH: Allows the cafe owner to update some of the details of a menu item. The request body should include the updated details of the menu item.
-   DELETE: This endpoint will return a 405 status code if a Delete request is made.

