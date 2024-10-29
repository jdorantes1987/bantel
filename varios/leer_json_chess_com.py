import requests
import json
import chess.pgn
import io
import pandas as pd
import math
import numpy as np

#pd.set_option('display.max_rows', None)
def get_data_by_month(username, year, month):
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"
    print(url)
    data = requests.get(url)
    if data.status_code != 200:
        raise Exception("The following response was returned: " + str(data.status_code))
    else:
        data = json.loads(data.text)
        games = data["games"]

    all_games = []
    for game in games:
        pgn = (game['pgn'])
        pgn = io.StringIO(pgn)
        game = chess.pgn.read_game(pgn)
        all_games.append(game)
    game_list = []
    for g in all_games:
        moves = (g.mainline_moves())
        moves = [str(x) for x in moves]
        # Jackson Dorantes: le agregué estas dos líneas ya que daba error cuando existe un elemento vacio de la lista
        if not bool(moves):
            break
        white = (g.headers['White'])
        if white.lower() == username.lower():
            playing_as_white = 1
        else:
            playing_as_white = 0

        if len(moves) > 1:
            move_made = (moves[1])
        else:
            move_made = ""
        game = {"date": (g.headers["Date"]), "player_white": white, "player_black": (g.headers['Black']),
                "playing_as_white": playing_as_white, "result": (g.headers['Result']),
                "termination": (g.headers['Termination']), "moves": moves, "no_of_moves": (math.ceil(len(moves) / 2)),
                "first_move": (moves[0]), "response": move_made}

        game_list.append(game)
    game_list = pd.DataFrame(game_list)
    return game_list

def combine_months(dfs):
    df = pd.concat(dfs, ignore_index=True)
    return df

def drop_not_required_columns(df):
    # For now I am not interested in these columns
    df = df.drop(["player_white", "player_black", "moves", "termination"], axis=1)
    return df


def create_wins_column(df):
    conditions = \
        [(df["playing_as_white"] == 1) & (df["result"] == "1-0"),
         (df["playing_as_white"] == 1) & (df["result"] == "0-1"),
         (df["playing_as_white"] == 0) & (df["result"] == "1-0"),
         (df["playing_as_white"] == 0) & (df["result"] == "0-1"),
         (df["playing_as_white"] == 1) & (df["result"] == "1/2-1/2"),
         (df["playing_as_white"] == 0) & (df["result"] == "1/2-1/2")]

    values = ["Win", "Loss", "Loss", "Win", "Draw", "Draw"]

    df['my_result'] = np.select(conditions, values)
    return df

def column_by_month(df):
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = pd.DatetimeIndex(df["date"]).month
    return df



