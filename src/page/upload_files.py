import streamlit as st
import streamlit_antd_components as sac
from utils.azure_open_ai import list_files_in_vector_store, fetch_vector_stores, upload_file


def upload_files():
    col_1 = st.columns([1])[0]

    with col_1:
        content_tabs = sac.tabs([
            sac.TabsItem('List Files', tag='List Files', icon='bi bi-file-earmark-word'),
            sac.TabsItem('Upload', tag='Upload', icon='upload'),
        ], color='dark', size='md', position='top', align='start', use_container_width=True)

    try:
        if content_tabs == 'List Files':
            st.write("Se en liste over filer i Vector Store")

            vector_stores = fetch_vector_stores()
            if vector_stores:
                vector_store_name = st.selectbox("Vælg en Vector Store", options=list(vector_stores.values()))
                vector_store_id = next((id for id, name in vector_stores.items() if name == vector_store_name), None)

                if vector_store_id:
                    if st.button("Hent filer"):
                        with st.spinner("Henter filer..."):
                            result = list_files_in_vector_store(vector_store_id)
                            if result:
                                st.success("Filer hentet succesfuldt!")
                                st.json(result)
            else:
                st.warning("Ingen Vector Store fundet.")
        elif content_tabs == 'Upload':
            st.write("Upload dine filer her")
            uploaded_files = st.file_uploader(
                "Vælg filer for at uploade",
                type=["txt", "json", "csv", "pdf", "docx"],
                accept_multiple_files=True
            )

            if uploaded_files:
                if st.button("Upload"):
                    with st.spinner("Uploader filer..."):
                        for uploaded_file in uploaded_files:
                            st.write(f"Uploader filen: {uploaded_file.name}")
                            result = upload_file(uploaded_file)
                            if result:
                                st.success(f"Filen '{uploaded_file.name}' blev uploadet succesfuldt til Azure OpenAI!")

    except Exception as e:
        st.error(f'En fejl opstod: {e}')
