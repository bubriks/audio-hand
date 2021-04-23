import vlc
import json


class Player:

    def __init__(self, run_on_start=True):
        file = open('songs.json')
        self.URL_LIST = json.load(file)

        instance = vlc.Instance()
        media_list = instance.media_list_new(self.URL_LIST)

        self.player = instance.media_list_player_new()
        self.player.set_media_list(media_list)

        if run_on_start:
            self.play_stop()

    def forward(self):
        self.player.next()

    def backward(self):
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

    def set_volume(self, value):
        self.player.get_media_player().audio_set_volume(value)

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
