import sqlite3
import urllib.request, urllib.error, urllib.parse
import re
import chess.pgn
import io

GAME_DELIMITER = '[Event "'

with sqlite3.connect('my-test.db') as sqliteConnection:
    sqliteConnection.execute("""
        CREATE TABLE IF NOT EXISTS ChessGame (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            pgn TEXT,
            white TEXT,
            black TEXT,
            date TEXT,
            round TEXT,
            whiteElo INTEGER,
            blackElo INTEGER,
            youtube_response TEXT,
            UNIQUE(date, white, black, round)
        );
    """)

    url = 'https://theweekinchess.com/a-year-of-pgn-game-files'
    response = urllib.request.urlopen(url)
    web_content = response.read().decode('utf-8')
    for match in re.finditer(r'href="([^"]*.pgn)"', web_content):
        url = 'https://theweekinchess.com/{0}'.format(match.group(1))
        print("downloading {0}".format(url))
        response = urllib.request.urlopen(url)
        pgn_content = response.read().decode('utf-8')
        games = []
        for single_game_pgn in pgn_content.split(GAME_DELIMITER):
            if single_game_pgn == '':
                continue
            single_game_pgn = "{0}{1}".format(GAME_DELIMITER, single_game_pgn)
            with io.StringIO(single_game_pgn) as game_io:
                game = chess.pgn.read_game(game_io)
                headers = game.headers
                games.append((
                    single_game_pgn,
                    headers["White"],
                    headers["Black"],
                    headers["Date"],
                    headers["Round"],
                    headers.get("WhiteElo", default=0),
                    headers.get("BlackElo", default=0),
                ))
        sqliteConnection.executemany("""
            INSERT OR IGNORE INTO ChessGame
            (pgn, white, black, date, round, whiteElo, blackElo)
            VALUES
            (  ?,     ?,     ?,    ?,     ?,         ?,        ?)
            """,
            games)
        break