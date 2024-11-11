import pipefy_token
import requests
import json
from string import Template

def me():
    gql = """
        {
            me {
                name
                email
            }
        }
    """
    response = api(gql)
    return response

def api(gql):
    url = "https://api.pipefy.com/graphql"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {pipefy_token.personal_access_token}"
    }
    payload = {"query": gql}
    response = requests.post(url, json=payload, headers=headers)
    return response


def set_table_record_field(value, field_id, record_id):
    # Updates the value of a field in a specific record in a table on Pipefy.
    #
    # Arguments:
    #   value (str): The value to be assigned to the field.
    #   field_id (str): The ID of the field to be updated.
    #   record_id (str): The ID of the record whose field will be updated.
    template = Template(
        """
            mutation {
              setTableRecordFieldValue(input: {
                field_id: "$field_id",
                table_record_id: "$record_id",
                value: "$value"
              }) {
                table_record_field {
                  name
                  value
                }
              }
            }
        """
    )
    gql = template.substitute(field_id=field_id, value=value, record_id=record_id)
    response = api(gql)
    return response

def get_table_record_fields(table_id, output_format=0):
    template = Template(
        """
            {
              table_record(id: $table_id) {
                record_fields {
                  value
                  field {
                    id
                  }
                }
              }
            }
        """
    )
    gql = template.substitute(table_id=table_id)
    response = api(gql)
    if output_format == 1 or output_format == "pretty":
        return json.dumps(response.json(), indent=4)
    elif output_format == 2 or output_format == "list":
        record_fields = response.json()["data"]["table_record"]["record_fields"]
        field_map = {field["field"]["id"]: field["value"] for field in record_fields}
        return field_map
    else:
        return response


def get_table_record_id(table_id, output_format=0):
    template = Template(
        """
            {
              table_records(table_id: $table_id) {
                edges {
                  node {
                    id
                    title
                  }
                }
              }
            }
        """
    )
    gql = template.substitute(table_id=table_id)
    response = api(gql)
    if output_format == 1 or output_format == "pretty":
        return json.dumps(response.json(), indent=4)
    elif output_format == 2 or output_format == "list":
        records = response.json()['data']['table_records']['edges']
        record_dict = {record['node']['title']: record['node']['id'] for record in records}
        return record_dict
    else:
        return response
