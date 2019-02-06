# CLIENT BASE
Base of clients. Stored first name, last name, date of birth, age, photo and likes in photo.

User can create and delete clients, see list of all client or search clients by first name and last name, see the map of the desired client, see all client photo and like it.

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

To apply all app migrations call

```
$ python manage.py migrate
```

To create and apply clientbase migrations call

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


## Built With
[Docker](https://www.docker.com/)

[Python](https://www.python.org/)

[Django](https://www.djangoproject.com/)

[Django rest framework](https://www.django-rest-framework.org/)
