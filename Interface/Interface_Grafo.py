from Sistema import Sistema_Grafo


def exibir_menu():
    print("\nSelecione uma opção:")
    print("1. Consultar a rede de circulação")
    print("2. Acrescentar vertices")
    print("3. Remover vertices")
    print("4. Acrescentar arestas")
    print("5. Remover arestas")
    print("6. Consultar vertices")
    print("7. Consultar arestas")
    print("8. Consultar pontos críticos da via de circulação")
    print("9. Interromper via de circulação")
    print("10. Obter itinerário")
    print("11. Consultar rotas para percursos de carro")
    print("0. Sair")


def main():
    # Carregar dados do ficheiro JSON
    rede = Sistema_Grafo.Sistema()
    rede.load_from_json("Grafo_data.json")

    opcao = None

    while opcao != "0":
        exibir_menu()
        opcao = input("Opção selecionada: ")


        if opcao == "1":
            print(rede)
            print(rede.mapa_city())

        elif opcao == "2":
            vertice = input("Nome do Ponto de interesse: ")
            print(rede.add_ponto_interresse(vertice))

        elif opcao == "3":
            vertice = input("Nome do Ponto de interesse: ")

            print(rede.remove_ponto_interresse(vertice))

        elif opcao == "4":
            vertice_1 = input("Nome do primeiro Ponto de interesse: ")
            vertice_2 = input("Nome do segundo Ponto de interesse: ")
            distancia = float(input("Distancia : "))
            sentido = int(input("Se a estrada for de duplo sentido insira 2: "))
            v_min = int(input("velocidade minima: "))
            v_max = int(input("velocidade maxima: "))
            print(rede.add_rua(vertice_1, vertice_2, distancia, v_min, v_max, sentido))

        elif opcao == "5":
            vertice_1 = input("Nome do primeiro Ponto de interesse: ")
            vertice_2 = input("Nome do segundo Ponto de interesse: ")

            print(rede.remove_rua(vertice_1, vertice_2))

        elif opcao == "6":
            print(rede.get_pontos_interresse())

        elif opcao == "7":
            print(rede.get_ruas())

        elif opcao == "8":
            max_internal_degree_vertices = rede.internal_degree_centrality()
            print("Vertices com maior centralidade de grau interno:", max_internal_degree_vertices)

            max_closeness_vertices = rede.closeness_centrality()
            print("Vertices com maior centralidade de proximidade:", max_closeness_vertices)

            max_external_degree_vertices = rede.external_degree_centrality()
            print("Vertices com maior centralidade de grau externo:", max_external_degree_vertices)

        elif opcao == "9":
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

        elif opcao == "10":
            vertice_1 = input("Nome do primeiro Ponto de interesse: ")
            vertice_2 = input("Nome do segundo Ponto de interesse: ")
            print(rede.obter_itinerario(vertice_1, vertice_2))

        elif opcao == "11":
            pontos_interesse = input("Digite os nomes dos pontos de interesse separados por vírgula: ")
            lista_pontos_interesse = pontos_interesse.split(",")
            rede.consultar_rotas_carro(lista_pontos_interesse)

        elif opcao == "0":
            print("Saiu \nDados guardados")
        else:
            print("Opção inválida. Por favor, tente novamente.")

    # Guardar dados para o ficheiro JSON
    rede.save_to_json("Grafo_data.json")
