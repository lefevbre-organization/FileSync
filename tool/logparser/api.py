import requests 

#methdos

##deleted (fake)
def method_delete(log_action):
    
    response = requests.post('https://httpbin.org/post', data = {'key':'value'})
    print("Requesting method_deleted: " + log_action['object'])    
    if (response.status_code == 200):
        print("The request of method_deleted : " +  log_action['object'] + " was a success!")
        # Code here will only run if the request is successful
    elif (response.status_code) == 404:
        print("Result method_deleted: " +  log_action['object'] + " not found!")
			# Code here will react to failed requests

##updated (fake)
def method_post(log_action):
    
    response = requests.post('https://httpbin.org/post', data = {'key':'value'})
    print("Requesting method_deleted: " + log_action['object'])    
    if (response.status_code == 200):
        print("The request of method_deleted : " +  log_action['object'] + " was a success!")
        # Code here will only run if the request is successful
    elif (response.status_code) == 404:
        print("Result method_deleted: " +  log_action['object'] + " not found!")
			# Code here will react to failed requests

##updated (fake)
def method_put(log_action):
    
    response = requests.post('https://httpbin.org/post', data = {'key':'value'})
    print("Requesting method_deleted: " + log_action['object'])    
    if (response.status_code == 200):
        print("The request of method_deleted : " +  log_action['object'] + " was a success!")
        # Code here will only run if the request is successful
    elif (response.status_code) == 404:
        print("Result method_deleted: " +  log_action['object'] + " not found!")
			# Code here will react to failed requests