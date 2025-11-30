import sys
import os
import random

# Adiciona o diretório pai ao caminho do Python
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Tabelas.bplustree import BPlusTree
from Analise.funcoes.metricas import PerformanceTracker
from Analise.funcoes.gerador import gerar_registro
from Analise.funcoes.auditor import auditar_arvore

def main():
    print("=== FERRAMENTA DE ANÁLISE DE DESEMPENHO B+ TREE ===")
    
    # Coleta de Parâmetros
    try:
        t = int(input("Grau mínimo t: "))
        pg_size = int(input("Tamanho da Página (bytes): "))
        qtd_tabelas = int(input("Qtd de Tabelas a criar: "))
        qtd_colunas = int(input("Qtd de Colunas por tabela (incluindo ID): "))
        qtd_inserts = int(input("Qtd de Inserts por tabela: "))
        qtd_selects = int(input("Qtd de Consultas (SELECTs) a realizar: "))
    except ValueError:
        print("Erro: Digite apenas números inteiros.")
        return

    tracker = PerformanceTracker()
    
    # Lista para guardar referências das árvores criadas
    tabelas_criadas = []

    # Criação e Insert
    print(f"\n[INICIANDO] Criando {qtd_tabelas} tabelas e inserindo {qtd_inserts} registros em cada...")
    
    for i in range(qtd_tabelas):
        nome_tabela = f"bench_tab_{i}"
        
        # Define as colunas dinamicamente para passar para a BPlusTree
        cols_schema = [('id', 'int', True)] # PK Fixa
        for c in range(1, qtd_colunas):
            cols_schema.append((f"col_{c}", 'str', False))

        # Mede Tempo de Criação
        tracker.start()
        tree = BPlusTree(nome_tabela, t, pg_size, cols_schema)
        tracker.stop('CREATE_TABLE')
        
        tabelas_criadas.append(tree)

        # Loop de Inserts
        print(f"  > Povoando {nome_tabela}...", end='\r')
        for _ in range(qtd_inserts):
            dados = gerar_registro(qtd_colunas)
            
            tracker.start()
            tree.insert(dados)
            tracker.stop('INSERT')
    
    print("\n Povoamento concluído.")

    # Consulta
    print(f"\n[INICIANDO] Realizando {qtd_selects} consultas aleatórias...")
    
    ids_possiveis = list(range(1, qtd_inserts + 1))
    
    for _ in range(qtd_selects):
        # Escolhe uma tabela aleatória e um ID aleatório
        tree_alvo = random.choice(tabelas_criadas)
        id_busca = random.choice(ids_possiveis)
        
        tracker.start()
        res = tree_alvo.search(id_busca)
        tracker.stop('SELECT_PK')

    # Relatorio e benchmark
    tracker.print_report()
    
    print("=== ANÁLISE ESTRUTURAL DAS ÁRVORES ===")
    for tree in tabelas_criadas:
        print(f"Auditando estrutura de '{tree.filename}'...")
        stats = auditar_arvore(tree)
        
        print(f"  > Altura da Árvore: {stats['height']}")
        print(f"  > Total de Nós (Páginas): {stats['total_nodes']}")
        print(f"  > Total de Folhas (Dados): {stats['total_leaves']}")
        print(f"  > Total I/O Disco: {tree.disk.get_stats()}")
        print("-" * 30)

if __name__ == "__main__":
    main()