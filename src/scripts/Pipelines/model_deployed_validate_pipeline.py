import sys
import yaml
import os
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score
from ibm_watson_machine_learning import APIClient

DATA_PATH = os.path.abspath(sys.argv[1])
CRED_PATH = os.path.abspath(sys.argv[2])
PROJ_PATH = os.path.abspath(sys.argv[3])
META_PATH = PROJ_PATH + "/metadata.yaml"


def main():
    with open(CRED_PATH) as stream:
        try:
            credentials = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    data = pd.read_csv(DATA_PATH)

    X = data.iloc[:, :-1]
    y = data[data.columns[-1]]

    wml_credentials = {"url": credentials["url"], "apikey": credentials["apikey"]}

    client = APIClient(wml_credentials)
    client.spaces.list()

    SPACE_ID = credentials["space_id"]
    DEPLOYMENT_UID = input("DEPLOYMENT UID: ")

    client.set.default_space(SPACE_ID)

    # deployment_uid = client.deployments.get_uid(DEPLOYMENT_UID)

    payload = {
        "input_data": [
            {"fields": X.columns.to_numpy().tolist(), "values": X.to_numpy().tolist()}
        ]
    }
    result = client.deployments.score(DEPLOYMENT_UID, payload)

    pred_values = np.squeeze(result["predictions"][0]["values"])
    y_pred_values = [i[0] for i in pred_values]

    def comb_eval(y, y_pred):
        cm = confusion_matrix(y, y_pred)
        acc = accuracy_score(y, y_pred)

        return {"cm": cm, "acc": acc}

    eval = comb_eval(y, y_pred_values)
    print(eval)

    return eval


if __name__ == "__main__":
    main()
