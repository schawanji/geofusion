import flask
from flask import Flask, render_template, request, jsonify
import requests
import geopandas as gpd
import pandas as pd
from flask_cors import CORS
from io import StringIO
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# GeoServer authentication details from .env file
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

@app.route('/')
def welcome():
    return render_template('welcome.html')
'''@app.route('/')
def index():
    title = "VectorTiles-Table Joining Service"
    return render_template("index.html", title=title)'''

@app.route('/tjs/api/joindata', methods=['GET'])
def joindata():
    try:
        # Get parameters from the request's query string
        FrameworkURI = request.args.get('FrameworkURI')
        layer_name = request.args.get('layer')
        GetDataURL = request.args.get('GetDataURL')
        FrameworkKey = request.args.get('FrameworkKey')
        AttributeKey = request.args.get('AttributeKey')

        if not FrameworkURI:
            return jsonify({'error': 'GeoData service URL is required'}), 400

        if not layer_name:
            return jsonify({'error': 'Layer name is required'}), 400

        # Check for missing parameters
        if not FrameworkURI or not GetDataURL or not FrameworkKey or not AttributeKey:
            return jsonify({"error": "Missing required parameters"}), 400

        # Define WFS request parameters
        params = {
            'service': 'WFS',
            'version': '1.0.0',  # or 2.0.0, depending on your GeoServer configuration
            'request': 'GetFeature',
            'typeName': layer_name,  # Use the layer name from the query parameters
            'outputFormat': 'application/json'  # GeoJSON format
        }

        # Make a request to GeoServer
        a ='&version=1.0.0&request=GetFeature&typeName=topp%3Astates&outputFormat=application%2Fjson'
        response = requests.get(FrameworkURI, params=params, auth=(USER, PASSWORD))
        print('FrameworkURI')
        print(FrameworkURI)
        print(response.text)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch GeoJSON data", "status_code": response.status_code}), 500

        # Read GeoJSON data into a GeoDataFrame
        try:
            # Assuming JSON text, not content
            gdf = gpd.read_file(StringIO(response.text))
        except Exception as e:
            return jsonify({"error": "Error reading GeoJSON data", "details": str(e)}), 500

        # Check if the FrameworkKey exists in GeoDataFrame
        if FrameworkKey not in gdf.columns:
            return jsonify({"error": f"'{FrameworkKey}' not found in GeoDataFrame"}), 400

        # Read CSV data into a DataFrame
        try:
            df = pd.read_csv(GetDataURL)
        except Exception as e:
            return jsonify({"error": "Error reading CSV data", "details": str(e)}), 500

        # Check if the AttributeKey exists in DataFrame
        if AttributeKey not in df.columns:
            return jsonify({"error": f"'{AttributeKey}' not found in DataFrame"}), 400

        # Merge GeoDataFrame and DataFrame based on FrameworkKey and AttributeKey
        try:
            merged_data = pd.merge(gdf[['geometry', FrameworkKey]], df,
                                   left_on=FrameworkKey, right_on=AttributeKey, how='inner')
        except Exception as e:
            return jsonify({"error": "Error merging data", "details": str(e)}), 500

        # Convert merged data to GeoJSON and return it
        return jsonify(merged_data.to_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tjs/api/tms/', methods=['GET'])
def get_geojson_tile():
    try:
        # Get parameters from the request's query string
        FrameworkURI = request.args.get('FrameworkURI')
        GetDataURL = request.args.get('GetDataURL')
        FrameworkKey = request.args.get('FrameworkKey')
        AttributeKey = request.args.get('AttributeKey')

        # Validate required parameters
        if not all([FrameworkURI, GetDataURL, FrameworkKey, AttributeKey]):
            return jsonify({"error": "Missing required parameters"}), 400

        # Make a request to GeoServer to get the GeoJSON tile
        response = requests.get(FrameworkURI, auth=(USER, PASSWORD))

        # Check if the request was successful
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch GeoJSON tile", "status_code": response.status_code}), 500

        # Read GeoJSON data into a GeoDataFrame
        try:
            gdf = gpd.read_file(StringIO(response.text))
        except Exception as e:
            return jsonify({"error": "Error reading GeoJSON data", "details": str(e)}), 500

        # Check if the FrameworkKey exists in GeoDataFrame
        if FrameworkKey not in gdf.columns:
            return jsonify({"error": f"'{FrameworkKey}' not found in GeoDataFrame"}), 400

        # Read CSV data into a DataFrame
        try:
            df = pd.read_csv(GetDataURL)
        except Exception as e:
            return jsonify({"error": "Error reading CSV data", "details": str(e)}), 500

        # Check if the AttributeKey exists in DataFrame
        if AttributeKey not in df.columns:
            return jsonify({"error": f"'{AttributeKey}' not found in DataFrame"}), 400

        # Ensure dataframes are not empty
        if gdf.empty or df.empty:
            return jsonify({"error": "GeoDataFrame or DataFrame is empty"}), 400

        # Merge GeoDataFrame and DataFrame based on FrameworkKey and AttributeKey
        try:
            merged_data = pd.merge(gdf[['geometry', FrameworkKey]], df,
                                   left_on=FrameworkKey, right_on=AttributeKey, how='inner')
        except Exception as e:
            return jsonify({"error": "Error merging data", "details": str(e)}), 500

        # Convert merged data to GeoJSON and return it
        return merged_data.to_json(), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
