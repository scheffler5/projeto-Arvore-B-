from .disk_manager import DiskManager
from .node import Node 

class BPlusTree:
    #Inicialização
    def __init__(self, table_name, t, page_size, columns=[]):
        self.t = t
        self.page_size = page_size
        self.filename = f"{table_name}.db"
        self.columns = columns
        self.disk = DiskManager(self.filename, page_size)
        self.root_id = 0 # Pagina sempre na pagina 0
        
        self.current_seq = 0
        
        # Inicializa a Raiz se o arquivo estiver vazio
        raw_root = self.disk.read_page(self.root_id)
        if not Node.from_bytes(raw_root):
            print(f"-> Inicializando Raiz na página {self.root_id}...")
            # Cria o primeiro nó folha
            root = Node(self.root_id, t, is_leaf=True)
            self.disk.write_page(self.root_id, root.to_bytes())


    def insert(self, data_dict):
        pk_col_name = self.columns[0][0]
        raw_val = data_dict.get(pk_col_name)
        if raw_val is None:
            self.current_seq += 1
            generated_id = self.current_seq
            data_dict[pk_col_name] = generated_id   # Gera uma nova primary key
            print(f"   [AUTO-INCREMENT] ID Gerado: {generated_id}")
        else:
            try:
                generated_id = int(raw_val)
                if generated_id > self.current_seq:
                    self.current_seq = generated_id
            except ValueError:
                return

        # Zera stats
        self.disk.num_reads = 0
        self.disk.num_writes = 0

        raw_data = self.disk.read_page(self.root_id)
        root = Node.from_bytes(raw_data)
        
        if root is None:
            root = Node(self.root_id, self.t, is_leaf=True)

        #Trabalho de Split
        if root.is_full():
            # arvore cresce em altura
            new_root = Node(self.root_id, self.t, is_leaf=False)
            new_child_id = self.disk.get_new_page_id()
            # A antiga raiz vira filha da nova raiz
            root.page_id = new_child_id 
            new_root.children.append(new_child_id)
            # Divide a antiga raiz
            self._split_child(new_root, 0, root)
            self._insert_non_full(new_root, generated_id, data_dict)
            self.disk.write_page(self.root_id, new_root.to_bytes())
        else:
            #Folha vazia, insere o dado e salva no disco
            self._insert_non_full(root, generated_id, data_dict)
        print(f"[DISK] Insert Concluído. Pág {self.root_id} atualizada.")
        print(f"[STATS] {self.disk.get_stats()}")

    def _insert_non_full(self, node, key, data_dict):
        if node.is_leaf:
            node.insert_leaf(key, data_dict)
            self.disk.write_page(node.page_id, node.to_bytes())
        else:
            # lógica para nó interno, Descobrir qual filho descer
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1 
            
            # Carrega o filho
            child_id = node.children[i]
            child_data = self.disk.read_page(child_id)
            child = Node.from_bytes(child_data)
            
            # Proactive Split: Se o filho estiver cheio, divide antes de entrar
            if child.is_full():
                self._split_child(node, i, child)
                # Depois de dividir, a chave mediana subiu.
                # Precisamos ver se nossa chave é maior que a chave que subiu
                if key > node.keys[i]:
                    i += 1
                # Recarrega o filho correto (pode ter mudado)
                child_data = self.disk.read_page(node.children[i])
                child = Node.from_bytes(child_data)
            
            self._insert_non_full(child, key, data_dict)

    def _split_child(self, parent, index, child):
        t = self.t
        
        # Cria o no Brother ao lado do no full
        new_brother_id = self.disk.get_new_page_id()
        brother = Node(new_brother_id, t, is_leaf=child.is_leaf)
        
        mid_idx = t - 1
        up_key = child.keys[mid_idx]
        
        # Distribui chaves
        if child.is_leaf:
            # Na B+, folhas mantêm cópia da chave na direita
            brother.keys = child.keys[mid_idx:] 
            brother.values = child.values[mid_idx:]
            
            # Link da lista (B+)
            brother.next_leaf = child.next_leaf
            child.next_leaf = brother.page_id
            
            child.keys = child.keys[:mid_idx]
            child.values = child.values[:mid_idx]
        else:
            # Nós internos apenas sobem a chave (B-Tree padrão)
            brother.keys = child.keys[mid_idx+1:]
            brother.children = child.children[mid_idx+1:]
            
            child.keys = child.keys[:mid_idx]
            child.children = child.children[:mid_idx+1]
        
        # Atualiza o Pai
        parent.keys.insert(index, up_key)
        parent.children.insert(index + 1, new_brother_id)
        
        # Salva os 3 envolvidos
        self.disk.write_page(parent.page_id, parent.to_bytes())
        self.disk.write_page(child.page_id, child.to_bytes())
        self.disk.write_page(brother.page_id, brother.to_bytes())

    #Busca na arvore 
    def search(self, key):
        try:
            search_key = int(key)
        except ValueError:
            return None
            
        self.disk.num_reads = 0
        
        raw_data = self.disk.read_page(self.root_id)
        node = Node.from_bytes(raw_data)
        
        # Se a raiz vier nula ou corrompida, nos a protejemos
        if not node: return None

        # Navegação
        while not node.is_leaf:
            i = 0
            # Encontra o ponteiro correto
            while i < len(node.keys) and search_key >= node.keys[i]:
                i += 1
            
            # Se o índice estourar os filhos nos a protejemos
            if i >= len(node.children):
                i = len(node.children) - 1

            child_id = node.children[i]
            # Carrega a próxima página do disco
            raw_data = self.disk.read_page(child_id)
            node = Node.from_bytes(raw_data)
            if not node: return None # Arquivo corrompido
        
        # Chegou na folha
        if search_key in node.keys:
            idx = node.keys.index(search_key)
            #Proteção contra Index Error
            if idx >= len(node.values):
                print(f" ERRO CRÍTICO: Chave {search_key} encontrada, mas valor sumiu! (Corrupção de DB)")
                return None
                
            return node.values[idx]
        
        return None