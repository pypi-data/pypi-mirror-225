import requests
import urllib.request

#Give saved client id , client secret and tenant id
def request_token(tenant_id, client_secret,client_id):
    token_request_url = 'https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(tenant_id) #default 
    auth_payload = {
                        'grant_type': 'client_credentials', #default
                        'client_id': client_id,
                        'client_secret': client_secret,
                        'scope': 'https://graph.microsoft.com/.default' #default
                    }
    header1 = {
        'Content-Type' : 'application/x-www-form-urlencoded' 
    }
    x = requests.post(token_request_url, data=auth_payload,headers=header1)
    token = x.json()
    print("\nToken received ...")
    return token
def get_file(token,site_name,domain_name,folder_name,file_name):
    headers = {
        "Authorization": f"Bearer {token['access_token']}"
    }
    Site_name = site_name # sharepoint site name
    domain = domain_name
    u1 = "https://graph.microsoft.com/v1.0/sites/"+domain+"/:/sites/"+Site_name+"/?$select=id" # Site id request URL
    res = requests.get(u1,headers=headers).json()
    print("\nSite Found ...")
    site_id = res['id']
    folder = folder_name 
    file = file_name 
    u2 = "https://graph.microsoft.com/v1.0/sites/"+site_id+"/drive/root:/"+folder+"/"+file #File access request 
    file_url = requests.get(u2,headers=headers).json()
    print("File Found ...")
    filed = urllib.request.urlopen(file_url['@microsoft.graph.downloadUrl'])
    csv = filed.read()
    print("\nFile reading ...")
    csvstr = str(csv).strip("b'")
    lines = csvstr.split("\\n")
    f = open("subfile.csv", "w") # file name want to be save
    for line in lines:
        f.write(line+"\n")

    print('\nFile Downloaded Success !!')

