# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

LABEL maintainer "axdber@gmail.com"


# create root directory for our project in the container
RUN mkdir /supertodolists_service

# Set the working directory to /music_service
WORKDIR /supertodolists_service

# Copy the current directory contents into the container at /supertodolists_service
ADD . /supertodolists_service/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN python manage.py collectstatic 

HEALTHCHECK --interval=5s \
            --timeout=5s \
            CMD curl -f http://127.0.0.1:8000 || exit 1

EXPOSE 8000