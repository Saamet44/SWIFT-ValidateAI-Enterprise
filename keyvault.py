import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def get_secret(secret_name):
    key_vault_url = os.getenv("KEY_VAULT_URL")
    if not key_vault_url:
        raise RuntimeError("KEY_VAULT_URL is not configured.")

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)
    return client.get_secret(secret_name).value
