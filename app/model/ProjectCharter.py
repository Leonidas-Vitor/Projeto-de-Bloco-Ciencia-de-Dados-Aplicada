import streamlit as st

def display_project_charter():
    st.title('Project Charter')

    # Objetivo do Projeto
    st.subheader('Objetivo do Projeto')
    st.markdown('''
    Desenvolver um dashboard que utilize dados públicos de fontes como Yahoo Finance, Banco Central, IBGE e IPEA
    para fornecer insights sobre a relação entre o desempenho de ações, a inflação e o valor do dólar. O objetivo é
    identificar ações que performam acima da inflação e/ou acompanham a alta do dólar, permitindo que investidores 
    escolham ativos que históricamente performaram bem em relação a essas duas métricas.
    ''')

    # Justificativa
    st.subheader('Justificativa')
    st.markdown('''
    O mercado financeiro é altamente volátil e a inflação, juntamente com a flutuação cambial, tem um impacto
    significativo no valor dos ativos. Este projeto visa fornecer uma ferramenta para ajudar investidores e analistas
    a tomar decisões mais informadas, cruzando o comportamento das ações com dados macroeconômicos.
    ''')

    # Escopo do Projeto
    st.subheader('Escopo do Projeto')
    st.markdown('''
    O escopo deste projeto inclui:
    - Coleta de dados públicos de várias fontes, como Yahoo Finance, Banco Central, IBGE e IPEA.
    - Desenvolvimento de um dashboard interativo para visualização desses dados.
    - Implementação de funcionalidades para comparar o desempenho das ações com a inflação e a flutuação cambial.
    - Integração de funcionalidades que permitam analisar tendências e prever comportamentos futuros.
    ''')

    # Principais Stakeholders
    st.subheader('Principais Stakeholders')
    st.markdown('''
    - **Investidores de pequeno porte**: Utilizarão o dashboard para identificar ações que oferecem melhor proteção contra a inflação ou
    aproveitam movimentos de alta do dólar.
    ''')

    # Metas de Sucesso
    st.subheader('Metas de Sucesso')
    st.markdown('''
    - Desenvolvimento e lançamento do dashboard dentro do prazo do projeto de bloco.
    - Revelar ao menos 5 ações que performaram acima da inflação e/ou da variação cambial nos últimos 12 meses.
    ''')

    # Cronograma de Alta Nível
    st.subheader('Cronograma de Alto Nível')
    st.markdown('''
    - **Fase de Planejamento**: 2 semanas
    - **Coleta e Integração de Dados**: 2 semanas
    - **Desenvolvimento do Dashboard**: 2 semanas
    - **Testes e Ajustes Finais**: 1 semana
    ''')

    # Orçamento Estimado
    st.subheader('Orçamento Estimado')
    st.markdown('''
    - O projeto será desenvolvido utilizando recursos gratuitos e open-source, portanto, não haverá custos diretos.
    ''')

    # Riscos e Mitigações
    st.subheader('Riscos e Mitigações')
    st.markdown('''
    - **Disponibilidade de dados**: Mitigação: Utilizar múltiplas fontes de dados, como datasets do kaggle.
    - **Limite de armazenamento de dados**: Mitigação: Resumir dados históricos em intervalos menores para economizar espaço.
    ''')

    # Equipe do Projeto
    st.subheader('Equipe do Projeto')
    st.markdown('''
    - **Leônidas Almeida**: Ciência de Dados
    ''')

display_project_charter()


