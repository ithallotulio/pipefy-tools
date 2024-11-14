from pandas.plotting import table

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
    if output_format == 1:
        return json.dumps(response.json(), indent=4)
    elif output_format == 2:
        record_fields = response.json()["data"]["table_record"]["record_fields"]
        field_map = {field["field"]["id"]: field["value"] for field in record_fields}
        return field_map
    else:
        return response

# def get_table_record_id(table_id, output_format=0): FUNCTION DISABLED, USE get_all_table_record_ids
    # template = Template(
    #     """
    #         {
    #           table_records(table_id: $table_id) {
    #             edges {
    #               node {
    #                 id
    #                 title
    #               }
    #             }
    #           }
    #         }
    #     """
    # )
    # gql = template.substitute(table_id=table_id)
    # response = api(gql)
    # if output_format == 1 or output_format == "pretty":
    #     return json.dumps(response.json(), indent=4)
    # elif output_format == 2 or output_format == "list":
    #     records = response.json()['data']['table_records']['edges']
    #     record_dict = {record['node']['title']: record['node']['id'] for record in records}
    #     return record_dict
    # else:
    #     return response

def create_table_record(table_id, fields_attributes, title=None):
        if title is None:
            title = ""
        else:
            title = f'title: "{title}"'
        template = Template(
            """
                $n createTableRecord(input: {
                  table_id: "$table_id"
                  $title
                  fields_attributes:[
                    $fields
                  ]}) {
                    clientMutationId
                  }
            """
        )
        gql_stack = ""
        all_responses = []
        full_requests_number = 0
        remaining_cards_to_create = len(fields_attributes)
        if len(fields_attributes) > 50: # API limit is 50 per request
            full_requests_number = len(fields_attributes) // 50
            remaining_cards_to_create = len(fields_attributes) % 50
        for i in range(full_requests_number):
            for j in range(50):
                fields = ",\n".join(
                    [f'{{field_id: "{field}", field_value: "{value}"}}' for field, value in fields_attributes[(i*50)+j].items()]
                )
                gql_stack += template.substitute(n=f"n{j}:", table_id=table_id, title=title, fields=fields)
            gql = "mutation {" + gql_stack + "}"
            gql_stack = ""
            response = api(gql)
            print(response.text)
            all_responses.append(response)
        for i in range(remaining_cards_to_create):
            fields = ",\n".join(
                [f'{{field_id: "{field}", field_value: "{value}"}}' for field, value in fields_attributes[(full_requests_number*50)+i].items()]
            )
            gql_stack += template.substitute(n=f"n{i}:", table_id=table_id, title=title, fields=fields)
        gql = "mutation {" + gql_stack + "}"
        response = api(gql)
        print(response.text)
        all_responses.append(response)
        return all_responses

def get_all_table_record_ids(table_id, output_format=0):
    """
    Returns all record IDs and titles in a Pipefy table, with pagination support.

    Arguments:
        table_id (str): The ID of the table.
        output_format (int): The output format. (0 for raw response, 1 for indented JSON, 2 for dictionary)

    Returns:
        The data formatted according to output_format, containing all records.
    """
    all_records = []
    cursor = None  # Inicializa o cursor como None para a primeira requisição
    has_next_page = True  # Controle para o loop

    while has_next_page:
        template = Template(
            """
                {
                  table_records(table_id: $table_id, after: $cursor) {
                    edges {
                      node {
                        id
                        title
                      }
                    }
                    pageInfo {
                      hasNextPage
                      endCursor
                    }
                  }
                }
            """
        )
        cursor = "null" if cursor is None else f'"{cursor}"'

        gql = template.substitute(table_id=table_id, cursor=cursor)
        response = api(gql)
        data = response.json()["data"]["table_records"]

        # Extrai os registros atuais
        edges = data["edges"]
        all_records.extend(edges)

        # Atualiza cursor e verifica se há próxima página
        page_info = data["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        cursor = page_info["endCursor"]

    # Formata a saída
    if output_format == 1:
        return json.dumps(all_records, indent=4)
    elif output_format == 2:
        return {record['node']['title']: record['node']['id'] for record in all_records}
    else:
        return all_records