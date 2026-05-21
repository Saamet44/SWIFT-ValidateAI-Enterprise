SWIFT ValidateAI Enterprise
A Flask-based SWIFT message validation API. The application runs locally without requiring an Azure connection during development; when Azure Blob Storage credentials are provided, it archives validation logs organized in date-based folders.

Features
SWIFT message validation via JSON API

Format checks for mandatory fields, amounts, currencies, and BICs

Optional protection via X-API-Key or Authorization: Bearer ...

Optional, lazy-loaded Azure Blob Storage connection

Support for fetching secrets from Azure Key Vault

Simple web interface

Pytest test suite

Installation
Windows:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py

Linux/macOS:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
The application runs on http://localhost:5000 by default.

Environment Variables
API_KEY: If set, the /validate endpoint will require an API key.

AZURE_STORAGE_CONNECTION_STRING: Connection string for Blob Storage.

AZURE_STORAGE_CONTAINER: Blob container name. Default: messages.

KEY_VAULT_URL: Azure Key Vault URL.

AZURE_STORAGE_CONNECTION_SECRET_NAME: The name of the storage secret inside Key Vault. Default: AZURE_STORAGE_CONNECTION_STRING.

REQUIRE_STORAGE: If set to true, the API returns an error if writing to storage fails.

API
GET /health
Health check endpoint.

POST /validate
Example request:
{
  "TransactionReference": "TRX-2026-0001",
  "Amount": "1250.50",
  "Currency": "USD",
  "SenderBIC": "DEUTDEFF",
  "ReceiverBIC": "NWBKGB2L"
}

Returns 200 for successful validation, 422 for invalid messages, and 400/415 for malformed JSON.

Testing
pytest
