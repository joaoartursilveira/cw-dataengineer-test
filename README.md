# cw data-engineer-test

This project convers two main functionalities:
    Collects the South-American countries GDP data from the worldbank api and insert them in a database.
    Queries the GDP database and outputs the pivot data as a csv file.


## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
    1. [Local Python](#local-python)
    2. [Docker](#docker)


## Installation

### Prerequisites
- Python (used version: 3.12)
- Docker (used version: 24.0.7)


### Installation Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/your_username/repository_name.git
    ```
2. Navigate to the project directory:
    ```sh
    cd repository_name
    ```

## Usage

### Local Python
- Navigate to the project directory.
- Run the terminal command "python -m venv venv" to create the python virtual environment.
- Run the terminal command "venv\Scripts\activate" to connect to the venv.
- Run the terminal command "pip install -r app/requirements.txt" to install all dependecies.
- Run the terminal command "python -m app.extractor.extract" to extract the worldbank api data.
- Run the terminal command "python -m app.query.query" to create a csv file with the Gdp pivot data on ./app/database folder.

### Docker
- Navigate to the project directory.
- Run the terminal command "docker volume create cloudwalk_volume", this will be the folder that the data will persist.
- Run the terminal command "docker-compose build" to create the project images.
- Run the terminal command "docker-compose up" to start the images on each container.
- Check the named volume to interact with the database, output files and logs.