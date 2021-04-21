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
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson_openscale import *
from ibm_watson_openscale.supporting_classes.enums import *
from ibm_watson_openscale.supporting_classes.payload_record import PayloadRecord
import ibm_watson_openscale


with open("../credentials.yaml") as stream:
    try:
        credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


with open("../metadata.yaml") as stream:
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

authenticator = IAMAuthenticator(apikey=credentials["apikey"])
wos_client = ibm_watson_openscale.APIClient(
    authenticator=authenticator, service_url="https://api.aiopenscale.cloud.ibm.com"
)


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
    "Rain Aus", WatsonMachineLearningInstance(wml_credentials)
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


for deployment in wml_client.deployments.get_details()["resources"]:
    if DEPLOYMENT_UID in deployment["metadata"]["id"]:

        scoring_endpoint = deployment["entity"]["status"]["online_url"]["url"]

print(scoring_endpoint)


data = pd.read_csv("../data/weatherAUS_processed.csv")

X = data.iloc[:, :-1]
y = data[data.columns[-1]]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.01, random_state=1337
)


# Payload Logging DAtASET

payload_data_set_id = (
    wos_client.data_sets.list(
        type=DataSetTypes.PAYLOAD_LOGGING,
        target_target_id=subscription_id,
        target_target_type=TargetTypes.SUBSCRIPTION,
    )
    .result.data_sets[0]
    .metadata.id
)
print("Payload data set id:", payload_data_set_id)


payload_scoring = {
    "input_data": [
        {"fields": X.columns.to_numpy().tolist(), "values": X_test.to_numpy().tolist()}
    ]
}

scoring_response = wml_client.deployments.score(DEPLOYMENT_UID, payload_scoring)

print("Logging")
records = [
    PayloadRecord(request=payload_scoring, response=scoring_response, response_time=72)
]
store_record_info = wos_client.data_sets.store_records(payload_data_set_id, records)


# Feedback Logging

feedback_dataset = wos_client.data_sets.list(
    type=DataSetTypes.FEEDBACK,
    target_target_id=subscription_id,
    target_target_type=TargetTypes.SUBSCRIPTION,
).result

feedback_dataset_id = feedback_dataset.data_sets[0].metadata.id
if feedback_dataset_id is None:
    print("Feedback data set not found. Please check quality monitor status.")
    sys.exit(1)

data = X_test.to_dict("records")

wos_client.data_sets.store_records(
    feedback_dataset_id,
    request_body=data,
    background_mode=False,
    header=True,
    delimiter=",",
    csv_max_line_length=1000,
)

print(wos_client.data_sets.get_records_count(data_set_id=feedback_dataset_id))


####


from ibm_watson_openscale.supporting_classes.enums import *

print("\nData marts: ")
datams = wos_client.data_marts.list().result.data_marts
for d in datams:
    print(d.metadata.id)
datamart_id = d.metadata.id

print("\nService providers: ")
services = wos_client.service_providers.list().result.service_providers
for service in services:
    print(service.metadata.id + " / Name: " + service.entity.name)
service_id = service.metadata.id

# wos_client.subscriptions.show()
# wos_client.data_sets.show()

print("\nSubscriptions: ")
subscriptions = wos_client.subscriptions.list(
    data_mart_id=datamart_id, service_provider_id=service_id
).result.subscriptions
for s in subscriptions:
    print(s.metadata.id + "   " + s.entity.asset.name)
subscription_id = s.metadata.id

print("\n")

payload_data_set_id = (
    wos_client.data_sets.list(
        type=DataSetTypes.PAYLOAD_LOGGING,
        target_target_id=subscription_id,
        target_target_type=TargetTypes.SUBSCRIPTION,
    )
    .result.data_sets[0]
    .metadata.id
)
print("Payload data set id:", payload_data_set_id)


pl_records_count = wos_client.data_sets.get_records_count(payload_data_set_id)
print("Number of records in the payload logging table: {}".format(pl_records_count))
if pl_records_count == 0:
    raise Exception("Payload logging did not happen!")


# Create Monitor

target = ibm_watson_openscale.base_classes.watson_open_scale_v2.Target(
    target_type=TargetTypes.SUBSCRIPTION, target_id=subscription.uid
)
parameters = {"min_feedback_data_size": 200}
thresholds = [{"metric_id": "area_under_roc", "type": "lower_limit", "value": 0.75}]
wos_client.monitor_instances.create(
    data_mart_id=datamart_id,
    background_mode=False,
    monitor_definition_id=wos_client.monitor_definitions.MONITORS.QUALITY.ID,
    target=target,
    parameters=parameters,
    thresholds=thresholds,
)

monitor_instances_info = wos_client.monitor_instances.show(data_mart_id=datamart_id)


# wos_client.monitor_instances.delete(
#         background_mode=False,
#         monitor_instance_id='94e582d5-c244-4533-9697-c16046c5fc40'
#      )

monitor_instance_run_info = wos_client.monitor_instances.run(
    background_mode=False, monitor_instance_id="5ddff093-25fa-44f8-abae-fd29659fd0d0"
)
