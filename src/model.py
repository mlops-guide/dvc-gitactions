import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt


def get_variables(data, column):
    # Seperating the dependant and independant variables
    y = data[column]
    X = data.drop([column], axis=1)

    return X, y


def train(data, num_estimators, isDataFrame=False):

    if not isDataFrame:
        data = pd.read_csv(data)

    # Seperating the dependant and independant variables
    # y = data["RainTomorrow"]
    # X = data.drop(["RainTomorrow"], axis=1)

    X, y = get_variables(data, "RainTomorrow")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0
    )

    pipe = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "RFC",
                RandomForestClassifier(
                    criterion="gini",
                    max_depth=10,
                    max_features="auto",
                    n_estimators=num_estimators,
                ),
            ),
        ]
    )

    training_logs = pipe.fit(X_train, y_train)

    logs = {"training_logs": training_logs}

    return pipe, logs


def evaluate(data, pipeline, OUTPUT_PATH, isDataFrame=False):

    pipe = pipeline

    if not isDataFrame:
        data = pd.read_csv(data)

    y = data["RainTomorrow"]
    X = data.drop(["RainTomorrow"], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0
    )

    # metrics
    def comb_eval(y, y_pred):
        acc = accuracy_score(y, y_pred)
        recall = recall_score(y, y_pred)
        precision = precision_score(y, y_pred)
        f1 = f1_score(y, y_pred)

        return {"accuracy": acc, "recall": recall, "precision": precision, "f1": f1}

    # y_pred_train = pipe.predict(X_train)
    # train_result = comb_eval(y_train, y_pred_train)

    y_pred_test = pipe.predict(X_test)
    test_result = comb_eval(y_test, y_pred_test)

    # cvs = cross_val_score(pipe, X, y, cv=3)

    # roc curve
    # y_pred = pipe.predict(X_test)

    dummy_probs = [0 for _ in range(len(y_test))]
    model_probs = pipe.predict_proba(X_test)
    model_probs = model_probs[:, 1]

    # model_auc = roc_auc_score(y_test, model_probs)

    dummy_fpr, dummy_tpr, _ = roc_curve(y_test, dummy_probs)
    model_fpr, model_tpr, _ = roc_curve(y_test, model_probs)

    # precision_recall_curve
    y_scores = pipe.predict_proba(X_test)[:, 1]
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_scores)

    logs = {
        "metrics": test_result,
        "roc_curve": {
            "model_tpr": model_tpr,
            "model_fpr": model_fpr,
            "dummy_tpr": dummy_tpr,
            "dummy_fpr": dummy_fpr,
        },
        "precision_recall_curve": {
            "precisions": precisions,
            "recalls": recalls,
            "thresholds": thresholds,
        },
    }

    # roc curve
    # plot the roc curve for the model
    plt.plot(
        logs["roc_curve"]["dummy_fpr"],
        logs["roc_curve"]["dummy_tpr"],
        linestyle="--",
        label="Dummy Classifer",
    )
    plt.plot(
        logs["roc_curve"]["model_fpr"],
        logs["roc_curve"]["model_tpr"],
        marker=".",
        label="RFC",
    )
    # axis labels
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    # show the legend
    plt.legend()
    out_path = OUTPUT_PATH + "/roc_curve.png"
    plt.savefig(out_path, dpi=80)
    plt.cla()

    def plot_prc(precisions, recalls, thresholds):
        plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
        plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
        plt.xlabel("Thresholds")
        plt.legend(loc="center left")
        plt.ylim([0, 1])
        out_path = OUTPUT_PATH + "/precision_recall_curve.png"
        plt.savefig(out_path, dpi=80)

    plot_prc(
        logs["precision_recall_curve"]["precisions"],
        logs["precision_recall_curve"]["recalls"],
        logs["precision_recall_curve"]["thresholds"],
    )

    return logs
