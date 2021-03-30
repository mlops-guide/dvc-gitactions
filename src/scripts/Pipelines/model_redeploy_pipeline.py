import sys
import os
import time
import yaml
from ibm_watson_machine_learning import APIClient

"""
    Usage:
        python3 model_reploy_pipeline.py ../path/to/project/ ../credentials.yaml

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

client.repository.list_models_revisions(MODEL_GUID)

MODEL_VERSION = input("MODEL VERSION: ")

meta = {
    client.deployments.ConfigurationMetaNames.ASSET: {
        "id": MODEL_GUID,
        "rev": MODEL_VERSION,
    }
}
updated_deployment = client.deployments.update(
    deployment_uid=DEPLOYMENT_UID, changes=meta
)

status = None
while status not in ["ready", "failed"]:
    print(".", end=" ")
    time.sleep(2)
    deployment_details = client.deployments.get_details(DEPLOYMENT_UID)
    status = deployment_details["entity"]["status"].get("state")

print("\nDeployment update finished with status: ", status)
# print(deployment_details)
