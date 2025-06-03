import requests

def getNveApi(url:str, client_id=None):

    if client_id is None:
        client_id = ""
    
    response = requests.get(url, auth = (client_id, ""))

    #Legg til test/exception hvis ikke 200

    responseJson = response.json()

    
    return(responseJson)