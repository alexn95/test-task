# CLIENT BASE
Base of clients. In base stored first name, last name, date of birth, age, photo and likes to photo.

User can create and delete clients, can view list of all client or search clients by first name and last name, can view the map of the desired client, can view all photo and set the "like" to selected photo.

Also application provide REST API to get photo list and setting likes.
## Prerequisites
The installation and launch process requires the installed docker and docker-compose. If any of the above is missing, install them yourself. You can check these commands.

```
$ docker --version  
$ ddocker-compose --version  
```

## Installing
1. Inside the project directory call

```
$ docker-compose up
```

2. Connect to docker container test-task_web

```
$ docker exec -it <container_id> bash  
```

To see all containers call

```
$ docker ps
```

3. Apply app migrations 

```
$ python manage.py migrate
```

4. Create and apply clientbase migrations

```
$ python manage.py makemigrations clientbase
$ python manage.py migrate clientbase
```

The application is available at http://0.0.0.0:8000/


## Running the tests
Connect to docker container test-task_web

And run tests

```
$ python manage.py test
``` 

## User guide

#### Visual web interfase

http://0.0.0.0:8000/ - Main page. In page you can see list of the client, can delete client and move to any page of app. Also you can search the client by first name and last name, download all clients data in xlsx format file.

http://0.0.0.0:8000/create - In this page you can create a new client.

http://0.0.0.0:8000/photo - This page allow to see all clients photo and set the "like" to selected photo.

#### REST API



## Built With
[Docker](https://www.docker.com/) - is a tool designed to make it easier to create, deploy, and run applications by using containers.

[Python](https://www.python.org/) - is an interpreted, object-oriented, high-level programming language with dynamic semantics. 

[Django](https://www.djangoproject.com/) - is a high-level Python Web framework.

[Django rest framework](https://www.django-rest-framework.org/) - is a powerful and flexible toolkit for building Web APIs in django python.
