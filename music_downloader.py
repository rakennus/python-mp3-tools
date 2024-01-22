import json
import yt_dlp
import requests
import sys

import os
import eyed3

URL = sys.argv[1]

# yt-dlp -o "%(playlist_index)s %(title)s" -x --embed-thumbnail --audio-format mp3 --embed-metadata ""

ydl_opts = {
        'outtmpl': 'Music/%(uploader)s/%(playlist_title)s/%(playlist_index)s %(title)s',
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            }]
        }


def add_metadata_to_mp3(mp3_file_path, index, artist=None, album=None, track_number=None, artwork=None):
    audiofile = eyed3.load(mp3_file_path)

    audiofile.tag.title = info['entries'][index]['title']

    if artist:
        audiofile.tag.artist = artist
    if album:
        audiofile.tag.album = album
  
    file_name = os.path.basename(mp3_file_path)
    words = file_name.split()
    if words:
        audiofile.tag.track_num = int(words[0])
    else:
        return None  # Return None if the file name is empty or doesn't contain any words

    if artwork:
        audiofile.tag.images.set(3, open(artwork, 'rb').read(), 'image/jpg')

    audiofile.tag.save()

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

    url = info['thumbnails'][1]['url']
    save_path = album_directory + "cover.jpg"

    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

    metadata_dict = {
        'artist': info['entries'][0]['channel'],
        'album': info['title'],
        'artwork': album_directory + "cover.jpg",
    }

    add_metadata_to_mp3_files_in_directory(album_directory, metadata_dict)
