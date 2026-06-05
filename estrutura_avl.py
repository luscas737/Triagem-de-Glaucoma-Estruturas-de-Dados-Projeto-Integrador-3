class NoAVL:
    def __init__(self, id, valor):
        self.id = id
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1

    def __repr__(self):
        return str(self.valor)
class ArvoreAVL:
    def __init__(self):
        self.raiz = None
        self.comparacao = 0
        self.rotacoes = 0

    def _altura(self, no):
        if no is None:
            return 0
        return no.altura

    def _fator_balanceamento(self, no):
        if no is None:
            return 0
        return self._altura(no.esquerda) - self._altura(no.direita)

    def _atualizar_altura(self, no):
        if no is not None:
            no.altura = 1 + max(self._altura(no.esquerda), self._altura(no.direita))

    def _rotacao_direita(self, y):
        self.rotacoes += 1
        x = y.esquerda
        T2 = x.direita

        # Realiza a rotação
        x.direita = y
        y.esquerda = T2

        # Atualiza alturas
        self._atualizar_altura(y)
        self._atualizar_altura(x)

        return x

    def _rotacao_esquerda(self, x):
        self.rotacoes += 1
        y = x.direita
        T2 = y.esquerda

        # Realiza a rotação
        y.esquerda = x
        x.direita = T2

        # Atualiza alturas
        self._atualizar_altura(x)
        self._atualizar_altura(y)

        return y

    def inserir(self, id, valor):
        self.raiz = self._inserir_recursivo(id ,self.raiz, valor)

    def _inserir_recursivo(self, id, no, valor):
        # 1. Realiza a inserção normal de BST
        if no is None:
            return NoAVL(id, valor)

        if valor < no.valor:
            self.comparacao += 1
            no.esquerda = self._inserir_recursivo(id, no.esquerda, valor)
        else:
            self.comparacao += 1
            no.direita = self._inserir_recursivo(id, no.direita, valor)

        # 2. Atualiza a altura do nó ancestral
        self._atualizar_altura(no)

        # 3. Obtém o fator de balanceamento
        fator = self._fator_balanceamento(no)

        # 4. Se o nó está desbalanceado, então há 4 casos

        # Caso LL (Left Left)
        if fator > 1 and valor < no.esquerda.valor:
            self.comparacao += 1
            return self._rotacao_direita(no)

        # Caso RR (Right Right)
        if fator < -1 and valor > no.direita.valor:
            self.comparacao += 1
            return self._rotacao_esquerda(no)

        # Caso LR (Left Right)
        if fator > 1 and valor > no.esquerda.valor:
            self.comparacao += 1
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)

        # Caso RL (Right Left)
        if fator < -1 and valor < no.direita.valor:
            self.comparacao += 1
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no

    def _menor_valor_no(self, no):
        atual = no
        while atual.esquerda is not None:
            self.comparacao += 1
            atual = atual.esquerda
        return atual

    def get_max_value(self):
        if self.raiz is None:
            return None
        current = self.raiz
        while current.direita is not None:
            current = current.direita
        return current.valor

    def remover(self, valor):
        self.raiz = self._remover_recursivo(self.raiz, valor)

    def _remover_recursivo(self, no, valor):
        # 1. Realiza a remoção normal de BST
        if no is None:
            return no
        if valor < no.valor:  # Corrigido: usar no.valor para comparação
            no.esquerda = self._remover_recursivo(no.esquerda, valor)
        elif valor > no.valor:  # Corrigido: usar no.valor para comparação
            no.direita = self._remover_recursivo(no.direita, valor)
        else:
            # Nó com um ou nenhum filho
            if no.esquerda is None:
                temp = no.direita
                no = None
                return temp
            elif no.direita is None:
                temp = no.esquerda
                no = None
                return temp

            # Nó com dois filhos: obtém o sucessor in-order (menor na subárvore direita)
            temp = self._menor_valor_no(no.direita)
            no.valor = temp.valor
            no.id = temp.id
            no.direita = self._remover_recursivo(no.direita, temp.valor)

        if no is None:
            return no

        # 2. Atualiza a altura do nó atual
        self._atualizar_altura(no)

        # 3. Obtém o fator de balanceamento
        fator = self._fator_balanceamento(no)

        # 4. Se o nó está desbalanceado, então há 4 casos

        # Caso LL
        if fator > 1 and self._fator_balanceamento(no.esquerda) >= 0:
            return self._rotacao_direita(no)

        # Caso LR
        if fator > 1 and self._fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)

        # Caso RR
        if fator < -1 and self._fator_balanceamento(no.direita) <= 0:
            return self._rotacao_esquerda(no)

        # Caso RL
        if fator < -1 and self._fator_balanceamento(no.direita) > 0:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, no, valor):
        if no is None or no.valor == valor:
            return no
        if valor < no.valor:
            return self._buscar_recursivo(no.esquerda, valor)
        else:
            return self._buscar_recursivo(no.direita, valor)

    def _imprimir_arvore(self, no, nivel=0, prefixo="Raiz: "):
        if no is not None:
            print("  " * nivel + prefixo + str(no.valor) + f" (FB: {self._fator_balanceamento(no)}, Altura: {no.altura})")
            self._imprimir_arvore(no.esquerda, nivel + 1, "E: ")
            self._imprimir_arvore(no.direita, nivel + 1, "D: ")

    def imprimir(self):
        self._imprimir_arvore(self.raiz)

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

    def __str__(self):
        linhas = []
        self._coletar_linhas(self.raiz, "", linhas)
        return "\n".join(linhas)

    def _coletar_linhas(self, no, prefixo, linhas):
        if no is not None:
            self._coletar_linhas(no.direita, prefixo + "   ", linhas)
            linhas.append(prefixo + str(no.valor))
            self._coletar_linhas(no.esquerda, prefixo + "   ", linhas)