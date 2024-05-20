import streamlit as st

# Título da página
st.title("Informações sobre Diabetes")

# Primeira seção: O que é e tipos
st.header("Primeiro: o que é e tipos")

# O que é a Diabetes?
st.subheader("O que é a Diabete?")
st.write("""
É uma doença causada pela produção insuficiente ou má absorção de insulina, hormônio que regula a glicose no sangue e garante energia para o organismo. 
A insulina é um hormônio que tem a função de quebrar as moléculas de glicose(açúcar) transformando-a em energia para manutenção das células do nosso organismo. 
O diabetes pode causar o aumento da glicemia e as altas taxas podem levar a complicações no coração, nas artérias, nos olhos, nos rins e nos nervos. 
Em casos mais graves, o diabetes pode levar à morte. O diabetes mellitus pode se apresentar de diversas formas e possui diversos tipos diferentes. 
Independente do tipo de diabetes, com aparecimento de qualquer sintoma é fundamental que o paciente procure com urgência o atendimento médico especializado 
para dar início ao tratamento.
""")

# Tipo 1
st.subheader("Tipo 1")
st.write("""
Sabe-se que, via de regra, é uma doença crônica não transmissível, hereditária, que concentra entre 5% e 10% do total de diabéticos no Brasil. 
Ele se manifesta mais frequentemente em adultos, mas crianças também podem apresentar. O diabetes tipo 1 aparece geralmente na infância ou adolescência, 
mas pode ser diagnosticado em adultos também. Pessoas com parentes próximos que têm ou tiveram a doença devem fazer exames regularmente para acompanhar 
a glicose no sangue.

O tratamento exige o uso diário de insulina e/ou outros medicamentos para controlar a glicose no sangue. A causa do diabetes tipo 1 ainda é desconhecida 
e a melhor forma de preveni-la é com práticas de vida saudáveis (alimentação, atividades físicas e evitando álcool, tabaco e outras drogas).
""")

# Tipo 2
st.subheader("Tipo 2")
st.write("""
O diabetes tipo 2 ocorre quando o corpo não aproveita adequadamente a insulina produzida. A causa do diabetes tipo 2 está diretamente relacionado ao 
sobrepeso, sedentarismo, triglicerídeos elevados, hipertensão e hábitos alimentares inadequados.

Por isso, é essencial manter acompanhamento médico para tratar, também, dessas outras doenças, que podem aparecer junto com o diabetes. 
Cerca de 90% dos pacientes diabéticos no Brasil têm esse tipo.
""")

# Rodapé ou mensagem final (opcional)
st.write("_Para mais informações, procure um profissional de saúde._")