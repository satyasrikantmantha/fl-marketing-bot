import streamlit as st
import time
import random
import requests
import os

st.image("https://assets-global.website-files.com/61ffed246e785f28c1a44633/63edbbc5b6b5f37b605cf0f2_fl-footer-p-500.png")

st.title("Welcome to our Marketing Bot!!")

st.write("This is a LLM powered chatbot trained on Fission Labs and its offerings. We are here to help you with your queries about us and what we do. Please feel free to reach out to us if you have any questions or feedback!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def respond(message, history):

    if len(message.strip()) == 0:
        return "ERROR the question should not be empty"

    url = 'https://skyhive-e2-us-east-1-deployment.cloud.databricks.com/serving-endpoints/dbdemos_endpoint_skyhive_nv_rag_chatbot_custom/invocations'
    headers = {'Authorization': f'Bearer {os.environ.get("DATABRICKS_TOKEN")}', 'Content-Type': 'application/json'}


    #prompt = list(itertools.chain.from_iterable(history))
    #prompt.append(message)
    #q = {"inputs": [prompt]}
    q = {"inputs": [message]}
    try:
        response = requests.post(
            url, json=q, headers=headers, timeout=100)
        response_data = response.json()
        #print(response_data)
        response_data=response_data["predictions"][0]
        #print(response_data)

    except Exception as error:
        response_data = f"ERROR status_code: {type(error).__name__}"
        # + str(response.status_code) + " response:" + response.text

    # print(response.json())
    for word in response_data.split():
        yield word + " "
        time.sleep(0.05)
        
        
if prompt := st.chat_input("Type in your questions about Fission Labs and its offerings!!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(respond(prompt, st.session_state.messages))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
        
