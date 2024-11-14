import pandas as pd
import pipefy_api as pipe

# Carrega o arquivo Excel (substitua 'seu_arquivo.xlsx' pelo caminho do seu arquivo)
df = pd.read_excel('arquivo.xlsx')

# Converte o DataFrame para um dicionário
dados_dict = df.to_dict(orient='records')

# Exibe o dicionário
#print(dados_dict)

print(pipe.create_table_record(305481920, dados_dict))
