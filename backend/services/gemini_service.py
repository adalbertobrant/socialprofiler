import os
import google.generativeai as genai

# Configura a API Key a partir das variáveis de ambiente
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') # Modelo atualizado e eficiente
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")
    print(f"{e}\n")
    model = None

def get_analysis_prompt(history_data: str) -> str:
    """
    Monta o prompt detalhado para a análise do histórico de navegação.
    """
    # Prompt atualizado para informar a IA sobre o formato dos dados
    prompt = f"""
    **Análise de Comportamento Digital - Perfil Psicológico e de Produtividade**

    **Contexto:** Você é um analista de comportamento digital e psicólogo organizacional. Sua tarefa é analisar o histórico de navegação a seguir, que pertence a um usuário anônimo. Com base nos dados, você deve criar um relatório detalhado e estruturado em Markdown.

    **Atenção:** Os dados a seguir foram pré-processados e agregados. Cada linha representa o total de visitas para um **domínio específico em um único dia**.
    - A coluna `URL` mostra o domínio principal (ex: `https://www.youtube.com`).
    - A coluna `Date` mostra o dia em que as visitas ocorreram.
    - A coluna `Visit Count` representa o **total de visitas para aquele domínio naquele dia**.
    Sua análise deve levar em conta essa estrutura de dados resumida para inferir os padrões de uso.

    **Dados do Histórico de Navegação (Resumido por Dia):**
    ```
    {history_data}
    ```

    **Estrutura do Relatório Solicitado:**

    **1. Principais Interesses:**
       - **Pessoais:** Identifique hobbies, curiosidades e tópicos de lazer (ex: youtube.com, netflix.com, x.com).
       - **Profissionais:** Identifique áreas de estudo, tecnologias, ferramentas e assuntos relacionados ao trabalho (ex: github.com, stackoverflow.com, documentações).

    **2. Perfil Psicológico (Inferido):**
       - **Traços de Personalidade:** Com base no padrão de busca e sites visitados, infira possíveis traços (ex: curiosidade, pragmatismo, criatividade, disciplina).
       - **Preferências Cognitivas/Emocionais:** O usuário parece ser mais analítico ou intuitivo? Busca soluções rápidas ou aprofundamento teórico? Há sinais de busca por bem-estar, entretenimento para alívio de estresse?

    **3. Padrão de Comportamento Digital:**
       - **Picos de Atividade Diária:** Analise os dias com maior `Visit Count` para entender os dias mais ativos.
       - **Foco vs. Dispersão:** Analise a variedade de domínios visitados em um mesmo dia. O usuário se concentra em poucos sites ou navega por muitos domínios diferentes diariamente?
       - **Sinais de Procrastinação:** Identifique dias com alta contagem de visitas tanto em sites de produtividade quanto em sites de lazer/redes sociais.

    **4. Fontes de Informação e Estilo de Consumo:**
       - **Fontes Favoritas:** Quais são os principais domínios (blogs, fóruns, documentação, portais de notícia) que o usuário mais acessa, considerando a soma das `Visit Count` ao longo dos dias?
       - **Estilo:** Baseado nos domínios, o usuário prefere vídeos (YouTube), textos longos (artigos, blogs), ou respostas rápidas (fóruns)?

    **5. Perfil de Aprendizagem e Raciocínio:**
       - Como o usuário parece aprender e resolver problemas? Ele busca tutoriais, documentação oficial, exemplos práticos, ou discussões teóricas?

    **6. Riscos e Potencialidades:**
       - **Riscos:** Identifique potenciais riscos como sobrecarga de informação, tendência à distração, ou fontes de informação pouco confiáveis.
       - **Potencialidades:** Identifique pontos fortes como autoaprendizagem, busca por melhores práticas, interesse em desenvolvimento contínuo.

    **7. Dossiê Psicológico (Resumo):**
       - Crie um parágrafo que resume o perfil do usuário, como um "dossiê" conciso.

    **8. Recomendações Acionáveis:**
       - **Para o Usuário (Foco em Performance e Bem-Estar):**
         - Dicas para melhorar a produtividade no trabalho.
         - Sugestões de hábitos digitais mais saudáveis.
         - Recomendações de postura e ergonomia (de forma genérica).
       - **Para um Observador/RH (Foco em Melhoria do Ambiente):**
         - Insights genéricos (sem identificar o usuário) sobre como o ambiente de trabalho poderia apoiar melhor os funcionários (ex: "Oferecer acesso a plataformas de cursos", "Promover pausas ativas").

    **Formato da Saída:** Use estritamente Markdown para formatação, com títulos, listas e negrito para clareza.
    """
    return prompt

def generate_analysis(history_data: str) -> str:
    """
    Envia o prompt para a API Gemini e retorna a análise.
    """
    if not model:
        return "Erro: A API do Google Gemini não foi configurada corretamente. Verifique a chave da API."

    prompt = get_analysis_prompt(history_data)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ocorreu um erro ao gerar a análise: {e}"
