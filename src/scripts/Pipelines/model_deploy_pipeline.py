import os
import sys
import pickle
import yaml
import joblib
from ibm_watson_machine_learning import APIClient

"""
    Usage:
        python3 model_deploy_pipeline.py ./pickle_model ../path/to/project/ ../credentials.yaml

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

MODEL_NAME = metadata["project_name"] + "_" + metadata["project_version"]
DEPLOY_NAME = MODEL_NAME + "-Deployment"
MODEL = pipeline
SPACE_ID = credentials["space_id"]

client.set.default_space(SPACE_ID)

model_props = {
    client.repository.ModelMetaNames.NAME: MODEL_NAME,
    client.repository.ModelMetaNames.TYPE: metadata["model_type"],
    client.repository.ModelMetaNames.SOFTWARE_SPEC_UID: client.software_specifications.get_id_by_name(
        "default_py3.7"
    ),
}

model_details = client.repository.store_model(model=MODEL, meta_props=model_props)
model_uid = client.repository.get_model_uid(model_details)

deployment_props = {
    client.deployments.ConfigurationMetaNames.NAME: DEPLOY_NAME,
    client.deployments.ConfigurationMetaNames.ONLINE: {},
}

deployment = client.deployments.create(
    artifact_uid=model_uid, meta_props=deployment_props
)

deployment_uid = client.deployments.get_uid(deployment)

metadata["model_uid"] = model_uid
metadata["deployment_uid"] = deployment_uid

f = open(META_PATH, "w+")
yaml.dump(metadata, f, allow_unicode=True)
