# This is Genius Shop back-end

## Dependency

all dependencies are mentioned in `/Pipfile`. There are Django and Django-rest. The server was developped in python 3.9

## Start the server

`python manage runserver`

## Create user

send a post request to `http://localhost:8000/api/account/signup`

with the fallowing form-data

{"user_name", "password", "password2"}

user_name must be unique and both password must match.

You will get a token in return which is required for any other request to the server. 

## Get products

send a get request to `http://localhost:8000/api/products`

you will get all products. You can also apply filters and ordering products. 

### sortby
products will be ordered according to the given key: price or name.

ex:
http://localhost:8000/api/products?sortby=price

### department
filter product matching the given department.

ex:
'http://localhost:8000/api/products?department=sport'

### minprice and maxprice

apply a filter to the price.

ex: 'http://localhost:8000/api/products?minprice=120'

## add to the cart

send a post request to 'http://localhost:8000/api/add_products'

with the fallowing form-data

{"product_id", "quantity"}

you can add a product multiple times

## validate cart

send a post request to 'http://localhost:8000/api/validate'
