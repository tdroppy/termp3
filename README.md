# termp3
--------------------------------------------------
## About

termp3 is a very simple terminal based mp3 player which soon will support
many more file types, playlists, audio visualizers and more maybe

Be warned there is like no UI at the moment as I am mainly just uploading this
to be able to work on it from multiple devices

The current packages being used are as follows:
  - textual (for the lack of UI)
  - python-vlc (for audio control and playback)
  - mutagen (for handling mp3 metadata)

As of right now I have no idea if windows or mac will run this, in theory it would because
its python but... idk??
I have build it to run on linux in the kitty terminal so mileage will vary

## Installation

Installation is fairly simple:

In your terminal use the following commands

$ git clone https://github.com/tdroppy/termp3.git
$ cd termp3
$ python -m venv ./            # Creates a virtual environment
$ ./bin/pip install -r requirements.txt    #Installs libraries

## Usage

### To Run:
Option 1: Use the convenient bash script provided to you :D
Option 2: $ ./bin/python -m main

In the program, the "P" button plays the track
the "S" button stops the track
"+" and "-" are volume control (This will be changed eventually I swear)

### Adding Audio Files:
Just drop your favorite .mp3 files in /audio/ and termp3 will add them 
automatically upon start up.
