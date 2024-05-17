import streamlit as st
from pages.cadastro import pagina_cadastro
from pages.login import pagina_login
from pages.dashboard import dashboard

st.set_page_config(page_title="Diabetes App", page_icon="🩸", initial_sidebar_state="collapsed")

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Login"

def config():
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)

def main():
    config()
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["pagina"] == "Login":
        pagina_login()

        st.write("Ainda não tem uma conta?")
        if st.button("Cadastre-se"):
            st.session_state["pagina"] = "Cadastro"
            st.rerun()

    elif st.session_state["pagina"] == "Cadastro":
        pagina_cadastro()
        if st.button("Voltar"):
            st.session_state["pagina"] = "Login"
            st.rerun()

    elif st.session_state["pagina"] == "Dashboard" and st.session_state["logged_in"]:
        dashboard()

    elif st.session_state["pagina"] == "Registro Medicação" and st.session_state["logged_in"]:
        # pagina_registro_medicao()
        pass

if __name__ == "__main__":
    main()
