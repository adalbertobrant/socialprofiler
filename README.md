# 🧠 Analisador de Hábitos Digitais com IA

Uma aplicação web para analisar o histórico de navegação do usuário, combinando uma análise de perfil comportamental (DISC) com insights detalhados gerados pela IA do Google Gemini.

## Funcionalidades

-   **Análise Dupla:** Oferece duas perspectivas sobre os seus hábitos:
    1.  **Perfil Comportamental (DISC):** Uma análise instantânea e local que gera um gráfico de radar (Dominância, Influência, eStabilidade, Consciência) com base nos sites visitados.
    2.  **Análise Detalhada por IA:** Envia um resumo anonimizado do seu histórico para a API do Google Gemini, que gera um relatório completo sobre seus interesses, padrões, riscos e potencialidades.
-   **Privacidade em Primeiro Lugar:** O histórico bruto é processado no backend para criar um resumo diário. Apenas este resumo, sem URLs específicas, é enviado para a IA, protegendo sua privacidade.
-   **Interface Interativa:** Frontend construído com Streamlit, permitindo o upload fácil do arquivo de histórico (`.csv`) e exibição clara dos resultados.
-   **Arquitetura Robusta:** Utiliza um backend FastAPI para lidar com a lógica de negócio e a comunicação com a API externa, garantindo que o frontend permaneça leve e responsivo.

## Arquitetura do Projeto

Este projeto utiliza uma arquitetura cliente-servidor para separar as responsabilidades:

-   **Frontend (Streamlit - `app.py`):** Responsável pela interface do usuário, upload de arquivos e pela análise DISC local e instantânea.
-   **Backend (FastAPI - `main.py`):** Um servidor de API que recebe o histórico bruto, o resume para anonimização e eficiência, e se comunica com a API do Google Gemini para a análise aprofundada.

**Fluxo de Dados:**
`Usuário (Frontend) -> Envia CSV -> Backend (FastAPI) -> Resume Dados -> Envia Resumo -> Google Gemini API -> Retorna Análise -> Backend -> Frontend -> Exibe para Usuário`

## Tecnologias Utilizadas

-   **Backend:** Python, FastAPI, Uvicorn, Google Generative AI, Pandas.
-   **Frontend:** Python, Streamlit, Requests, Plotly, Pandas.
-   **IA:** Google Gemini 1.5 Flash.

---

## 🚀 Configuração e Execução

Siga estes passos para configurar e rodar o projeto localmente.

### Pré-requisitos

-   Python 3.12.3 ou superior instalado.
-   `git` instalado para clonar o repositório.

### Passo 1: Clone o Repositório

Abra seu terminal e clone o projeto para sua máquina local.

```bash
git clone https://SUA_URL_DE_REPOSITORIO_AQUI
cd nome-do-repositorio
```

##  Crie e Ative um Ambiente Virtual

### No Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### No macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## Instale as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias com um único comando:

```bash
pip install -r requirements.txt
```

## Configure a Chave da API do Google Gemini

A API do Gemini é essencial para a análise de IA.

 1- Obtenha sua API Key: Acesse o Google AI Studio e crie sua chave de API gratuita.
 2- Crie o arquivo .env: Na raiz do seu projeto (na mesma pasta de main.py), crie um arquivo chamado .env.
 3- Adicione a chave ao arquivo: Abra o arquivo .env e adicione a seguinte linha, substituindo sua_chave_de_api_aqui pela chave que você gerou:

```bash
GOOGLE_API_KEY="sua_chave_de_api_aqui"
```
## Execute a Aplicação

Você precisará de dois terminais separados (ou duas abas no seu terminal) para rodar o backend e o frontend simultaneamente.
No Terminal 1 (Backend):
Navegue até a pasta do projeto, ative o ambiente virtual e inicie o servidor FastAPI.

```bash
uvicorn main:app --reload
```
No Terminal 2 (Frontend):
Abra um novo terminal, navegue até a mesma pasta do projeto e ative o mesmo ambiente virtual.

```bash
streamlit run app.py
```
O Streamlit abrirá automaticamente uma nova aba no seu navegador. Se não abrir, acesse o endereço fornecido (geralmente http://localhost:8501).
Agora você está pronto! Faça o upload do seu arquivo browser_history.csv na interface do Streamlit e clique em "Analisar Histórico".

## Como Obter seu Histórico de Navegação

Google Chrome:

Vá para chrome://history.

Procure por uma extensão na Chrome Web Store chamada "Export History" ou similar que exporte em formato CSV com as colunas URL, Last Visited, Visit Count.

Firefox:

Use um complemento como o "Export History/Bookmarks to JSON/CSV/XLS".

Certifique-se de que o CSV exportado tenha as colunas URL, Last Visited, e Visit Count.
