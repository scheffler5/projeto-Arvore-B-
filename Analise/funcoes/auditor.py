# Arquivo: Analise/funcoes/auditor.py
#Percorre a arvore de forma recursiva para poegar metricas e criar o benchmark
def auditar_arvore(tree):
    
    # Importação tardia para evitar erro de ciclo
    from Tabelas.node import Node
    
    stats = {
        'total_nodes': 0,
        'total_leaves': 0,
        'height': 0,
    }
    
    # Lê a raiz
    raw_root = tree.disk.read_page(tree.root_id)
    
    root = Node.from_bytes(raw_root)
    
    if root is None:
        return stats

    # Função recursiva de travessia
    def traverse(node, current_depth):
        stats['total_nodes'] += 1
        stats['height'] = max(stats['height'], current_depth)
        
        if node.is_leaf:
            stats['total_leaves'] += 1
            return
        
        # Se for nó interno, desce nos filhos
        for child_id in node.children:
            raw_child = tree.disk.read_page(child_id)
            child_node = Node.from_bytes(raw_child) 
            if child_node:
                traverse(child_node, current_depth + 1)

    traverse(root, 1) # Começa na profundidade 1
    return stats