import streamlit as st
import webbrowser
import itertools
from pages import ui

def app(name, description, image, link):
    ui.linked_image(image, link)
    st.subheader(f"[{name}]({link})")
    st.write(f"[Ver Artigo]({link})")
    st.write("")

def pagina_educacional():
    
    st.title("Artigos Educacionais")
    col1, col2, col3 = st.columns(3)
    with col1:
        app(
            "Diabetes: Causas, Sintomas e Tratamentos",
            "Saiba mais sobre as causas, sintomas e tratamentos do diabetes.",
            "images/1.png",
            "https://www.medium.com/diabetes-causas-sintomas-tratamentos"
        )
    with col2:
        app(
            "Diabetes: Alimentação Saudável",
            "Descubra como ter uma alimentação saudável para controlar o diabetes.",
            "images/2.png",
            "https://www.medium.com/diabetes-alimentacao-saudavel"
        )
    with col3:
        app(
            "Diabetes: Exercícios Físicos Recomendados",
            "Conheça os exercícios físicos recomendados para quem tem diabetes.",
            "images/1.png",
            "https://www.medium.com/diabetes-exercicios-fisicos-recomendados"
        )
        
    col1, col2, col3 = st.columns(3)
    with col1:
        app(
            "Diabetes: Controle da Glicemia",
            "Aprenda a controlar a glicemia e manter o diabetes sob controle.",
            "images/4.png",
            "https://www.medium.com/diabetes-controle-glicemia"
        )
    with col2:
        app(
            "Diabetes: Complicações e Prevenção",
            "Saiba mais sobre as complicações do diabetes e como preveni-las.",
            "images/3.png",
            "https://www.medium.com/diabetes-complicacoes-prevencao"
        )
    with col3:
        app(
            "Diabetes: Dicas para o Dia a Dia",
            "Confira dicas úteis para lidar com o diabetes no dia a dia.",
            "images/5.png",
            "https://www.medium.com/diabetes-dicas-dia-a-dia"
        )