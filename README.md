# cw data-engineer-test

This project convers two main functionalities:
    Collects the South-American countries GDP data from the worldbank api and insert them in a database.
    Queries the GDP database and outputs the pivot data as a csv file.

There's a single docker image with the default command to extract the api data.
However this can be changed to execute the querier by modifying the cmd command on docker run, which is shown later at [Defaut Docker](#default-docker).


## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
    1. [Local Python](#local-python)
    2. [Docker](#docker)
        1. [Defaut Docker](#default-docker)
        2. [Docker Compose](#docker-compose)


## Installation

### Prerequisites
- Python (used version: 3.12)
- Docker (used version: 24.0.7)


### Installation Steps
- git clone https://github.com/joaoartursilveira/cw-dataengineer-test.git
- Navigate to the project directory.
- Run the terminal command "python -m venv venv" to create the python virtual environment.
- Run the terminal command "venv\Scripts\activate" to connect to the venv.
- Run the terminal command "pip install -r requirements.txt" to install all dependecies.


## Usage

### Local Python
- Run the terminal command "python -m app.extractor.extract" to extract the worldbank api data.
- Run the terminal command "python -m app.query.query" to create a csv file with the Gdp pivot data on ./app/database folder.


### Docker
- Navigate to the project directory.
- Run the terminal command "docker volume create cloudwalk_volume", this will be the folder that the data will persist.

#### Default Docker
- Run the terminal command "docker build -t cloudwalk-image" to build the image
- Run the teminal command "docker run -v cloudwalk_volume:/usr/src/cloudwalk/app/database --name extract1 cloudwalk-image" to start a extraction container'
- Run the teminal command "docker run -v cloudwalk_volume:/usr/src/cloudwalk/app/database --name query1 cloudwalk-image python -m app.query.query" to start a querier container
- Check the named volume to interact with the database, output files and logs.

#### Docker Compose
- Run the terminal command "docker-compose build" to create the project image.
- Run the terminal command "docker-compose up" to start the image on each container.
- Check the named volume to interact with the database, output files and logs.