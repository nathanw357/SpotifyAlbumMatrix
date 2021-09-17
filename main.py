import requests
import time
import sys
import spotipy
from pprint import pprint
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth('3d31fcc6a14c40b2b492f87063852c70', '895959dea41240288d128add49a73b66', 'http://localhost.com', scope=scope))

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = 'BQCaao8A0pgVMIP_qLb-QkaQ-Ldx1Elh7gQwEA532g9pWZOcl4L7hq8cHKKkgKZ2v3Hxd8ql1maZZYdkQM5a7oCTPJjFXGi-uPeX9r5MzyjCy5dA1XhKZ5zUe3YcZeWeL5gHlFFq2JVnET9dAjwMionY9A9e5IJfvcPG4B0vHqd4NfjGlhAoJrMmemr1tyNwvnxU_JppOiWMNXQmjPqMEWRSBUXY_9BYXp3UOPIDzjgJVbV5nhNlShyqv4nkLM4lrTaPfnw3CulxlaZbYDHvRHFNK4rr6Hg-MmGK_hr15Qrc'

def get_current_track():
    results = sp.current_playback()

    track = results['item']
    track_id = results['item']['id']
    track_name = results['item']['name']
    album_images = results['item']['album']['images'][2]

    link = results['item']['external_urls']['spotify']

    current_track_info = {
        "id": track_id,
        "image": album_images['url'],

    }

    return current_track_info


def main():
    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 64
    options.cols = 64
    options.gpio_slowdown = 4
    options.hardware_mapping = 'adafruit-hat'

    matrix = RGBMatrix(options = options)
    
    current_track_id = None
    while True:
        current_track_info = get_current_track()
        if current_track_info['id'] != current_track_id:
            img_data = requests.get(current_track_info['image']).content
            with open('album_cover.jpg', 'wb') as handler:
                handler.write(img_data)

            # Make image fit
            image = Image.open('album_cover.jpg')

            image.thumbnail((64,64), Image.ANTIALIAS)

            matrix.SetImage(image.convert('RGB'))
            
          #  pprint(
          #      current_track_info,
          #      indent=4,
          #  )

        current_track_id = current_track_info['id']


        time.sleep(1)


if __name__ == '__main__':
    main()

