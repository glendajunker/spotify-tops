# Spotify Tops

Spotify Tops is a tool that allows Spotify users to view their top 10 artists and tracks from the last year, 6 months or 4 weeks.

## Requirements

1. [Python](https://www.python.org/)
2. A [Spotify App](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app) set up in your Spotify account

Make sure that you set the Redirect URI in your Spotify App to match the `redirect_url` used in the project: `http://localhost:8888/callback`

## Installation

Install the project dependencies with `pip`:

```bash
pip install -r requirements.txt
```

## How to run

1. Copy the `.env.example` file, rename it to `.env` and use your actual Spotify API credentials:

`CLIENT_ID`: Your Spotify Client ID

`CLIENT_SECRET`: Your Spotify Client Secret

2. Execute the program

```bash
python3 project.py
```

## References

[Spotify WebAPI Documentation](https://developer.spotify.com/documentation/web-api)
