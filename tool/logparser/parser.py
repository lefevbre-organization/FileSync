import json
import utils

## all possible action of rclone  
possible_action_rclone= ['idcompany','iduser','logpath','stats','Moved','Renamed','Copied (replaced existing)', 'Copied (new)','Updated', 'Deleted', 'Duplicate', 'Couldn\'t delete', 'Not copying', 'Not updating','Not deleting', 'Others']



## Parse Logs and insert into a object
def select_actions_based_on_condition(datetime_condition, logpath,  list_of_actions_from_log):

    ## utils
    util = utils.Utils() # Call only once

    # check if file is OK
    if util.check_file(logpath) == False:
        return False

    ## dico to save logs actions
    # create a dico log_actions
    # each key of log_actions is an item from possible_action_rclone
    # each value is an empty list, which would be used to store the action from rclone log
    log_actions ={key:[] for key in possible_action_rclone}  

    #getting idcompany from log file
    idcompany = util.get_idcompany(logpath)
    # check if idcompany is OK
    if idcompany == False:
        return False

    # adding idcompany to the main object
    log_actions['idcompany'].append(idcompany)

    #getting idcuser from log file
    iduser = util.get_iduser(logpath)
    ##check if iduser is OK
    if iduser == False:
        return False

    # adding iduser name to the main object
    log_actions['iduser'].append(iduser)
    
    #adding log file path to the main object
    log_actions['logpath'].append(logpath)

    val = 0
    ##loop trough log 
    for action_from_log in list_of_actions_from_log:
        val= val +1
        #if key in stats:						
        # if 'stats' in action_from_log:
        #     # adding stats to the main object
        #     log_actions['stats'].append(action_from_log)
        #     break
        
        key_found= False  # if key  found will be set to True

        # if "Copied (new)" in action_from_log:
        #     print('')
        
            
        for key, value in log_actions.items():

            #check data type with type() method
            ##convert string to json object
            try:
                msg_json_object = json.loads(action_from_log)
            except:
                break

            msg_json_object['idcompany']= idcompany
            msg_json_object['iduser']= iduser
            msg_json_object['logpath']= logpath

            
            #if key in action_from_log:            
            if key in msg_json_object["msg"] :			
                log_actions[key].append(json.dumps(msg_json_object))
                key_found = True
        if key_found == False:
            log_actions['Others'].append(json.dumps(msg_json_object))

    return log_actions

