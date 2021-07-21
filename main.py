import ChessScript
import Video
import VideoUploader
import NarratedScript
import io
import os
import sqlite3

# Service Account JSON Key downloaded from https://console.cloud.google.com/iam-admin/serviceaccounts
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service_account_key.json'

with sqlite3.connect('my-test.db') as sqliteConnection:
    rows = sqliteConnection.execute("""
        SELECT id, pgn
        FROM ChessGame
        WHERE youtube_response is NULL
        ORDER BY (whiteElo + blackElo) DESC
        LIMIT 1
    """)
    for row in rows:
        id = row[0]
        pgn = row[1]
        handle = io.StringIO(pgn)
        chess_script = ChessScript.ChessScript(handle)
        video_title = chess_script.get_title()
        print(video_title)
        narrated_script = NarratedScript.NarratedScript(chess_script)
        filename = Video.to_video(narrated_script)
        youtube_response = VideoUploader.upload(filename, video_title)
        print(youtube_response)
        sqliteConnection.execute("""
                UPDATE ChessGame
                SET youtube_response = ?
                WHERE id = ?
            """,
            (str(youtube_response), id))
