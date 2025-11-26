import os


# Coversao de ordens logica em operaçoes fisicas
class DiskManager:
    #Incialização
    def __init__(self, filename, page_size=4096):
        self.filename = filename
        self.PAGE_SIZE = page_size 
        self.num_reads = 0  
        self.num_writes = 0
        
        #Cria um Arquivo de banco de dados 
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                pass 
                    #Numero da pagina
    def read_page(self, page_id):
        self.num_reads += 1 #Contabiliza a quantidade de leituras
        try:
            with open(self.filename, 'rb') as f:
                offset = page_id * self.PAGE_SIZE # Calculo o Inicio de cada pagina
                f.seek(offset) # Move a leitrua para a posição calculada (Random Access)
                data = f.read(self.PAGE_SIZE)
                return data
        except FileNotFoundError:
            return b'\x00' * self.PAGE_SIZE

    def write_page(self, page_id, data):
        self.num_writes += 1 # Contabiliza a quantidade de Escritas
        if len(data) > self.PAGE_SIZE:
            print(f" AVISO: Dados maiores que a página! ({len(data)} > {self.PAGE_SIZE})")
            raise ValueError("Overflow de Página")
        # modo R+B permite alteração apenas de trecho do arquivo sem excluido e reescreve-lo
        with open(self.filename, 'r+b') as f:
            offset = page_id * self.PAGE_SIZE
            f.seek(offset)
            f.write(data.ljust(self.PAGE_SIZE, b'\x00')) # Padding 
    #Alocação de Espaço Livre
    def get_new_page_id(self):
        size = os.path.getsize(self.filename)
        return size // self.PAGE_SIZE
    # Paga o estatus de escrita e leitura executadas
    def get_stats(self):
        return f"Leituras: {self.num_reads} | Escritas: {self.num_writes}"