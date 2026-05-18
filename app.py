from datetime import datetime, timezone
import json
import logging
import os
import uuid

from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient, ContentSettings
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from ai_mock import validate_message
from keyvault import get_secret


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        API_KEY=os.getenv("API_KEY", ""),
        AZURE_STORAGE_CONNECTION_STRING=os.getenv("AZURE_STORAGE_CONNECTION_STRING", ""),
        AZURE_STORAGE_CONNECTION_SECRET_NAME=os.getenv(
            "AZURE_STORAGE_CONNECTION_SECRET_NAME",
            "AZURE_STORAGE_CONNECTION_STRING",
        ),
        AZURE_STORAGE_CONTAINER=os.getenv("AZURE_STORAGE_CONTAINER", "messages"),
        REQUIRE_STORAGE=os.getenv("REQUIRE_STORAGE", "false").lower() == "true",
        BLOB_SERVICE_CLIENT=None,
    )

    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/validate")
    def validate():
        auth_error = _authenticate(app)
        if auth_error:
            return auth_error

        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json."}), 415

        message = request.get_json(silent=True)
        if not isinstance(message, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        validation = validate_message(message)
        status_code = 200 if validation["status"] == "Valid" else 422
        storage = _store_validation(app, message, validation)

        if storage.get("error") and app.config["REQUIRE_STORAGE"]:
            return jsonify({"error": "Validation storage failed."}), 503

        return jsonify(
            {
                "status": validation["status"].lower(),
                "validation": validation,
                "storage": storage,
            }
        ), status_code

    return app


def _authenticate(app):
    expected_api_key = app.config.get("API_KEY")
    if not expected_api_key:
        return None

    supplied_key = request.headers.get("X-API-Key")
    authorization = request.headers.get("Authorization", "")
    bearer_key = authorization.removeprefix("Bearer ").strip()

    if supplied_key == expected_api_key or bearer_key == expected_api_key:
        return None

    return jsonify({"error": "Unauthorized."}), 401


def _store_validation(app, message, validation):
    client = _get_blob_service_client(app)
    if client is None:
        return {"stored": False, "reason": "storage_not_configured"}

    blob_name = _new_blob_name()
    payload = {
        "message": message,
        "validation": validation,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        blob_client = client.get_blob_client(
            container=app.config["AZURE_STORAGE_CONTAINER"],
            blob=blob_name,
        )
        blob_client.upload_blob(
            json.dumps(payload, ensure_ascii=False),
            overwrite=False,
            content_settings=ContentSettings(content_type="application/json"),
        )
    except AzureError:
        logger.exception("Azure Blob Storage upload failed")
        return {"stored": False, "error": "azure_upload_failed"}

    return {"stored": True, "blob": blob_name}


def _get_blob_service_client(app):
    if app.config.get("BLOB_SERVICE_CLIENT") is not None:
        return app.config["BLOB_SERVICE_CLIENT"]

    connection_string = app.config.get("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        connection_string = _get_connection_string_from_keyvault(app)

    if not connection_string:
        return None

    try:
        app.config["BLOB_SERVICE_CLIENT"] = BlobServiceClient.from_connection_string(
            connection_string
        )
    except ValueError:
        logger.exception("Invalid Azure Storage connection string")
        return None

    return app.config["BLOB_SERVICE_CLIENT"]


def _get_connection_string_from_keyvault(app):
    try:
        return get_secret(app.config["AZURE_STORAGE_CONNECTION_SECRET_NAME"])
    except Exception:
        logger.info("Azure Storage connection string was not resolved from Key Vault")
        return ""


def _new_blob_name():
    now = datetime.now(timezone.utc)
    return f"{now:%Y/%m/%d}/{uuid.uuid4()}.json"


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
