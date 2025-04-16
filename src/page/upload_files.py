import streamlit as st
import streamlit_antd_components as sac
from utils.azure_open_ai import (
    fetch_vector_stores,
    add_file_to_assistant,
    fetch_files,
    add_file_to_vector_store,
    delete_file_from_vector_store,
    fetch_files_from_vector_store
)
from utils.config import HJAELPEMIDDEL_VECTOR_ID


def upload_files():
    col_1 = st.columns([1])[0]

    with col_1:
        content_tabs = sac.tabs([
            sac.TabsItem('Upload', tag='Upload', icon='upload'),
            sac.TabsItem('TIlføj filer', tag='TIlføj', icon='bi bi-file-earmark-text'),
            sac.TabsItem('Slet filer', tag='Slet', icon='bi bi-trash3')
        ], color='teal', size='md', position='top', align='start', use_container_width=True)

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
                            result = add_file_to_assistant(uploaded_file)
                            if result:
                                st.success(f"Filen '{uploaded_file.name}' blev uploadet succesfuldt til Azure OpenAI!", icon="✅")
                            else:
                                st.error(f"Fejl under upload af fil '{uploaded_file.name}'.", icon="❌")

        elif content_tabs == 'TIlføj filer':
            st.write("Tilføj eksisterende filer til Hjælpemiddel-Assistenten")

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
                    selected_files = st.multiselect("Vælg filer", options=list(files.values()), help="Vælg de filer, du vil tilføje til Hjælpemiddel Assistenten.", placeholder="Vælg filer, du vil tilføje")
                    selected_file_ids = [id for id, name in files.items() if name in selected_files]

                    if selected_file_ids:
                        if st.button("Tilføj valgte filer"):
                            with st.spinner("Tilføjer filer..."):
                                for file_id in selected_file_ids:
                                    result = add_file_to_vector_store(vector_store_id, file_id)
                                    if result:
                                        st.success("Filen blev tilføjet succesfuldt!", icon="✅")
                                    else:
                                        st.error("Fejl under tilføjelse af fil.", icon="❌")
                else:
                    st.warning("Ingen filer fundet. Upload filer først.")

        elif content_tabs == 'Slet filer':
            st.write("Slet filer fra Hjælpemiddel-Assistenten")

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
                files = fetch_files_from_vector_store(vector_store_id)
                if files:
                    selected_files = st.multiselect(
                        "Vælg filer", 
                        options=list(files.values()), 
                        help="Vælg de filer, du vil slette", 
                        placeholder="Vælg filer, du vil slette"
                    )
                    selected_file_ids = [id for id, name in files.items() if name in selected_files]

                    if selected_file_ids:
                        if st.button("Slet valgte filer"):
                            with st.spinner("Sletter filer..."):
                                for file_id in selected_file_ids:
                                    result = delete_file_from_vector_store(vector_store_id, file_id)
                                    if result:
                                        st.success("Filen blev slettet succesfuldt!", icon="✅")
                                    else:
                                        st.error("Fejl under sletning af fil.", icon="❌")
                else:
                    st.warning("Ingen filer fundet. Upload filer først.")

    except Exception as e:
        st.error(f'En fejl opstod: {e}')
