# read the last modified rclone log stored in a folder and display each action by categories of action (copied, delete...)
# possible to select action by date

import glob
import os

#import easygui
import datetime

## var to customize
path_to_rclone_log_folder = r'LogRsync\*'


## all possible action of rclone  
possible_action_rclone= ['Moved','Renamed','Copied (replaced existing)', 'Copied (new)','Updated', 'Duplicate', 'Couldn\'t delete', 'Not copying', 'Not updating','Not deleting', 'Others']

## get all log files of rclone_log_folder
for name in glob.glob(path_to_rclone_log_folder):
    print(name)

## get lastest modified log of rclone
list_of_files = glob.glob(path_to_rclone_log_folder) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getmtime)
print(latest_file)

## read log and store each line in 
with open(latest_file,errors='ignore') as f:  # errors='ignore' : when strange character in log -then ignore
    content = f.readlines()
list_of_actions_from_log = [x.strip() for x in content] 


##process the actions from the log and display them
def select_actions_based_on_condition(datetime_condition):

	## dico to save logs actions
	# create a dico log_actions
	# each key of log_actions is an item from possible_action_rclone
	# each value is an empty list, which would be used to store the action from rclone log
	log_actions ={key:[] for key in possible_action_rclone}  
	
	##loop trough log 
	for action_from_log in list_of_actions_from_log:
		try: 
			# get time from action_from_log
			datetime_action_from_log = datetime.datetime.strptime(action_from_log[0:19], '%Y/%m/%d %H:%M:%S')
			# print(f"{datetime_one_hour_ago:%Y/%m/%d %H:%M:%S}")
		except:
			datetime_action_from_log= datetime.datetime(1900, 1, 1, 1, 1, 1, 1)
		# compare  datetime_action_from_log to condition time (ex: time_one_hour_ago -  datetime_action_from_log)
		lapse= datetime_condition - datetime_action_from_log
		
		#convert lapse to string and check if condition is true (first char of lapse wiill be - if the condition is respected)
		format_lapse = f"{lapse}"
		action_respect_condition = True if format_lapse[0]=="-" else False
		
		if action_respect_condition:
			# save the action_from_log in dico log_actions under appropriate key  
			key_found= False  # if key  found will be set to True
			for key, value in log_actions.items():
				if key in action_from_log:
					log_actions[key].append(action_from_log)
					key_found = True
			if key_found == False:
				log_actions['Others'].append(action_from_log)
				
	display_dico(log_actions)
	#choose_timeframe()
		

def display_log_based_on_condition():
	## dico to save logs actions
	# create a dico log_actions
	# each key of log_actions is an item from possible_action_rclone
	# each value is an empty list, which would be used to store the action from rclone log
	log_actions ={key:[] for key in possible_action_rclone}  
	
	for action_from_log in list_of_actions_from_log:
		# save the action_from_log in dico log_actions under appropriate key  
		key_found= False  # if key  found will be set to True
		for key, value in log_actions.items():
			if key in action_from_log:
				log_actions[key].append(action_from_log)
				key_found = True
		if key_found == False:
			log_actions['Others'].append(action_from_log)
	display_dico(log_actions)
	#choose_timeframe()
	
## print the dico 
def display_dico(log_actions):
	
	empty_keys=[]  # if key empty, don't display it
	for key, value in log_actions.items():
		if len(value) != 0:
			print('\n\n\n')
			print('*******' + key+'*******')
			print('number of files: ', len(value))
			print(('\n').join(value))
		else:
			empty_keys.append(key)
	#print("Actions not done:" + (', ').join(empty_keys))



# def choose_timeframe():
# 	timeframe_select_log = easygui.buttonbox ("See previous actions from log", choices = ["Actions from Last Hour","Actions from 4 Hours","Actions from today", "Actions from beginning of time", "All Log", "Close"])

# 	if timeframe_select_log == "Close":
# 		pass
# 	elif timeframe_select_log=="Actions from Last Hour":
# 		print("\n\n\n+++++++++++++ All actions from last hour (not full log) +++++++++++++\n\n\n")
# 		datetime_one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 1)
# 		select_actions_based_on_condition(datetime_one_hour_ago)
# 	elif timeframe_select_log=="Actions from 4 Hours":
# 		print("\n\n\n+++++++++++++ All actions from last 4 hour (not full log) +++++++++++++\n\n\n")
# 		datetime_four_hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 4)
# 		select_actions_based_on_condition(datetime_four_hour_ago)
# 	elif timeframe_select_log=="Actions from today":
# 		print("\n\n\n+++++++++++++ All actions from last day (not full log) +++++++++++++\n\n\n")
# 		datetime_one_day_ago = datetime.datetime.now() - datetime.timedelta(days = 1)
# 		select_actions_based_on_condition(datetime_one_day_ago)
# 	elif timeframe_select_log=="Actions from beginning of time":
# 		print("\n\n\n+++++++++++++ All actions from beginning of time (not full log) +++++++++++++\n\n\n")
# 		datetime_beginning_of_time = datetime.datetime(1900, 1, 1, 1, 1, 1, 1)
# 		select_actions_based_on_condition(datetime_beginning_of_time)			
# 	elif timeframe_select_log=="All Log":
# 		print("\n\n\n+++++++++++++ All log from beginning of time +++++++++++++\n\n\n")
# 		display_log_based_on_condition()
		
		
# # by default display log from last 4h 
# datetime_one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 4)
# # print(f"{datetime.datetime.now():%Y/%m/%d}")
# print("\n\n\n+++++++++++++ All actions from last 4h (not full log) +++++++++++++\n\n\n")
# select_actions_based_on_condition(datetime_one_hour_ago)


datetime_one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 4)
# print(f"{datetime.datetime.now():%Y/%m/%d}")
datetime_beginning_of_time = datetime.datetime(1900, 1, 1, 1, 1, 1, 1)
print("\n\n\n+++++++++++++ All actions +++++++++++++\n\n\n")
select_actions_based_on_condition(datetime_beginning_of_time)

	
## choose which action to display = by date/type 
# def choose_timeframe_all():
# 	timeframe_select_log = easygui.buttonbox ("See previous actions from log", choices = ["Actions from Last Hour","Actions from 4 Hours","Actions from today", "Actions from beginning of time", "All Log", "Close"])

# 	if timeframe_select_log == "Close":
# 		pass
# 	elif timeframe_select_log=="Actions from Last Hour":
# 		print("\n\n\n+++++++++++++ All actions from last hour (not full log) +++++++++++++\n\n\n")
# 		datetime_one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 1)
# 		select_actions_based_on_condition(datetime_one_hour_ago)
# 	elif timeframe_select_log=="Actions from 4 Hours":
# 		print("\n\n\n+++++++++++++ All actions from last 4 hour (not full log) +++++++++++++\n\n\n")
# 		datetime_four_hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 4)
# 		select_actions_based_on_condition(datetime_four_hour_ago)
# 	elif timeframe_select_log=="Actions from today":
# 		print("\n\n\n+++++++++++++ All actions from last day (not full log) +++++++++++++\n\n\n")
# 		datetime_one_day_ago = datetime.datetime.now() - datetime.timedelta(days = 1)
# 		select_actions_based_on_condition(datetime_one_day_ago)
# 	elif timeframe_select_log=="Actions from beginning of time":
# 		print("\n\n\n+++++++++++++ All actions from beginning of time (not full log) +++++++++++++\n\n\n")
# 		datetime_beginning_of_time = datetime.datetime(1900, 1, 1, 1, 1, 1, 1)
# 		select_actions_based_on_condition(datetime_beginning_of_time)			
# 	elif timeframe_select_log=="All Log":
# 		print("\n\n\n+++++++++++++ All log from beginning of time +++++++++++++\n\n\n")
# 		display_log_based_on_condition()
		
		





	
	
	
