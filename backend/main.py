from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Importa os serviços
from services import gemini_service
from services import history_service 

app = FastAPI(
    title="Analisador de Hábitos Digitais API",
    description="Uma API para analisar históricos de navegação usando Google Gemini.",
    version="1.0.0"
)

# Modelo de dados para o corpo da requisição
class HistoryPayload(BaseModel):
    content: str
    filename: str

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API do Analisador de Hábitos Digitais"}

@app.post("/analyze", tags=["Analysis"])
async def analyze_history(payload: HistoryPayload):
    """
    Recebe o conteúdo de um histórico de navegação, resume-o e retorna a análise da IA.
    """
    if not payload.content:
        raise HTTPException(status_code=400, detail="O conteúdo do histórico não pode estar vazio.")

    try:
        # Limita o tamanho do conteúdo para evitar custos excessivos e sobrecarga
        # O limite do Gemini 1.5 Flash é grande, mas é bom ter uma salvaguarda.
        # 2000kb é um bom começo.
        if len(payload.content) > 2000 * 1024:
             raise HTTPException(status_code=413, detail="Arquivo muito grande. O limite é de 2000KB.")

        print(f"Recebida análise para o arquivo: {payload.filename}")

        # 1. Resumir o histórico de navegação
        print("Resumindo o histórico de navegação...")
        summarized_content = history_service.summarize_history_data(payload.content)
        lines_count = len(summarized_content.strip().split('\n'))
        print(f"Histórico resumido com {lines_count} linhas.")

        # 2. Enviar o conteúdo resumido para a análise da IA
        print("Enviando para análise da IA...")
        analysis_result = gemini_service.generate_analysis(summarized_content)
        print("Análise gerada com sucesso.")

        return {"filename": payload.filename, "analysis": analysis_result}
    except Exception as e:
        # Adiciona um print do erro no console para facilitar o debug
        print(f"Erro no servidor: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro inesperado no servidor: {e}")
