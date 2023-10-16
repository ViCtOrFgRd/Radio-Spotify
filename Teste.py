import datetime

def find_chave(chave): 
    f = open('env.yml','r')
    conteudo = f.read()
    f.close()    
    indice_palavra = conteudo.index(chave)
    if indice_palavra != -1:
        indice_virgula = conteudo.find(',', indice_palavra)
        if indice_virgula != -1:
            resultado = conteudo[indice_palavra+len(chave):indice_virgula]
        else:
            resultado = conteudo[indice_palavra+len(chave):]
        return (resultado.replace(';',''))
    else:
        print('A palavra não foi encontrada no arquivo.')

def conversor_date_time(min,max):

    min_time = datetime.datetime.strptime(min, '%H:%M:%S').time()
    max_time = datetime.datetime.strptime(max, '%H:%M:%S').time()
    return min_time, max_time

def horario(mensagem):
    agora = datetime.datetime.now()
    ano = agora.year 
    mes = agora.month 
    dia = agora.day
    date = str(dia) + '/' + str(mes) + '/' + str(ano)
    horario_atual = datetime.datetime.now().time()

    data = find_chave("Day")
    print(data)
    if data == "!":
        # Abrir o arquivo em modo de leitura
        with open('env.yml', 'r') as file:
            # Ler o conteúdo do arquivo
            conteudo = file.read()

        # Procurar a palavra no conteúdo
        if data in conteudo:
            # Abrir o arquivo novamente em modo de escrita
            with open('env.yml', 'w') as file:
                # Escrever o conteúdo original
                file.write(conteudo)

                # Escrever o novo texto após a palavra encontrada
                file.write(date)

                print("Texto adicionado com sucesso.")
        else:
            print("Palavra não encontrada no arquivo.")










    if mensagem == 'Day':
        limite_inferior, limite_superior = conversor_date_time(find_chave('Time_day_morning'), find_chave('Time_day_morning_max'))
        if limite_inferior <= horario_atual <= limite_superior:
            print('Mensagem de Bom Dia!!')
        else:
            return "Não é o momento" 
    elif mensagem =='Tarde':
        limite_inferior, limite_superior = conversor_date_time(find_chave('Time_day_afternoon'), find_chave('Time_day_afternoon_max'))
        if limite_inferior <= horario_atual <= limite_superior:
            print('Mensagem de Boa Tarde!!')
        else:
            return "Não é o momento"
    elif mensagem == 'Noite':
        limite_inferior, limite_superior = conversor_date_time(find_chave('Time_day_night'), find_chave('Time_day_night_max'))
        if limite_inferior <= horario_atual <= limite_superior:
            print('Mensagem de Boa Noite!!')
        else:
            return "Não é o momento"

print(horario('Day'))