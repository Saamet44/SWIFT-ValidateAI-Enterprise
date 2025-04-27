**SWIFT ValidateAI Enterprise**

A Flask-based web application for validating SWIFT messages, integrated with Azure Blob Storage and Azure Key Vault for secure and scalable operations. This project provides a robust API for message validation, enhanced with API key authentication, comprehensive error handling, and Swagger documentation. It includes a simple frontend for user interaction and supports Docker for easy deployment.

**Features**

- SWIFT Message Validation: Validates SWIFT messages with checks for required fields and formats.
- Azure Integration: Stores validated messages in Azure Blob Storage with date-based organization and retrieves secrets securely from Azure Key Vault.
- Secure API: Protects endpoints with API key authentication.
- Swagger UI: Interactive API documentation at /swagger.
- Docker Support: Containerized deployment with Dockerfile and Docker Compose.
- Testing: Unit tests for validation logic using pytest.
- Logging: Detailed logging of operations and errors.

Getting Started

Clone the repository.
Set up environment variables in .env (see .env template).
Install dependencies: pip install -r requirements.txt.
Run locally: python app.py or use Docker: docker-compose up.
Access the app at http://localhost:5000 and Swagger at http://localhost:5000/swagger.
