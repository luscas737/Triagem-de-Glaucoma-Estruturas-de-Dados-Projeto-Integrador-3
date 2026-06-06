import time
import matplotlib.pyplot as plt
import seaborn as sns
from images import gerar_resultados
from estrutura_heap import FilaPrioridade, Paciente
from estrutura_abb import ArvoreBinariaBusca
from estrutura_avl import ArvoreAVL



def gerar_metricas():
    resultados_finais = gerar_resultados()
    # ==========================
    # Inserção
    # ==========================

    BST_timed = ArvoreBinariaBusca()

    start_time_bst = time.time()
    for chave, valor in resultados_finais.items():
        BST_timed.inserir(chave, valor)
    time_bst = time.time() - start_time_bst

    AVL_timed = ArvoreAVL()

    start_time_avl = time.time()
    for chave, valor in resultados_finais.items():
        AVL_timed.inserir(chave, valor)
    time_avl = time.time() - start_time_avl

    HEAP_timed = FilaPrioridade()

    start_time_heap = time.time()
    for chave, valor in resultados_finais.items():
        HEAP_timed.inserir(Paciente(chave, valor))
    time_heap = time.time() - start_time_heap

    # ==========================
    # Arquivo de atendimento
    # ==========================

    start_time_heap_file = time.time()
    HEAP_timed.gerar_ordem_atendimento()
    time_heap_file = time.time() - start_time_heap_file
    altura_avl = AVL_timed.raiz.altura
    altura_bst = BST_timed.altura()
    # ==========================
    # Recuperação da ordem
    # ==========================

    start_time_avl_inorder = time.time()
    AVL_timed.inorder_traversal()
    time_avl_inorder = time.time() - start_time_avl_inorder

    start_time_bst_inorder = time.time()
    BST_timed.inorder_traversal()
    time_bst_inorder = time.time() - start_time_bst_inorder

    # ==========================
    # Remoção Heap
    # ==========================

    start_time_heap_removal = time.time()

    while HEAP_timed.heap:
        HEAP_timed.remover()

    time_heap_removal = time.time() - start_time_heap_removal

    # ==========================
    # Remoção AVL
    # ==========================

    start_time_avl_removal = time.time()

    while AVL_timed.raiz is not None:
        max_val = AVL_timed.get_max_value()

        if max_val is None:
            break

        AVL_timed.remover(max_val)

    time_avl_removal = time.time() - start_time_avl_removal

    # ==========================
    # Remoção BST
    # ==========================

    start_time_bst_removal = time.time()

    while BST_timed.raiz is not None:
        max_val = BST_timed.get_max_value()

        if max_val is None:
            break

        BST_timed.remover(max_val)

    time_bst_removal = time.time() - start_time_bst_removal

    # ==========================
    # Gráfico 1
    # ==========================

    removal_times = {
        "BST": time_bst_removal,
        "AVL": time_avl_removal,
        "HEAP": time_heap_removal
    }

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=list(removal_times.keys()),
        y=list(removal_times.values())
    )

    plt.title("Comparativo de Tempo de Remoção")
    plt.savefig("graficos/grafico_1.png")
    plt.close()

    # ==========================
    # Gráfico 2
    # ==========================

    order_times = {
        "BST": time_bst_inorder,
        "AVL": time_avl_inorder,
        "HEAP": time_heap_removal
    }

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=list(order_times.keys()),
        y=list(order_times.values())
    )

    plt.title("Comparativo de Recuperação da Ordem")
    plt.savefig("graficos/grafico_2.png")
    plt.close()

    # ==========================
    # Gráfico 3
    # ==========================

    insert_times = {
        "BST": time_bst,
        "AVL": time_avl,
        "HEAP": time_heap
    }

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=list(insert_times.keys()),
        y=list(insert_times.values())
    )

    plt.title("Comparativo de Inserção")
    plt.savefig("graficos/grafico_3.png")
    plt.close()

    # ==========================
    # Resposta
    # ==========================

    return {
        "quantidade_pacientes": len(resultados_finais),

        "tempo_insercao": {
            "bst": time_bst,
            "avl": time_avl,
            "heap": time_heap
        },

        "tempo_remocao": {
            "bst": time_bst_removal,
            "avl": time_avl_removal,
            "heap": time_heap_removal
        },

        "tempo_recuperacao_ordem": {
            "bst": time_bst_inorder,
            "avl": time_avl_inorder
        },

        "comparacoes": {
            "bst": BST_timed.comparacao,
            "avl": AVL_timed.comparacao
        },

        "altura": {
            "bst": altura_bst,
            "avl": altura_avl
        },

        "rotacoes_avl": AVL_timed.rotacoes,

        "arquivo_gerado": "ordem_atendimento.txt",

        "graficos": [
            "graficos/grafico_1.png",
            "graficos/grafico_2.png",
            "graficos/grafico_3.png"
        ]
    }