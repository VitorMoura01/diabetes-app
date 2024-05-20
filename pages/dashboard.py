import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta
from scripts import db_repository as db
from pytz import timezone
from time import sleep
from pages.educacional import pagina_educacional
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

load_dotenv()

def initialize_session_state():
    # if 'is_new_user' not in st.session_state:
    #     st.session_state['is_new_user'] = False
    if 'medicao' not in st.session_state:
        st.session_state['medicao'] = '_Vamos medir pela primeira vez?_'
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'nome' not in st.session_state:
        st.session_state['nome'] = 'Usuário'

initialize_session_state()

# Context manager for database connection
class DBConnection:
    def __enter__(self):
        self.conn = db.connect_to_db()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

# Generic data collection function
def coletar_dados(query_func, columns):
    with DBConnection() as conn:
        data = query_func(conn, st.session_state['user_id'])
        if len(data) == 0:
            return None
        return pd.DataFrame(data, columns=columns).set_index('id')

def coletar_dados_glicemia():
    return coletar_dados(db.get_glucoses, ['id', 'Glicose (mg/dL)', 'Dia'])

def coletar_dados_exercicios_users():
    return coletar_dados(db.get_exercises_user, ['id', 'Exercicio', 'Duracao', 'Calorias Totais'])

def coletar_dados_corpo():
    with DBConnection() as conn:
        weight_data = db.get_weight(conn, st.session_state['user_id'])
        height_data = db.get_height(conn, st.session_state['user_id'])
        if not weight_data or height_data is None:
            return None
        df = pd.DataFrame(weight_data, columns=['Peso (kg)', 'Dia'])
        df['Altura (cm)'] = height_data[0]
        return df

def exibir_grafico1(df):
    fig = px.line(df, x='Dia', y='Glicose (mg/dL)', title='Nível de Glicose ao Longo do Tempo', line_shape='spline')
    avg_glucose = df['Glicose (mg/dL)'].mean()
    fig.update_traces(line_color='#208128')
    fig.add_trace(go.Scatter(x=df['Dia'], y=[avg_glucose] * len(df), mode='lines', name='Sua Média de Glicose', line=dict(color='royalblue', width=4, dash='dot')))
    fig.update_layout(dragmode="pan")  # Disable drag mode interaction
    fig.update_yaxes(fixedrange=True)  # Disable zoom on y-axis
    st.plotly_chart(fig)

def exibir_grafico2(df):
    df['Status'] = pd.cut(df['Glicose (mg/dL)'], bins=[0, 70, 100, 125, np.inf], labels=['Baixo', 'Normal', 'Pré-diabético', 'Diabético'], include_lowest=True)

    st.write('**Quantas vezes você esteve em cada nível de glicose:**')
    cols = st.columns(4)
    for i, status in enumerate(['Baixo', 'Normal', 'Pré-diabético', 'Diabético']):
        count = df[df['Status'] == status].shape[0]
        cols[i].metric(label=f'{status}', value=count)
    fig2 = px.histogram(df, x='Status', title='Distribuição dos Níveis de Glicose')
    fig2.update_traces(marker_color='#208128')
    fig2.update_layout(dragmode="pan")  # Disable drag mode interactions
    fig2.update_yaxes(fixedrange=True)  # Disable zoom on y-axis
    st.plotly_chart(fig2)

def exibir_grafico3(df):
    fig3 = px.bar(df, x='Exercicio', y='Calorias Totais', title='Calorias Gastas por Exercício')
    fig3.update_layout(dragmode="pan")  # Disable drag mode interactions
    fig3.update_yaxes(fixedrange=True)  # Disable zoom on y-axis
    st.plotly_chart(fig3)

def exibir_grafico4(df):
    df['IMC'] = df['Peso (kg)'] / ((df['Altura (cm)'] / 100) ** 2)
    avg_peso = df['Peso (kg)'].mean()
    if len(df) >= 2:
        st.metric('IMC (Índice de Massa Corporal)', value=df['IMC'].iloc[-1], delta=(df['IMC'].iloc[-2] - df['IMC'].iloc[-1]))
    elif len(df) == 1:
        st.metric('IMC (Índice de Massa Corporal)', value=df['IMC'].iloc[-1])
    else:
        st.write('Sem dados suficientes para cálculo de IMC (Índice de Massa Corporal).')

    fig4 = px.line(df, x='Dia', y='Peso (kg)', title='Peso ao Longo do Tempo', line_shape='spline')
    fig4.update_traces(line_color='#208128')
    fig4.add_trace(go.Scatter(x=df['Dia'], y=[avg_peso] * len(df), mode='lines', name='Sua Média de Peso', line=dict(color='royalblue', width=4, dash='dot')))
    fig4.update_layout(dragmode="pan")  # Disable drag mode interactions
    fig4.update_yaxes(fixedrange=True)  # Disable zoom on y-axis
    st.plotly_chart(fig4)

@st.experimental_dialog('Registro de hoje📆')
def exibir_dialog_glicose():
    st.write('Registre o resultado da sua última medição de glicose no sangue.')
    nivel = st.slider('Nível de glicose (mg/dL):', 0, 800, step=1)
    horario = st.time_input('Horário da medição de :green-background[HOJE]:', time(11, 50), step=timedelta(minutes=30))
    timestamp = datetime.combine(datetime.today(), horario)
    if st.button('Registrar', use_container_width=True, type='primary'):
        with DBConnection() as conn:
            db.insert_glucose(conn, nivel, timestamp, st.session_state['user_id'])
        # st.session_state['is_new_user'] = False
        st.success('Medição de glicose registrada com sucesso!')
        st.rerun()

@st.experimental_dialog('Registro de exercícios 🏋️')
def exibir_dialog_exercicio():
    with DBConnection() as conn:
        exercises = db.get_exercises(conn, st.session_state['user_id'])
    options = [exercise[1] for exercise in exercises]
    calories = [exercise[2] for exercise in exercises]
    exercicio = st.selectbox('Qual exercício você realizou?', options)
    if exercicio is not None:
        exercise_index = options.index(exercicio)
    else:
        st.write("Exercício não selecionado.")
    duracao = st.slider('Duração do exercício (minutos):', 0, 180, step=1)
    calorias_totais = (duracao / 60) * calories[exercise_index]
    peso = st.number_input('Qual é o seu peso atual?', min_value=0.0, step=0.1)

    if st.button('Registrar', use_container_width=True, type='primary'):
        with DBConnection() as conn:
            db.insert_exercises_user(conn, st.session_state['user_id'], exercise_index + 1, options[exercise_index], duracao, calorias_totais)
            current_time = datetime.now(timezone('America/Sao_Paulo')) + timedelta(minutes=45)
            db.insert_weight(conn, peso, current_time, st.session_state['user_id'])
        st.success('Registro de exercício realizado com sucesso!')
        # st.rerun()

def pagina_dashboard():
    st.title(f'Olá, :green[{st.session_state.get("nome", "usuário")}] 👋, como vai?')
    with DBConnection() as conn:
        last_glucose = db.get_last_glucose(conn, st.session_state['user_id'])

    btn1, btn2 = st.columns([1, 1])
    if last_glucose[0] is not None:
        last_glucose_time = timezone('America/Sao_Paulo').localize(last_glucose[1])
        current_time = datetime.now(timezone('America/Sao_Paulo'))
        time_difference = abs(current_time - last_glucose_time)

        with btn1:
            if time_difference < timedelta(hours=1):
                st.session_state['medicao'] = 'Volte aqui mais tarde.'
                next_measurement = int(abs(time_difference - timedelta(hours=1)).total_seconds() // 60)
                st.button(f'Próxima medição disponível em :red-background[{next_measurement} minutos]', disabled=True)
            else:
                st.session_state['medicao'] = 'Já chegou a hora de medir novamente!'
                if st.button('Registrar medição de glicose', type='primary', use_container_width=True):
                    exibir_dialog_glicose()
    else:
        with btn1:
            st.session_state['medicao'] = '_Vamos medir pela primeira vez?_'
            if st.button('Registrar medição de glicose', type='primary', use_container_width=True):
                exibir_dialog_glicose()
            st.write(st.session_state['medicao'])

    with btn2:
        if st.button('Registrar exercício físico', type='primary', use_container_width=True):
            exibir_dialog_exercicio()

    if st.session_state['medicao'] != '_Vamos medir pela primeira vez?_':
        st.write(f'Última medição de glicose: :green-background[{last_glucose[0]} mg/dL] às :green-background[{last_glucose_time.strftime("%H:%M")}] do dia {last_glucose_time.strftime("%d/%m")}.  _{st.session_state["medicao"]}_')
    st.divider()

    tab1, tab2 = st.tabs(['Glicemia🧁', 'Exercícios🏋️'])
    if st.session_state['medicao'] != '_Vamos medir pela primeira vez?_':
        with tab1:
            st.subheader('Aqui estão os seus dados de glicemia')
            dados_glicemia = coletar_dados_glicemia()
            if dados_glicemia is not None:
                exibir_grafico1(dados_glicemia)
                exibir_grafico2(dados_glicemia)

    check_exercicio = coletar_dados_exercicios_users()
    if check_exercicio is not None:
        with tab2:
            st.subheader('Aqui estão os seus dados de exercícios')
            dados_exercicio = coletar_dados_exercicios_users()
            dados_peso = coletar_dados_corpo()
            exibir_grafico4(dados_peso)
            exibir_grafico3(dados_exercicio)
            

    st.divider()
    pagina_educacional()
    st.divider()

    if st.button('Sair', key='sair_button', type='primary'):
        st.session_state.clear()
        st.warning('Você saiu da sua conta.')
        st.rerun()

    if st.session_state['user_id'] == 1:
        st.divider()
        if st.button('Apagar lista de exercícios', key='apagar_exercicios_button', type='primary'):
            with DBConnection() as conn:
                db.delete_exercises(conn)
                st.write('Lista de exercícios apagada com sucesso.')
                st.rerun()
        if st.button('Apagar lista de usuários', key='apagar_usuarios_button', type='primary'):
            with DBConnection() as conn:
                db.delete_users(conn)
                st.write('Lista de usuários apagada com sucesso.')
        if st.button('Apagar banco de dados', key='apagar_db_button', type='primary'):
            with DBConnection() as conn:
                db.delete_tables(conn)
                st.session_state.clear()
                st.write('Banco de dados apagado com sucesso.')
                st.rerun()

        with DBConnection() as conn:
            users_list = coletar_dados(db.get_users, ['id', 'email', 'display_name', 'gender', 'age', 'height'])
            exercises_list = coletar_dados(db.get_exercises, ['id', 'title', 'calories', 'intensity'])
            st.write('Usuários cadastrados:')
            st.write(users_list)
            st.write('Exercícios cadastrados:')
            st.write(exercises_list)
        