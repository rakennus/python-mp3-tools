import json
import yt_dlp
import requests
import sys
import os
import eyed3

from PIL import Image
from io import BytesIO

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TRCK, error

URL = sys.argv[1]

cover_image_data = b''

ydl_opts = {
        'outtmpl': 'Music/%(uploader)s/%(playlist_title)s/%(playlist_index)s %(title)s',
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            }]
        }


def add_metadata_to_mp3(mp3_file_path, index, artist=None, album=None, track_number=None, artwork=None):
    print(mp3_file_path)

    # Load the audio file using mutagen.
    audio = MP3(mp3_file_path, ID3=ID3)
    tags = ID3(mp3_file_path)

    image_bytearray = cover_image_data

    audio.tags.delall("APIC") # Delete every APIC tag (Cover art)
    audio.tags.add(APIC(mime='image/png',type=3,desc=u'Front cover',data=image_bytearray))

    audio['TRCK'] = TRCK(encoding=3, text=str())

    audio.save()  # save the current changes

def add_metadata_to_mp3_files_in_directory(album_directory, metadata_dict):
    # Get a list of filenames in the folder
    files = os.listdir(album_directory)
    
    # Use a for loop with enumerate to get the index and filename
    for index, filename in enumerate(files):
        # Check if the file has a .mp3 extension (case-insensitive)
        if filename.lower().endswith(".mp3"):
            print(f"Index: {index}, File: {filename}")
            mp3_file_path = os.path.join(album_directory, filename)
            add_metadata_to_mp3(mp3_file_path, index, **metadata_dict)

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(URL)

    info = ydl.extract_info(URL, download=False)
    album_directory = "Music/" + info['entries'][0]['channel'] + "/" + info['title'] + "/"
    
    with open(album_directory + info['title'] + '.json', 'w') as fp:
        json.dump(info, fp)

    response = requests.get(info['thumbnails'][1]['url'])
    if response.status_code == 200:
        cover_image_data = response.content
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

    metadata_dict = {
        'artist': info['entries'][0]['channel'],
        'album': info['title'],
        'artwork': album_directory + "cover.jpg",
    }

    add_metadata_to_mp3_files_in_directory(album_directory, metadata_dict)
