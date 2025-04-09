from openai import AzureOpenAI
from utils.api_requests import APIClient
from utils.config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY
import streamlit as st


def get_azure_openai_assistant():
    client_assistant = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version="2024-05-01-preview"
    )
    return client_assistant


def fetch_files():
    client = APIClient(base_url=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY)

    try:
        response = client.make_request(path="/openai/files?api-version=2024-10-21", method="GET")
        files = response.get("data", [])
        return {file["id"]: file["filename"] for file in files}
    except Exception as e:
        st.error(f"Kunne ikke hente filer. Fejl: {e}")
        return {}


def map_internal_references_to_file_ids(assistant_message):
    reference_to_file_id = {}
    if hasattr(assistant_message, "content") and assistant_message.content:
        for block in assistant_message.content:
            if hasattr(block, "text") and hasattr(block.text, "annotations"):
                for annotation in block.text.annotations:
                    if hasattr(annotation, "file_citation") and annotation.file_citation:
                        internal_reference = annotation.text.split("†")[0].strip("【")
                        reference_to_file_id[internal_reference] = annotation.file_citation.file_id
    return reference_to_file_id


def get_vector_store_name(vector_store_id):
    vector_stores = fetch_vector_stores()
    return vector_stores.get(vector_store_id, vector_store_id)


def list_files_in_vector_store(vector_store_id):
    client = APIClient(base_url=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY)
    path = f"/openai/vector_stores/{vector_store_id}/files?api-version=2025-03-01-preview&limit=100"

    try:
        vector_store_name = get_vector_store_name(vector_store_id)
        st.write(f"Henter filer fra vector store: '{vector_store_name}'...")
        response = client.make_request(path=path, method="GET")
        st.write(f"Filer i vector store: '{vector_store_name}'")
        st.write(client.base_url)
        return response
    except Exception as e:
        st.error(f"Kunne ikke hente filer fra vector store '{vector_store_id}'. Fejl: {e}")
        return None


def fetch_vector_stores():
    client = APIClient(base_url=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY)
    path = "/openai/vector_stores?api-version=2025-03-01-preview"

    try:
        response = client.make_request(path=path, method="GET")
        vector_stores = response.get("data", [])
        return {store["id"]: store["name"] for store in vector_stores}
    except Exception as e:
        st.error(f"Kunne ikke hente vector stores. Fejl: {e}")
        return {}
