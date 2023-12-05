from Sistema import Sistema_Ponto_Turistico
from Sistema import Sistema_Grafo


def exibir_menu():
    print("Selecione uma opção!")
    print("1. Consultar a rede de circulação")
    print("2. Adicionar ponto de interesse")
    print("3. Remover Ponto de interesse")
    print("4. Acrescentar arestas")
    print("5. Remover arestas")
    print("6. Consultar Pontos de interesse")
    print("7. Consultar arestas")
    print("8. Consultar estatísticas de visitas aos pontos de interesse")
    print("9. Consultar pontos críticos da via de circulação")
    print("10. Interromper via de circulação")
    print("11. Consultar rotas para percursos de carro")
    print("12. Pesquisar pontos de interesse")
    print("13. Descrição do concelho")

    print("0. Sair")


def main():
    # Carregar dados do ficheiro JSON
    rede = Sistema_Grafo.Sistema()
    pontos = Sistema_Ponto_Turistico.Sistema()
    rede.load_from_json("Grafo_data.json")
    pontos.carregar_dados("Ponto_turistico_data.json")

    opcao = None

    while opcao != "0":
        exibir_menu()
        opcao = input("Opção selecionada: ")

        if opcao == "1":
            print(rede)
            print(rede.mapa_city())

        elif opcao == "2":
            nome = str(input("Nome do ponto: "))
            designacao = str(input("Designação do ponto: "))
            morada = str(input("Morada do ponto: "))
            latitude = float(input("Latitude: "))
            longitude = float(input("longitude: "))
            coordenadas = [latitude, longitude]
            categoria = str(input("natureza, cultura, aventura, gastronomia \n Categorias do ponto: "))
            acessibilidade = str(input("Acessibilidade do ponto: "))
            atividades = str(input("Atividades do ponto: "))
            print(pontos.adicionar_ponto(nome, designacao, morada, coordenadas,
                                         categoria, 0, None, None, acessibilidade, atividades))
            print(rede.add_ponto_interresse(nome))

        elif opcao == "3":
            nome = str(input("Nome do ponto: "))
            print(rede.remove_ponto_interresse(nome))
            print(pontos.remover_ponto(nome))

        elif opcao == "4":
            vertice_1 = str(input("Nome do primeiro Ponto de interesse: "))
            vertice_2 = str(input("Nome do segundo Ponto de interesse: "))
            distancia = pontos.calcular_distancia_entre_pontos(vertice_1, vertice_2)
            sentido = int(input("Se a estrada for de duplo sentido insira 2: "))
            v_min = int(input("velocidade minima: "))
            v_max = int(input("velocidade maxima: "))
            print(rede.add_rua(vertice_1, vertice_2, distancia, v_min, v_max, sentido))

        elif opcao == "5":
            vertice_1 = str(input("Nome do primeiro Ponto de interesse: "))
            vertice_2 = str(input("Nome do segundo Ponto de interesse: "))

            print(rede.remove_rua(vertice_1, vertice_2))

        elif opcao == "6":
            print(rede.get_pontos_interresse())
            print(pontos.listar_pontos())

        elif opcao == "7":
            print(rede.get_ruas())

        elif opcao == "8":
            print(pontos.consultar_estatisticas())

        elif opcao == "9":
            max_internal_degree_vertices = rede.internal_degree_centrality()
            print("Vertices com maior centralidade de grau interno:", max_internal_degree_vertices)

            max_closeness_vertices = rede.closeness_centrality()
            print("Vertices com maior centralidade de proximidade:", max_closeness_vertices)

            max_external_degree_vertices = rede.external_degree_centrality()
            print("Vertices com maior centralidade de grau externo:", max_external_degree_vertices)

        elif opcao == "10":
            num_vias = int(input("Quantas vias deseja interromper? "))
            via_list = []
            for i in range(num_vias):
                via = input(f"Informe a {i + 1}ª via (separe os vértices por espaço): ").split()
                via_list.append(via)
            caminhos_alternativos = rede.interromper_via(via_list)
            if caminhos_alternativos:
                print("Caminhos alternativos:")
                for caminho in caminhos_alternativos:
                    print(" -> ".join(caminho))

            else:
                print("Não existem caminhos alternativos para as vias informadas.")

        elif opcao == "11":
            pontos_interesse = str(input("Digite os nomes dos pontos de interesse separados por vírgula: "))
            lista_pontos_interesse = pontos_interesse.split(",")
            rede.consultar_rotas_carro(lista_pontos_interesse)

        elif opcao == "12":
            categoria = input("natureza, cultura, aventura, gastronomia \n Categoria do ponto: ")
            print(pontos.pesquisar_por_categoria(categoria))
            vertice_1 = input("Nome do primeiro Ponto de interesse: ")
            vertice_2 = input("Nome do segundo Ponto de interesse: ")
            print(rede.obter_itinerario(vertice_1, vertice_2))

        elif opcao == "13":
            print("O concelho da Lagoa está situado na ilha de São Miguel, nos Açores, e é reconhecido pela "
                  "sua beleza natural impressionante e encantadores pontos turísticos. A Lagoa é uma das nove ilhas do "
                  "arquipélago dos Açores e proporciona uma combinação perfeita de paisagens deslumbrantes, "
                  "história rica e autenticidade cultural.\n Link1: https://byacores.com/lagoa/ \n "
                  "link2: https://www.tripadvisor.pt/Attractions-g1900300-Activities-Lagoa_Sao_Miguel_Azores.html")

        elif opcao == "0":
            print("Saiu \nDados guardados")

    # Guardar dados para o ficheiro JSON
    rede.save_to_json("Grafo_data.json")
    pontos.atualizar_dados("Ponto_turistico_data.json")
