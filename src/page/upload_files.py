import streamlit as st
import streamlit_antd_components as sac
from utils.azure_open_ai import list_files_in_vector_store, fetch_vector_stores


def upload_files():
    col_1 = st.columns([1])[0]

    with col_1:
        content_tabs = sac.tabs([
            sac.TabsItem('List Files', tag='List Files', icon='bi bi-file-earmark-word'),
            sac.TabsItem('Upload', tag='Upload', icon='upload')
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
            st.write("Upload dokumenter")

    except Exception as e:
        st.error(f'En fejl opstod: {e}')
