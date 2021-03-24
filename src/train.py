import sys
import importlib.util
import pickle
import os
import json
import matplotlib.pyplot as plt

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

    ret, log = model.train(DATA_PATH,PARAM)
    # print(ret)
    # if sys.argv[4]:
    with open('./models/model', 'wb') as file:
        pickle.dump(ret[0], file)
    with open('./results/metrics.json', 'w') as outfile:
        json.dump(log['metrics'],outfile)

    # roc curve
    # plot the roc curve for the model
    plt.plot(log['roc_curve']['dummy_fpr'], log['roc_curve']['dummy_tpr'], linestyle='--', label='Dummy Classifer')
    plt.plot(log['roc_curve']['model_fpr'], log['roc_curve']['model_tpr'], marker='.', label='RFC')
    # axis labels
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    # show the legend
    plt.legend()
    plt.savefig("./results/roc_curve.png",dpi=80)
    plt.cla()
    def plot_prc (precisions, recalls, thresholds):
        plt.plot(thresholds, precisions[:-1], 'b--', label='Precision')
        plt.plot(thresholds, recalls[:-1], 'g-', label='Recall')
        plt.xlabel('Thresholds')
        plt.legend(loc='center left')
        plt.ylim([0,1])
        plt.savefig("./results/precision_recall_cruve.png",dpi=80)

    plot_prc(log['precision_recall_curve']['precisions'], log['precision_recall_curve']['recalls'], log['precision_recall_curve']['thresholds'])


