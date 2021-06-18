"""
	Author: Srikar
	Code to get stats from minecraft logs.
"""

import zipfile
import os
import gzip
import shutil
from datetime import datetime
from pathlib import Path

logs = Path("{}/logs".format(os.environ["MINECRAFT_PATH"])) # Path to the logs folder

def get_time_from_secs(time):
	
	hours = time // 3600
	mins = (time - hours * 3600) // 60
	secs = (time - hours * 3600 - mins * 60)
	return '{}h {}m {}s'.format(hours, mins, secs)

def extract_file(file_name):

	try:
		if not os.path.exists('log_cache'): 
			os.makedirs('log_cache') 

	except OSError: 
		print ('Error: Creating directory of data')

	with gzip.open(logs / '{}.log.gz'.format(file_name), 'rb') as in_FPtr:
		with open('log_cache/{}.txt'.format(file_name), 'wb') as out_FPtr:
			shutil.copyfileobj(in_FPtr, out_FPtr)


def read_log_file(file_name, log_date = datetime.now()):

	file_log = {}

	with open(file_name, 'r') as FPtr:
		all_logs_text = FPtr.read()

	all_logs = all_logs_text.split('\n')

	for log in all_logs:

		# User logged in
		if 'logged in with entity id' in log:

			split_log = log.split(' ')

			time = split_log[0]

			try:
				u_index = split_log[3].index('[')
			except Exception as e:
				print("Something bad happened: {}".format(e))
				continue

			username = split_log[3][:u_index]

			# print('Joined log: {} at {}'.format(username, time))

			if username not in file_log:
				file_log[username] = {}
				file_log[username]['game_time'] = 0
				file_log[username]['is_logged_in'] = True
				file_log[username]['msgs_sent'] = 0
				file_log[username]['login_count'] = 1
				file_log[username]['logout_count'] = 0
				file_log[username]['longest_session'] = 0

			elif not file_log[username]['is_logged_in']:
				file_log[username]['login_count'] += 1
				file_log[username]['is_logged_in'] = True
			
			file_log[username]['start_time'] = datetime.combine(log_date, datetime.strptime(time, '[%H:%M:%S]').time())

		
		# User left the game
		elif 'left the game' in log:
			
			split_log = log.split(' ')

			time = split_log[0]
			username = split_log[3]

			# print('left log: {} at {}'.format(username, time))

			if username not in file_log:
				file_log[username] = {}
				file_log[username]['first_disconnect'] = datetime.combine(log_date, datetime.strptime(time, '[%H:%M:%S]').time())
				file_log[username]['is_logged_in'] = False
				file_log[username]['start_time'] = None
				file_log[username]['game_time'] = 0
				file_log[username]['msgs_sent'] = 0
				file_log[username]['login_count'] = 0
				file_log[username]['logout_count'] = 1
				file_log[username]['longest_session'] = 0

			elif file_log[username]['is_logged_in']:

				# print(file_log[username])

				diff = datetime.combine(log_date, datetime.strptime(time, '[%H:%M:%S]').time())- file_log[username]['start_time']

				if(file_log[username]['longest_session'] < int(diff.total_seconds())):
					file_log[username]['longest_session'] = int(diff.total_seconds())
					
				file_log[username]['game_time'] += int(diff.total_seconds())
				file_log[username]['is_logged_in'] = False
				file_log[username]['logout_count'] += 1


		# User message log

		elif '[Server thread/INFO]: <' in log:

			# split_log = log.split(' ')


			# time = split_log[0]

			# username = split_log[6][1:][:-1]
			username = log[log.find('<') + 1:log.find('>')]

			if username not in file_log:
				file_log[username] = {}
				file_log[username]['is_logged_in'] = False
				file_log[username]['start_time'] = None
				file_log[username]['game_time'] = 0
				file_log[username]['msgs_sent'] = 1
				file_log[username]['login_count'] = 0
				file_log[username]['logout_count'] = 0
				file_log[username]['longest_session'] = 0

			else:
				file_log[username]['msgs_sent'] += 1

	return file_log



# TODO: fix the way this function works. The current implementation is very inefficient
def read_all_logs():

	all_files = []
	zip_files = []

	zip_files_logs = {}
	
	latest_log = {}

	for (root, dir, files) in os.walk(logs):
		all_files = files

	for file in all_files:
		
		if file[-7:] == '.log.gz':
			# print('Extract this: {}'.format(file))
			extract_file(file[:-7])
			
			zip_files.append(file[:-7])

		elif file[-4:] == '.log':
			# print('Current log: {}'.format(file))
			latest_log = read_log_file(logs / '{}'.format(file))

	for file in zip_files:

		log_date = datetime.strptime(file, '%Y-%m-%d-{}'.format(file[11:]))

		if file not in zip_files_logs:
			zip_files_logs[file] = {}

		zip_files_logs[file] = read_log_file('log_cache/{}.txt'.format(file), log_date)


	real_logs = {}

	for i, log_name in enumerate(sorted(zip_files_logs.keys())):

		if not zip_files_logs[log_name]:
			continue

		else:
			for user in zip_files_logs[log_name]:

				if zip_files_logs[log_name][user]['is_logged_in']:

					try:
						exit_time = zip_files_logs[i + 1][user]['first_disconnect']
						
						diff = exit_time - zip_files_logs[log_name][user]['start_time']
						
						if(real_logs[user]['longest_session'] < int(diff.total_seconds())):
							real_logs[user]['longest_session'] = int(diff.total_seconds())

					except Exception as e:
						print("Something bad happened: {}".format(e))
						print("{} is still online somehow".format(user))
				
				else:

					if user not in real_logs:
						
						real_logs[user] = {}

						real_logs[user]['total_time_played'] = 0
						real_logs[user]['msgs_sent'] = 0
						real_logs[user]['login_count'] = 0
						real_logs[user]['logout_count'] = 0
						real_logs[user]['longest_session'] = 0

					real_logs[user]['total_time_played'] += zip_files_logs[log_name][user]['game_time']
					real_logs[user]['msgs_sent'] += zip_files_logs[log_name][user]['msgs_sent']
					real_logs[user]['login_count'] += zip_files_logs[log_name][user]['login_count']
					real_logs[user]['logout_count'] += zip_files_logs[log_name][user]['logout_count']

					if(real_logs[user]['longest_session'] < zip_files_logs[log_name][user]['longest_session']):
						real_logs[user]['longest_session'] = zip_files_logs[log_name][user]['longest_session']

	all_stats = {}

	for user in real_logs:
		
		all_stats[user] = {}

		try:

			if latest_log[user]:

				all_stats[user]['total_time_played'] = real_logs[user]['total_time_played'] + latest_log[user]['game_time']
				all_stats[user]['msgs_sent'] = real_logs[user]['msgs_sent'] + latest_log[user]['msgs_sent']
				all_stats[user]['login_count'] = real_logs[user]['login_count'] + latest_log[user]['login_count']
				all_stats[user]['logout_count'] = real_logs[user]['logout_count'] + latest_log[user]['logout_count']

				if(real_logs[user]['longest_session'] < latest_log[user]['longest_session']):
					all_stats[user]['longest_session'] = latest_log[user]['longest_session']
				
				else:
					all_stats[user]['longest_session'] = real_logs[user]['longest_session']

		except KeyError:

			all_stats[user]['total_time_played'] = real_logs[user]['total_time_played']
			all_stats[user]['msgs_sent'] = real_logs[user]['msgs_sent']
			all_stats[user]['login_count'] = real_logs[user]['login_count']
			all_stats[user]['logout_count'] = real_logs[user]['logout_count']
			all_stats[user]['longest_session'] = real_logs[user]['longest_session']


	# shutil.rmtree('log_cache')

	return all_stats


def get_all_stats():

	all_stats = read_all_logs()

	gametime = {}
	gametime['ranks'] = ''
	gametime['usernames'] = ''
	gametime['total_time_played'] = ''

	session_ranks = {}
	session_ranks['ranks'] = ''
	session_ranks['usernames'] = ''
	session_ranks['longest_session'] = ''

	logged_in_off = {}
	logged_in_off['ranks'] = ''
	logged_in_off['usernames'] = ''
	logged_in_off['login_count'] = ''
	

	msg_ranks = {}
	msg_ranks['ranks'] = ''
	msg_ranks['usernames'] = ''
	msg_ranks['msgs_sent'] = ''



	for index, user in enumerate(sorted(all_stats.items(), key = lambda i: i[1]['total_time_played'], reverse = True)):

		gametime['ranks'] += str(index + 1) + '\n'
		gametime['usernames'] += user[0] + '\n'
		gametime['total_time_played'] += get_time_from_secs(all_stats[user[0]]['total_time_played']) + '\n'


	for index, user in enumerate(sorted(all_stats.items(), key = lambda i: i[1]['longest_session'], reverse = True)):
		session_ranks['ranks'] += str(index + 1) + '\n'
		session_ranks['usernames'] += user[0] + '\n'
		session_ranks['longest_session'] += get_time_from_secs(all_stats[user[0]]['longest_session']) + '\n'


	for index, user in enumerate(sorted(all_stats.items(), key = lambda i: i[1]['login_count'], reverse = True)):
		logged_in_off['ranks'] += str(index + 1) + '\n'
		logged_in_off['usernames'] += user[0] + '\n'
		logged_in_off['login_count'] += str(all_stats[user[0]]['login_count']) + '\n'


	for index, user in enumerate(sorted(all_stats.items(), key = lambda i: i[1]['msgs_sent'], reverse = True)):
		msg_ranks['ranks'] += str(index + 1) + '\n'
		msg_ranks['usernames'] += user[0] + '\n'
		msg_ranks['msgs_sent'] += str(all_stats[user[0]]['msgs_sent']) + '\n'

	return {
		'gametime': gametime,
		'session_ranks': session_ranks,
		'logged_in_off': logged_in_off,
		'msg_ranks': msg_ranks
	}


def get_individual_stats(username):

	all_stats = read_all_logs()

	if username in all_stats:

		sum_of_playtimes = 0

		for usernames in all_stats:
			sum_of_playtimes += all_stats[usernames]['total_time_played']

		return {
			'total_time_played': get_time_from_secs(all_stats[username]['total_time_played']),
			'longest_session': get_time_from_secs(all_stats[username]['longest_session']),
			'percent': (all_stats[username]['total_time_played'] / sum_of_playtimes) * 100,
			'msgs_sent': all_stats[username]['msgs_sent'],
			'login_count': all_stats[username]['login_count']
		}

	return {
		'message': "User not found."
	}

if __name__ == "__main__":
	print(get_all_stats())