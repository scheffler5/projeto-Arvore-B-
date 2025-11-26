from Tabelas.bplustree import BPlusTree


#Controller do Banco
class CommandProcessor:
    #Inicializador
    def __init__(self, t_param, page_size_param):
        self.active_tables = {}
        self.default_t = t_param
        self.default_page_size = page_size_param
    #Cria a Tabela, aciona o Arquivo bplusstree e criar o arquivo .db
    def create_table(self, name, columns):
        print(f"[PROCESSOR] Criando tabela '{name}'...")
        new_tree = BPlusTree(name, self.default_t, self.default_page_size, columns)
        self.active_tables[name] = new_tree
        
        print(f" Tabela '{name}' criada com sucesso!")

    #Insere dados na tabela
    def insert_data(self, table_name, values_list):
        if table_name not in self.active_tables:
            print(f" Erro: Tabela '{table_name}' não encontrada.")
            return

        tree = self.active_tables[table_name]
        
        # Validação simples do tamanho de insert e colunas
        if len(values_list) != len(tree.columns):
            print(f" Erro: Tabela tem {len(tree.columns)} colunas, mas você enviou {len(values_list)} valores.")
            return

        # Monta o dicionário {coluna: valor}
        data_to_insert = {}
        
        for i, (col_name, col_type, is_pk) in enumerate(tree.columns):
            raw_val = values_list[i]
            
            # Tratamento de NULL/AUTO para PK
            if is_pk and (raw_val.upper() in ["NULL", "AUTO"]):
                data_to_insert[col_name] = None
            else:
                data_to_insert[col_name] = raw_val

        # Chama a árvore para inserir
        tree.insert(data_to_insert)
    def execute_select(self, table_name, field, value):
        print(f"[PROCESSOR] Buscando em '{table_name}' onde {field} = {value}...")
        
        if table_name not in self.active_tables:
            print(f" Erro: Tabela '{table_name}' não carregada.")
            return

        tree = self.active_tables[table_name]
        
        # Verifica se a busca é pela Chave Primária (PK)
        pk_name = tree.columns[0][0]
        
        if field == pk_name:
            # Se for busca por PK, usamos o algoritmo rápido da Árvore B+
            result = tree.search(value) # Manda buscar na árvore
            
            if result:
                print(f" Registro Encontrado: {result}")
            else:
                print("  Registro não encontrado.")
        else:
            print(" Use a PK!")