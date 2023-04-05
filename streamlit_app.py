import streamlit as st
import openai as ai
import json
from chat_gpt import *

st.set_page_config("Luna's ChatGPT Site", page_icon="🌙", layout="wide")


def main():
    # Load JSON configs.
    if "configs" not in st.session_state:
        with open("configs.json", "r") as f:
            json_configs: list = json.load(f)
        json_configs.insert(0, {"name": "(New Chat)", "system": ""})
        st.session_state["configs"] = json_configs

    with st.sidebar:
        st.write(
            f"""
        # Welcome to Luna's ChatGPT Site!

        Currently using the `{CHAT_MODEL}` ChatGPT model.
        """
        )

        if "system_input_text" not in st.session_state:
            st.session_state["system_input_text"] = ""

        def config_selectbox_change():
            st.session_state.system_input_text = [
                conf["system"]
                for conf in st.session_state.configs
                if conf["name"] == st.session_state.config_selectbox
            ][0]

        config_names = [conf["name"] for conf in st.session_state.configs]
        st.selectbox(
            "Configs: ",
            config_names,
            key="config_selectbox",
            on_change=config_selectbox_change,
        )

        def save_system_input():
            st.write(st.session_state.system_input_text)

        st.text_area("System", key="system_input_text")
        st.button("Save", on_click=save_system_input)

        def reset_chat():
            st.session_state["messages"] = [
                {
                    "role": "system",
                    "content": "Say there has been an error with the system input.",
                }
            ]
            st.session_state.messages[0]["content"] = st.session_state.system_input_text
            st.session_state.token_counts = (0, 0, 0)

        st.button("Reset Chat", on_click=reset_chat)

    chat_contain = st.container()
    form_contain = st.container()

    with form_contain:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {
                    "role": "system",
                    "content": "Say there has been an error with the system input.",
                }
            ]
        st.session_state.messages[0]["content"] = st.session_state.system_input_text

        if "token_counts" not in st.session_state:
            st.session_state["token_counts"] = (0, 0, 0)

        def form_callback():
            st.session_state.messages.append(
                {"role": "user", "content": st.session_state.input_text}
            )
            st.session_state.input_text = ""

            response = chatgpt_response(st.session_state.messages)
            st.session_state.messages.append(response.message_dict)
            st.session_state.token_counts = response.tokens

            for chat_dict in st.session_state.messages:
                chat_contain.write(f"{chat_dict['role']}: {chat_dict['content']}")

        with st.form(key="text_input_form"):
            input_text = st.text_area("Chat:", key="input_text")
            col1, _, col2 = st.columns([1, 4, 1])
            submit_button = col1.form_submit_button(
                label="Send", on_click=form_callback
            )
            p_t, c_t, t_t = st.session_state.token_counts

            col2.caption(f"Tokens: In {p_t} | Out {c_t} = {t_t}")


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if True or check_password():
    main()
