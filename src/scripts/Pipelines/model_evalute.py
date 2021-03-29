import sys
import importlib.util
import pickle
import os
import json

# from sklearn.externals import joblib
import joblib

DATA_PATH = os.path.abspath(sys.argv[1])
# PROJ_PATH = os.path.abspath(sys.argv[2])
# MODEL_PATH = PROJ_PATH+"/src/model.py"
MODEL_PATH = sys.argv[2]
PICKLE_PATH = sys.argv[3]


sys.path.insert(1, MODEL_PATH)


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


model = module_from_file("model", MODEL_PATH)

# with open(PICKLE_PATH, "rb") as file:
#         pipeline = pickle.load(file)
pipeline = joblib.load(PICKLE_PATH)
log_eval = model.evaluate(DATA_PATH, pipeline, "./results")

with open("./results/metrics.json", "w") as outfile:
    json.dump(log_eval["metrics"], outfile)
