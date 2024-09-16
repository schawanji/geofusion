# Geofusion 

Here are the instructions to build and run a Docker image for your Python application based on the provided Dockerfile:

### Steps to build the Docker image:

**Build the Docker image**
   Run the following command in the directory where the `Dockerfile` is located:
   ```bash
   docker build -t my-python-app .
   ```
   This will build a Docker image named `my-python-app`.

### Steps to run the Docker container:

**Run the Docker container**
   After the image is built, you can run it with the following command:
   ```bash
   docker run -d -p 5000:5000 my-python-app
   ```
   This runs the container in detached mode (`-d`) and maps port 5000 on the host to port 5000 inside the container.

