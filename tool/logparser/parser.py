import json

## all possible action of rclone  
possible_action_rclone= ['Logname','stats','Moved','Renamed','Copied (replaced existing)', 'Copied (new)','Updated', 'Deleted', 'Duplicate', 'Couldn\'t delete', 'Not copying', 'Not updating','Not deleting', 'Others']


## Parse Logs and insert into a object
def select_actions_based_on_condition(datetime_condition, logname,  list_of_actions_from_log):

	## dico to save logs actions
	# create a dico log_actions
	# each key of log_actions is an item from possible_action_rclone
	# each value is an empty list, which would be used to store the action from rclone log
	log_actions ={key:[] for key in possible_action_rclone}  

    # log_actions['logname'].append(logname)
    # log_actions['Stats'].append(logname)
    
    
	##loop trough log 
	for action_from_log in list_of_actions_from_log:
		
		key_found= False  # if key  found will be set to True

		for key, value in log_actions.items():	
			
			#check data type with type() method
			# #convert string to json object
			msg_json_object = json.loads(action_from_log)

			#if key in Logname:
			if 'Logname' in key:				
				if len(log_actions[key]) == 0:
					log_actions[key].append(logname)

            #if key in stats:
			if 'stats' in key:				
				if 'stats' in action_from_log:
					log_actions[key].append(action_from_log)
					break

            #if key in action_from_log:            
			if key in msg_json_object["msg"] :			
				log_actions[key].append(action_from_log)
				key_found = True
		if key_found == False:
			log_actions['Others'].append(action_from_log)

	return log_actions