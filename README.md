# 🧬 DVC CI/CD MLOps Pipeline
MLOps pipeline with DVC and CML using Github Actions and IBM Cloud


[![model-deploy-on-release](https://github.com/MLOPsStudyGroup/dvc-gitactions/actions/workflows/deploy_on_release.yaml/badge.svg)](https://github.com/MLOPsStudyGroup/dvc-gitactions/actions/workflows/deploy_on_release.yaml)
[![Python Package and Test](https://github.com/MLOPsStudyGroup/dvc-gitactions/actions/workflows/test_on_push.yaml/badge.svg)](https://github.com/MLOPsStudyGroup/dvc-gitactions/actions/workflows/test_on_push.yaml)

## 📋 Requirements

* DVC
* Python3 and pip
* Access to IBM Cloud Object Storage (IBM's equivalent to AWS S3)

## 🏃🏻 Running Project

### 🔑 Setup IBM Bucket Credentials

#### MacOS
Setup your credentials on ```~/.aws/credentials``` and ```~/.aws/config```. DVC works perfectly with IBM Obejct Storage, although it uses de AWS template for the S3, you can also see this in other portions of the repository.


~/.aws/credentials

```credentials
[default]
aws_access_key_id = {{Key ID}}
aws_secret_access_key = {{Access Key}}
```


### ✅ Pre-commit Testings

In order to activate pre-commit testing you need ```pre-commit```

Installing pre-commit with pip
```
pip install pre-commit
```

Installing pre-commit on your local repository. Keep in mind this creates a Github Hook.
```
pre-commit install
```

Now everytime you make a commit, it will run some tests defined on ```.pre-commit-config.yaml``` before allowing your commit.

**Example**
```
$ git commit -m "Example commit"

black....................................................................Passed
pytest-check.............................................................Passed
```


### ⚗️ Using DVC

Download data from the DVC repository(analog to ```git pull```)
```
dvc pull
```

Reproduces the pipeline using DVC
```
dvc repro
```


### ⚙️ DVC Pipelines


✂️ Preprocessing pipeline
```
dvc run -n preprocess -d ./src/preprocess_data.py -d data/weatherAUS.csv \
-o ./data/weatherAUS_processed.csv -o ./data/features.csv \
python3 ./src/preprocess_data.py ./data/weatherAUS.csv
```


📘 Training pipeline
```
dvc run -n train -d ./src/train.py -d ./data/weatherAUS_processed.csv \
 -d ./src/model.py \
-o ./models/model.joblib \
python3 ./src/train.py ./data/weatherAUS_processed.csv ./src/model.py 200
```


📊 Evaluate pipeline
```
dvc run -n evaluate -d ./src/evaluate.py -d ./data/weatherAUS_processed.csv \
-d ./src/model.py -d ./models/model.joblib -o ./results/metrics.json \
-o ./results/precision_recall_curve.png -o ./results/roc_curve.png \
python3 ./src/evaluate.py ./data/weatherAUS_processed.csv ./src/model.py ./models/model.joblib
```

