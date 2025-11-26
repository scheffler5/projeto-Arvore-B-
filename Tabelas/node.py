import pickle

class Node:               #      Numero da Pagina   Tamanho maximo do no    Boolean para guardar dado
    def __init__(self,              page_id,                t,                    is_leaf=False):
        self.page_id = page_id
        self.t = t
        self.is_leaf = is_leaf
        
        # Listas fundamentais
        self.keys = []     # uma lista que compoe as chaves primaria ou ID
        self.children = [] # Lista de Filhas apenas se nao for folha
        self.values = []   # Lista com dicionarios, usada apenas em folhas 
        
        self.next_leaf = 0 # Ponteiro para a proxima folha

        # apenas verifica se a arvore esta cheia
    def is_full(self):
        return len(self.keys) >= (2 * self.t) - 1 # maximo de 5 Chaves Primarias caso t = 3, caso fique cheia ele retorna para a arvore
                                                                            #assim ocorrera o split
    
    #Durante a inserção de dados, permite que os dados fiquem ordanados, ajudando posteriormente na colsulta
    def insert_leaf(self, key, value_dict):

        if not self.keys:
            self.keys.append(key)
            self.values.append(value_dict)
            return
        # Procura na arvore e caso encontre um numero maior que a chave ele adiciona uma nova chave antes do numero
        for i, k in enumerate(self.keys):
            if key < k:
                self.keys.insert(i, key)
                self.values.insert(i, value_dict) 
                return
        
        self.keys.append(key)
        self.values.append(value_dict) 
    # prepara o no para ser gravado em Disk_manager
    def to_bytes(self):
        #if para verificar se os valores e as chaves tem o mesmo tamanho, evita erro de erro de IndexError
        if self.is_leaf and len(self.keys) != len(self.values):
            print(f"ERRO CRÍTICO NA PÁGINA {self.page_id}: Keys={len(self.keys)} vs Values={len(self.values)}")
            while len(self.values) < len(self.keys):
                self.values.append({})
        
        return pickle.dumps(self)
    # Leitura de Bytes (Deserialização)
    @staticmethod
    def from_bytes(data):
        try:
            if not data: return None
            return pickle.loads(data)
        except:
            return None
        
    # Debug       
    def __repr__(self):
        return f"<Node {self.page_id} Leaf={self.is_leaf} Keys={self.keys}>"