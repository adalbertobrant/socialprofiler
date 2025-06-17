import pandas as pd
from urllib.parse import urlparse
import io

def get_hostname(url: str) -> str:
    """
    Extrai o nome do host (domínio) de uma URL.
    """
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme == 'file':
            return 'local_files'
        if parsed_url.netloc:
            return parsed_url.netloc
        return 'invalid_or_other'
    except Exception:
        return 'invalid_or_other'

def summarize_history_data(csv_content: str) -> str:
    """
    Recebe o conteúdo de um CSV de histórico como string,
    agrega os dados por domínio e data, e retorna um novo CSV como string.
    Esta versão é robusta contra vírgulas nas URLs.
    """
    if not csv_content:
        return ""

    try:
        lines = csv_content.strip().split('\n')
        if len(lines) < 2:
            return "" # Retorna vazio se não houver dados

        # Processamento manual para evitar erros de tokenização com pandas
        data_rows = []
        for i, line in enumerate(lines[1:], 1): # Pula o cabeçalho
            parts = line.rsplit(',', 2)
            if len(parts) == 3:
                data_rows.append(parts)
            else:
                print(f"Aviso no backend: Linha {i+1} ignorada por formato inesperado.")
        
        if not data_rows:
            return ""

        # Cria o DataFrame a partir dos dados limpos
        df = pd.DataFrame(data_rows, columns=['URL', 'Last Visited', 'Visit Count'])
        df['Visit Count'] = pd.to_numeric(df['Visit Count'], errors='coerce').fillna(0).astype(int)

        # Continua com a lógica de sumarização
        df['Domain'] = df['URL'].apply(get_hostname)
        df['Last Visited'] = pd.to_datetime(df['Last Visited'])
        df['Visit_Date'] = df['Last Visited'].dt.date

        aggregated_data = df.groupby(['Domain', 'Visit_Date']).agg(
            Daily_Visit_Count=('Visit Count', 'sum')
        ).reset_index()

        aggregated_data['URL'] = aggregated_data['Domain'].apply(
            lambda domain: f"https://{domain}" if domain != 'local_files' else 'local_files'
        )
        
        summary_df = aggregated_data[['URL', 'Visit_Date', 'Daily_Visit_Count']]
        summary_df = summary_df.rename(columns={
            'Visit_Date': 'Date',
            'Daily_Visit_Count': 'Visit Count'
        })

        summary_df = summary_df.sort_values(by=['Date', 'Visit Count'], ascending=[False, False])
        
        output_buffer = io.StringIO()
        summary_df.to_csv(output_buffer, index=False)
        
        return output_buffer.getvalue()

    except Exception as e:
        print(f"Erro CRÍTICO ao processar o histórico no backend: {e}")
        # Em caso de um erro inesperado, retorna uma string vazia para não sobrecarregar a IA
        return "Erro ao processar dados do histórico."
