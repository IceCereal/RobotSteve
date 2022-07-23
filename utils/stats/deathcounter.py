from nbt import nbt
import collections

def get_death_scores(scoreboard_path):
	scoreboard = nbt.NBTFile(scoreboard_path,"rb")

	death_scores = {}
	for player in scoreboard["data"]["PlayerScores"].tags:
		death_scores[str(player['Name'])] = int(str(player['Score']))

	sorted_data = sorted(death_scores.items(), key=lambda kv: kv[1], reverse=True)
	death_scores = collections.OrderedDict(sorted_data)

	for user in death_scores:
		death_scores[user] = str(death_scores[user])

	return death_scores
