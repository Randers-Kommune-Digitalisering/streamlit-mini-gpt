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
