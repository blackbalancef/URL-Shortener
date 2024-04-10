# Asynchronous URL Shortener Service

## Introduction


This project is an asynchronous web service for URL shortening, designed to provide a fast and efficient way to shorten URLs, redirect to original URLs using shortened links, and collect click-through statistics. The service is intended to run on localhost and should be deployed using Docker for ease of setup and scalability.

## Objective
The main goal is to develop a fully functional asynchronous URL shortener service that can be used as a portfolio piece, showcasing the developer's skills in creating web services, mastering modern technology stacks, and understanding asynchronous programming.

## Technical stack

### FASTAPI + SQLALCHEMY + REDIS + POSTGRESQL + DOCKER

### Core Technologies

- FastAPI: To create the asynchronous web service.
- PostgreSQL: As the primary database for storing URL data.
- SQLAlchemy 2: For asynchronous interaction with PostgreSQL.
- Pydantic 2: For data validation and model serialization/deserialization.
- Redis: For caching frequently accessed links and detailed statistics on each redirection.
- Docker: For containerizing the service and its dependencies.
- Async/Await: To leverage asynchronous programming throughout the project.

## Functionalities
#### URL Shortening (POST)
- Endpoint to accept an original URL and prefix for personalizing -> return a shortened link.
#### Redirection (GET)
- When accessing a shortened link, user redirected to the original URL. 
- Each redirection is logging for statistical purposes.

#### Statistics (GET)
- An endpoint to provide statistics on the number of visits for a specific shortened link, returning total numer of visits and visits by day and time. 


# Getting Started

Copy .env.local to .env

`cp .env.local .env`

## Running the service
### 1st option: Run with docker

`docker-compose up`


### 2nd option: Run with local python environment

1. Install dependencies with poetry `poetry install`
2. Change in .env file DATABASE_HOST=localhost and REDIS_HOST=localhost
2. Run export command to set environment variables `export $(cat .env | xargs)`
3. Run debug.py file in debug/run mode in your IDE

## Documentation

#### http://localhost:8000/docs to see the API documentation
#### http://localhost:8000/redoc to see the API documentation in redoc format
#### http://localhost:8081 to see redis commander interface