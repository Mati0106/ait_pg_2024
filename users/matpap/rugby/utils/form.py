import pandas as pd


def calculate_team_form(df: pd.DataFrame, team_name: str, current_row_index: int, n_games: int) -> float:
    # List to store the form results of the team
    team_form = []

    # Consider only the matches before the current index
    games_b = df.iloc[:current_row_index]

    # Iterate from the end to the beginning of the match list
    for _ in range(len(games_b) - 1, -1, -1):
        row1 = games_b.iloc[_]

        if row1['home_team'] == team_name or row1['away_team'] == team_name:
            # Determine winner based on margin
            if row1['margin'] > 0 and row1['home_team'] == team_name:
                team_form.append(1)
            elif row1['margin'] < 0 and row1['away_team'] == team_name:
                team_form.append(1)
            elif row1['margin'] == 0:
                team_form.append(0.5)
            else:
                team_form.append(0)

            # Stop iterating after gathering N results
            if len(team_form) == n_games:
                break

    # Calculate the average of the form results if the list is not empty
    if team_form:
        return sum(team_form) / len(team_form)
    else:
        return 0  # No data to calculate



def add_teams_form(df: pd.DataFrame, n_games: int) -> None:
    for _, row in df.iterrows():
        df.at[_, 'home_form'] = calculate_team_form(df, row['home_team'], _, n_games=n_games)
        df.at[_, 'away_form'] = calculate_team_form(df, row['away_team'], _, n_games=n_games)
