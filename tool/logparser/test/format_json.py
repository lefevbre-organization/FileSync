# Alberto Valverde
# Read rclone logs stored in a folder and append into the array each action by categories of action (copied, delete...)

import glob
import json
import datetime

## var to customize
path_to_rclone_log_folder = r'LogRsync\*'

## all possible action of rclone  
possible_action_rclone= ['Logname', 'stats', 'Moved','Renamed','Copied (replaced existing)', 'Copied (new)','Updated', 'Deleted', 'Duplicate', 'Couldn\'t delete', 'Not copying', 'Not updating','Not deleting', 'Others']

##process the actions from the log and display them
def select_actions_based_on_condition(datetime_condition, logname):

	## dico to save logs actions
	# create a dico log_actions
	# each key of log_actions is an item from possible_action_rclone
	# each value is an empty list, which would be used to store the action from rclone log
	log_actions ={key:[] for key in possible_action_rclone}  
	
	##loop trough log 
	for action_from_log in list_of_actions_from_log:
		
		key_found= False  # if key  found will be set to True

		for key, value in log_actions.items():	
			
			#check data type with type() method
			#convert string to json object
			msg_json_object = json.loads(action_from_log)

			#if key in Logname:
			if 'Logname' in key:				
				if len(log_actions[key]) == 0:
					log_actions[key].append(logname)


            #if key in stats:
			if 'stats' in key:				
				if 'stats' in msg_json_object:
					log_actions[key].append(action_from_log)
            #if key in action_from_log:
			if key in msg_json_object["msg"]:
				log_actions[key].append(action_from_log)
				key_found = True
		if key_found == False:
			log_actions['Others'].append(action_from_log)


	display_dico(log_actions) 		

	
## print the dico 
def display_dico(log_actions):
	
	empty_keys=[]  # if key empty, don't display it
	for key, value in log_actions.items():
		if len(value) != 0:
			print('\n')
			print('*******' + key+'*******')
			print('number of files: ', len(value))
			print(('\n').join(value))
		else:
			empty_keys.append(key)
	#print("Actions not done:" + (', ').join(empty_keys))



## get all log files of rclone_log_folder
for logname in glob.glob(path_to_rclone_log_folder):
	print("\n\n\n++++++++ PROCESING LOG " + logname + "+++++++++++++")
	with open(logname,errors='ignore') as f:  # errors='ignore' : when strange character in log -then ignore
		content = f.readlines()
		list_of_actions_from_log = [x.strip() for x in content]

	## read log and store each line in 
	datetime_one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 4)
	# print(f"{datetime.datetime.now():%Y/%m/%d}")
	datetime_beginning_of_time = datetime.datetime(1900, 1, 1, 1, 1, 1, 1)
	print("\n+++++++++++++ All actions +++++++++++++\n")
	select_actions_based_on_condition(datetime_beginning_of_time, logname)






	






	
	
	
