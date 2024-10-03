# Geofusion 

This project is a Flask-based API that fetches geospatial data (GeoJSON) from a GeoServer and joins it with tabular data from a CSV file. The API provides endpoints for data merging and fetching GeoJSON tiles.

## Features

- **Join geospatial data with tabular data**: Fetch GeoJSON from a GeoServer and join it with data from a CSV file using common keys.
- **GeoJSON Tile Fetching**: Retrieve GeoJSON tiles from a GeoServer for further use.
- **CORS Support**: Cross-origin requests are supported using Flask-CORS.

## Installation 
1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/geofusion.git
   cd geofusion ```
2. Create virtual python environment and actvate it:

   ```bash python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate` 
   ```
3. Install the required dependencies:
   ```bash 
   pip install -r requirements.txt
   ```
4. Update geoserver password and username in the .env file:
   ```bash 
   USER = 'your_geoserver_username'
   PASSWORD = 'your_geoserver_password'
   ```

###  Usage
#### Run the Flask app:

   ```bash
   python app.py 
   ```
Open your browser and navigate to:

   ```arduino
   http://localhost:5001 
   ```

You should see the welcome page with information about how to use the API.


## Docker Installion

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
   docker run -d -p 5001:5001 my-python-app
   ```
   This runs the container in detached mode (`-d`) and maps port 5000 on the host to port 5000 inside the container.

