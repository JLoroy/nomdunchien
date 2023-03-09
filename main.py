import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Tu es un assistant spécialisé dans le choix de nom de chien. Tu arrives toujours à trouver les meilleurs noms pour les chiens.
    Ton but est de:
    - Proposer une liste de 5 noms qui pourraient aller à un chien, en fonction de la description et des contraintes qui te sont données. Pour chaque nom, donne une explication du nom et pourquoi tu penses que cela irait bien au chien.
    
    Voici la description du chien: c'est un {size} chien {sex} de couleur {color}. {description}
    {initial}
    TA RESPONSE, SOUS FORME DE LISTE:
"""

prompt = PromptTemplate(
    input_variables=["size","sex", "color", "initial", "description"],
    template=template,
)

def load_LLM():
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7)
    return llm

llm = load_LLM()

st.set_page_config(page_title="Nom d'un chien", page_icon=":dog:")
st.header("Nom d'un chien")
st.markdown("Cet outil permet de choisir un nom qui va parfaitement à votre chien. Cet outil est possible grâce \
            à [LangChain](https://langchain.com/) et [OpenAI](https://openai.com) fait par \
            Justin Loroy. \n\n Source Code on [Github](https://github.com/jloroy/nomdunchien/blob/main/main.py)")

col1, col2 = st.columns(2)
def get_color():
    input_color = st.text_input(label="Couleur", placeholder="brun, noir, jaune", key="color_input")
    return input_color
def get_initial():
    input_initial = st.text_input(label="Initiale", placeholder="N'importe", key="initial_input")
    if input_initial == "":
        return ""
    return "Le nom du chien doit commencer par "+input_initial
def get_description():
    input_description = st.text_input(label="Description", placeholder="mignon, gentil, calin", key="description_input")
    return input_description

def get_names():
    print ("click on button: "+input_size +" "+ input_sex  +" "+ input_color  +" "+ input_initial  +" "+ input_description )
    if input_size and input_sex and input_color and input_description: 
        prompt_with_params = prompt.format(size=input_size, sex=input_sex, color=input_color, initial=input_initial, description=input_description)
        col2.write(llm(prompt_with_params))
    else:
        print("at least one param missing: "+input_size +" "+ input_sex  +" "+ input_color  +" initiale:"+ input_initial  +" "+ input_description )

with col1:
    st.markdown("## Parametres")
    input_size = st.radio('taille',['Petit', 'Moyen', 'Grand'])
    input_sex = st.radio('sexe',['Male', 'Femelle'])
    input_color = get_color()
    input_initial = get_initial()
    input_description = get_description()



with col2:
    st.button("Generer", type='primary', help="Generer 5 noms de chiens", on_click=get_names)


