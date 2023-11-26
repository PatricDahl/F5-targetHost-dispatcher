from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def api():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Check if the required fields are present
        if 'parameters' in data and 'targetHost' in data['parameters']:
            target_host = data['parameters']['targetHost']


            # Process the extracted data (you can add your logic here)
            result = {'message': 'Request received successfully', 'targetHost': target_host}

            # Debugging: Print information about the extracted data
            print(f'Payload: {result}')

            # Make a POST request to the new endpoint
            endpoint_url = f'https://{target_host}/mgmt/shared/fast/applications'

            # Debugging: Print information about the POST request
            print(f'Sending POST request to: {endpoint_url}')
            print(f'Payload: {data}')

            # Include verify=False to skip SSL certificate verification
            response = requests.post(endpoint_url, json=data, verify=False)

            # Debugging: Print information about the response from the new endpoint
            print(f'Response status code: {response.status_code}')
            print(f'Response content: {response.text}')

            # Check the response from the new endpoint
            if response.status_code == 200:
                result['newEndpointResponse'] = response.json()
            else:
                result['newEndpointError'] = f'Error {response.status_code}: {response.text}'

            # Return a JSON response
            return jsonify(result)
        else:
            return jsonify({'error': 'Invalid JSON format. Missing required fields.'}), 400

    except Exception as e:
        # Handle exceptions
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the application on http://127.0.0.1:5000/
    app.run(debug=True)
