"""
DataPak deployment space manage script

"""

import os
import sys
from pprint import pprint
import json
from ibm_watson_machine_learning import APIClient

TERRAFORM_OUTPUT = ".terraform/terraform.tfstate"


def authentication():

    if os.getenv("IBMCLOUD_API_KEY"):

        wml_credentials = {
            "url": "https://us-south.ml.cloud.ibm.com",
            "apikey": os.environ.get("IBMCLOUD_API_KEY"),
        }
        client = APIClient(wml_credentials)  # Connect to IBM cloud

        return client

    raise Exception("API_KEY environment variable not defined")


def terraform_output(terraform_path=TERRAFORM_OUTPUT):

    output = dict(json.load(open(terraform_path)))["outputs"]

    cos_crn = output["cos_crn"]["value"]
    wml_crn = output["wml_crn"]["value"]["crn"]
    wml_name = output["wml_crn"]["value"]["resource_name"]

    state = {"cos_crn": cos_crn, "wml_name": wml_name, "wml_crn": wml_crn}
    return state


def create_deployment_space(
    client, cos_crn, wml_name, wml_crn, space_name="default", description=""
):

    metadata = {
        client.spaces.ConfigurationMetaNames.NAME: space_name,  ## Project info
        client.spaces.ConfigurationMetaNames.DESCRIPTION: description,
        client.spaces.ConfigurationMetaNames.STORAGE: {
            "type": "bmcos_object_storage",
            "resource_crn": cos_crn,
        },
        client.spaces.ConfigurationMetaNames.COMPUTE: {  ## Project compute instance (WML)
            "name": wml_name,
            "crn": wml_crn,
        },
    }

    space_details = client.spaces.store(meta_props=metadata)  # Create a space
    return space_details


def update_deployment_space(client, new_name, space_id):

    metadata = {client.spaces.ConfigurationMetaNames.NAME: new_name}

    space_details = client.spaces.update(space_id, changes=metadata)
    return space_details


def delete_deployment_space(client, space_id):

    client.spaces.delete(space_id)


def list_deployment_space(client):
    spaces = client.spaces.list()
    print(spaces)


def describe_deployment_space(client, space_id):
    info = client.spaces.get_details(space_id)
    pprint(info)


def help():

    print(
        """
        datapak_config.py [options] 

        create  
        update  
        delete  
        list    
        describe
        """
    )


if __name__ == "__main__":

    client = authentication()

    args = sys.argv[1:]

    if len(args) >= 1:
        action = args[0]

        if action == "create":

            infos = terraform_output()
            if len(args) == 2:
                space_name = args[1]
                space = create_deployment_space(
                    client,
                    infos["cos_crn"],
                    infos["wml_name"],
                    infos["wml_crn"],
                    space_name,
                )

            elif len(args) > 2:
                space_name = args[1]
                description = args[2]
                space = create_deployment_space(
                    client,
                    infos["cos_crn"],
                    infos["wml_name"],
                    infos["wml_crn"],
                    space_name,
                    description,
                )

            pprint(space)

        elif action == "update":

            try:
                new_name = args[1]
                space_id = args[2]
            except:
                raise Exception("Missing arguments")

            space = update_deployment_space(client, new_name, space_id)
            pprint(space)

        elif action == "delete":
            try:
                space_id = args[1]
            except:
                raise Exception("Missing space_id")

            delete_deployment_space(client, space_id)

        elif action == "list":
            list_deployment_space(client)

        elif action == "describe":

            try:
                space_id = args[1]
            except:
                raise Exception("Missing space_id")

            describe_deployment_space(client, space_id)

        else:
            help()

    else:
        help()
