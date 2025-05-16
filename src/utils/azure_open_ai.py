from openai import AzureOpenAI
from utils.api_requests import APIClient
from utils.config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_API_VERSION, AZURE_API_VERSION_FILES, AZURE_API_VERSION_VECTORS
import streamlit as st


def get_azure_openai_assistant():
    client_assistant = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version=AZURE_API_VERSION
    )
    return client_assistant


def fetch_files():
    client = APIClient(base_url=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY)

    try:
        response = client.make_request(path=f"/openai/files?api-version={AZURE_API_VERSION_FILES}", method="GET")
        files = response.get("data", [])
        filename_count = {}
        for file in files:
            filename = file["filename"]
            if filename in filename_count:
                filename_count[filename] += 1
                file["filename"] = f"{filename} ({filename_count[filename]})"
            else:
                filename_count[filename] = 1

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
    path = f"/openai/vector_stores/{vector_store_id}/files?api-version={AZURE_API_VERSION_VECTORS}&limit=100"

    try:
        vector_store_name = get_vector_store_name(vector_store_id)
        st.write(f"Henter filer fra vector store: '{vector_store_name}'...")
        response = client.make_request(path=path, method="GET")
        st.write(f"Filer i vector store: '{vector_store_name}'")
        return response
    except Exception as e:
        st.error(f"Kunne ikke hente filer fra vector store '{vector_store_id}'. Fejl: {e}")
        return None


def fetch_vector_stores():
    client = APIClient(base_url=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY)
    path = f"/openai/vector_stores?api-version={AZURE_API_VERSION_VECTORS}"

    try:
        response = client.make_request(path=path, method="GET")
        vector_stores = response.get("data", [])
        return {store["id"]: store["name"] for store in vector_stores}
    except Exception as e:
        st.error(f"Kunne ikke hente vector stores. Fejl: {e}")
        return {}


def add_file_to_assistant(file):
    client = APIClient(base_url=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY)
    path = f"/openai/files?api-version={AZURE_API_VERSION_FILES}"
    files = {
        "file": (file.name, file),
        "purpose": (None, "assistants"),
    }

    try:
        st.write(f"Starter upload af fil: {file.name}...")
        response = client.make_request(path=path, method="POST", files=files)
        return response
    except Exception as e:
        st.error(f"Kunne ikke uploade filen {file.name}. Fejl: {e}")
        return None


def add_file_to_vector_store(vector_store_id, file_id):
    client = APIClient(base_url=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY)
    path = f"/openai/vector_stores/{vector_store_id}/files?api-version={AZURE_API_VERSION_VECTORS}"
    payload = {
        "file_id": file_id
    }

    vector_store_name = get_vector_store_name(vector_store_id)
    files = fetch_files()
    file_name = files.get(file_id, file_id)

    try:
        st.write(f"Tilføjer fil '{file_name}' til vector store '{vector_store_name}'...")
        response = client.make_request(path=path, method="POST", json=payload)
        st.write(f"Fil '{file_name}' blev tilføjet til vector store '{vector_store_name}'.")
        return response
    except Exception as e:
        st.error(f"Kunne ikke tilføje filen '{file_name}' til vector store '{vector_store_name}'. Fejl: {e}")
        return None


def delete_file_from_vector_store(vector_store_id, file_id):
    client = APIClient(base_url=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY)
    path = f"/openai/vector_stores/{vector_store_id}/files/{file_id}?api-version={AZURE_API_VERSION_VECTORS}"

    vector_store_name = get_vector_store_name(vector_store_id)
    files = fetch_files()
    file_name = files.get(file_id, file_id)

    try:
        st.write(f"Sletter fil '{file_name}' fra vector store '{vector_store_name}'...")
        response = client.make_request(path=path, method="DELETE")
        st.write(f"Fil '{file_name}' blev slettet fra vector store '{vector_store_name}'.")
        return response
    except Exception as e:
        st.error(f"Kunne ikke slette filen '{file_name}' fra vector store '{vector_store_name}'. Fejl: {e}")
        return None


def fetch_files_from_vector_store(vector_store_id):
    client = APIClient(base_url=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY)
    path = f"/openai/vector_stores/{vector_store_id}/files?api-version={AZURE_API_VERSION_VECTORS}&limit=100"

    try:
        response = client.make_request(path=path, method="GET")
        vector_store_files = response.get("data", [])
        all_files = fetch_files()

        return {file["id"]: all_files.get(file["id"], f"Ukendt fil ({file['id']})") for file in vector_store_files}
    except Exception as e:
        st.error(f"Kunne ikke hente filer fra vector store '{vector_store_id}'. Fejl: {e}")
        return {}
