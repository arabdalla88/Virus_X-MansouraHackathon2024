import streamlit as st
import os
from sklearn.metrics.pairwise import cosine_similarity
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from google.generativeai.types import BlockedPromptException
from langchain_core.messages import AIMessage
load_dotenv()  # Load environment variables from .env file

chat_histor = []


def cosine_similarity_score(str1, str2):
    """
    Calculate cosine similarity between two strings
    """
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Create vectorizer
    vectorizer = TfidfVectorizer()

    # Compute TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform([str1, str2])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    return cosine_sim[0][0]


def generate_response_langchain(user_question, complexity_level, memory):
    """
    Generate a response based on user question using LangChain
    """
    groq_chat = None
    if complexity_level == "simple":
        groq_chat = ChatGroq(
            # Fetch the API key from environment variable
            model_name='Llama3-70b-8192'  # LLaMA2-70b model
        )
    elif complexity_level == "large":
        groq_chat = ChatGroq(
            # Fetch the API key from environment variable
            model_name='mixtral-8x7b-32768'  # Mixtral-8x7b model
        )
    elif complexity_level == "complex":
        groq_chat = ChatGroq(
            model_name='gemma-7b-it'  # Gemma-7b-it model
        )

    conversation = ConversationChain(
        llm=groq_chat,
        memory=memory
    )

    response = conversation(user_question)['response']
    response = response.replace(" Meta", " SkyConfig")
    response = response.replace(" Meta AI", " SkyConfig")
    response = response.replace(" Touvron", " Mahmoud")

    return response


def generate_response_google(user_question):
    """
    Generate a response based on user question using Google Generative AI
    """
    try:
        # Create a message with user input
        user_message = HumanMessage(type="human", content=user_question)

        # Invoke the model with the user message
        response = llm_google.invoke([user_message])

        # Check the type of response
        if isinstance(response, AIMessage):
            # This is a response from Google Generative AI
            response_content = response.content
        else:
            # This is a response from LangChain Core
            response_content = response[0].content

        # Replace "Google" with "Parmajha Team" in the response
        response_content = response_content.replace(" Google", " SkyConfig Team")
        response_content = response_content.replace(" Meta", " SkyConfig Team")
        response_content = response_content.replace(" Meta AI", " SkyConfig")
        response_content = response_content.replace(" Touvron", " Mahmoud")

        response_content = response_content.replace("بواسطة جوجل", "بواسطة فريق بارما جاها")

        return response_content

    except BlockedPromptException as e:
        return "Sorry, your message triggered safety filters and cannot be processed. Please try again with a different message."

    except Exception as e:
        # Regenerate the response by invoking the model again
        response = generate_response_google(user_question)
        return response


def generate_response(user_question, complexity_level, memory):
    """
    Generate a response based on user question using LangChain or Google API
    """
    try:
        if complexity_level == "simple" or complexity_level == "large" or complexity_level == "complex":
            # Attempt to use LangChain
            response = generate_response_langchain(user_question, complexity_level, memory)
        else:
            raise ValueError("Invalid complexity level")
    except Exception as e:
        # If LangChain fails (e.g., model inactive), fall back to Google API
        response = generate_response_google(user_question)

    return response








def main():
    col1, col2 = st.columns([1, 5])



    with col2:
        st.header("SkyConfig ")

    conversational_memory_length = 100

    if 'chat_histor' not in st.session_state:
        st.session_state.chat_histor = []

    memory = ConversationBufferWindowMemory(k=conversational_memory_length)



    chat_log = []

    # Display chat history
    st.write("Chat History:")
    for sender, message in st.session_state.chat_histor:
        st.write(f"{sender} {message}")
        chat_log.append((sender, message))  # Add each pair to the chat log

    user_question = st.chat_input("Say something")




    if user_question:
        st.session_state.chat_histor.append(("You 🧠\n\n", user_question))

        if user_question:
            if any("\u0600" <= c <= "\u06FF" for c in user_question):  # Check if input contains Arabic characters
                combined_input = (" هذه المحاثه الاخيره بيننا ") + str(
                    chat_log) + "\n و هذا الرد السؤول الحالي جاوب فقط عليه   -->  " + user_question
                response = generate_response_google(user_question)



            else:
                    try:
                        complexity_level = "simple"

                        # Concatenate user_question with chat log
                        combined_input = (" This The Info of last Chat Between  dont apper The Last Chat Just Check it"
                                          "to provide Your information  ") + str(
                            chat_log) + "\n and This Is current User Input reply only about  -->  " + user_question
                        response = generate_response_langchain(combined_input, complexity_level, memory)




                    except Exception as e:
                        response = f"Error occurred: {str(e)}"
                        if 'model_not_active' in str(e):

                            complexity_level = "large"
                            combined_input = (" This The Info of last Chat Between  dont apper The Last Chat Just Check it"
                                              "to provide Your information  i dont need the User Know  previous chat dont Write about This Chat    ") + str(
                                chat_log) + "\n and This Is current User Input reply only about  -->  " + user_question
                            response = generate_response_langchain(combined_input, complexity_level, memory)
                        else:
                            response = generate_response_google(combined_input)



            st.session_state.chat_histor.append(("ParmaJHA Bot 🤖 \n\n", response))  # appended Chat
            st.write("You 🧠\n\n", user_question)
            st.write("ParmaJHA Bot 🤖 \n\n", response)
        # st.session_state.chat_history.append()


    chat_log = chat_log[-4:]

    if len(chat_log) ==4 :
        chat_log=[]

    return chat_log




# Inject the CSS using st.markdown

if __name__ == "__main__":
    main()
