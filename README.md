# DVC CI/CD MLOps Pipeline
MLOps pipeline with DVC and CML using Github Actions and IBM Cloud

#### Requirements
* DVC
* Python3 and pip
* Access to IBM Cloud Object Storage (IBM's equivalent to AWS S3)

## Running Project

### Setup IBM Bucket Credentials
#### MacOS
Setup your credentials on ```~/.aws/credentials``` and ```~/.aws/config```. DVC works perfectly with IBM Obejct Storage, although it uses de AWS template for the S3, you can also see this in other portions of the repository.


#### ~/.aws/credentials

```credentials
[default]
aws_access_key_id = {{Key ID}}
aws_secret_access_key = {{Access Key}}
```

### Setup project

Download data from the DVC repository(analog to ```git pull```)
```
dvc pull
```

Reproduces the pipeline using DVC
```
dvc repro
```

