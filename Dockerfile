FROM python:3.5.2

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV CMSPYDER_SRC=cmspyder
# Directory in container for all project files
ENV CMSPYDER_ROOT=/app
# Directory in container for project source files
ENV CMSPYDER_PROJ=/app/cmspyder

# Update the default application repository sources list
#RUN apt-get update && apt-get -y upgrade

# Create application subdirectories
WORKDIR $CMSPYDER_ROOT
RUN mkdir media static logs
VOLUME ["$CMSPYDER_ROOT/media/", "$CMSPYDER_ROOT/logs/"]

# Copy application source code to SRCDIR
COPY requirements.txt $CMSPYDER_ROOT
COPY $CMSPYDER_SRC $CMSPYDER_PROJ

# Install Python dependencies
RUN pip install -r $CMSPYDER_ROOT/requirements.txt

# Copy entrypoint script into the image
WORKDIR $CMSPYDER_PROJ

# Run the application in master mode
# $ docker run -it -p 8000:8000 j4v/cmspyder-docker
EXPOSE 8000
CMD ["python", "manage.py", "migrate", "--settings=cmspyder.settings.dev"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=cmspyder.settings.dev"]

# Run the application in worker mode
# $ docker run -it j4v/cmspyder-docker
#ENV DJANGO_SETTINGS_MODULE=cmspyder.settings.dev
#CMD ["celery", "-A", "cmspyder", "worker", "-l", "info", "--concurrency=2", "--pool=eventlet"]

