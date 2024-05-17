import streamlit as st
from scripts import db_repository as db

def cadastrar_usuario(email, senha, nome, genero, idade, altura):
    try:
        conn = db.connect_to_db()
        db.create_tables(conn)
        if db.verify_email(conn, email):
            db.insert_user(conn, email, senha, nome, genero, idade, altura)
            return True
        else:
            print("Email já cadastrado.")
            return False
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        return False

def pagina_cadastro():
    st.title("Cadastro de Usuário")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        nome = st.text_input("Nome:")
        email = st.text_input("Email:")
        senha = st.text_input("Senha:", type="password")
    with col2:
        idade = st.number_input("Idade", min_value=0, value=18)
        genero = st.radio('Selecione o seu gênero', ['Homem', 'Mulher'], index=None)
        altura = st.select_slider('Coloque a sua altura em centímetros', options=range(50, 220))

    if st.button("Cadastrar"):
        if cadastrar_usuario(email, senha, nome, genero, idade, altura):
            st.success("Usuário cadastrado com sucesso!")
        else:
            st.error("Erro ao cadastrar usuário. Tente novamente.")
