import time
import matplotlib.pyplot as plt
import seaborn as sns

from estrutura_heap import FilaPrioridade, Paciente
from estrutura_abb import ArvoreBinariaBusca
from estrutura_avl import ArvoreAVL

def executar_metricas(resultados):

    BST_timed = ArvoreBinariaBusca()
    # Medir tempo de inserção para BST
    start_time_bst = time.time()
    for chave, valor in resultados.items():
        BST_timed.inserir(chave, valor)
    end_time_bst = time.time()
    time_bst = end_time_bst - start_time_bst
    print(f"Tempo de inserção para BST: {time_bst:.6f} segundos")

    # Medir tempo de inserção para AVL
    AVL_timed = ArvoreAVL()
    start_time_avl = time.time()
    for chave, valor in resultados.items():
        AVL_timed.inserir(chave, valor)
    end_time_avl = time.time()
    time_avl = end_time_avl - start_time_avl
    print(f"Tempo de inserção para AVL: {time_avl:.6f} segundos")

    # Medir tempo de inserção para Heap
    HEAP_timed = FilaPrioridade()
    start_time_heap = time.time()
    for chave, valor in resultados.items():
        paciente = Paciente(chave, valor)
        HEAP_timed.inserir(paciente)
    end_time_heap = time.time()
    time_heap = end_time_heap - start_time_heap
    print(f"Tempo de inserção para HEAP: {time_heap:.6f} segundos")

    # Medir tempo de geração do arquivo para Heap
    start_time_heap_file = time.time()
    HEAP_timed.gerar_ordem_atendimento()
    end_time_heap_file = time.time()
    time_heap_file = end_time_heap_file - start_time_heap_file
    print(f"Tempo de geração do arquivo para HEAP: {time_heap_file:.6f} segundos")

    # Quantidade total de comparações realizadas;

    print(f"Quantidade total de comparações realizadas para BST: {BST_timed.comparacao}")
    print(f"Quantidade total de comparações realizadas para AVL: {AVL_timed.comparacao}")

    # Altura final da árvore (ABB e AVL);

    print(f"Altura final da árvore (ABB): {BST_timed.altura()}")
    print(f"Altura final da árvore (AVL): {AVL_timed.raiz.altura}")

    # Número de rotações realizadas (apenas AVL);

    print(f"Número de rotações realizadas (AVL): {AVL_timed.rotacoes}")


    # Medir tempo de travessia em ordem para AVL
    start_time_avl_inorder = time.time()
    avl_ordenada = AVL_timed.inorder_traversal()
    end_time_avl_inorder = time.time()
    time_avl_inorder = end_time_avl_inorder - start_time_avl_inorder
    print(f"Tempo de recuperação da ordem (in-order traversal) para AVL: {time_avl_inorder:.6f} segundos")

    # Opcional: Para visualizar os primeiros elementos ordenados, descomente a linha abaixo
    # print(f"Primeiros 10 elementos da AVL em ordem: {avl_ordenada[:10]}")


    # Medir tempo de travessia em ordem para BST
    start_time_bst_inorder = time.time()
    bst_ordenada = BST_timed.inorder_traversal()
    end_time_bst_inorder = time.time()
    time_bst_inorder = end_time_bst_inorder - start_time_bst_inorder
    print(f"Tempo de recuperação da ordem (in-order traversal) para BST: {time_bst_inorder:.6f} segundos")

    # Opcional: Para visualizar os primeiros elementos ordenados, descomente a linha abaixo
    # print(f"Primeiros 10 elementos da BST em ordem: {bst_ordenada[:10]}")


    start_time_heap_removal = time.time()
    while HEAP_timed.heap: # Loop enquanto a heap não estiver vazia
        HEAP_timed.remover()
        end_time_heap_removal = time.time()
        time_heap_removal = end_time_heap_removal - start_time_heap_removal
        print(f"Tempo de remoção para HEAP (até ficar vazia): {time_heap_removal:.6f} segundos")

        start_time_avl_removal = time.time()
    while AVL_timed.raiz is not None:
        max_val = AVL_timed.get_max_value()
        if max_val is not None:
            AVL_timed.remover(max_val)
        else:
            break
    end_time_avl_removal = time.time()
    time_avl_removal = end_time_avl_removal - start_time_avl_removal
    print(f"Tempo de remoção do maior valor para AVL (até ficar vazia): {time_avl_removal:.6f} segundos")


    start_time_bst_removal = time.time()
    while BST_timed.raiz is not None:
        max_val_bst = BST_timed.get_max_value()
        if max_val_bst is not None:
            BST_timed.remover(max_val_bst)
        else:
            break
    end_time_bst_removal = time.time()
    time_bst_removal = end_time_bst_removal - start_time_bst_removal
    print(f"Tempo de remoção do maior valor para BST (até ficar vazia): {time_bst_removal:.6f} segundos")


    # Definindo os tempos de remoção
    removal_times = {
        'BST': time_bst_removal,
        'AVL': time_avl_removal,
        'HEAP': time_heap_removal
    }

    algorithms_removal_order = list(removal_times.keys())
    removal_values = list(removal_times.values())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=algorithms_removal_order, y=removal_values, palette='viridis')
    plt.title('Comparativo de Tempo de Remoção (BST, AVL, HEAP)')
    plt.xlabel('Algoritmo')
    plt.ylabel('Tempo de Remoção (segundos)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


    # Definindo os tempos de recuperação da ordem
    # Para Heap, consideramos o tempo de remoção total dos elementos
    order_retrieval_times = {
        'BST': time_bst_inorder,
        'AVL': time_avl_inorder,
        'HEAP (Remoção Total)': time_heap_removal
    }

    algorithms_order = list(order_retrieval_times.keys())
    retrieval_times = list(order_retrieval_times.values())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=algorithms_order, y=retrieval_times, palette='plasma')
    plt.title('Comparativo de Tempo de Recuperação da Ordem (BST, AVL, HEAP)')
    plt.xlabel('Algoritmo')
    plt.ylabel('Tempo de Recuperação da Ordem (segundos)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


    times = {
        'BST': time_bst,
        'AVL': time_avl,
        'HEAP': time_heap
    }

    algorithms = list(times.keys())
    insertion_times = list(times.values())

    plt.figure(figsize=(8, 5))
    sns.barplot(x=algorithms, y=insertion_times, palette='viridis')
    plt.title('Comparativo de Tempo de Inserção (BST, AVL, HEAP)')
    plt.xlabel('Algoritmo')
    plt.ylabel('Tempo de Inserção (segundos)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()