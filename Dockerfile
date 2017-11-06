# Base image
FROM ubuntu:17.10

# Commands to run to install dependencies
RUN apt-get update -y && \
	apt-get install -y python-pip python-dev

COPY requirements.txt /potions_inventory/requirements.txt

# Sets the container working directory
WORKDIR /potions_inventory

RUN pip install -r requirements.txt

# Copy file or directory from the source (local folder, same location as Dockerfile) to the destination (docker container, relative to WORKDIR)
COPY app.py app.py
COPY validations.py validations.py
COPY tests.py tests.py
COPY seed.py seed.py
COPY fixtures/potions.yaml fixtures/potions.yaml

# When you pass commands to the container, what should interpret them
ENTRYPOINT ["python"]

# Command to run when the container starts
CMD ["app.py"]

# Make port available
EXPOSE 5000
