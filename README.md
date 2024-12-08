# Jobs Project

## Overview

The **Jobs Project** is a web scraping and data processing pipeline designed to extract job listings from various sources, process the data, and store it in PostgreSQL and MongoDB databases. This project leverages Scrapy for web scraping, Docker for containerization, and integrates Redis for duplicate detection.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Copying JSON Files into Project Directory](#2-copying-json-files-into-project-directory)
  - [3. Environment Variables](#3-environment-variables)
  - [4. Docker Setup](#4-docker-setup)
- [Pipeline Process](#pipeline-process)
  - [1. Scrapy Spider](#1-scrapy-spider)
  - [2. Item Processing](#2-item-processing)
  - [3. Data Storage](#3-data-storage)
  - [4. Data Export](#4-data-export)
- [Project Structure](#project-structure)

## Features

- **Web Scraping**: Extracts job listings using Scrapy.
- **Data Storage**: Stores processed data in PostgreSQL and MongoDB.
- **Duplicate Detection**: Utilizes Redis to prevent duplicate entries.
- **Containerization**: Docker and Docker Compose for easy setup and deployment.
- **Data Export**: Exports data from databases to CSV files for analysis.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/jobs_project.git
cd jobs_project
```
### 2. Copying JSON Files into Project Directory
Please copy/move the s01.json and s02.json precisely to the project's root directory (the directory containing the Dockerfile).

### 3. Environment Variables
Create a .env file in the root directory of the project and populate it with the necessary environment variables. You can use the provided .env.example as a reference.

```
# .env

# Postgres settings
SQL_NAME=jobs_db
SQL_USER=arda
SQL_PASSWORD=password
SQL_HOST=postgres_db
SQL_PORT=5432

# Redis settings
REDIS_HOST=redis_db
REDIS_PORT=6379

# Mongo settings
MONGO_HOST=mongo_db
MONGO_PORT=27017
MONGO_INITDB_ROOT_USERNAME=arda
MONGO_INITDB_ROOT_PASSWORD=password
```

### 4. Docker Setup
Ensure Docker and Docker Compose are installed on your machine.

Build and start the Docker containers using Docker Compose:

```
docker-compose up --build
```

This command will:

- Build the Docker image for the Scrapy service.
- Start PostgreSQL, Redis, and MongoDB services.
- Ensure all services are healthy and running.
- Run the scrapy crawl project then run the query script for producing csv files.

## Pipeline Process
### 1. Scrapy Spider
The JobSpider is responsible for crawling and extracting job listings from specified JSON files. It reads local JSON files, sends HTTP requests, and parses the responses to extract relevant job data.

**Key Components:**

- start_requests: Initiates requests to JSON files.
- parse_page: Parses each JSON response and yields JobsProjectItem objects.

### 2. Item Processing
Processed items go through the JobsProjectPipeline, which handles data validation, type conversion, duplicate detection, and storage.

Pipeline Steps:

1. Field Existence Check: Ensures required fields like title and req_id are present.
2. Duplicate Detection: Uses Redis to check if a job with the same req_id already exists.
3. Data Conversion:
- Converts date strings to PostgreSQL-compatible formats.
- Converts string fields to specified data types (e.g., latitude, longitude).
- Serializes list and dictionary fields to JSON strings.
4. Data Storage:
- Inserts validated and processed data into PostgreSQL.
- Inserts data into MongoDB for NoSQL storage.

### 3. Data Storage
- PostgreSQL: Stores structured job data in the raw_table. The database schema is defined in postgresql_connector.py.
- MongoDB: Stores job data in a flexible document format. The connection and insertion logic are handled in mongodb_connector.py.
- Redis: Used for duplicate detection to ensure each job listing is unique.

### 4. Data Export
The query.py script retrieves data from PostgreSQL and MongoDB, converts it into pandas DataFrames, and exports the data to CSV files (postgres_data.csv and mongodb_data.csv) for further analysis or reporting.

## Project Structure
```
jobs_project/
├── infra/
│   ├── mongodb_connector.py
│   ├── postgresql_connector.py
│   └── redis_connector.py
├── jobs_project/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── pipelines.py
│   └── spiders/
│       ├── __init__.py
│       └── json_spider.py
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── scrapy.cfg
├── query.py
├── .env
├── s01.json
├── s02.json
└── README.md
```
