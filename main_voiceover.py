import random
import os
from playsound import playsound
import pygame

# Função que funciona e seleciona aleatório os arquivos da pasta e trata erros (Vitor Martins)
def Get_random_voiceover():
    
    try:# Abre o arquivo txt e pega a lista de músicas tocadas
        f = open('played_voiceover.txt','r')
        played_list = sorted(list(f.read()))
        f.close()
    except:
        pass
    # Coletando a lista de músicas da pasta
    print(os.getcwd())
    directory =  os.getcwd() + r'\musics'
    musics_list = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Teste de validação caso se todas as músicas já forem tocadas
    if len(played_list) == len(musics_list):
        f = open('played_voiceover.txt','w')
        played_list = []
        for i in played_list:
            f.write(str(i))
        f.close()
        
    # Gerando número aleatório dentro do range excluindo os já tocados
    random_number = (random.choice([i for i in range(0,len(musics_list)) if str(i) not in played_list]))
    
    # Adicionando o número selecionado na lista
    played_list.append(random_number)

    # Abre o arquivo txt e atualiza a lista de músicas tocadas
    f = open('played_voiceover.txt','w')
    for i in played_list:
        f.write(str(i))
    f.close()
    
    # Tocando o áudio relacionado ao index do numero aleatório
    try:
        print(musics_list[random_number])
        path = "musics/{}".format(musics_list[random_number])
        playsound(path)
        print("Playsound Sucess")
    except:
        print(musics_list[random_number])
        print("Playsound Fail")

        #Caso Playsound Fail
        pygame.mixer.init()

        # Carregar o arquivo de áudio
        pygame.mixer.music.load(path)

        # Reproduzir o arquivo de áudio
        pygame.mixer.music.play()

        # Manter o programa em execução até que a música termine
        while pygame.mixer.music.get_busy():
            continue
    else:
        pass

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
        return(resultado.replace(';',''))
    else:
        print('A palavra não foi encontrada no arquivo.')