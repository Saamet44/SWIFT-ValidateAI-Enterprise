from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

key_vault_url = os.getenv("KEY_VAULT_URL")

credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)

def get_secret(secret_name):
    return client.get_secret(secret_name).value