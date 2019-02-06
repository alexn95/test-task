# CLIENT BASE
Base of clients. Stored first name, last name, date of birth, age, photo and likes yo photo.
User can create and delete clients, see list of all client or search clients by first name and last name, see the map of the desired client, see all client photo and like it.
Also application provide REST API to get photo list and setting likes.
# Prerequisites
## The installation and launch process requires the installed docker and docker-compose. If any of the above is missing, install them yourself. You can check these commands.
docker --version
docker-compose --version
# Installing
Inside the project directory call
docker-compose up

# Running the tests
Connect to do docker container 
docker exec -it <container_id> bash
And run tests
./manage.py test

# Built With
[Docker](https://www.docker.com/)
[Python](https://www.python.org/)
[Django](https://www.djangoproject.com/)
[Django rest framework](https://www.django-rest-framework.org/)






