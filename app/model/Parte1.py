import streamlit as st

# Função para exibir um painel do Business Model Canvas com cores de fundo
def display_business_model_canvas():
    st.title('Business Model Canvas')

    # Define o estilo CSS
    st.markdown("""
        <style>
        .canvas-section {
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
            color: #fff;
            font-weight: bold;
            text-align: center;
            font-size: 16px;
            position: relative;
            overflow: hidden;
            min-height: 175px;
        }
        .canvas-section .description {
            background-color: rgba(255, 255, 255, 0.7); /* Fundo branco com transparência */
            color: #000; /* Texto preto para contraste */
            padding: 5px;
            border-radius: 5px;
            position: absolute;
            top: 40px;
            bottom: 10px;
            left: 10px;
            right: 10px;
            font-size: 14px; /* Reduz a fonte das descrições */
            min-height: 100px; /* Ajusta a altura para comportar o texto sem rolagem */
            overflow: hidden; /* Remove rolagem */
            text-align: left; /* Alinha o texto à esquerda */
            line-height: 1.2; /* Reduz o espaço entre linhas para menos espaço entre título e descrição */
        }
        .customer-segments { background-color: #1f77b4; }
        .value-proposition { background-color: #ff7f0e; }
        .channels { background-color: #2ca02c; }
        .customer-relationships { background-color: #d62728; }
        .revenue-streams { background-color: #9467bd; }
        .key-resources { background-color: #8c564b; }
        .key-activities { background-color: #e377c2; }
        .key-partners { background-color: #7f7f7f; }
        .cost-structure { background-color: #bcbd22; }
        </style>
    """, unsafe_allow_html=True)

    # Layout para o Business Model Canvas com cores de fundo e texto dentro das seções coloridas
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        st.markdown('''
            <div class="canvas-section customer-segments">
                Segmentos de Clientes
                <div class="description">
                    - Pessoas físicas (pequeno investidor) que buscam ações com desempenho histórico acima da inflação, ou seja, ações de empresas mais consolidadas e estáveis.<br>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
            <div class="canvas-section value-proposition">
                Proposta de Valor
                <div class="description">
                    ODS: Trabalho decente e Crescimento Econômico<br>
                    - Insights sobre ações em relação à inflação e ao dólar.<br>
                    - Identificar ações com valorização acima da inflação e/ou acima da variação cambial.
                </div>
            </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown('''
            <div class="canvas-section channels">
                Canais
                <div class="description">
                    - Dashboard streamlit para visualização das ações e demais dados.<br>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    with col4:
        st.markdown('''
            <div class="canvas-section customer-relationships">
                Relacionamento com Clientes
                <div class="description">
                    - Sugestões e feedbacks via e e-mail.<br>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    col5, col6 = st.columns([1, 1])

    with col5:
        st.markdown('''
            <div class="canvas-section revenue-streams">
                Fontes de Receita
                <div class="description">
                    - Para esse projeto, a receita será proveniente de propagandas no dashboard.<br>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    with col6:
        st.markdown('''
            <div class="canvas-section key-resources">
                Recursos Principais
                <div class="description">
                    - Computadores/servidores para coleta e processamento de dados.<br>
                    - Dados financeiros e econômicos de fontes públicas;
                    IBGE, Yahoo Finance, Banco Central, IPEA, B3<br>
                    - StreamCloud<br>
                    - MongoDB<br>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    col7, col8 = st.columns([1, 1])

    with col7:
        st.markdown('''
            <div class="canvas-section key-activities">
                Atividades-Chave
                <div class="description">
                    - Coleta e atualização de dados<br>
                    - Desenvolvimento e manutenção do dashboard.<br>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    with col8:
        st.markdown('''
            <div class="canvas-section key-partners">
                Parcerias Principais
                <div class="description">
                    - Provedores de dados financeiros.<br>
                    - Streamlit Comunity<br>
                    - MongoDB Atlas<br>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('''
        <div class="canvas-section cost-structure">
            Estrutura de Custos
            <div class="description">
                - O projeto utilizará recursos gratuitos e open-source, portanto, não haverá custos diretos.<br>
            </div>
        </div>
    ''', unsafe_allow_html=True)

display_business_model_canvas()
