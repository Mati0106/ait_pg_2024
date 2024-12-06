import pandas as pd

# Function to update rankings based on game results
def add_team_rankings(df: pd.DataFrame) -> None:
    # Initialize rankings starting at 80 for each team
    initial_ranking = 80
    team_rankings = {team: initial_ranking for team in set(df['home_team']).union(set(df['away_team']))}

    # Iterate over each match in the dataset
    for _, match in df.iterrows():
        home_team = match['home_team']
        away_team = match['away_team']

        # Current pre-match rankings
        home_rank = team_rankings[home_team]
        away_rank = team_rankings[away_team]

        # Calculate Modified pre-match Points Ranking Score
        A = home_rank + 3  # Home team advantage
        B = away_rank
        D = A - B

        # Score difference
        score_difference = match['home_score'] - match['away_score']
        world_cup = match['world_cup']

        # Determine ranking change factor based on match type and result
        if score_difference > 16:
            factor = 0.3 if world_cup else 0.15
            change = (10 + B - A) * factor
            change = min(change, 6 if world_cup else 3)
        elif score_difference >= 0:
            factor = 0.2 if world_cup else 0.1
            change = (10 + B - A) * factor
            change = min(change, 4 if world_cup else 2)
        elif score_difference == 0:
            factor = 0.2 if world_cup else 0.1
            change = D * factor
            change = min(change, 2 if world_cup else 1)
        elif -15 <= score_difference < 0:
            factor = 0.2 if world_cup else 0.1
            change = (10 + A - B) * factor
            change = min(change, 4 if world_cup else 2)
        else:
            factor = 0.3 if world_cup else 0.15
            change = (10 + A - B) * factor
            change = min(change, 6 if world_cup else 3)

        # Apply changes to rankings
        if score_difference >= 0:
            home_rank += change
            away_rank -= change
        else:
            home_rank -= change
            away_rank += change

        # Update team rankings in the global dictionary
        team_rankings[home_team] = home_rank
        team_rankings[away_team] = away_rank

        # Add the calculated rankings to the DataFrame
        df.at[_, 'home_rank'] = home_rank
        df.at[_, 'away_rank'] = away_rank
