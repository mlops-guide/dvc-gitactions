import sys
import os
import yaml
import pandas as pd

# from ibm_watson_machine_learning.helpers import DataConnection, S3Connection, S3Location
from ibm_watson_machine_learning.experiment import AutoAI
from ibm_watson_machine_learning.autoai.helpers.connections import (
    S3Connection,
    S3Location,
    DataConnection,
)

DATA_PATH = os.path.abspath(sys.argv[1])
CRED_PATH = os.path.abspath(sys.argv[2])
PROJ_PATH = os.path.abspath(sys.argv[3])
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

SPACE_ID = credentials["space_id"]

data = pd.read_csv(DATA_PATH)

X = data.iloc[:, :-1]
y = data[data.columns[-1]]
cols = data.columns.tolist()
TARGET = cols[-1]
AUTOAI_ENDPOINT = "auto_ml/a4243da5-a8b0-4e6a-8273-13c161f7e117/wml_data/d8ab3fe3-17a2-4474-b702-9c8309586a40"

experiment = AutoAI(
    wml_credentials=wml_credentials,
    # project_id=credentials['project_id'],
    space_id=credentials["space_id"],
)


pipeline_optimizer = experiment.optimizer(
    name=metadata["project_name"],
    desc="",
    prediction_type=AutoAI.PredictionType.BINARY,
    prediction_column=TARGET,
    scoring=AutoAI.Metrics.ACCURACY_SCORE,
    test_size=0.2,
    max_num_daub_ensembles=1,
    train_sample_rows_test_size=1.0,
    daub_include_only_estimators=[
        AutoAI.ClassificationAlgorithms.XGB,
        AutoAI.ClassificationAlgorithms.LGBM,
    ],
    cognito_transform_names=[AutoAI.Transformers.SUM, AutoAI.Transformers.MAX],
)


# note: this DataConnection will be used as a reference where to find your training dataset
training_data_connection = DataConnection(
    connection=S3Connection(
        endpoint_url="url of the COS endpoint",
        access_key_id="COS access key id",
        secret_access_key="COS secret acces key",
    ),
    location=S3Location(
        bucket="bucket_name",  # note: COS bucket name where training dataset is located
        path="my_path",  # note: path within bucket where your training dataset is located
    ),
)

# note: this DataConnection will be used as a reference where to save all of the AutoAI experiment results
results_connection = DataConnection(
    connection=S3Connection(
        endpoint_url="url of the COS endpoint",
        access_key_id="COS access key id",
        secret_access_key="COS secret acces key",
    ),
    # note: bucket name and path could be different or the same as specified in the training_data_connection
    location=S3Location(bucket="bucket_name", path="my_path"),
)

# training_data_connection = [DataConnection(
#     connection=S3Connection(
#         api_key=credentials['s3_apikey'],
#         auth_endpoint='https://iam.bluemix.net/oidc/token/',
#         endpoint_url='https://s3-api.us-geo.objectstorage.softlayer.net'
#     ),
#         location=S3Location(
#         bucket=credentials['s3_bucket'],
#         path=DATA_PATH
#     ))
# ]
# results_connection = DataConnection(
#     connection=S3Connection(
#         api_key=credentials['s3_apikey'],
#         auth_endpoint='https://iam.bluemix.net/oidc/token/',
#         endpoint_url='https://s3-api.us-geo.objectstorage.softlayer.net'
#     ),
#     location=S3Location(
#         bucket=credentials['s3_bucket'],
#         path=AUTOAI_ENDPOINT+'/data/automl',
#         model_location=AUTOAI_ENDPOINT+'/data/automl/cognito_output/Pipeline1/model.pickle',
#         training_status=AUTOAI_ENDPOINT+'/training-status.json'
#     ))

fit_details = pipeline_optimizer.fit(
    training_data_reference=[training_data_connection],
    training_results_reference=results_connection,
    background_mode=True,
)


status = pipeline_optimizer.get_run_status()
print(status)

run_details = pipeline_optimizer.get_run_details()

results = pipeline_optimizer.summary()
print(results)
