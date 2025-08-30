import vlc

class TrackPlayback():
    def __init__(self, volume: int):
        super().__init__()
        
        instance = vlc.Instance("--no-audio-time-stretch", "--file-caching=100", "--aout=pulse")
        self.track = instance.media_player_new()

        #self.track = vlc.MediaPlayer()
        self.volume = volume
        self.change_volume(self.volume)

    def play_track(self, song: str) -> None:
        self.track.set_media(vlc.Media(song))
        self.track.play()

    def resume_track(self) -> None:
        self.track.play()

    def pause_track(self) -> None:
        self.track.pause()

    def get_track_runtime(self) -> tuple:
        cur_time = self.track.get_time()
        total_length = self.track.get_length()
        relative_pos = self.track.get_position()

        return (cur_time, total_length, relative_pos)

    def change_volume(self, volume_change: int) -> None:
        self.volume = volume_change
        self.track.audio_set_volume(self.volume)
    
    def get_volume(self) -> int:
        return self.volume

def audio_instance(volume: str):
    return TrackPlayback(volume)
