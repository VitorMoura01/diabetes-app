import streamlit as st
from pages.cadastro import pagina_cadastro
from pages.login import pagina_login
from pages.dashboard import pagina_dashboard

st.set_page_config(page_title='GliceControle', page_icon='🧁', initial_sidebar_state='collapsed')

if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'Login'

def config():
    
    #COR DAS TABS
    st.markdown(
        '''
    <style>

        .stTabs [data-baseweb='tab-list'] {
            gap: 2px;
        }

        .stTabs [data-baseweb='tab'] {
            height: 50px;
            width: 500px;
            white-space: pre-wrap;
            background-color: ;
            border-radius: 4px 4px 0px 0px;
            gap: 10px;
            padding-top: 10px;
            padding-bottom: 10px;
        }

        .stTabs [data-baseweb='tab']:hover {
            color: green;
        }

        .stTabs [aria-selected='true'] {
            color: green;
        }

    </style>
    ''',
        unsafe_allow_html=True)
    
    #LINKS ARTIGOS
    st.markdown(
    '''
    <style>
        .screenshot {
            border: 1px solid rgba(38, 39, 48, 0.2);
            border-radius: 0.25rem;
        }
        
        h3 {
            padding-top: 1rem;
        }
        
        h3 a {
            color: var(--text-color) !important;
            text-decoration: none;
        }
        
        small a {
            color: var(--text-color) !important;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: none;
        }
    </style>
    
    <!-- Open links in new tabs by default. Required for Streamlit sharing to not open links within the iframe. -->
    <base target='_blank'>
    ''',
    unsafe_allow_html=True,
)

def main():
    config()
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['pagina'] == 'Login':
        pagina_login()

        st.write('Ainda não tem uma conta?')
        if st.button('Cadastre-se'):
            st.session_state['pagina'] = 'Cadastro'
            st.rerun()

    elif st.session_state['pagina'] == 'Cadastro':
        pagina_cadastro()
        if st.button('Voltar'):
            st.session_state['pagina'] = 'Login'
            st.rerun()

    elif st.session_state['pagina'] == 'Dashboard' and st.session_state['logged_in']:
        pagina_dashboard()  

if __name__ == '__main__':
    main()
