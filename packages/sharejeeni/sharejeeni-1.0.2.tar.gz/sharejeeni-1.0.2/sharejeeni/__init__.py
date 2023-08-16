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
class Get():
    def __init__(self, path="",id = ""):
        self.path = path
        self.id = id

    def folder(self, folder):
        return Get(f"{self.path}/{folder}")

    def subfolder(self, subfolder):
        return Get(f"{self.path}/{subfolder}")

    def file(self, file,token,site,save_as):
        headers = {
        "Authorization": f"Bearer {token['access_token']}"
                    }
        path = f"{self.path}/{file}"
        site_id = site
        u2 = "https://graph.microsoft.com/v1.0/sites/"+site_id+"/drive/root:"+path #File access request 
        file_url = requests.get(u2,headers=headers).json()
        print("File Found ...")
        filed = urllib.request.urlopen(file_url['@microsoft.graph.downloadUrl'])
        csv = filed.read()
        print("\nFile reading ...")
        csvstr = str(csv).strip("b'")
        lines = csvstr.split("\\n")
        f = open(save_as, "w") # file name want to be save
        for line in lines:
            f.write(line+"\n")
        print('\nFile Downloaded Success !!')

    
def get_site(token,site_name,domain_name):
    headers = {
    "Authorization": f"Bearer {token['access_token']}"
                }
    Site_name = site_name # sharepoint site name
    domain = domain_name
    u1 = "https://graph.microsoft.com/v1.0/sites/"+domain+"/:/sites/"+Site_name+"/?$select=id" # Site id request URL
    res = requests.get(u1,headers=headers).json()
    print("\nSite Found ...")
    site_id = res['id']
    return site_id


        

    




