# Geocoding API

## Setup
Edit credentials for geocoding services.
1. Navigate to settings.py
2. Add your google maps API key in the GOOGLE variable
3. Add your here app_id and app_code to the HERE_APP_ID and HERE_APP_CODE variables

## Use

### API
1. Run the server `python server.py 8888 localhost` or on a different port and IP.
2. Retrieve Lat and Long JSON object by using `curl http://localhost:8888/latlong/v1/getaddress/New+York`.
