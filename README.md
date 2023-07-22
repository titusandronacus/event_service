# Event Service
small demonstration of api building using FastApi and PostgreSQL

## Architecture Description
Fastapi provides the REST api framework (https://fastapi.tiangolo.com/)
SQLAlchemy provides ORM functionality with PostgreSQL as the database (https://www.sqlalchemy.org/)
docker-compose is used for running a local dev environment with PostgreSQL
Pytest for testing with a SQLite3 local file testing database

The application is structured to allow easy modification for expanding the capabilities of the events this service works with. Simply change the ORM model (event_service.models.models) and expand the Pydantic model (event_service.models.schema) to support the changes. Adjust the crud layer, and update the routes to handle any additional parameters as needed.

This project is powered by poetry. For more info see https://python-poetry.org/

The application requires authentication using the OAuth2 password bearer token flow. The admin user and its password are configured via environment variables. See step 4 under Install Instructions for more info on configuring the application.

## Install Instructions
1) Install poetry (see above reference for documentation related to poetry) and copy project to directory of your choice
2) Run `poetry init` in project directory
3) Run `poetry install` in project directory
4) Copy `.env.sample` to `.env`. You'll need to make some adjustments
    * Mandatory: You'll need to run `openssl rand -hex 32` (or some other method to get a random set of 32 bytes) and put it into the SECRET_KEY env variable (`.env.sample` also states this)
    * Optional: If you'd like to change the admin password (and the hash for it), run the following from within the project's virtual environment and copy the output to the ADMIN_PASS env variable:
    ```python
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

    print(pwd_context.hash('new_password_you_like_to_use'))
    ```
    * To get a running shell instance of python using poetry, it's advised to use `poetry shell`, then invoke a python interpreter from within the spawned shell. To exit, simply enter `exit` at the shell
5) To run tests for application, use `poetry run pytest` in the project directory
6) To run a local dev instance, use `docker-compose up --build` (Docker and docker-compose required)

### Interacting with the service
Fastapi provides functionality to auto-document a REST api with an OpenAPI doc. You can access this document via the web when a Fastapi service is running. If the application container is running, you should be able to goto [localhost:8080/docs] and you'll see a Swagger page.

You'll need to authorize yourself as the admin user before being able to make any requests. Click the 'Authorize' button in the upper right of the page, and a prompt for OAuth2 password will appear. You should only need the username and password (defaults are username: admin, password: secret) for this.

Once you're authorized, you can interact with the api. Expand any endpoint and click the 'Try it out' button, and you'll be given a prompt for the request. You can ignore the /auth request (you use it by authorizing via the OAuth2 flow already)

## This solution should provide
* GET /events/?name={filter_by_name}
* POST /events/
* GET /events/{event_id}
* PATCH /events/{event_id}
* DELETE /events/{event_id}

If you'd like to use a different tool to interact with the service, the Swagger page can show you how to make any request using curl, though you will have to execute the request once through the Swagger page.
