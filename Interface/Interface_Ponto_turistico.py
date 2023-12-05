from Sistema import Sistema_Ponto_Turistico


def exibir_menu():
    print("Selecione uma opção:")
    print("1. Adicionar ponto de interesse")
    print("2. Alterar ponto de interesse")
    print("3. Pesquisar pontos de interesse")
    print("4. Avaliar visita a ponto de interesse")
    print("5. Assinalar visita a ponto de interesse")
    print("6. Consultar estatísticas de visitas aos pontos de interesse")
    print("7. Obter sugestões de visitas a pontos de interesse")
    print("8. Listar pontos de interesse")
    print("9. Obter ponto de interesse")
    print("10. Remover ponto de interesse")
    print("11. Descrição do concelho")
    print("0. Sair")


def main():
    # Carregar dados do ficheiro JSON
    pontos = Sistema_Ponto_Turistico.Sistema()
    pontos.carregar_dados("Ponto_turistico_data.json")

    opcao = None

    while opcao != "0":
        exibir_menu()
        opcao = input("Opção selecionada: ")

        if opcao == '1':
            nome = input("Nome do ponto: ")
            designacao = input("Designação do ponto: ")
            morada = input("Morada do ponto: ")
            latitude = input("Latitude: ")
            longitude = input("longitude: ")
            coordenadas = [latitude, longitude]
            categoria = input("natureza, cultura, aventura, gastronomia \n Categorias do ponto: ")
            acessibilidade = input("Acessibilidade do ponto: ")
            atividades = input("Atividades do ponto: ")

            print(pontos.adicionar_ponto(nome, designacao, morada, coordenadas,
                                         categoria, 0, None, None, acessibilidade, atividades))

        elif opcao == '2':
            nome = input("Nome do ponto: ")
            designacao = input("Designação do ponto: ")
            morada = input("Morada do ponto: ")
            latitude = input("Latitude: ")
            longitude = input("longitude: ")
            coordenadas = [latitude, longitude]
            categoria = input("natureza, cultura, aventura, gastronomia \n Categorias do ponto: ")
            acessibilidade = input("Acessibilidade do ponto: ")
            atividades = input("Atividades do ponto: ")

            print(pontos.alterar_ponto(nome, designacao, morada, coordenadas, categoria, acessibilidade, atividades))

        elif opcao == '3':
            categoria = input("natureza, cultura, aventura, gastronomia \n Categorias do ponto: ")
            print(pontos.pesquisar_por_categoria(categoria))

        elif opcao == '4':
            nome = input("Nome do ponto: ")
            rate = int(input("Pontuação: "))
            print(pontos.avaliar_experiencia(nome, rate))

        elif opcao == '5':
            nome = input("Nome do ponto: ")
            print(pontos.assinalar_visita(nome))

        elif opcao == '6':
            print(pontos.consultar_estatisticas())

        elif opcao == '7':
            lati = float(input("Inserir latitude(x): "))
            long = float(input("Inserir longitude(y):  "))
            print(pontos.sugerir_pontos_interesse([lati, long]))

        elif opcao == '8':
            print(pontos.listar_pontos())

        elif opcao == '9':
            nome = input("Nome do ponto: ")
            print(pontos.obter_ponto(nome))

        elif opcao == '10':
            nome = input("Nome do ponto: ")
            print(pontos.remover_ponto(nome))

        elif opcao == '11':
            print("O concelho da Lagoa está situado na ilha de São Miguel, nos Açores, e é reconhecido pela "
                  "sua beleza natural impressionante e encantadores pontos turísticos. A Lagoa é uma das nove ilhas do "
                  "arquipélago dos Açores e proporciona uma combinação perfeita de paisagens deslumbrantes, "
                  "história rica e autenticidade cultural.")

        elif opcao == '0':
            print("Saiu \nDados guardados")
        else:
            print("Opção inválida. Por favor, tente novamente.")

    # Guardar dados para o ficheiro JSON
    pontos.atualizar_dados("Ponto_turistico_data.json")
