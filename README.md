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
