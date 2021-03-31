import os
import sys
import yaml

"""
    Usage:
        python3 model_deploy_pipeline.py ./pickle_model ../path/to/project/ ../credentials.yaml

"""

PROJ_PATH = os.path.abspath(sys.argv[1])
META_PATH = PROJ_PATH + "/metadata.yaml"

with open(META_PATH) as stream:
    try:
        metadata = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

if "deployment_uid" in metadata.keys():
    sys.exit(1)

else:
    sys.exit(0)
