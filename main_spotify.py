from spotipy.oauth2 import SpotifyOAuth
import spotipy
import spotipy.util as util
import psutil
import os
import time
from main_voiceover import find_chave

#Radio Spotify 

#Executar o spotify
#Verificar se está aberto
def Open_Program():
    connect_Disp(devices)
    print(devices)
    processo = False
    erro = 0
    while processo == False:
        processos = psutil.process_iter()
        spotify_em_execucao = False
        if erro == 5:
            processo = True
            with open('erro.txt','w') as arquivo:
                arquivo.write("Erro 1 - Problema ao abrir o Spotify \n"
                             '\n'
                            'Verificar o Spotify')
        else:
            for processo in processos:
                if "spotify" in processo.name().lower():
                    spotify_em_execucao = True
                    break

            if spotify_em_execucao:
                print("O Spotify está em execução.")
                time.sleep(10)
            else:
                print("O Spotify não está em execução.")
                processo = False
                erro = erro + 1
                os.system('Spotify')
                time.sleep(2)
                
# Configura as credenciais da API do Spotify [Spotify Desenvolvedor]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=find_chave('client_id_standard'),
                                            client_secret=find_chave('client_secret_standard'),
                                            redirect_uri=find_chave('redirect_uri_standard'),
                                            scope=find_chave('scope_standard'),
                                            requests_timeout=100))

# Obtém os dispositivos conectados à sua conta
devices = sp.devices()
#Conexão do Dispositivo
def connect_Disp(devices):
    try:
        if devices['devices'][0]['is_active'] == False:
            device_id = []
            track_uri=find_chave('track_uri_standard')
            sp.start_playback(device_id= find_chave('ID_DEVICE'), uris=[track_uri])
            print(devices)
        elif len(devices['devices']) > 0:
            # Escolhe o primeiro dispositivo ativo da lista
            print(devices['is_active'])
            device_id = devices['devices'][0]['id']
            return device_id
            
        else:
            with open('erro.txt','w') as arquivo:
                arquivo.write("Erro 2 - Problema de Autenticação \n"
                             '\n'
                            'Token incorreto\n'
                            'Spotify sem autenticar\n'
                            'Usuario não logado')
    except:
        with open('erro.txt','w') as arquivo:
                arquivo.write("Erro 2 - Problema de Autenticação \n"
                             '\n'
                            'Token incorreto\n'
                            'Spotify sem autenticar\n'
                            'Usuario não logado')

#Seleção de uma Musica
def choice_onetrack():
    try:
        device_id = []
        device_id = connect_Disp(device_id)
        padrao = 'spotify:track:'
        http = input('ID da Musica:').split('/')
        id = http[4].split('?')[0]
        track_uri = ''.join([padrao,id])
        sp.start_playback(device_id=device_id, uris=[track_uri])
    except:
        with open('erro.txt','w') as arquivo:
                arquivo.write("Erro 3 - Musica não encontrada \n"
                             '\n'
                            'Url com problema\n'
                            'Url incorreta')
        choice_onetrack()

#Seleção de uma Playlist
def playlist_Music():
    try:
        device_id = []
        device_id = connect_Disp(device_id)
        http = input('ID da Playlist:').split('/')
        playlist_id = http[4].split('?')[0]
        print(playlist_id)
        results = sp.playlist(playlist_id, fields="tracks")
        tracks = results['tracks']['items']
        sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
    except:
            with open('erro.txt','w') as arquivo:
                    arquivo.write("Erro 4 - Playlist não encontrada \n"
                                '\n'
                                'Url com problema\n'
                                'Url incorreta')
            playlist_Music()

def playlist_Padrao():
    try:
        connect_Disp(devices)
        device_id = []
        device_id = find_chave("ID_DEVICE")
        #Alterar o Device_id de acordo com computador
        playlist_id = find_chave("Playlist_standard")
        
        #playlist_id = '37i9dQZF1DXasHMl0oGqXp'
        
        results = sp.playlist(playlist_id, fields="tracks")
        tracks = results['tracks']['items']
        sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}",device_id=device_id)
    except:
            with open('erro.txt','w') as arquivo:
                    arquivo.write("Erro 4 - Playlist não encontrada \n"
                                '\n'
                                'Url com problema\n'
                                'Url incorreta')
            
#Pause Music
def pause_music():
    sp.pause_playback()

#Play Music
def play_music():
     sp.start_playback()

#Proxima Music
def next_music():
    sp.next_track()

#Voltar Musica
def back_music():
    sp.previous_track()

#Ativar ou Desativar ordem aleatorio
def ordem_aleatorio():
    current_playback = sp.current_playback()
    shuffle_state = current_playback['shuffle_state']
    if shuffle_state:
        sp.shuffle(False)
    else:
        sp.shuffle(True)

#Repetir Musica
def repeat():
    current_playback = sp.current_playback()
    repeat_state = current_playback['repeat_state']
    if repeat_state == 'context':
        print('A repetição de contexto está ativada.')
        return sp.repeat('off')
    elif repeat_state == 'track':
        print('A repetição de faixa está ativada.')
        return sp.repeat("context")
    else:
        print('A repetição está desativada.')
        return sp.repeat('context')

#Busca informação da Musica
def music_play():
    # Obtém informações sobre o player atual do Spotify
    current_playback = sp.current_playback()

    # Verifica se o player está ativo e tocando uma música
    if current_playback is not None:
        # Obtém informações sobre a música atual
        current_track = current_playback['item']
        track_name = current_track['name']
        artists = ', '.join([artist['name'] for artist in current_track['artists']])
        album_name = current_track['album']['name']

        # Exibe as informações sobre a música atual
        print(f"Tocando agora: {track_name} - {artists} ({album_name})")
        return track_name, artists
    else:
        print('Nenhuma música está tocando no momento.')

def painel_Music():
    valor = (music_play())

def Get_Duration():
    try:
        current_playback = sp.current_playback()

        if current_playback and current_playback['currently_playing_type'] == 'track':
            track = current_playback['item']
        progress_ms = current_playback['progress_ms']
        duration_ms = track['duration_ms']
        remaining_ms = duration_ms - progress_ms
        if remaining_ms < 2000:
            return True
        else:
            return False
    except:
        pass
playback = sp.current_playback()

def Get_troca_de_musica():
    playback = sp.current_playback()
    if playback is not None:
        print('Nova música tocando:', playback['item']['name'])



