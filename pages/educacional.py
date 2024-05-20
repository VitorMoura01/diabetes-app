import streamlit as st
import webbrowser
import itertools
from pages import ui

def app(id, name, description, image):
    ui.linked_image(image, id)
    st.subheader(f"{name}")
    st.markdown(
        f"""
        <div style="width:100%; word-wrap: break-word;">
            <a href="{id}"style="text-decoration: none; color: inherit;">
                {description}
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.write("")

def pagina_educacional():
    
    st.title("Artigos Educacionais")
    col1, col2, col3 = st.columns(3)
    with col1:
        app(
            "id1",
            "O que é a Diabete e seus tipos?",
            "Saiba mais sobre as causas, sintomas e tratamentos do diabetes.",
            "images/1.png",
            )
    with col2:
        app(
            "id2",
            "Diabetes: Fatores de risco",
            "Descubra os fatores de risco do diabetes além dos genéticos!",
            "images/2.png",
            )
    with col3:
        app(
            "id3",
            "Como usar insulina?",
            "Guia essencial: Como usar insulina no tratamento do diabetes.",
            "images/1.png",
            )
        
    col1, col2, col3 = st.columns(3)
    with col1:
        app(
            "id4",
            "Alimentação na Diabete",
            "Dicas e orientações práticas para a alimentação saudável dos diabéticos: ",
            "images/4.png",
            )
    with col2:
        app(
            "id5",
            "Diabetes: Complicações",
            "Saiba mais sobre as complicações do diabetes e como preveni-las.",
            "images/3.png",
            )
    with col3:
        app(
            "id6",
            "Pé diabético",
            "Sintomas, prevenção e tratamento especializado.",
            "images/5.png",
            )