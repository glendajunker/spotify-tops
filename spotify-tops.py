import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import webbrowser
import base64
import requests


load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

auth_url = "https://accounts.spotify.com/authorize?"
token_url = "https://accounts.spotify.com/api/token"
top_items_url = "https://api.spotify.com/v1/me/top"
redirect_url = "http://localhost:8888/callback"


def get_authorisation_code():
    auth_headers = {
        "client_id": client_id,
        "response_type": "code",  # get authorisation code from Spotify
        "redirect_uri": redirect_url,
        "scope": "user-top-read"  # request to read the user's top artists and tracks
    }

    input("🔐 Press Enter to authenticate your Spotify account.\n💡 IMPORTANT: After authentication, copy the value of the 'code' parameter from the URL and paste it back into this terminal.")

    webbrowser.open(auth_url + urlencode(auth_headers))


def get_access_token():
    while True:
        auth_code = input("🔑 Paste the authentication code here: ")

        if auth_code.strip():
            break
        else:
            print("❌ Please enter a valid code!")

    encoded_credentials = base64.b64encode(
        client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_url
    }

    try:
        token_response = requests.post(token_url, data=token_data, headers=token_headers)
        token_response.raise_for_status()
        token_data = token_response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"❌ Unable to connect to Spotify: {e}")

    return token_data["access_token"]


def get_time_range():
    time_ranges = {
        "1 year": ("long_term", "year"),
        "6 months": ("medium_term", "6 months"),
        "4 weeks": ("short_term", "4 weeks"),
    }

    while True:
        user_input = input("🗓️ Which time frame do you want to check? Available options: 1 year, 6 months, 4 weeks: ")

        if user_input in time_ranges:
            return time_ranges[user_input]
        else:
            print("❌ Please provide a valid time frame!")


def get_top_item(item, access_token, time_range):
    request_headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        top_item_response = requests.get(f"{top_items_url}/{item}?time_range={time_range}&limit=10", headers=request_headers)
        top_item_response.raise_for_status()
        top_item_data = top_item_response.json()["items"]
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"❌ Unable to get top {item}: {e}")

    return top_item_data


def print_top_items(top_artists, top_tracks, time_range):
    print(f"🎧 These are your top {len(top_artists)} artists of the last {time_range} on Spotify:")

    for index, artist in enumerate(top_artists):
        print(index + 1, artist["name"])

    print(f"🎧 These are your top {len(top_tracks)} tracks of the last {time_range} on Spotify:")

    for index, track in enumerate(top_tracks):
        track_artists = []

        for artist in track['artists']:
            track_artists.append(artist["name"])

        print(f"{index + 1} {track['name']} by {', '.join(track_artists)}")


def main():
    get_authorisation_code()

    access_token = get_access_token()
    time_range, time_range_str = get_time_range()

    top_artists = get_top_item('artists', access_token, time_range)
    top_tracks = get_top_item('tracks', access_token, time_range)

    print_top_items(top_artists, top_tracks, time_range_str)


if __name__ == "__main__":
    main()