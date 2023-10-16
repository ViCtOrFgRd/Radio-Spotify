#Integração Entre Locução e Spotify
import main_spotify 
import main_voiceover
import time

main_spotify.Open_Program()
time.sleep(2)
main_spotify.playlist_Padrao()
#Iniciar Spotify
while True:
    time.sleep(5)
    main_spotify.music_play()
    while main_spotify.Get_Duration() == False:
        time.sleep(1)
    else:
        main_spotify.pause_music()
        main_voiceover.Get_random_voiceover()
        main_spotify.next_music()
