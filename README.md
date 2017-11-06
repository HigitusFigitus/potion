# Potion

> Potion is a custom RESTful API built with Flask.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Tests](#tests)

## Install
+ Clone this repository `git clone https://github.com/HigitusFigitus/potion.git`
+ Move into the repo directory
+ Build the Docker image `docker build -t potion:1.0 .`
+ Verify that the image built correctly `docker images`
+ Start the container `docker run -p 5000:5000 -d potion:1.0`
+ Verify that the container is running `docker ps`
+ Start an interactive session inside the container `docker exec -it <CONTAINER ID> /bin/bash`
+ Seed the database with sample data `python seed.py`
+ Exit the interactive shell `exit`
+ Access the API by navigating to `http://0.0.0.0:5000/api/v1/potions`

## Usage
Every potion has a potion name, which is a string and must be between 4 and 64 characters long, and globally unique. Also, potion names can only contain alphanumeric ascii characters, underscores, and dashes, and cannot start with an underscore or dash. \
Every potion has a potion type, which is a string and must be either `active` or `passive`. \
Every potion has a potion class, which is a string and depends on its potion type. For potions of type `passive` it can be `life` or `mana`. For potions of type `active` it can be `fire` or `poison`.

Users can retrieve the whole list of potions: \
`http://0.0.0.0:5000/api/v1/potions`

Users can retrieve a single potion by name: \
`http://0.0.0.0:5000/api/v1/potions/light_mana_potion`

Users can filter potions by specifying a potion_class or a potion_type: \
``

Authorized users can create potions. To do so, they must supply the potion name, potion type, and potion class. \
Authorization header must be set to `admin`. \
``

A potion cannot be deleted. Also its name, type, and class cannot be modified.

## Tests
To run the tests, move into the repo directory and run `python tests.py` \
Coverage report:
```
Name             Stmts   Miss  Cover
------------------------------------
app.py              52      2    96%
seed.py              8      8     0%
tests.py           151      0   100%
validations.py      33      0   100%
------------------------------------
TOTAL              244     10    96%
```



