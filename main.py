import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

forbidden_names = ["hitler", "shadow"]

system_prompt_template = """
    Tu es un assistant spécialisé dans le choix de nom de chien. Tu arrives toujours à trouver les meilleurs noms pour les chiens. Tes goûts sont inattendus et originaux. Les noms que tu proposes sont rares et unique. Tu ne donne jamais un nom figurant sur la liste des noms interdits.
    Ton but est de proposer une liste de 20 noms qui pourraient aller à un chien, en fonction de la description et des contraintes qui te sont données.
    les noms interdits sont [{forbidden}]
"""

human_prompt_template = """Voici la description du chien: c'est un {size} chien {sex} de couleur {color}. {description}"""

system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt_template)
human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

def load_Chat():
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    chat = ChatOpenAI(streaming=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), verbose=True, temperature=0)
    return chat

chat = load_Chat()


st.set_page_config(layout="wide", page_title="Nom d'un chien", page_icon=":dog:")
st.header("Nom d'un chien")
st.markdown("Cet outil permet de choisir un nom qui va parfaitement à votre chien. Cet outil est possible grâce \
            à [LangChain](https://langchain.com/) et [OpenAI](https://openai.com) fait par \
            Justin Loroy. \n\n Source Code on [Github](https://github.com/jloroy/nomdunchien/blob/main/main.py)")

col1, col2 = st.columns(2)
def get_color():
    input_color = st.text_input(label="Couleur", value="brun et noir", key="color_input")
    return input_color

def get_description():
    input_description = st.text_area(label="Description", placeholder="il est mignon, gentil, et il aime les calins. Son nom doit commencer par un P.", key="description_input")
    return input_description

def extract_names(text):
    names = []
    for word in text.split():
        if word[0].isupper():
            names.append(word.strip("'-"))
    return names

def get_names():
    if input_size and input_sex and input_color and input_description:
        chat_prompt_with_values = chat_prompt.format_prompt(size=input_size, sex=input_sex, color=input_color, description=input_description, forbidden=", ".join(forbidden_names))
        print(chat_prompt_with_values.to_messages())
        response = chat(chat_prompt_with_values.to_messages()).content
        print(response)
        forbidden_names.extend(extract_names(response))
        col2.write(response)
    else:
        print("at least one param missing: "+input_size +" "+ input_sex  +" "+ input_color  +" "+ input_description )
    
with col1:
    st.markdown("## Parametres")
    input_size = st.radio('taille',['Petit', 'Moyen', 'Grand'])
    input_sex = st.radio('sexe',['Male', 'Femelle'])
    input_color = get_color()
    input_description = get_description()
    st.button("Generer", type='primary', help="Generer 20 noms de chiens", on_click=get_names)

