from flask import Flask, request, jsonify, render_template
import uuid
from azure.storage.blob import BlobServiceClient
from keyvault import get_secret
from ai_mock import validate_message
import os

app = Flask(__name__)

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING') or get_secret("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    message = request.json
    result = validate_message(message)
    blob_name = f"{uuid.uuid4()}.json"
    blob_client = blob_service_client.get_blob_client(container="messages", blob=blob_name)
    blob_client.upload_blob(str(message))
    return jsonify({"status": "OK", "validation": result})

if __name__ == "__main__":
    app.run(debug=True)