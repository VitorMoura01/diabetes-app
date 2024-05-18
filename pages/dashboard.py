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

if 'medicao' not in st.session_state:
    st.session_state['medicao'] = "_Vamos medir pela primeira vez?_"

def coletar_dados_glicemia():
    conn = db.connect_to_db()
    glucose_data = db.get_glucoses(conn, st.session_state['user_id'])
    if len(glucose_data) == 0:
        return None
    else:
        df = pd.DataFrame(glucose_data, columns=['Glicose (mg/dL)', 'Dia'])
        return df

def coletar_dados_exercicios_users():
    conn = db.connect_to_db()
    exercises_data = db.get_exercises_user(conn, st.session_state['user_id'])
    if len(exercises_data) == 0:
        return None
    else:
        df = pd.DataFrame(exercises_data, columns=['Exercicio', 'Duracao', 'Calorias Totais'])
        return df
    
def coletar_dados_corpo():
    conn = db.connect_to_db()
    weight_data = db.get_weight(conn, st.session_state['user_id'])
    height_data = db.get_height(conn, st.session_state['user_id'])
    if len(weight_data) == 0:
        return None
    elif height_data is None:
        return None
    else:
        df = pd.DataFrame(weight_data, columns=['Peso (kg)', 'Dia'])
        df['Altura (cm)'] = height_data[0]
        return df

def exibir_grafico1(df):
    fig = px.line(df, x='Dia', y='Glicose (mg/dL)', title='Nível de Glicose ao Longo do Tempo')
    # Calculate the average glucose level
    avg_glucose = df['Glicose (mg/dL)'].mean()

    # Add a horizontal line representing the average glucose level
    fig.add_trace(go.Scatter(x=df['Dia'], y=[avg_glucose]*len(df), mode='lines', name='Média de Glicose'))
    st.plotly_chart(fig)

def exibir_grafico2(df):
    df['Status'] = pd.cut(df['Glicose (mg/dL)'], bins=[0, 70, 100, 125, np.inf], labels=['Baixo', 'Normal', 'Pré-diabético', 'Diabético'], include_lowest=True)
    fig2 = px.histogram(df, x='Status', title='Distribuição dos Níveis de Glicose')

    st.plotly_chart(fig2)

def exibir_grafico3(df):
    fig3 = px.bar(df, x='Exercicio', y='Calorias Totais', title='Calorias Gastas por Exercício')
    st.plotly_chart(fig3)

def exibir_grafico4(df):
    df['IMC'] = df['Peso (kg)'] / ((df['Altura (cm)'] / 100) ** 2)
    # Plot for weight over time
    fig4 = px.line(df, x='Dia', y='Peso (kg)', title='Peso ao Longo do Tempo')
    st.plotly_chart(fig4)
    #IMC
    if len(df) >= 2:
        st.metric("IMC (Índice de Massa Corporal)", value=df['IMC'].iloc[-1], delta= (df['IMC'].iloc[-2] - df['IMC'].iloc[-1]))
    elif len(df) == 1:
        st.metric("IMC (Índice de Massa Corporal)", value=df['IMC'].iloc[-1])
    else:
        st.write("Sem dados suficientes para cálculo de IMC (Índice de Massa Corporal).")


@st.experimental_dialog("Registro de hoje📆")
def exibir_dialog_glicose():
    st.write("Registre o resultado da sua última medição de glicose no sangue.")
    nivel = st.slider(
        "Nível de glicose (mg/dL):",
        70, 180,
        step=1)
    horario = st.time_input("Horário da medição:", time(11, 50), step=timedelta(minutes=30))
    timestamp = datetime.combine(datetime.today(), horario)
    if st.button("Registrar"):
        conn = db.connect_to_db()
        db.insert_glucose(conn, nivel, timestamp, st.session_state['user_id'])
        st.success("Medição de glicose registrada com sucesso!")
        sleep(1)
        st.rerun()

@st.experimental_dialog("Registro de exercícios 🏋️")
def exibir_dialog_exercicio():
    conn = db.connect_to_db()
    exercises = db.get_exercises(conn)
    
    options = [exercise[1] for exercise in exercises]
    calories = [exercise[2] for exercise in exercises]
    exercicio = st.selectbox("Qual exercício você realizou?", options)
    exercise_index = options.index(exercicio)
    duracao = st.slider(
        "Duração do exercício (minutos):",
        0, 180,
        step=1)
    calorias_totais = (duracao / 60) * calories[exercise_index]
    peso = st.number_input("Qual é o seu peso atual?", min_value=0.0, step=0.1)
    if st.button("Registrar"):
        conn = db.connect_to_db()
        db.insert_exercises_user(conn, st.session_state['user_id'], exercise_index + 1, options[exercise_index], duracao, calorias_totais)
        current_time = datetime.now(timezone('America/Sao_Paulo')) + timedelta(minutes=45)
        db.insert_weight(conn, peso, current_time, st.session_state['user_id'])
        st.success("Registro de exercício realizado com sucesso!")
        st.session_state['exercicio'] = "Medido"
        sleep(1)
        st.rerun()

def pagina_dashboard():
    if 'nome' in st.session_state:
        st.title('Olá, :blue[{}] 👋, como vai?'.format(st.session_state['nome']))
    else:
        st.title('Olá usuário 👋, como vai?')

    conn = db.connect_to_db()
    last_glucose = db.get_last_glucose(conn, st.session_state['user_id'])

    btn1, btn2 = st.columns([1,1])
    if last_glucose[0] is not None:
        last_glucose_time = last_glucose[1]
        last_glucose_level = last_glucose[0]

        tmz = timezone('America/Sao_Paulo')
        last_glucose_time = timezone('America/Sao_Paulo').localize(last_glucose_time)

        current_time = datetime.now(tmz) + timedelta(minutes=45)
        time_difference = abs(current_time - last_glucose_time)

        with btn1:
            if time_difference < timedelta(hours=1):
                st.session_state['medicao'] = "Volte aqui mais tarde."
                next_measurement = int(abs(time_difference - timedelta(hours=1)).total_seconds() // 60)
                st.button("Próxima medição disponível em :red-background[{} minutos]".format(next_measurement), disabled=True)
            else:
                st.session_state['medicao'] = "Já chegou a hora de medir novamente!"
                if st.button("Registrar medição de glicose"):
                    exibir_dialog_glicose()
    else:
        with btn1:
            st.session_state['medicao'] = "_Vamos medir pela primeira vez?_"
            if st.button("Registrar medição de glicose"):
                exibir_dialog_glicose()
            st.write(st.session_state['medicao'])
        
    with btn2:
        if st.button("Registrar exercício físico"):
            exibir_dialog_exercicio()

   
    if st.session_state['medicao'] != "_Vamos medir pela primeira vez?_":
        st.write("Última medição de glicose: :blue-background[{} mg/dL] às :blue-background[{}].  _{}_. ".format(last_glucose_level, last_glucose_time.strftime('%H:%M'), st.session_state['medicao']))
    st.divider()

    tab1, tab2 = st.tabs(["Glicemia🧁", "Exercícios🏋️"])
    if st.session_state['medicao'] != "_Vamos medir pela primeira vez?_":
        with tab1:
            st.subheader("Aqui estão os seus dados de glicemia")
            dados_glicemia = coletar_dados_glicemia()
            exibir_grafico1(dados_glicemia)
            exibir_grafico2(dados_glicemia)
    
    check_exercicio = coletar_dados_exercicios_users()
    if check_exercicio is not None:
        with tab2:
            st.subheader("Aqui estão os seus dados de exercícios")
            dados_exercicio = coletar_dados_exercicios_users()
            dados_peso = coletar_dados_corpo()   
            exibir_grafico3(dados_exercicio)
            exibir_grafico4(dados_peso)
    
    st.divider()
    pagina_educacional()