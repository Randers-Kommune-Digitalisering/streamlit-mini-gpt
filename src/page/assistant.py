import streamlit as st
import time
from st_copy_to_clipboard import st_copy_to_clipboard
from utils.config import ASSISTANT_ID
from utils.azure_open_ai import get_azure_openai_assistant, fetch_files, map_internal_references_to_file_ids

client_assistant = get_azure_openai_assistant()


def process_user_input(user_input, files, display_in_chat=True):
    st.session_state.messages.append({"role": "user", "content": user_input})

    if display_in_chat:
        with st.chat_message("user"):
            st.write(user_input)

    with st.spinner("Assistenten svarer..."):
        try:
            thread = client_assistant.beta.threads.create()

            for msg in st.session_state.messages:
                client_assistant.beta.threads.messages.create(
                    thread_id=thread.id,
                    role=msg["role"],
                    content=msg["content"]
                )

            run = client_assistant.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=ASSISTANT_ID
            )

            while run.status in ["queued", "in_progress", "cancelling"]:
                time.sleep(1)
                run = client_assistant.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

            if run.status == "completed":
                messages = client_assistant.beta.threads.messages.list(thread_id=thread.id)
                messages_list = list(messages)

                if messages_list:
                    assistant_message = next(
                        (msg for msg in messages_list if msg.role == "assistant"), None
                    )

                    if assistant_message:
                        reference_to_file_id = map_internal_references_to_file_ids(assistant_message)
                        mapped_files = {file_id: files[file_id] for file_id in reference_to_file_id.values() if file_id in files}

                        assistant_response = " ".join(
                            block.text.value for block in assistant_message.content if hasattr(block, "text") and hasattr(block.text, "value")
                        )

                        footnotes = []
                        for idx, (internal_reference, file_id) in enumerate(reference_to_file_id.items(), start=1):
                            if file_id in mapped_files:
                                footnotes.append(f"[{idx}] 📄 {mapped_files[file_id]}")

                        for idx, (internal_reference, file_id) in enumerate(reference_to_file_id.items(), start=1):
                            if file_id in mapped_files:
                                assistant_response = assistant_response.replace(
                                    f"【{internal_reference}†source】", f"[{idx}]"
                                )

                        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

                        if display_in_chat:
                            with st.chat_message("assistant"):
                                col1, col2 = st.columns([0.9, 0.1])
                                with col1:
                                    st.write(assistant_response)
                                    if footnotes:
                                        for footnote in footnotes:
                                            st.markdown(f"- {footnote}")
                                with col2:
                                    st_copy_to_clipboard(assistant_response, key=f"{assistant_response}_copy")
                    else:
                        st.error("Assistentens svar kunne ikke hentes korrekt.")
                else:
                    st.error("Ingen beskeder blev fundet i tråden.")
        except Exception as e:
            st.error(f"Der opstod en fejl: {e}")


def display_hjælpemiddel_chat():
    st.title("Chat med Hjælpemiddel Assistant")
    st.write("Velkommen til chatbotten! Start en samtale nedenfor.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    files = fetch_files()
    if not files:
        files = {}

    st.write("Eller vælg en af de prædefinerede spørgsmål:")
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Beskriv de væsentlige punkter for Småhjælpemidler?", type="primary"):
                process_user_input("Beskriv de væsentlige punkter for Småhjælpemidler?", files, display_in_chat=False)
        with col2:
            if st.button("Hvad er email til Hjælpemiddelcenteret?", type="primary"):
                process_user_input("Hvad er email til Hjælpemiddelcenteret?", files, display_in_chat=False)
        with col3:
            if st.button("Hvad kan du fortælle om Forbrugsgoder?", type="primary"):
                process_user_input("Hvad kan du fortælle om Forbrugsgoder?", files, display_in_chat=False)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Skriv dit spørgsmål her...")
    if user_input:
        process_user_input(user_input, files)
