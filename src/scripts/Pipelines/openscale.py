import os
import sys
import yaml
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.utils import *
from ibm_ai_openscale.supporting_classes import PayloadRecord, Feature
from ibm_ai_openscale.supporting_classes.enums import *
import requests
from ibm_ai_openscale.utils import get_instance_guid
import ibm_watson_machine_learning
import json


with open("../../../credentials.yaml") as stream:
    try:
        credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


with open("../../../metadata.yaml") as stream:
    try:
        metadata = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


service_credentials = {
    "apikey": credentials["apikey"],
    "url": "https://api.aiopenscale.cloud.ibm.com",
}

DEPLOYMENT_UID = metadata["deployment_uid"]
MODEL_UID = metadata["model_uid"]
MODEL_NAME = metadata["project_name"] + "_" + metadata["project_version"]
SPACE_ID = credentials["space_id"]
WOS_GUID = get_instance_guid(api_key=service_credentials["apikey"])
WOS_CREDENTIALS = {
    "instance_guid": WOS_GUID,
    "apikey": service_credentials["apikey"],
    "url": "https://api.aiopenscale.cloud.ibm.com",
}

if WOS_GUID is None:
    print("Watson OpenScale GUID NOT FOUND")
else:
    print(WOS_GUID)

ai_client = APIClient(aios_credentials=WOS_CREDENTIALS)
print(ai_client.version)

wml_credentials = {"url": credentials["url"], "apikey": credentials["apikey"]}

wml_client = ibm_watson_machine_learning.APIClient(wml_credentials)

wml_credentials = {
    "url": credentials["url"],
    "apikey": credentials["apikey"],
    "instance_id": "wml_local",
}

wml_client.set.default_space("16148a4d-9055-4220-af26-0c0369cdf31a")


KEEP_MY_INTERNAL_POSTGRES = True
DB_CREDENTIALS = None
try:
    data_mart_details = ai_client.data_mart.get_details()
    if (
        "internal_database" in data_mart_details
        and data_mart_details["internal_database"]
    ):
        if KEEP_MY_INTERNAL_POSTGRES:
            print("Using existing internal datamart.")
        else:
            if DB_CREDENTIALS is None:
                print(
                    "No postgres credentials supplied. Using existing internal datamart"
                )
            else:
                print("Switching to external datamart")
                ai_client.data_mart.delete(force=True)
                ai_client.data_mart.setup(db_credentials=DB_CREDENTIALS)
    else:
        print("Using existing external datamart")
except:
    if DB_CREDENTIALS is None:
        print("Setting up internal datamart")
        ai_client.data_mart.setup(internal_db=True)
    else:
        print("Setting up external datamart")
        try:
            ai_client.data_mart.setup(db_credentials=DB_CREDENTIALS)
        except:
            print("Setup failed, trying Db2 setup")
            ai_client.data_mart.setup(
                db_credentials=DB_CREDENTIALS, schema=DB_CREDENTIALS["username"]
            )
data_mart_details = ai_client.data_mart.get_details()

binding_uid = ai_client.data_mart.bindings.add(
    "Rain Australia", WatsonMachineLearningInstance(wml_credentials)
)

bindings_details = ai_client.data_mart.bindings.get_details()

if binding_uid is None:
    binding_uid = [
        binding["metadata"]["guid"]
        for binding in bindings_details["service_bindings"]
        if binding["entity"]["name"] == "WML Cloud Instance"
    ][0]
ai_client.data_mart.bindings.list()

ai_client.data_mart.bindings.list_assets(binding_uid=binding_uid)

subscriptions_uids = ai_client.data_mart.subscriptions.get_uids()
# for subscription in subscriptions_uids:
#     sub_name = ai_client.data_mart.subscriptions.get_details(subscription)['entity']['asset']['name']
#     if sub_name == MODEL_NAME:
#         ai_client.data_mart.subscriptions.delete(subscription)
#         print('Deleted existing subscription for', MODEL_NAME)


# subscription = ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(
#     MODEL_UID,
#     problem_type=ProblemType.BINARY_CLASSIFICATION,
#     input_data_type=InputDataType.STRUCTURED,
#     label_column='RainTomorrow',
#     prediction_column='predictedLabel',
#     probability_column='probability',
#     transaction_id_column='transaction_id',
#     feature_columns = ["Humidity3pm", "Humidity9am", "MaxTemp", "MinTemp", "Pressure3pm", "Pressure9am", "RainToday", "Rainfall", "Temp3pm", "Temp9am", "WindDir3pm_E", "WindDir3pm_ENE", "WindDir3pm_ESE", "WindDir3pm_N", "WindDir3pm_NE", "WindDir3pm_NNE", "WindDir3pm_NNW", "WindDir3pm_NW", "WindDir3pm_S", "WindDir3pm_SE", "WindDir3pm_SSE", "WindDir3pm_SSW", "WindDir3pm_SW", "WindDir3pm_W", "WindDir3pm_WNW", "WindDir3pm_WSW", "WindDir9am_E", "WindDir9am_ENE", "WindDir9am_ESE", "WindDir9am_N", "WindDir9am_NE", "WindDir9am_NNE", "WindDir9am_NNW", "WindDir9am_NW", "WindDir9am_S", "WindDir9am_SE", "WindDir9am_SSE", "WindDir9am_SSW", "WindDir9am_SW", "WindDir9am_W", "WindDir9am_WNW", "WindDir9am_WSW", "WindGustDir_E", "WindGustDir_ENE", "WindGustDir_ESE", "WindGustDir_N", "WindGustDir_NE", "WindGustDir_NNE", "WindGustDir_NNW", "WindGustDir_NW", "WindGustDir_S", "WindGustDir_SE", "WindGustDir_SSE", "WindGustDir_SSW", "WindGustDir_SW", "WindGustDir_W", "WindGustDir_WNW", "WindGustDir_WSW", "WindGustSpeed", "WindSpeed3pm", "WindSpeed9am"],
#     categorical_columns = ["RainToday", "WindDir3pm_E", "WindDir3pm_ENE", "WindDir3pm_ESE", "WindDir3pm_N", "WindDir3pm_NE", "WindDir3pm_NNE", "WindDir3pm_NNW", "WindDir3pm_NW", "WindDir3pm_S", "WindDir3pm_SE", "WindDir3pm_SSE", "WindDir3pm_SSW", "WindDir3pm_SW", "WindDir3pm_W", "WindDir3pm_WNW", "WindDir3pm_WSW", "WindDir9am_E", "WindDir9am_ENE", "WindDir9am_ESE", "WindDir9am_N", "WindDir9am_NE", "WindDir9am_NNE", "WindDir9am_NNW", "WindDir9am_NW", "WindDir9am_S", "WindDir9am_SE", "WindDir9am_SSE", "WindDir9am_SSW", "WindDir9am_SW", "WindDir9am_W", "WindDir9am_WNW", "WindDir9am_WSW", "WindGustDir_E", "WindGustDir_ENE", "WindGustDir_ESE", "WindGustDir_N", "WindGustDir_NE", "WindGustDir_NNE", "WindGustDir_NNW", "WindGustDir_NW", "WindGustDir_S", "WindGustDir_SE", "WindGustDir_SSE", "WindGustDir_SSW", "WindGustDir_SW", "WindGustDir_W", "WindGustDir_WNW", "WindGustDir_WSW", "WindGustSpeed", "WindSpeed3pm", "WindSpeed9am"]
# ))

subscription = None

if subscription is None:
    print("Subscription already exists; get the existing one")
    subscriptions_uids = ai_client.data_mart.subscriptions.get_uids()

    for sub in subscriptions_uids:
        if (
            ai_client.data_mart.subscriptions.get_details(sub)["entity"]["asset"][
                "name"
            ]
            == MODEL_NAME
        ):
            subscription = ai_client.data_mart.subscriptions.get(sub)

subscriptions_uids = ai_client.data_mart.subscriptions.get_uids()
ai_client.data_mart.subscriptions.list()

subscription_details = subscription.get_details()
subscription.uid


for deployment in wml_client.deployments.get_details()["resources"]:
    if DEPLOYMENT_UID in deployment["metadata"]["id"]:

        credit_risk_scoring_endpoint = deployment["entity"]["status"]["online_url"][
            "url"
        ]

print(credit_risk_scoring_endpoint)

data = df33

X = data.iloc[:, :-1]
y = data[data.columns[-1]]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

payload_scoring = {
    "input_data": [
        {
            "fields": X.columns.to_numpy().tolist(),
            "values": X_test.to_numpy().tolist(),
        }
    ]
}

scoring_response = wml_client.deployments.score(DEPLOYMENT_UID, payload_scoring)

time.sleep(10)
subscription.payload_logging.get_records_count()
