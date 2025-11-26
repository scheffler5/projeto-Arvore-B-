# Arquivo: Main.py
from Comandos.interpreter import Interpreter

def main():
    print("=== SQL Database ===")
    # Aqui fiz as configuraçoes iniciais do projeto como por exemplo
        # definir o t e Tamanho da pagina.
    print("\n--- Configuração do Sistema ---")
    try:
        #input de t e tamanho de pagina
        user_t = int(input("Defina o grau mínimo t (Padrão 3): ") or 3)
        user_page = int(input("Defina o tamanho da página em bytes (Padrão 4096): ") or 4096)
    
    except ValueError:
        #caso nao input nada ele pega valores padroes
        print("Valor inválido! Usando padrões (t=3, page=4096).")
        user_t = 3
        user_page = 4096

    print(f"Sistema iniciado com t={user_t} e PageSize={user_page} bytes.")
    print("Use: CREATE TABLE..., INSERT INTO..., ou EXIT")
    

    # Colocamos as variaveis dentro do interpretador
    interpreter = Interpreter(user_t, user_page)

    #While para rodar a linha de comando SQL ate o comando EXIT
    while True:
        try:
            sql_command = input("\nSQL> ")
            if not sql_command.strip(): continue

            #Mandamos o resultado para a função de execução do nosso interpretador
            result = interpreter.parse_and_execute(sql_command)
            
            if result == "EXIT": break
            
        except Exception as e:
            print(f"Erro Crítico: {e}")

if __name__ == "__main__":
    main()