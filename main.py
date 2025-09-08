# -*- coding: utf-8 -*-

# ---
# Projeto: Analisador Rápido de CSV (CSV Quick Profiler)
# Descrição: Uma ferramenta de linha de comando que lê um arquivo CSV e gera um
#            perfil básico dos dados, incluindo contagem de linhas, tipos de dados
#            inferidos para cada coluna, contagem de valores únicos e os valores
#            mais comuns.
# Bibliotecas necessárias: Nenhuma. Utiliza apenas módulos padrão do Python.
# Como executar: python main.py <caminho_para_o_arquivo.csv>
# Exemplo: python main.py dados_de_vendas.csv
# ---

import sys
import csv
import os
from collections import Counter

def inferir_tipo_dado(valor: str) -> str:
    """Tenta inferir o tipo de dado de uma string (int, float ou string)."""
    if not valor:
        return "vazio"
    # Tenta converter para int
    try:
        int(valor)
        return "int"
    except ValueError:
        pass
    # Tenta converter para float
    try:
        float(valor)
        return "float"
    except ValueError:
        pass
    # Se falhar, é uma string
    return "string"

def analisar_csv(caminho_arquivo: str):
    """Lê e analisa o conteúdo de um arquivo CSV, gerando um perfil dos dados."""
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            
            try:
                cabecalho = next(leitor)
                num_colunas = len(cabecalho)
            except StopIteration:
                print(f"Erro: O arquivo CSV '{caminho_arquivo}' está vazio ou não possui cabeçalho.")
                return

            # Inicializa estruturas para armazenar a análise
            dados_colunas = {col: [] for col in cabecalho}
            contagem_linhas = 0

            # Processa cada linha do CSV
            for linha in leitor:
                contagem_linhas += 1
                if len(linha) != num_colunas:
                    # Lida com linhas malformadas pulando-as
                    continue
                for i, valor in enumerate(linha):
                    dados_colunas[cabecalho[i]].append(valor.strip())
            
            # Gera o relatório final
            imprimir_relatorio(caminho_arquivo, contagem_linhas, cabecalho, dados_colunas)

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{caminho_arquivo}'")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def imprimir_relatorio(nome_arquivo: str, total_linhas: int, cabecalho: list, dados: dict):
    """Formata e imprime o relatório de análise do CSV no console."""
    print("=" * 60)
    print(f"  Análise do Arquivo: '{os.path.basename(nome_arquivo)}'")
    print("=" * 60)
    print(f"\nResumo Geral:")
    print(f"  - Total de Linhas de Dados: {total_linhas}")
    print(f"  - Total de Colunas: {len(cabecalho)}")

    print("\nAnálise por Coluna:")
    for coluna in cabecalho:
        print("-" * 50)
        print(f"  Coluna: '{coluna}'")
        print("-" * 50)
        
        valores_coluna = dados[coluna]
        valores_nao_vazios = [v for v in valores_coluna if v]
        
        if not valores_nao_vazios:
            print("  -> Todos os valores nesta coluna estão vazios.")
            continue

        # Estatísticas básicas
        total_valores = len(valores_coluna)
        valores_vazios = total_valores - len(valores_nao_vazios)
        contagem_unicos = len(set(valores_nao_vazios))
        
        print(f"  - Contagem de Valores Não Vazios: {len(valores_nao_vazios)} de {total_valores}")
        print(f"  - Contagem de Valores Vazios: {valores_vazios}")
        print(f"  - Contagem de Valores Únicos: {contagem_unicos}")

        # Inferência de Tipo de Dado
        tipos_inferidos = Counter(inferir_tipo_dado(v) for v in valores_nao_vazios)
        tipo_predominante = tipos_inferidos.most_common(1)[0][0]
        print(f"  - Tipo de Dado Predominante: {tipo_predominante.upper()}")

        # Valores mais comuns
        contagem_valores = Counter(valores_nao_vazios)
        print("  - 5 Valores Mais Comuns:")
        for valor, contagem in contagem_valores.most_common(5):
            percentual = (contagem / len(valores_nao_vazios)) * 100
            print(f'    - "{valor}" (aparece {contagem} vezes, ~{percentual:.1f}%)')
        print("")

    print("=" * 60)
    print("  Análise Concluída")
    print("=" * 60)


if __name__ == "__main__":
    # Verifica se o caminho do arquivo foi fornecido como argumento
    if len(sys.argv) != 2:
        print("Uso: python main.py <caminho_para_o_arquivo.csv>")
        sys.exit(1) # Código de erro para uso incorreto

    caminho_do_arquivo = sys.argv[1]

    # Verifica se a extensão do arquivo é .csv
    if not caminho_do_arquivo.lower().endswith('.csv'):
        print("Erro: O arquivo fornecido não parece ser um arquivo CSV.")
        sys.exit(1)

    analisar_csv(caminho_do_arquivo)
