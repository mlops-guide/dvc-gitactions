import sys
import os
import yaml
from ibm_watson_machine_learning import APIClient

CRED_PATH = os.path.abspath(sys.argv[1])

with open(CRED_PATH) as stream:
    try:
        credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


wml_credentials = {"url": credentials["url"], "apikey": credentials["apikey"]}

client = APIClient(wml_credentials)
client.spaces.list()

SPACE_ID = credentials["space_id"]
MODEL_ID = input("MODEL ID: ")
DEPLOYMENT_ID = input("DEPLOYMENT ID: ")

client.set.default_space(SPACE_ID)

change_meta = {client.deployments.ConfigurationMetaNames.ASSET: {"id": MODEL_ID}}

print("Alterando o deploy abaixo: ")
print(client.deployments.get_details(DEPLOYMENT_ID))

client.deployments.update(DEPLOYMENT_ID, change_meta)
