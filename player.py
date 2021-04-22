#https://stackoverflow.com/questions/46758360/how-to-play-streaming-audio-from-internet-radio-on-python-3-5-3

import vlc
import json

class Player:
    
    def __init__(self):
        file = open('songs.json')
        self.URL_LIST = json.load(file)
        
        instance = vlc.Instance()
        media_list = instance.media_list_new(self.URL_LIST)
        
        self.player = instance.media_list_player_new()
        self.player.set_media_list(media_list)
        self.play_stop()

    def next_song(self):
        self.player.next()
    
    def previous_song(self):
        self.player.previous()
    
    def play_stop(self):
        if self.player.is_playing():
            self.playing = False
            self.player.stop()
        else:
            self.playing = True
            self.player.play()
    
    def is_playing(self):
        return self.playing
    
    def set_volume(self, mvalue):
        self.player.get_media_player().audio_set_volume(mvalue)
        
    def get_volume(self):
        return self.player.get_media_player().audio_get_volume()
    
    def info(self):
        media = self.player.get_media_player().get_media()
        media.parse_with_options(vlc.MediaParseFlag.network, 1)
        
        text = ""
        for i in range(13):
            meta = media.get_meta(i)
            if meta is not None:
                text = text + meta + " "
        return text