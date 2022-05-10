import logging
import requests 
import settings
import os
import utils 


## settigs 
settings.Settings.init() # Call only once


#methdos

##deleted (fake)
# def method_delete(log_action):
    
#     response = requests.post('https://httpbin.org/post', data = {'key':'value'})
#     print("Requesting method_deleted: " + log_action['object'])    
#     if (response.status_code == 200):
#         print("The request of method_deleted : " +  log_action['object'] + " was a success!")
#         # Code here will only run if the request is successful
#     elif (response.status_code) == 404:
#         print("Result method_deleted: " +  log_action['object'] + " not found!")
#             # Code here will react to failed requests

##updated (fake)
# def method_post(log_action, base64data):

#     for _ in range(settings.MAX_RETRIES):
#         try:
#             response = requests.post('https://httpbin.org/post', data = {'key':'value'})
#             print("Requesting method_deleted: " + log_action['object'])    
#             if (response.status_code == 200):
#                 print("The request of method_deleted : " +  log_action['object'] + " was a success!")
#             # Code here will only run if the request is successful
#             elif (response.status_code) == 404:
#                 print("Result method_deleted: " +  log_action['object'] + " not found!")
#                 # Code here will react to failed requests
#             break
#         except TimeoutError:
#             pass
    
    

##updated (fake)
# def method_put(log_action):
    
#     response = requests.post('https://httpbin.org/post', data = {'key':'value'})
#     print("Requesting method_deleted: " + log_action['object'])    
#     if (response.status_code == 200):
#         print("The request of method_deleted : " +  log_action['object'] + " was a success!")
#         # Code here will only run if the request is successful
#     elif (response.status_code) == 404:
#         print("Result method_deleted: " +  log_action['object'] + " not found!")
# 			# Code here will react to failed requests

## insert and updated


##check endpoint (bool)
def method_check(endpoint_to_check): 
    try: 
        print("Calling method_to_check")     
        response = requests.post(endpoint_to_check, data = {'key':'value'})
        print("Requesting method_check")    
        if (response.status_code == 200):
            print("The request of endpoint_to_check :  was a success!")
            # Code here will only run if the request is successful
            return True
        elif (response.status_code) == 404:
            print("endpoint_to_check: not found!")
                # Code here will react to failed requests
            return False
    except requests.RequestException as err:
        logging.error({"message": err})
        return False
        

    
## insert and updated

def method_post(log_action):
    
    companyid = log_action['idcompany']
    userid = log_action['iduser']    
    
    ## if Renamed then 
    if "Renamed" in log_action['msg']:
        #dirname TO-DO        
        dirnamenew = os.path.dirname(log_action['object'])
        dirname = os.path.dirname(utils.Utils.extact_double_cuotes(log_action['msg']))
        filename = os.path.basename(utils.Utils.extact_double_cuotes(log_action['msg']))
        newfilename = log_action['object']
        value = "{\"path\": \"%s\",\"fileName\": \"%s\",\"idEntityType\": \"78\",\"idEntity\": \"1, \"newFileName\": \"%s\"}" %(dirname, filename, newfilename)
        files = None
    ## Copied new   
    else:
        dirname = os.path.dirname(log_action['object'])
        filename = os.path.basename(log_action['object'])    
        filepath = log_action['idcompany'] + "/" + log_action['object']
        value="{\"path\": \"%s\",\"fileName\": \"%s\",\"idEntityType\": \"78\",\"idEntity\": \"1\"}" %(dirname, filename) 
        # passing files on copied new items
        
        try:
            files = {'fileData': open(filepath,'rb')}
        except IOError as e:
            logging.error({"message": os.strerror})
            return False
        
    data= ({'userId':userid,'companyId':companyid,'document':value})
    
    for _ in range(settings.MAX_RETRIES):
        try:
            response = requests.post('https://led-qa-api-lexon.lefebvre.es/rclone/document/save', files=files, data=data, timeout=settings.MAX_TIMEOUT)
    
            print("Requesting method_post: " + log_action['object'])
            #raise requests.exceptions.Timeout
            if (response.status_code == 200):
                print("The request of method_post : " +  log_action['object'] + " was a success!")
                return True
                # Code here will only run if the request is successful
            elif (response.status_code) == 404:
                print("Result method_post: " +  log_action['object'] + " not found! " + str(response.reason))
                return False
                    # Code here will react to failed requests
            elif (response.status_code) == 401:
                print("Result method_post: " +  log_action['object'] + " error 401 " + str(response.reason))
                return False
                    # Code here will react to failed request        
            elif (response.status_code) == 400:
                print("Result method_post: " +  log_action['object'] + " error 400 " + str(response.reason))
                return False
                    # Code here will react to failed request
            elif (response.status_code) == 500:
                print("Result method_post: " +  log_action['object'] + " error 500 " + str(response.reason))
                return False
                    # Code here will react to failed request
            elif (response.status_code) == 504:
                print("Result method_post: " +  log_action['object'] + " error 504 " + str(response.reason))
                return False
                    # Code here will react to failed request
            else:
                print("other error")
                return False
                #break
        except requests.Timeout as err:
            logging.error({"message": err})
            pass
            #return False
        # except requests.RequestException as err:
        #     logging.error({"message": err})
        #     pass
            #return False
    
    
    

def method_delete(log_action): 
    
    companyid = log_action['idcompany']
    userid = log_action['iduser']
    dirname = os.path.dirname(log_action['object'])
    filename = os.path.basename(log_action['object'])  
    
    value="{\"path\": \"%s\",\"fileName\": \"%s\",\"idEntityType\": \"78\",\"idEntity\": \"1\"}" %(dirname, filename)    
    data= ({'userId':userid,'companyId':companyid,'document':value})    

    for _ in range(settings.MAX_RETRIES):
        try:
            response = requests.post('https://led-qa-api-lexon.lefebvre.es/rclone/document/delete', data=data, timeout=settings.MAX_TIMEOUT )
            
            print("Requesting method_post: " + log_action['object'])
            
            if (response.status_code == 200):
                print("The request of method_post : " +  log_action['object'] + " was a success!")
                return True
                # Code here will only run if the request is successful
            elif (response.status_code) == 404:
                print("Result method_post: " +  log_action['object'] + " not found! " + str(response.reason))
                return False
                    # Code here will react to failed requests
            elif (response.status_code) == 401:
                print("Result method_post: " +  log_action['object'] + " error 401 " + str(response.reason))
                return False
                    # Code here will react to failed request        
            elif (response.status_code) == 400:
                print("Result method_post: " +  log_action['object'] + " error 400 " + str(response.reason))
                return False
                    # Code here will react to failed request
            elif (response.status_code) == 500:
                print("Result method_post: " +  log_action['object'] + " error 500 " + str(response.reason))
                return False
                    # Code here will react to failed request
            elif (response.status_code) == 504:
                print("Result method_post: " +  log_action['object'] + " error 504 " + str(response.reason))
                return False
                    # Code here will react to failed request
            else:
                print("other error")
                return False
            
        except requests.Timeout as err:
            logging.error({"message": err})
            pass
        # except requests.RequestException as err:
        #     logging.error({"message": err})
        #     pass
            #return False
            

#method_post(log_action={})