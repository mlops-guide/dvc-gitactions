#!/bin/sh

if  ! python3 ./src/scripts/Pipelines/git_release_pipeline.py ./
then 
    echo "      Model already has been deployed, updating it"
    python3 ./src/scripts/Pipelines/model_update_pipeline.py ./models/model.joblib ./ ./credentials.yaml
    python3 ./src/scripts/Pipelines/model_update_deployment_pipeline.py ./ ./credentials.yaml
else    
    echo "      Deploying model for the first time" 
    python3 ./src/scripts/Pipelines/model_deploy_pipeline.py ./models/model.joblib ./ ./credentials.yaml
fi
