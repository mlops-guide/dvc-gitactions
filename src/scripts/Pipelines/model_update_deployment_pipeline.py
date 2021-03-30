import sys
import os
import yaml
from ibm_watson_machine_learning import APIClient

"""
    Usage:
        python3 model_update_deployment_pipeline.py ../path/to/project/ ../credentials.yaml

"""

PROJ_PATH = os.path.abspath(sys.argv[1])
CRED_PATH = os.path.abspath(sys.argv[2])
META_PATH = PROJ_PATH + "/metadata.yaml"

with open(CRED_PATH) as stream:
    try:
        credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(META_PATH) as stream:
    try:
        metadata = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

wml_credentials = {"url": credentials["url"], "apikey": credentials["apikey"]}

client = APIClient(wml_credentials)
client.spaces.list()

SPACE_ID = credentials["space_id"]

if "deployment_uid" in metadata.keys():
    MODEL_GUID = metadata["model_uid"]
    DEPLOYMENT_UID = metadata["deployment_uid"]
    print("\nExtracting DEPLOYMENT UID and MODEL GUID from metadata file\n")

else:
    MODEL_GUID = input("MODEL GUID: ")
    DEPLOYMENT_UID = input("DEPLOYMENT UID: ")

client.set.default_space(SPACE_ID)

change_meta = {client.deployments.ConfigurationMetaNames.ASSET: {"id": MODEL_GUID}}

print("Alterando o deploy abaixo: ")
print(client.deployments.get_details(DEPLOYMENT_UID))

client.deployments.update(DEPLOYMENT_UID, change_meta)
