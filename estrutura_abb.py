class No:
    def __init__(self, id, valor):
        self.id = id
        self.valor = valor
        self.esquerda = None
        self.direita = None

    def __repr__(self):
        return str(self.valor)
    
class ArvoreBinaria:
    def __init__(self, raiz=None):
        self.raiz = raiz
        self.comparacao = 0
    def esta_vazia(self):
        return self.raiz is None

    def altura(self):
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, no):
        if no is None:
            return -1
        return 1 + max(self._altura_recursiva(no.esquerda),
                       self._altura_recursiva(no.direita))

    def __len__(self):
        return self._tamanho_recursivo(self.raiz)

    def _tamanho_recursivo(self, no):
        if no is None:
            return 0
        return 1 + self._tamanho_recursivo(no.esquerda) + self._tamanho_recursivo(no.direita)

    def __repr__(self):
        return f"{self.__class__.__name__}(raiz={repr(self.raiz)})"

    def __str__(self):
        if self.esta_vazia():
            return "<árvore vazia>"

        linhas = []
        self._coletar_linhas(self.raiz, "", linhas)
        return "\n".join(linhas)

    def _coletar_linhas(self, no, prefixo, linhas):
        if no is not None:
            # Visita primeiro o filho direito (para visualização mais natural)
            self._coletar_linhas(no.direita, prefixo + "   ", linhas)
            # Adiciona o nó atual
            linhas.append(prefixo + str(no.valor))
            # Visita o filho esquerdo
            self._coletar_linhas(no.esquerda, prefixo + "   ", linhas)
class ArvoreBinariaBusca(ArvoreBinaria):
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, no, valor):
        if no is None or no.valor == valor:
            return no
        if valor < no.valor:
            return self._buscar_recursivo(no.esquerda, valor)
        else:
            return self._buscar_recursivo(no.direita, valor)

    def inserir(self, id, valor):
        self.raiz = self._inserir_recursivo(id, self.raiz, valor)

    def _inserir_recursivo(self, id,  no, valor):
        if no is None:
            self.comparacao += 1
            return No(id, valor)
        if valor < no.valor:
            self.comparacao += 1
            no.esquerda = self._inserir_recursivo(id, no.esquerda, valor)
        else:
            self.comparacao += 1
            no.direita = self._inserir_recursivo(id, no.direita, valor)
        return no

    def remover(self, valor):
        self.raiz = self._remover_recursivo(self.raiz, valor)

    def _remover_recursivo(self, no, valor):
        if no is None:
            return None

        if valor < no.valor:  # Corrigido: usar no.valor para comparação
            no.esquerda = self._remover_recursivo(no.esquerda, valor)
        elif valor > no.valor:  # Corrigido: usar no.valor para comparação
            no.direita = self._remover_recursivo(no.direita, valor)
        else:
            # Caso 1: Nó sem filhos
            if no.esquerda is None and no.direita is None:
                return None
            # Caso 2: Um filho apenas
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            # Caso 3: Dois filhos
            sucessor = self._menor_valor(no.direita)
            no.valor = sucessor.valor
            no.id = sucessor.id
            no.direita = self._remover_recursivo(no.direita, sucessor.valor)

        return no

    def _menor_valor(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def get_max_value(self):
        if self.raiz is None:
            return None
        current = self.raiz
        while current.direita is not None:
            current = current.direita
        return current.valor

    # Novo método para travessia em ordem (inorder traversal)
    def inorder_traversal(self):
        result = []
        self._inorder_traversal_recursivo(self.raiz, result)
        return result

    def _inorder_traversal_recursivo(self, no, result):
        if no:
            self._inorder_traversal_recursivo(no.esquerda, result)
            result.append(no.valor)
            self._inorder_traversal_recursivo(no.direita, result)