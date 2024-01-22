import os, sys, fnmatch

from PIL import Image
from io import BytesIO

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

folder_path = sys.argv[1]
mp3_files = []

for root, dirs, files in os.walk(folder_path):
    for file in fnmatch.filter(files, '*.mp3'):
        mp3_files.append(os.path.join(root, file))

for index, mp3_file in enumerate(mp3_files, 1):
    print(f"Processing file {index}: {mp3_file}")

    # Load the audio file using eyed3.
    audio = MP3(mp3_file, ID3=ID3)
    tags = ID3(mp3_file)

    if tags.getall('APIC'):
        image_data = tags.getall('APIC')[0].data
        image = Image.open(BytesIO(image_data))

        width, height = image.size
        left = (width - height) // 2
        right = left + height

        cropped_image = image.crop((left, 0, right, height))

        image_bytes_io = BytesIO()
        cropped_image.save(image_bytes_io, format="PNG")

        image_bytearray = bytes(image_bytes_io.getvalue())

        audio.tags.delall("APIC") # Delete every APIC tag (Cover art)
        audio.tags.add(APIC(mime='image/png',type=3,desc=u'Front cover',data=image_bytearray))

        audio.save()  # save the current changes

    else:
        print('No album cover found in the MP3 file.')
