This project provides an API for managing user accounts, recipes and ingredients, built with Django and Django Rest Framework. Users can register, login, and logout using Django token authentication. The API allows users to view, create, update, and delete their own recipes and ingredients, as well as view recipes uploaded by other users. Users can also leave reviews for recipes, which include a rating and a comment.

# Installation

1.  Clone this repository:


- `git clone https://github.com/kirantyefun/cupofjoe.git`
- `cd recipe-hero/recipe-apis` 

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

## Usage

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
