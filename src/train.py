import sys
import importlib.util
import pickle
import os
import json

DATA_PATH = os.path.abspath(sys.argv[1])
# PROJ_PATH = os.path.abspath(sys.argv[2])
# MODEL_PATH = PROJ_PATH+"/src/model.py"
MODEL_PATH = sys.argv[2]
PARAM = int(sys.argv[3])

# if sys.argv[4]:
#     OUTPUT_PATH = sys.argv[4]

sys.path.insert(1, MODEL_PATH)


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


model = module_from_file("model", MODEL_PATH)

if __name__ == "__main__":

    pipeline, log_train = model.train(DATA_PATH, PARAM)

    # if sys.argv[4]:
    with open("./models/model", "wb") as file:
        pickle.dump(pipeline[0], file)

    log_eval = model.evaluate(DATA_PATH, pipeline, "./results")

    with open("./results/metrics.json", "w") as outfile:
        json.dump(log_eval["metrics"], outfile)
