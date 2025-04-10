import streamlit as st
import streamlit_antd_components as sac
from utils.azure_open_ai import fetch_vector_stores, upload_file, fetch_files, add_file_to_vector_store
from utils.config import HJAELPEMIDDEL_VECTOR_ID


def upload_files():
    col_1 = st.columns([1])[0]

    with col_1:
        content_tabs = sac.tabs([
            sac.TabsItem('Upload', tag='Upload', icon='upload'),
            sac.TabsItem('TIlføj fil til Hjælpemiddel-Assistenten', tag='TIlføj fil til Hjælpemiddel-Assistenten', icon='bi bi-file-earmark-x'),
        ], color='dark', size='md', position='top', align='start', use_container_width=True)

    try:
        if content_tabs == 'Upload':
            st.write("Upload dine filer her")
            uploaded_files = st.file_uploader(
                "Vælg filer for at uploade",
                type=["txt", "json", "csv", "pdf", "docx"],
                accept_multiple_files=True,
                help="Vælg de filer, du vil uploade til Azure OpenAI."
            )

            if uploaded_files:
                if st.button("Upload"):
                    with st.spinner("Uploader filer..."):
                        for uploaded_file in uploaded_files:
                            st.write(f"Uploader filen: {uploaded_file.name}")
                            result = upload_file(uploaded_file)
                            if result:
                                st.success(f"Filen '{uploaded_file.name}' blev uploadet succesfuldt til Azure OpenAI!")

        elif content_tabs == 'TIlføj fil til Hjælpemiddel-Assistenten':
            st.write("Tilføj en eksisterende fil til din vector store")
            specific_vector_store_id = HJAELPEMIDDEL_VECTOR_ID

            if specific_vector_store_id:
                vector_stores = fetch_vector_stores()
                vector_store_name = next((name for id, name in vector_stores.items() if id == specific_vector_store_id), None)

                if vector_store_name:
                    st.write(f"Bruger den specifikke vector store: {vector_store_name}")
                else:
                    st.write(f"Bruger den specifikke vector store med ID: {specific_vector_store_id}")
                vector_store_id = specific_vector_store_id
            else:
                vector_stores = fetch_vector_stores()
                if vector_stores:
                    vector_store_name = st.selectbox("Vælg en vector store", options=list(vector_stores.values()))
                    vector_store_id = next((id for id, name in vector_stores.items() if name == vector_store_name), None)
                else:
                    st.warning("Ingen vector stores fundet.")
                    vector_store_id = None

            if vector_store_id:
                files = fetch_files()
                if files:
                    file_name = st.selectbox("Vælg en fil", options=list(files.values()), help="Vælg en fil fra listen over tilgængelige filer.")
                    file_id = next((id for id, name in files.items() if name == file_name), None)

                    if file_id:
                        if st.button("Tilføj fil"):
                            with st.spinner("Tilføjer fil..."):
                                result = add_file_to_vector_store(vector_store_id, file_id)
                                if result:
                                    st.success("Filen blev tilføjet succesfuldt!")
                else:
                    st.warning("Ingen filer fundet. Upload filer først.")

    except Exception as e:
        st.error(f'En fejl opstod: {e}')
