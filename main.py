from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Static, Button, DataTable
from textual.containers import Center, HorizontalGroup, VerticalScroll
from textual import work

from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError

import vlc
import os
import time

from track_module import audio_instance
track_playback = audio_instance(20) #global instance of TrackPlayback()

class PlaybackBar(Static):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_bar = ""
        self.progress_percent = 0
        self.bar = Static("")
        self.time_label = Static("[0 / 0 (0%)]")


    def on_mount(self, width=None, bar="") -> None:
        self._timer = self.set_interval(0.1, self.update_bar)

    def _rebuild_empty(self) -> None:
        width = max(0, self.size.width - 2)
        self.empty_bar = "-" * width

    def on_resize(self, event) -> None:
        self._rebuild_empty()
        self.update_bar()
    
    def set_progress(self, value: int) -> None:
        self.progress_percent = max(0, min(100, int(value)))

    @work(thread=True)
    def update_bar(self, width=None) -> None:
        current_time, total_length, relative_position = track_playback.get_track_runtime()
        show_progress = f"[{current_time / 1000} / {total_length / 1000} ({relative_position * 100}%)]"
        self.progress_percent = relative_position * 100

        if not self.empty_bar or len(self.empty_bar) != max(0, self.size.width - 2): #If not size that it SHOULD be
            self._rebuild_empty()

        if self.progress_percent < 0: #relative_position will return negative values if no track (kills scaling D: )
            self.progress_percent = 0 #this will temporarily fix that
        
        filled = int((self.progress_percent / 100) * len(self.empty_bar))
        inner = "#" * filled + "-" * (len(self.empty_bar) - filled) #len - filled just fills none progressed space
        final_bar = f"[{inner}]"
        self.bar.update(final_bar)
        self.time_label.update(show_progress)

    def compose(self) -> ComposeResult:
        yield self.time_label
        yield self.bar


class VolumeControl(Static):

    def __init__(self):
        super().__init__()

        self.volume = track_playback.get_volume()
        self.label = Static(str(self.volume))

    def update_vol(self) -> None:
        self.volume = track_playback.get_volume()
        self.label.update(str(self.volume))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'plus':
            track_playback.change_volume(track_playback.get_volume() + 5)
            self.update_vol()
        if event.button.id == 'minus':
            track_playback.change_volume(track_playback.get_volume() - 5)
            self.update_vol()

    def compose(self) -> ComposeResult:
        yield self.label
        yield Button("+", id='plus')
        yield Button("-", id='minus')


class Playback(HorizontalGroup):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        playbar = self.query_one(PlaybackBar)
        if event.button.id == "play":
            track_playback.resume_track()

        if event.button.id == "stop":
            track_playback.pause_track()

    def compose(self) -> ComposeResult:
        yield Button("S", id="stop")
        yield Button("P", id="play")
        yield PlaybackBar("Starting..", id="bar")


class MediaList(DataTable): #TODO: make uhhhh better maybe
    def on_mount(self) -> None:
        self.add_columns("Song-Name", "Artist", "Duration")
        self.cursor_type = "row"

        self.MEDIA_LIST = []

        self.propagate_media_table()

    def propagate_media_table(self) -> None:
        for file in os.listdir('./audio/'):
            if file.endswith(".mp3"):
                audio = MP3(f"./audio/{file}")
                track_length = time.strftime("%M:%S", time.gmtime(audio.info.length))
                track_title = audio.get('TIT2')
                track_artist = audio.get('TPE1') 

                if track_title == None:
                    track_title = str(file[:-4])

                self.MEDIA_LIST.append((f"{track_title}", f"{track_artist}", f"{track_length}"))

        for number, song in enumerate(self.MEDIA_LIST[0:], start=1):
            label = Text(str(number))
            self.add_row(*song, label=label)

    #TODO: Make find_tit2 redundant by idk saving the file data in this function
    #TODO: instead of having to find again
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        table = event.control
        row_key = event.row_key
        row_data = table.get_row(row_key)

        tit2_value = row_data[0]
        
        audio_file_name = self.find_tit2(tit2_value)

        test = self.app.query_one(Static).update(f"{audio_file_name}")

        #track.audio_instance(f"./audio/{audio_file_name[0]}", 20)
        # play_audio_selected.play_track()
        
        if audio_file_name[0].endswith("mp3"):
            track_playback.play_track(f'./audio/{audio_file_name[0]}')
        else:
            track_playback.play_track(f'./audio/{audio_file_name[0]}.mp3')
        #track_playback.change_volume(20)

        playbar = self.app.query_one("#bar", PlaybackBar)
        playbar.set_progress(0)
        playbar.play = True

    def find_tit2(self, search_text, folder="./audio/") -> list:
        matches = []
        
        for file in os.listdir('./audio/'):
            if file.endswith(".mp3"):
                audio = MP3(f"./audio/{file}")
                if audio.get('TIT2') == search_text:
                    matches.append(file)
                else:
                    pass
        matches.append(search_text)
        return matches


class TermifyApp(App):
    BINDINGS = [
        ("ctrl+c", "quit", "Quit")
    ]

    CSS = """
    * {
        background: transparent;

    }

    #play {
        border: none;
    }

    #bar {

        width: 60;
        height: 4;
        background: red;
    }

    """

    def compose(self) -> ComposeResult:
        yield Playback(id="playback") #Play, Pause button, Time Stamp, playbar
        yield MediaList() #Track list
        yield Static(f"Select") #Selected track
        yield VolumeControl() #Current volume label, + & - button

if __name__ == "__main__":
    TermifyApp().run()
