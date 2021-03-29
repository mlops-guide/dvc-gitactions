import sys
import os
import yaml
from ibm_watson_machine_learning import APIClient

# MODEL_PATH = os.path.abspath(sys.argv[1])
CRED_PATH = os.path.abspath(sys.argv[1])
# PROJ_PATH = os.path.abspath(sys.argv[3])
# META_PATH = PROJ_PATH+"/metadata.yaml"

with open(CRED_PATH) as stream:
    try:
        credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


wml_credentials = {"url": credentials["url"], "apikey": credentials["apikey"]}

client = APIClient(wml_credentials)
client.spaces.list()

SPACE_ID = credentials["space_id"]
MODEL_GUID = input("MODEL GUID: ")
DEPLOYMENT_UID = input("DEPLOYMENT UID: ")

client.set.default_space(SPACE_ID)
MODEL_GUID = "b065a8c6-01ec-461b-96cc-c3abdcc35405"
DEPLOYMENT_UID = "560eed08-7d74-4ed8-8429-8d26b88cd8a3"

client.repository.list_models_revisions(MODEL_GUID)

MODEL_VERSION = input("MODEL VERSION: ")

metadata = {
    client.deployments.ConfigurationMetaNames.ASSET: {
        "id": MODEL_GUID,
        "rev": MODEL_VERSION,
    }
}
updated_deployment = client.deployments.update(
    deployment_uid=DEPLOYMENT_UID, changes=metadata
)

import time

status = None
while status not in ["ready", "failed"]:
    print(".", end=" ")
    time.sleep(2)
    deployment_details = client.deployments.get_details(DEPLOYMENT_UID)
    status = deployment_details["entity"]["status"].get("state")

print("\nDeployment update finished with status: ", status)
