import re
from .processor import CommandProcessor

# Interpretador de comandos SQL criados pelo usuario
# Usa Expressões Regulares Regex para entender a intenção
class Interpreter:
    def __init__(self, t, page_size):
        # E repassa para o Processor
        self.processor = CommandProcessor(t, page_size)

    def parse_and_execute(self, query):
        query = query.strip()
        
        # Regex: CREATE TABLE nome (colunas)
        match_create = re.match(r"CREATE\s+TABLE\s+(\w+)\s*\((.+)\)", query, re.IGNORECASE)
        if match_create:
            table_name = match_create.group(1)
            columns_str = match_create.group(2)
            
            # O Interpretador processa a string das colunas antes de passar pro processador
            columns_list = self._parse_columns(columns_str)
            
            return self.processor.create_table(table_name, columns_list)

        # Regex: INSERT INTO nome VALUES (valores)
        match_insert = re.match(r"INSERT\s+INTO\s+(\w+)\s+VALUES\s*\((.+)\)", query, re.IGNORECASE)
        if match_insert:
            table_name = match_insert.group(1)
            values_str = match_insert.group(2)
            
            values_list = [v.strip() for v in values_str.split(',')]
            
            return self.processor.insert_data(table_name, values_list)
        
        match_select = re.match(r"SELECT\s+\*\s+FROM\s+(\w+)\s+WHERE\s+(\w+)\s*=\s*(.+)", query, re.IGNORECASE)
        if match_select:
            table_name = match_select.group(1)
            col_name = match_select.group(2)
            val_str = match_select.group(3).strip()
            
            return self.processor.execute_select(table_name, col_name, val_str)
        
        match_source = re.match(r"SOURCE\s+(.+)", query, re.IGNORECASE)
        if match_source:
            filename = match_source.group(1).strip()
            return self._run_script(filename)

        if query.upper() == "EXIT":
            return "EXIT"

        print("  Erro de Sintaxe: Comando não reconhecido.")

    def _parse_columns(self, columns_str):
        raw_cols = columns_str.split(',')
        parsed = []
        for raw in raw_cols:
            parts = raw.strip().split()
            col_name = parts[0]
            col_type = parts[1]
            is_pk = "PRIMARY" in parts and "KEY" in parts
            parsed.append((col_name, col_type, is_pk))
        return parsed
    
    def _run_script(self, filename):
        print(f"---  Executando script: {filename} ---")
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                
            for line in lines:
                line = line.strip()
                if line and not line.startswith('--'): # Ignora vazios e comentários
                    print(f"\n[SCRIPT] > {line}")
                    self.parse_and_execute(line)
            print("--- Fim do Script ---")
        except FileNotFoundError:
            print(f"Erro: Arquivo '{filename}' não encontrado.")