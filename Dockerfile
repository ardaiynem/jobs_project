# setting up base image
FROM python:3.11.10-slim-bullseye

# prevents python buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# prevents python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1

# sets up the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions 
WORKDIR /usr/src/app

# install system dependencies and dependencies from requirements.txt
COPY requirements.txt .
RUN apt-get update && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# copies files and directories from current directory to WORKDIR
COPY . .

# Expose the Scrapy HTTP API port if needed
EXPOSE 6080

# Command to run the Scrapy spider
WORKDIR /usr/src/app/jobs_project
# CMD ["/bin/bash", "-c", "scrapy crawl job_spider && echo 'Container started' && tail -f /dev/null"]
CMD ["/bin/bash", "-c", "scrapy crawl job_spider && cd .. && python query.py && echo 'Container started' && tail -f /dev/null"]
