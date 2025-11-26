import random
import string

def gerar_registro(num_colunas):
    #Retorna um dicionario e colunas de forma randomica
    data = {}
    
    # Começa do 0, mas a col 0 é  a PK 
    for i in range(1, num_colunas):
        col_name = f"col_{i}"
        
        # Aleatoriamente escolhe se gera um numero ou string
        if random.choice([True, False]):
            # Gera string aleatória de 5 letras
            val = ''.join(random.choices(string.ascii_uppercase, k=5))
        else:
            # Gera numero aleatório
            val = random.randint(1, 1000)
            
        data[col_name] = val
        
    return data