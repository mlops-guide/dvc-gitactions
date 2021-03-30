import sys
import os
import yaml
import joblib
from ibm_watson_machine_learning import APIClient

"""
    Usage:
        python3 model_update_pipeline.py ./pickle_model ../path/to/project/ ../credentials.yaml

"""

MODEL_PATH = os.path.abspath(sys.argv[1])
PROJ_PATH = os.path.abspath(sys.argv[2])
CRED_PATH = os.path.abspath(sys.argv[3])
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

with open(MODEL_PATH, "rb") as file:
    # pickle_model = pickle.load(file)
    pipeline = joblib.load(file)

wml_credentials = {"url": credentials["url"], "apikey": credentials["apikey"]}

client = APIClient(wml_credentials)
client.spaces.list()

SPACE_ID = credentials["space_id"]

if "model_uid" in metadata.keys():
    MODEL_GUID = metadata["model_uid"]
    print("\nExtracting MODEL GUID from metadata file\n")

else:
    MODEL_GUID = input("MODEL GUID: ")

client.set.default_space(SPACE_ID)

print("\nCreating new version")

published_model = client.repository.update_model(
    model_uid=MODEL_GUID,
    update_model=pipeline,
    updated_meta_props={
        client.repository.ModelMetaNames.NAME: metadata["project_name"]
        + "_"
        + metadata["project_version"]
    },
)

new_model_revision = client.repository.create_model_revision(MODEL_GUID)

rev_id = new_model_revision["metadata"].get("rev")
print("\nversion", rev_id)

client.repository.list_models_revisions(MODEL_GUID)
