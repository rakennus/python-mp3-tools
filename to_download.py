import yt_dlp
import sys
import os
import cover
import fnmatch

URL = ["https://youtube.com/playlist?list=PLGs4pK_mA5Fdg1-jvQTt64d2A4ATcKOen&feature=shared"]

folder_path = os.path.abspath(sys.argv[1])

ydl_opts = {
        'extract_flat': 'discard_in_playlist',
        'final_ext': 'mp3',
        'format': 'bestaudio/best',
        'fragment_retries': 10,
        'ignoreerrors': 'only_download',
        'outtmpl': {'default': folder_path + '/' + '%(title)s', 'pl_thumbnail': ''},
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'nopostoverwrites': False,
                'preferredcodec': 'mp3',
                'preferredquality': '5'
                },
            {
                'add_chapters': True,
                'add_infojson': 'if_exists',
                'add_metadata': True,
                'key': 'FFmpegMetadata'
                },
            {
                'already_have_thumbnail': False, 'key': 'EmbedThumbnail'
                },
            {
                'key': 'FFmpegConcat',
                'only_multi_video': True,
                'when': 'playlist'
                }
            ],
        'retries': 10,
        'writethumbnail': True
        }

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    if(len(sys.argv) > 2):
        error_code = ydl.download(sys.argv[2])
    else:
        error_code = ydl.download(URL)

mp3_files = []

for root, dirs, files in os.walk(folder_path):
    for file in fnmatch.filter(files, '*.mp3'):
        mp3_files.append(os.path.join(root, file))

cover.make_square(mp3_files)
