
import requests
import json
import sys
# base_url = "http://localhost:1333/api/v1"

base_url = "https://dev-cloud-api.virtuousai.com/api/v1"

def bulk_pipelines(file):
    files = {'file': open(file,'rb')}
    print(files )
    response = requests.post(base_url + '/automation-add-accounts', files=files)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def bulk_models(file):
    files = {'file': open(file,'rb')}
    print(files )
    response = requests.post(base_url + '/automation-add-models', files=files)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def bulk_upload(file,isDuplicateAllow= True):
    files = {'file': open(file,'rb')}
    response = requests.post(base_url + '/validate-csv-conf-file', files=files)
    res = json.loads(response.text)
    # return res
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        stored_files={'file': open(file,'rb')}  
        file_contents = json.loads(stored_files['file'].read())
        request_url = base_url + "/upload-csv?isDuplicateAllow="+("true" if isDuplicateAllow is True else "false")
        for  orgKey,organization in file_contents["organizations"].items():
                for key, pipeline in organization["pipelines"].items():
                   for location,datasetValue in pipeline.items():
                        headers = {   "location":  res[orgKey][key]["location"][location],  "pipeline":  res[orgKey][key]["apiKey"], "user-secret" :res["ownerId"]}
                        for index,file in enumerate(pipeline[location]):
                            files = {'file': open(file,'rb')}
                            response = requests.post(request_url+"&path="+file, files=files, headers=headers)
                            response = json.loads(response.text)
                            if ('message' in response):
                                print({ 'success' :False , "message" :  (response['message'])}) 
                            else :
                                print(response)
        
def bulk_accounts(file):
    files = {'file': open(file,'rb')}
    response = requests.post(base_url + '/automation-add-access', files=files)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    
def rollback(id): 
    response = requests.delete(base_url + '/automation-remove/'+id)
    res = json.loads(response.text)
    if ('message' in res):
        return  sys.stderr.write(res['message'])
    else :
        return res
    