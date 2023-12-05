import math
import json
from TDA.LinkedList import LinkedList
import matplotlib.pyplot as plt


class PontoTuristico:
    def __init__(self, nome, designacao="vazio", morada="vazio", coordenadas=None,
                 categorias="vazio", visitas=0, avaliacao=None, media=None, acessibilidade="vazio", atividades="vazio"):
        self.nome = nome
        self.designacao = designacao
        self.morada = morada
        self.coordenadas = coordenadas
        self.categorias = categorias
        self.visitas = visitas
        self.avaliacao = avaliacao
        self.media = media
        self.acessibilidade = acessibilidade
        self.atividades = atividades
        self.next = None

    def __str__(self):
        return f"Nome: {self.nome}\n" \
               f"\tDesignação: {self.designacao}\n" \
               f"\tMorada: {self.morada}\n" \
               f"\tCoordenadas: {self.coordenadas}\n" \
               f"\tCategorias: {self.categorias}\n" \
               f"\tAcessibilidade: {self.acessibilidade}\n" \
               f"\tAtividades: {self.atividades}\n" \
               f"\tVisitas: {self.visitas}\n" \
               f"\tAvaliação: {self.avaliacao}\n" \
               f"\tMedia: {self.media}"


class Sistema:
    def __init__(self):
        self.p_turistico = LinkedList()

    def adicionar_ponto(self, nome, designacao="vazio", morada="vazio", coordenadas=None,
                        categorias="vazio", visitas=0, avaliacao=None, media=None,
                        acessibilidade="vazio", atividades="vazio"):
        if not self.validar_categorias(categorias):
            return "Categorias inválidas. As categorias permitidas são: natureza, cultura, aventura, gastronomia."

        if coordenadas is None:
            coordenadas = [0, 0]

        ponto = PontoTuristico(nome, designacao, morada, coordenadas, categorias, visitas, avaliacao, media,
                               acessibilidade, atividades)
        self.p_turistico.append(ponto)
        return "Ponto turístico adicionado com sucesso."

    def alterar_ponto(self, nome, designacao=None, morada=None, coordenadas=None,
                      categorias=None, acessibilidade=None, atividades=None):
        if not self.validar_categorias(categorias):
            return "Categorias inválidas. As categorias permitidas são: natureza, cultura, aventura, gastronomia."

        ponto = self.p_turistico.find_by_key(nome)
        if ponto:
            if designacao:
                ponto.designacao = designacao
            if morada:
                ponto.morada = morada
            if coordenadas:
                ponto.coordenadas = coordenadas
            if categorias:
                ponto.categorias = categorias
            if acessibilidade:
                ponto.acessibilidade = acessibilidade
            if atividades:
                ponto.atividades = atividades
            return "Ponto turístico alterado com sucesso."
        else:
            return "Ponto turístico não encontrado."

    def remover_ponto(self, nome):
        ponto = self.p_turistico.find_by_key(nome)
        if ponto:
            self.p_turistico.pop(ponto)
            return "Ponto turístico removido com sucesso."
        else:
            return "Ponto turístico não encontrado."

    def obter_ponto(self, nome):
        ponto = self.p_turistico.find_by_key(nome)
        if ponto:
            return ponto
        else:
            return "Ponto turístico não encontrado."

    def listar_pontos(self):
        """
        :return: Lista os pontos de interesse turísticos
        """
        pontos = self.p_turistico.get_all()
        if len(pontos) == 0:
            return "Sem pontos turísticos definidos."
        else:
            pontos_str = [str(ponto) for ponto in pontos]
            return "\n".join(pontos_str)

    def pesquisar_por_categoria(self, categoria):
        if not self.validar_categorias(categoria):
            return "Categorias inválidas. As categorias permitidas são: natureza, cultura, aventura, gastronomia."

        resultados = []
        current = self.p_turistico.head
        while current is not None:
            ponto = current.data
            if categoria in ponto.categorias:
                resultados.append(ponto)
            current = current.next

        if len(resultados) == 0:
            return "Nenhum ponto turístico encontrado para a categoria especificada."

        resultados_ordenados = self.bubble_sort(resultados, key=lambda x: x.designacao)

        resultado_str = '\n'.join(str(ponto) for ponto in resultados_ordenados if categoria in ponto.categorias)
        return resultado_str

    def assinalar_visita(self, nome):
        """
        Permite incrementar em uma unidade o contador de visitas
        :param nome: Nome do ponto de interesse turístico
        :return: Acrescenta 1 ao número de visitas ou informa que o ponto turístico não foi encontrado
        """
        ponto = self.p_turistico.find_by_key(nome)
        if ponto:
            if ponto.visitas:
                ponto.visitas = int(ponto.visitas) + 1
            else:
                ponto.visitas = 1
            return "Visita ao ponto turístico registrada com sucesso. Total de visitas: " + str(ponto.visitas)
        else:
            return "Ponto turístico não encontrado."

    def avaliar_experiencia(self, nome, rate):
        """
        Atualiza as classificações da experiência da visita nesse ponto.
        :param nome: Nome do ponto de interesse turístico
        :param rate: Classificação da visita
        :return: Retorna a média atualizada das avaliações ou uma mensagem de erro
        """
        if rate < 0 or rate > 4:
            return "A classificação deve ser maior que 0 e menor que 4."

        ponto = self.p_turistico.find_by_key(nome)

        if ponto is None:
            return "Ponto turístico não encontrado."

        if ponto.avaliacao is None:
            ponto.avaliacao = []

        ponto.avaliacao.append(float(rate))

        avaliacoes_numericas = [avaliacao for avaliacao in ponto.avaliacao if isinstance(avaliacao, (int, float))]

        if len(avaliacoes_numericas) > 0:
            media = sum(avaliacoes_numericas) / len(avaliacoes_numericas)
            ponto.media = round(media, 2)
            return media
        else:
            return "Não há avaliações disponíveis para calcular a média."

    def consultar_estatisticas(self):
        """
        Consultar estatísticas de visitas aos pontos de interesse
        :return: pontos de interesse turísticos, indicando o número de visitantes, a classificação média
                 e um gráfico com a distribuição das classificações
        """
        estatisticas = []
        classificacoes = []
        current = self.p_turistico.head

        while current is not None:
            ponto = current.data
            num_visitantes = ponto.visitas
            media = ponto.media
            categoria = ponto.categorias
            designacao = ponto.designacao

            estatisticas.append(
                f"Nome: {ponto.nome}\n"
                f"\tDesignação: {designacao}\n"
                f"\tCategorias: {categoria}\n"
                f"\tVisitas: {num_visitantes}\n"
                f"\tMédia: {media}"
            )

            if media is not None:
                classificacoes.append(media)

            current = current.next

        if classificacoes:

            plt.hist(classificacoes, bins=[1, 2, 3, 4, 5], align='left', rwidth=0.8)

            plt.title("Distribuição da Classificação dos Pontos de Interesse")
            plt.xlabel("Classificação")
            plt.ylabel("Número de Pontos de Interesse")
            plt.xticks([1, 2, 3, 4], ["Nada Satisfeito", "Pouco Satisfeito", "Satisfeito", "Muito Satisfeito"])

            plt.show()

        return "\n".join(estatisticas)

    def sugerir_pontos_interesse(self, coordenadas):
        """
        Obter sugestões de visitas a pontos de interesse.
        :param coordenadas: Coordenadas [x, y] do utilizador
        :return: Lista de pontos de interesse ordenados pela distancia usando o merge sort
        """
        resultados = []
        current = self.p_turistico.head
        while current is not None:
            ponto = current.data
            ponto_coord = ponto.coordenadas
            if ponto_coord:
                distancia = self.calcular_distancia(coordenadas[0], coordenadas[1], ponto_coord[0], ponto_coord[1])
                visitas = ponto.visitas
                designacao = ponto.designacao
                resultados.append({
                    "nome": ponto.nome,
                    "designacao": designacao,
                    "distancia": distancia,
                    "visitas": visitas
                })
            current = current.next

        resultados = self.merge_sort(resultados)
        res_formatados = []
        for resultado in resultados:
            formatted_resultado = f"Nome: {resultado['nome']}\n" \
                                  f"\tDesignação: {resultado['designacao']}\n" \
                                  f"\tDistância: {resultado['distancia']}\n" \
                                  f"\tVisitas: {resultado['visitas']}"
            res_formatados.append(formatted_resultado)

        return '\n'.join(res_formatados)

    def carregar_dados(self, nome_arquivo):
        """
        Os dados sobre os pontos de interesse são guardados em ficheiro JSON
        :param nome_arquivo: Nome do arquivo json para carregar os dados
        :return: Carrega os dados na linked list
        """
        try:
            with open(nome_arquivo, 'r') as arquivo:
                data = json.load(arquivo)
                for ponto in data:
                    nome = ponto.get("nome")
                    designacao = ponto.get("designacao")
                    visitas = ponto.get("visitas", 0)
                    media = ponto.get("media", 0)
                    categorias = ponto.get("categorias", "vazio")
                    coordenadas = ponto.get("coordenadas")
                    avaliacao = ponto.get("avaliacao", [])
                    atividades = ponto.get("atividades", [])
                    acessibilidade = ponto.get("acessibilidade", "vazio")
                    morada = ponto.get("morada", "vazio")
                    novo_ponto = PontoTuristico(nome, designacao, "vazio", coordenadas,
                                                categorias, visitas, avaliacao, media, "vazio", "vazio")
                    novo_ponto.atividades = atividades
                    novo_ponto.acessibilidade = acessibilidade
                    novo_ponto.morada = morada
                    self.p_turistico.append(novo_ponto)
            return "Dados carregados com sucesso."
        except FileNotFoundError:
            return "Arquivo não encontrado."
        except json.JSONDecodeError:
            return "Erro ao decodificar o arquivo JSON."

    def atualizar_dados(self, nome_arquivo):
        """
        Guardar no ficheiro json os dados
        :param nome_arquivo: Nome do arquivo json para carregar os dados
        :return: Guarda no ficheiro json os dados da linked list
        """
        try:
            data = []
            current = self.p_turistico.head
            while current is not None:
                ponto = current.data
                data.append({
                    "nome": ponto.nome,
                    "designacao": ponto.designacao,
                    "visitas": ponto.visitas,
                    "media": ponto.media,
                    "categorias": ponto.categorias,
                    "coordenadas": ponto.coordenadas,
                    "avaliacao": ponto.avaliacao,
                    "atividades": ponto.atividades,
                    "acessibilidade": ponto.acessibilidade,
                    "morada": ponto.morada
                })
                current = current.next

            with open(nome_arquivo, 'w') as arquivo:
                json.dump(data, arquivo)
            return "Dados atualizados com sucesso."
        except IOError:
            return "Erro ao escrever no arquivo JSON."

    def bubble_sort(self, pontos, key=None):
        if pontos is None:
            return None

        swapped = True
        while swapped:
            swapped = False
            current = self.p_turistico.head
            while current.next is not None:
                if key(current.data) > key(current.next.data):
                    current.data, current.next.data = current.next.data, current.data
                    swapped = True
                current = current.next

        # Criar uma nova lista ordenada
        sorted_list = []
        current = self.p_turistico.head
        while current is not None:
            sorted_list.append(current.data)
            current = current.next

        return sorted_list

    def calcular_distancia(self, x0, y0, x1, y1):
        """
        Calcular a distancia entre 2 pontos no plano
        :param x0: X do primeiro ponto
        :param y0: Y do primeiro ponto
        :param x1: X do segundo ponto
        :param y1: Y do segundo ponto
        :return: A distancia entre 2 pontos no plano
        """
        x0 = float(x0)
        y0 = float(y0)
        x1 = float(x1)
        y1 = float(y1)

        a = (x1 - x0) ** 2 + (y1 - y0) ** 2
        b = math.sqrt(a)
        return b

    def merge_sort(self, array):
        if len(array) <= 1:
            return array

        mid = len(array) // 2
        left = array[:mid]
        right = array[mid:]

        left = self.merge_sort(left)
        right = self.merge_sort(right)

        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            left_visitas = int(left[i]["visitas"]) if left[i]["visitas"] else 0
            right_visitas = int(right[j]["visitas"]) if right[j]["visitas"] else 0

            if left_visitas > right_visitas:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        while i < len(left):
            result.append(left[i])
            i += 1

        while j < len(right):
            result.append(right[j])
            j += 1

        return result

    def validar_categorias(self, categorias):
        categ = ("natureza", "cultura", "aventura", "gastronomia")
        if categorias not in categ:
            return False
        return True

    def calcular_distancia_entre_pontos(self, ponto1, ponto2):
        """
        Calcular a distância entre dois pontos turísticos.
        :param ponto1: Nome do primeiro ponto turístico
        :param ponto2: Nome do segundo ponto turístico
        :return: Distância entre os dois pontos
        """
        coordenadas_ponto1 = None
        coordenadas_ponto2 = None

        current = self.p_turistico.head
        while current is not None:
            ponto = current.data
            if ponto.nome == ponto1:
                coordenadas_ponto1 = ponto.coordenadas
            elif ponto.nome == ponto2:
                coordenadas_ponto2 = ponto.coordenadas

            if coordenadas_ponto1 and coordenadas_ponto2:
                break

            current = current.next

        if coordenadas_ponto1 and coordenadas_ponto2:
            distancia = self.calcular_distancia(coordenadas_ponto1[0], coordenadas_ponto1[1],
                                                coordenadas_ponto2[0], coordenadas_ponto2[1])
            return distancia
        else:
            return None
