from pro_football_reference_web_scraper import player_game_log as p

game_log = p.get_player_game_log(player = 'Josh Allen', position = 'QB', season = 2022)
print(game_log)
