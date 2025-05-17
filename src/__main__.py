import os
from dotenv import load_dotenv
import discogs_client

load_dotenv()

TOKEN = os.getenv('DISCOGS_USER_TOKEN')
if not TOKEN:
    raise RuntimeError("Missing DISCOGS_USER_TOKEN in environment")

d = discogs_client.Client(
    'MyApp/1.0 +https://example.com',
    user_token=TOKEN
)

# fill these out separately
EXCLUDE_TITLES  = {'Song A', 'Song B', 'My Favorite Song'}
EXCLUDE_ARTISTS = {'Artist X', 'Artist Y'}

LABEL_NAME = 'Your Label Name'
releases = d.search(label=LABEL_NAME, type='release')

filtered_tracks = []
for rel in releases:
    try:
        tracklist = rel.tracklist
    except Exception:
        continue

    for track in tracklist:
        title   = track.title
        artists = [a.name for a in getattr(track, 'artists', [])]

        if title in EXCLUDE_TITLES or any(a in EXCLUDE_ARTISTS for a in artists):
            continue

        filtered_tracks.append({
            'release_title': rel.title,
            'track_title':   title,
            'artists':       artists,
            'year':          getattr(rel, 'year', None),
            'country':       getattr(rel, 'country', None),
        })

for t in filtered_tracks:
    print(f"{t['track_title']} — {', '.join(t['artists'])} "
          f"({t['release_title']}, {t['year']}, {t['country']})")
