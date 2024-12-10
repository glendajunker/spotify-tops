import pytest
import json

from unittest import mock
from spotify_tops import get_access_token, get_top_item, get_time_range, get_top_items_str


@mock.patch("builtins.input")
def test_get_access_token(mocked_input):
    with pytest.raises(SystemExit):
        mocked_input.side_effect = ["invalid_access_code"]
        get_access_token()


def test_get_top_item():
    with pytest.raises(SystemExit):
        get_top_item("artists", "invalid_token", "4 weeks")


@mock.patch("builtins.input")
def test_get_time_range(mocked_input):
    mocked_input.side_effect = ["4 weeks"]
    assert get_time_range() == ("short_term", "4 weeks")

    mocked_input.side_effect = ["1 year"]
    assert get_time_range() == ("long_term", "year")

    mocked_input.side_effect = ["6 months"]
    assert get_time_range() == ("medium_term", "6 months")


def test_get_top_items_str():
    with open("mocked_data.json") as f:
        data = json.load(f)
        top_artists = data.get("top_artists")
        top_tracks = data.get("top_tracks")
        
        assert get_top_items_str(top_artists, top_tracks, "4 weeks") == "🎧 These are your top 3 artists of the last 4 weeks on Spotify:\n1 Arctic Monkeys\n2 P!nk\n3 Papa Roach\n🎧 These are your top 3 tracks of the last 4 weeks on Spotify:\n1 Drive by Incubus\n2 Lights Out by Royal Blood\n3 Scars by Papa Roach"
