import datetime
from io import BytesIO
import pandas as pd
import psycopg2
import streamlit as st
from scripts import db_repository as db
from pages.dashboard import DBConnection, coletar_dados

def export_to_excel(dataframes):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for table_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=table_name, index=False)
    output.seek(0)
    return output

def get_data():
    with DBConnection() as conn:
        if isinstance(conn, psycopg2.extensions.connection):
            tables = db.get_all_tables(conn)
            dataframes = {}
            for table in tables:
                dataframes[table] = db.fetch_table_data(conn, table)
            excel_file = export_to_excel(dataframes)
            return excel_file
        else:
            st.error("Connection to the database failed.")
            return None

def pagina_admin():

    st.title('Página de Administração')
    with DBConnection() as conn:
        users_list = coletar_dados(db.get_users, ['id', 'email', 'display_name', 'gender', 'age', 'height'])
        exercises_list = coletar_dados(db.get_exercises, ['id', 'title', 'calories', 'intensity'])
        st.write('Usuários cadastrados:')
        st.write(users_list)
        st.write('Exercícios cadastrados:')
        st.write(exercises_list)
        #Gráficos do indice de glicose dos usuários
    st.divider()

    st.title('Controles de Administração')
    st.info('Use somente caso necessário')

    # Section: Export Data
    st.subheader('Exportar dados')
    if st.button('Carregar Excel', type='primary'):
        excel_data = get_data()
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        st.download_button(
            label="Baixar arquivo Excel",
            data=excel_data,
            file_name=f'registros_glicecontrole-{now_str}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    # Section: Delete Exercise
    st.subheader('Apagar exercício')
    exercise_id = st.number_input('Digite o ID do exercício que deseja apagar:', step=1, min_value=1)
    if st.button('Apagar exercício', key='apagar_exercicio_button'):
        with DBConnection() as conn:
            db.delete_exercise_by_id(conn, exercise_id)
            st.write('Exercício apagado com sucesso.')
            st.rerun()

    # Section: Delete User
    st.subheader('Apagar usuário')
    user_id = st.number_input('Digite o ID do usuário que deseja apagar:', step=1, min_value=2)
    if st.button('Apagar usuário', key='apagar_usuario_button') and user_id:
        with DBConnection() as conn:
            db.delete_user_by_id(conn, user_id)
            st.write(f'Usuário {user_id} apagado com sucesso.')
            st.rerun()
    
    st.divider()

    # Section: Delete Exercise List
    st.subheader('Apagar lista de exercícios')
    if st.button('Apagar lista de exercícios', key='apagar_exercicios_button'):
        with DBConnection() as conn:
            db.delete_exercises(conn)
            st.write('Lista de exercícios apagada com sucesso.')
            st.rerun()

    # Section: Logout
    st.subheader('Sair')
    if st.button('Sair', key='sair_button', type='primary'):
        st.session_state.clear()
        st.warning('Você saiu da sua conta.')
        st.rerun()
