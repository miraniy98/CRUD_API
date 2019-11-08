# CRUD API for a blog

API that facilitates CRUD application with exclusiveness to owners of the post. The permissions of the application have been set to IsOwnerOrReadOnly meaning the third party is allowed to read only and not update or delete.

## Getting Started

The API is implemented in Python using Django and Django Rest Framework. Linux shell, Python 3.6 and pip are needed on the machine to follow the subsequent steps and run the API locally on your machine

### Prerequisites

After having the source folder on your machine, follow the below steps while staying in CRUD_API folder:

```
source env/bin/activate
pip3 install -r requirements.txt
```

### Running the application

After all the requirements have been installed perform the following actions to start interacting with the API

```
cd src
python3 manage.py runserver
```

The API is configured with all the required permission related nuances and can be found at the localhost at which the server has been started by the machine. In most common cases, the server will be started at http://127.0.0.1:8000. In this case find the following views:

1. The Create and List View can be found at http://127.0.0.1:8000/post/api where the list of all the post along with the URL and details is present, The detailed view of a post to delete or update can be accessed by clicking the said URL or as below.

2. The Retrieve Update and Delete view can be found at http://127.0.0.1:8000/post/api/1 where the trailing 1 is the primary key of first post in the list

3. In addition, to facilitate permission/ownership related nuances JWT(JSON Web Authentication Token) was used. The demonstration of the same can be found at http://127.0.0.1:8000/api/auth/login.

## Running the tests

To facilitate accurate testing of update on ownership only and various other features, automated tests have been developed in tests.py which can be run through following command:

```
python3 manage.py test
```

Developed by: Yash Mirani
