from datetime import datetime, timedelta
from time import sleep

from pytz import timezone
from pages.login import fazer_login
import streamlit as st
from scripts import db_repository as db
from scripts import encrypt

def cadastrar_usuario(email, senha, nome, genero, idade, altura, peso):
    if not email or not senha or not nome or not genero or not idade or not altura or not peso:
        st.error('Todos os campos são obrigatórios.')
        return False
    try:
        conn = db.connect_to_db()
        db.create_tables(conn)
        if db.verify_email(conn, email):
            senha = encrypt.handle(senha)
            db.insert_user(conn, email, senha, nome, genero, idade, altura)
            return True
        else:
            st.error('Email já cadastrado.')
            return False
    except Exception as e:
        st.error(f'Erro ao inserir usuário: {e}')
        return False

def pagina_cadastro():
    st.title('Cadastro de Usuário')

    col1, col2 = st.columns(2, gap='medium')
    with col1:
        nome = st.text_input('Nome:')
        email = st.text_input('Email:')
        senha = st.text_input('Senha:', type='password')
    with col2:
        idade = st.number_input('Idade', min_value=0, value=18)
        genero = st.radio('Selecione o seu gênero', ['Homem', 'Mulher'], index=None)
        altura = st.select_slider('Coloque a sua altura em centímetros', options=range(100, 220), value=160)
        peso = st.number_input('Qual é o seu peso atual?', min_value=0.0, step=0.1, value=65.0)

    if st.button('Cadastrar', type='primary'):
        if cadastrar_usuario(email, senha, nome, genero, idade, altura, peso):
            if fazer_login(email,senha):
                conn = db.connect_to_db()
                current_time = datetime.now(timezone('America/Sao_Paulo')) + timedelta(minutes=45)
                db.insert_weight(conn, peso, current_time, st.session_state['user_id'])
                
                st.success('Usuário cadastrado com sucesso!')
                # st.session_state['is_new_user'] = True
                st.session_state['logged_in'] = True
                st.session_state['pagina'] = 'Dashboard'
                with st.spinner('Carregando...'):
                    sleep(1)
                    st.rerun()
        else:
            print('Erro ao cadastrar usuário. Tente novamente.')
