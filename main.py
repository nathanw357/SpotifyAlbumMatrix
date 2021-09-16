import requests
import time
import sys
from pprint import pprint
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = 'BQAf1xP2c3qzQpLjYIHwMKrBKJykE9-hlkmtrk1GwX9XbQsrWk5bzcUf4LI7w6oFa61bIsqXvUkaJievM5Tyyao82v0qesv6SFxKZK8eXnSpI4WAEv4n6_wYl-4BV5jtu5aBSv1_pVOjgfkjgrzemSAMZadUj3ZTmFdMSXWbHlLzKVsadkKvsGHUQGWQcajZxB8DvQeG9JOqtEWKgk07LKGRnfdSx8SBOVSn-zRptrEgGOysNJFYkN2Euo81yLjKGbWtwCDu4U3coYG5s2fzcM9ooGOSzVmfJIf-bbZIm4sH'


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    album_images = json_resp['item']['album']['images'][2]

    link = json_resp['item']['external_urls']['spotify']

    current_track_info = {
        "id": track_id,
        "image": album_images['url'],

    }

    return current_track_info


def main():
    # Configuration for the matrix
    options = RGBMatrixOptions
    options.rows = 64
    options.cols = 64
    options.gpio_slowdown = 4
    options.hardware_mapping = 'adafruit-hat'

    matrix = RGBMatrix(options = options)
    
    current_track_id = None
    while True:
        current_track_info = get_current_track(ACCESS_TOKEN)
        if current_track_info['id'] != current_track_id:
            img_data = requests.get(current_track_info['image']).content
            with open('album_cover.jpg', 'wb') as handler:
                handler.write(img_data)

            # Make image fit

            image.thumbnail((64,64), Image.ANTIALIAS)

            matrix.SetImage(image.convert('RGB'))

            try:
                print("Press CTRL+C to STOP!")
                while True:
                    time.sleep(100)
            except KeyboardInterrupt:
                sys.exit(0)

    
          #  pprint(
          #      current_track_info,
          #      indent=4,
          #  )

        current_track_id = current_track_info['id']


        time.sleep(1)


if __name__ == '__main__':
    main()


