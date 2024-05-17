import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime, time, timedelta
from scripts import db_repository as db
from pytz import timezone
import plotly.graph_objects as go

def coletar_dados_glicemia():
    conn = db.connect_to_db()
    glucose_data = db.get_glucoses(conn, st.session_state['user_id'])
    if len(glucose_data) == 0:
        st.error("Sem medições de glicose.")
    else:
        df = pd.DataFrame(glucose_data, columns=['Glicose', 'Dia'])
        return df

def exibir_grafico1(df):
    fig = px.line(df, x='Dia', y='Glicose', title='Nível de Glicose ao Longo do Tempo')
    # Calculate the average glucose level
    avg_glucose = df['Glicose'].mean()

    # Add a horizontal line representing the average glucose level
    fig.add_trace(go.Scatter(x=df['Dia'], y=[avg_glucose]*len(df), mode='lines', name='Média de Glicose'))
    st.plotly_chart(fig)

def exibir_grafico2(df):
    df['Status'] = pd.cut(df['Glicose'], bins=[0, 70, 100, 125, np.inf], labels=['Baixo', 'Normal', 'Pré-diabético', 'Diabético'], include_lowest=True)
    fig2 = px.histogram(df, x='Status', title='Distribuição dos Níveis de Glicose')

    st.plotly_chart(fig2)

@st.experimental_dialog("Registro de hoje📆")
def exibir_dialog_glicose():
    st.divider()
    st.subheader("Qual foi o resultado da sua última medição de glicose no sangue?")
    nivel = st.slider(
        "nível de glicose (mg/dL):",
        70, 180,
        step=1)
    st.subheader("À que horas foi medida?")
    current_time = datetime.now()
    horario = st.time_input("selecione o horário", time(11, 50), step=timedelta(minutes=5))
    timestamp = datetime.combine(datetime.today(), horario)
    if st.button("Submit"):
        conn = db.connect_to_db()
        print("user_id before insertion: ", st.session_state['user_id'])

        db.insert_glucose(conn, nivel, timestamp, st.session_state['user_id'])
        st.rerun()

# @st.experimental_dialog("Registro de exercícios🏋️")
# def exibir_dialog_exercicio():
#     st.divider()
#     st.subheader("Qual exercício você realizou?")
#     exercicio = st.text_input("Digite o tipo de exercício:")
#     st.subheader("Quanto tempo durou o exercício (em minutos)?")
#     duracao = st.slider(
#         "Duração do exercício (minutos):",
#         0, 180,
#         step=1)
#     st.subheader("À que horas você fez o exercício?")
#     horario = st.time_input("selecione o horário", time(11, 50))
#     timestamp = datetime.combine(datetime.today(), horario)
#     if st.button("Submit"):
#         conn = db.connect_to_db()
#         db.insert_exercises(conn, exercicio, duracao)
#         st.rerun()

def dashboard():
    if 'nome' in st.session_state:
        st.title('Olá, {}👋, como vai?'.format(st.session_state['nome']))
    else:
        st.title('Olá usuário👋, como vai?')

    conn = db.connect_to_db()
    last_glucose = db.get_last_glucose(conn, st.session_state['user_id'])


    if last_glucose[0] is not None:
        last_glucose_time = last_glucose[1]
        last_glucose_level = last_glucose[0]
        st.write("Última medição de glicose: {} mg/dL às {}".format(last_glucose_level, last_glucose_time))

        tmz = timezone('America/Sao_Paulo')
        last_glucose_time = timezone('America/Sao_Paulo').localize(last_glucose_time)
        
        print("last_glucose_time: ", last_glucose_time)
        current_time = datetime.now(tmz) + timedelta(minutes=45)
        print("current_time: ", current_time)
        time_difference = abs(current_time - last_glucose_time)
        print("time_difference: ", time_difference)
        
        btn1, btn2 = st.columns([1,1])
        with btn1:
            if time_difference < timedelta(hours=1):
                next_measurement = int(abs(time_difference - timedelta(hours=1)).total_seconds() // 60)
                st.button("Próxima medição disponível em :orange-background[{} minutos]".format(next_measurement), disabled=True)
            else:
                if st.button("Registrar medição de glicose"):
                    st.write("Já chegou a hora de medir novamente!")
                    exibir_dialog_glicose()
    else:
        if st.button("Registrar medição de glicose"):
            st.write("Vamos medir pela primeira vez?")
            exibir_dialog_glicose()
    with btn2:
        st.button("Registrar exercício")
    
    dados = coletar_dados_glicemia()
    exibir_grafico1(dados)
    exibir_grafico2(dados)
