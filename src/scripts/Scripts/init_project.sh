MODEL=$1
VERSION=$2
PROJECT_NAME="$1_$2"
echo "Creating $MODEL $VERSION"
mkdir -p -m 777 $PROJECT_NAME 
mkdir -p -m 777 $PROJECT_NAME/src
touch $PROJECT_NAME/src/__init__.py
touch $PROJECT_NAME/src/model.py
mkdir -p -m 777 $PROJECT_NAME/notebooks
mkdir -p -m 777 $PROJECT_NAME/tests
echo "Created by: "$USERNAME 
now=$(date +%x_%H:%M:%S:%N)
echo "At: "$now

cat <<EOF >./$PROJECT_NAME/metadata.yaml
project_name: $MODEL
project_version: $VERSION
model_type: scikit-learn_0.23
author: $USERNAME
datetime_creted: $now
EOF

cp ./requirements.txt ./$PROJECT_NAME
cp -avr ./scripts  ./$PROJECT_NAME/src/
