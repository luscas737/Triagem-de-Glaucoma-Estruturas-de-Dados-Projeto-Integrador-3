import heapq
import time

class Paciente:
    def __init__(self, id, risco):
        self.id = id
        self.risco = risco
        self.timestamp = time.time()

    def __repr__(self):
        return f"{self.id} (Risco: {self.risco})"


class FilaPrioridade:
    def __init__(self):
        self.heap = []
        self.mapa = {}  # id → paciente

    def inserir(self, paciente):
        # heapq é Min-Heap → usamos negativo para simular Max-Heap
        entrada = (-paciente.risco, paciente.timestamp, paciente.id, paciente)
        heapq.heappush(self.heap, entrada)
        self.mapa[paciente.id] = paciente

    def remover(self):
        if not self.heap:
            return None

        _, _, id, paciente = heapq.heappop(self.heap)
        del self.mapa[id]
        return paciente

    def atualizar_risco(self, id_paciente, novo_risco):
        if id_paciente not in self.mapa:
            return

        paciente = self.mapa[id_paciente]
        paciente.risco = novo_risco
        paciente.timestamp = time.time()
        self.reconstruir_heap()

    def reconstruir_heap(self):
        self.heap = [
            (-p.risco, p.timestamp, p.id, p)
            for p in self.mapa.values()
        ]
        heapq.heapify(self.heap)

    def exibir(self):
        return [entrada[3] for entrada in self.heap]

    def gerar_ordem_atendimento(self, caminho="ordem_atendimento.txt"):

        # Cópia da heap para não alterar a estrutura original
        heap_temp = self.heap.copy()

        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write("Posição,ID_Paciente,Score\n")

            posicao = 1

            while heap_temp:
                _, _, _, paciente = heapq.heappop(heap_temp)

                arquivo.write(
                    f"{posicao},{paciente.id},{paciente.risco:.3f}\n"
                )

                posicao += 1

        print(f"Arquivo salvo em: {caminho}")
