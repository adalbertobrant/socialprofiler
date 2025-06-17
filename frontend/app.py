import streamlit as st
import requests
import pandas as pd
import io
from urllib.parse import urlparse
import plotly.graph_objects as go

# --- Configuração ---
BACKEND_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="Analisador de Hábitos Digitais com IA",
    page_icon="🧠",
    layout="wide"
)

# --- Dicionário de Palavras-chave para Análise DISC ---
DISC_KEYWORDS = {
    'Dominance (D)': [
        'investing.com', 'tradingview.com', 'bloomberg.com', 'wsj.com', 'forbes.com', 
        'businessinsider.com', 'cnbc.com', 'reuters.com', 'marketwatch.com', 'financial',
        'stocks', 'crypto', 'leadership', 'management', 'strategy', 'competition'
    ],
    'Influence (I)': [
        'instagram.com', 'x.com', 'facebook.com', 'tiktok.com', 'linkedin.com', 
        'social', 'marketing', 'networking', 'influencer', 'fashion', 'entertainment',
        'celebrity', 'events', 'community', 'trends'
    ],
    'Steadiness (S)': [
        'pinterest.com', 'web.whatsapp.com', 'telegram.org', 'allrecipes.com', 'cooking',
        'gardening', 'family', 'home', 'well-being', 'meditation', 'community',
        'support', 'routine', 'planning', 'stability'
    ],
    'Conscientiousness (C)': [
        'github.com', 'stackoverflow.com', 'scholar.google.com', 'arxiv.org', 'pypi.org', 
        'docs.python.org', 'medium.com', 'wikipedia.org', 'research', 'analysis', 'data',
        'science', 'programming', 'tutorial', 'documentation', 'learning', 'how-to'
    ]
}

# --- Funções de Análise e Visualização DISC ---

def analyze_disc_from_history(csv_content: str):
    """
    Analisa o conteúdo do CSV para gerar scores DISC baseados em palavras-chave.
    Esta função foi reescrita para ser mais robusta contra vírgulas nas URLs.
    """
    try:
        lines = csv_content.strip().split('\n')
        if len(lines) < 2:
            st.warning("Arquivo CSV vazio ou sem dados.")
            return None

        # Pega o cabeçalho
        header = lines[0].strip().split(',')
        if header != ['URL', 'Last Visited', 'Visit Count']:
             st.warning("O formato do cabeçalho do CSV parece incorreto. A análise DISC pode falhar.")

        data_rows = []
        for i, line in enumerate(lines[1:], 1):
            # rsplit(',', 2) divide a string a partir da direita, no máximo 2 vezes.
            # Isso isola corretamente a data e a contagem, deixando o resto (a URL) junto.
            parts = line.rsplit(',', 2)
            if len(parts) == 3:
                data_rows.append(parts)
            else:
                # Informa sobre uma linha malformada, mas continua o processo
                print(f"Aviso: Linha {i+1} ignorada por ter um formato inesperado: {line[:100]}...")

        if not data_rows:
            st.warning("Nenhuma linha de dados válida encontrada no CSV.")
            return None

        df = pd.DataFrame(data_rows, columns=['URL', 'Last Visited', 'Visit Count'])
        
        # Converte a contagem para numérico, tratando possíveis erros
        df['Visit Count'] = pd.to_numeric(df['Visit Count'], errors='coerce').fillna(0).astype(int)

        scores = {'Dominance (D)': 0, 'Influence (I)': 0, 'Steadiness (S)': 0, 'Conscientiousness (C)': 0}
        
        for index, row in df.iterrows():
            url = str(row['URL']).lower()
            count = row['Visit Count']
            
            for profile, keywords in DISC_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in url:
                        scores[profile] += count
                        break # Evita contar a mesma URL múltiplas vezes para o mesmo perfil

        total_score = sum(scores.values())
        if total_score == 0:
            st.info("Nenhuma palavra-chave para a análise DISC foi encontrada no seu histórico.")
            return None

        normalized_scores = {k: (v / total_score) * 100 for k, v in scores.items()}
        return normalized_scores
        
    except Exception as e:
        st.warning(f"Não foi possível gerar a análise DISC: {e}")
        return None


def create_disc_radar_chart(scores: dict):
    """
    Cria um gráfico de radar Plotly a partir dos scores DISC.
    """
    if not scores or sum(scores.values()) == 0:
        return None
        
    categories = list(scores.keys())
    values = list(scores.values())

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Perfil DISC Inferido'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.1] if any(v > 0 for v in values) else 100
            )),
        showlegend=False,
        title='Perfil Comportamental (DISC)',
        template='plotly_dark'
    )
    return fig

def get_disc_interpretation(profile: str):
    """Retorna uma breve descrição de cada perfil DISC."""
    interpretations = {
        'Dominance (D)': "**Dominância (D):** Foco em resultados, ação e competição. Pessoas com alta pontuação aqui tendem a ser diretas, assertivas e buscam controle sobre o ambiente. Podem ser vistas em sites de notícias financeiras, negócios e ferramentas de produtividade.",
        'Influence (I)': "**Influência (I):** Foco em interação social, persuasão e otimismo. Alta pontuação sugere uma pessoa extrovertida, que valoriza o reconhecimento e a colaboração. Frequentemente encontrada em redes sociais, sites de marketing e tendências.",
        'Steadiness (S)': "**Estabilidade (S):** Foco em cooperação, consistência e apoio. Pessoas com essa característica valorizam a segurança e relacionamentos estáveis. O histórico pode mostrar uso de apps de mensagens, fóruns comunitários e sites de hobbies relaxantes.",
        'Conscientiousness (C)': "**Consciência (C):** Foco em qualidade, precisão e análise. Pessoas com alta pontuação são detalhistas, sistemáticas e buscam conhecimento. O histórico revela acesso a documentações técnicas, artigos científicos e sites de aprendizado."
    }
    return interpretations.get(profile, "")


# --- Interface Principal ---

st.title("🧠 Analisador de Hábitos Digitais com IA")
st.markdown("""
Uma aplicação para analisar seu histórico de navegação usando a API Google Gemini,
fornecendo insights comportamentais e recomendações para produtividade e bem-estar.
""")

st.info("""
**Aviso de Privacidade e Uso de Dados:**
- **Processamento seguro no servidor:** Ao fazer o upload, seu histórico é processado em nosso servidor.
- **Privacidade em primeiro lugar:** Apenas um **resumo anônimo**, contendo os sites visitados (domínios) e a contagem de visitas por dia, é enviado para a análise da IA. As URLs completas e específicas nunca saem do nosso servidor.
- **Não armazenamos seus dados:** O conteúdo do arquivo e seu resumo são usados apenas para a análise e descartados em seguida.
- **Responsabilidade do Usuário:** Revise seu histórico antes do upload se houver informações sensíveis que não queira processar.
""")

uploaded_file = st.file_uploader(
    "Carregue seu histórico de navegação (apenas formato .csv)",
    type=['csv']
)

if uploaded_file is not None:
    if st.button("Analisar Histórico", type="primary"):
        try:
            file_content = uploaded_file.getvalue().decode("utf-8")
            filename = uploaded_file.name

            # Limpar resultados antigos da sessão
            st.session_state.analysis_done = False
            st.session_state.analysis_result = None
            st.session_state.disc_chart = None
            st.session_state.disc_scores = None

            with st.spinner(f"Analisando '{filename}'... Gerando perfil DISC e consultando a IA. Isso pode levar um minuto! 🤖"):
                # --- Análise DISC Local (Frontend) ---
                disc_scores = analyze_disc_from_history(file_content)
                if disc_scores:
                    st.session_state.disc_scores = disc_scores
                    st.session_state.disc_chart = create_disc_radar_chart(disc_scores)

                # --- Análise Gemini (Backend) ---
                payload = {"content": file_content, "filename": filename}
                try:
                    response = requests.post(BACKEND_URL, json=payload, timeout=300)
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.analysis_result = result['analysis']
                    else:
                        st.session_state.analysis_result = f"**Erro ao analisar o arquivo.** O servidor respondeu com o status: {response.status_code}\n\nDetalhes: ```{response.text}```"
                
                except requests.exceptions.RequestException as e:
                    st.session_state.analysis_result = f"**Erro de conexão com o servidor de análise.** Verifique se o backend está rodando.\n\nDetalhes técnicos: ```{e}```"
                
                st.session_state.analysis_done = True
        
        except Exception as e:
            st.error(f"Ocorreu um erro ao ler ou processar o arquivo: {e}")
            st.session_state.analysis_done = False

# --- Exibição dos Resultados ---
if st.session_state.get('analysis_done', False):
    st.divider()
    
    # --- Seção da Análise DISC ---
    if st.session_state.get('disc_chart'):
        st.subheader("Análise de Perfil Comportamental (DISC)")
        st.markdown("Esta é uma análise **inferida e não-clínica** do seu comportamento digital com base nos sites que você visita.")

        col1, col2 = st.columns([1, 1.5])

        with col1:
            st.plotly_chart(st.session_state.disc_chart, use_container_width=True)

        with col2:
            scores = st.session_state.get('disc_scores', {})
            if scores:
                sorted_profiles = sorted(scores, key=scores.get, reverse=True)
                for profile in sorted_profiles:
                    st.markdown(get_disc_interpretation(profile))
                    st.progress(int(scores[profile]))

    st.divider()

    # --- Seção da Análise da IA Gemini ---
    if st.session_state.get('analysis_result'):
        st.subheader("Análise Detalhada por IA (Google Gemini)")
        st.markdown(st.session_state.analysis_result)
