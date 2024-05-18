import streamlit as st
from time import sleep
from scripts import db_repository as db

def fazer_login(email, senha):
    conn = db.connect_to_db()
    db.create_tables(conn)
    user_id, display_name = db.login(conn, email, senha)
    if user_id:
        st.session_state["user_id"] = user_id
        st.session_state["nome"] = display_name
        return True
    else:
        return False
    
def pagina_login():
    st.title("Faça login na sua conta da X App")
    email = st.text_input("Email:", value="vitor")
    senha = st.text_input("Senha:", type="password", value="vitor@")
    
    if st.button("Fazer Login"):
        if fazer_login(email, senha):
            st.success("Login realizado com sucesso!")
            st.session_state["logged_in"] = True
            st.session_state["pagina"] = "Dashboard"
            with st.spinner("Carregando..."):
                sleep(1)
                st.rerun()
        else:
            st.error("Email ou senha incorretos. Tente novamente.")
