import json
import jwt
import random
import requests
from ddt import ddt, file_data, data


def random_user_id():
    user = str(random.randint(1000, 9999))
    return user

USER = random_user_id()

def copy_all_file_text(path):
        with open(path, 'r') as f:
            data = f.read()
        return data

def open_data_json():
    with open('./data.json', 'r') as f:
        file = json.load(f)
        data = dict(enterprise_id=file['ENTERPRISE_ID'], user=file['CUSTOMER_ID'],
                    host_address=file['HOST_ADDRESS'], path_to_key=file['PATH_TO_KEY'],
                    dt_ids=file['DATA_TYPE_IDS'], context_ids=file['CONTEXT_IDS'])
    return data

def create_jwt():
    enterprise = open_data_json()["enterprise_id"]
    user = USER
    payload = {
        "iss": enterprise,
        "aud": [
            "Trunomi",
            enterprise,
            user
        ],
        "jti": "86869840-1c96-11e8-b7fc-f162c8621d7f",
        "pol": "enterprise on behalf of customer",
        "sub": enterprise + "::" + user,
        "iat": 1519923598
    }
    key = copy_all_file_text(open_data_json()["path_to_key"])
    result = jwt.encode(payload, key, algorithm='RS512')
    result = b"Bearer " + result
    return result

def ledger_list():
    response = requests.get("https://test.trunomi.com/ledger",
                            data={"customerId": USER,
                                  "enterpriseId": open_data_json()["enterprise_id"]},
                            headers={"authorization": create_jwt()})
    print(response.url, response.status_code)

def consent_last_ledger(context_id):
    response = requests.get("https://test.trunomi.com/ledger/context/" + context_id + "/last",
                 data={"customerId": USER,
                       "enterpriseId": open_data_json()["enterprise_id"]},
                 headers={"authorization": create_jwt()}
                 )
    print(response.url, response.status_code)

def consent_message(context_id):
    response = requests.post("https://test.trunomi.com/ledger/context/" + context_id + "/" + "message",
                             json={
                                  "payload": {
                                    "consentDefinitionId": 0,
                                    "event": "string",
                                    "message": "string",
                                    "customData": "string",
                                    "moc": "string",
                                    "justification": "string",
                                    "genericFields": {
                                      "products": [
                                        "string"
                                      ],
                                      "dataController": "string",
                                      "jurisdiction": "string",
                                      "preferences": [
                                        "string"
                                      ]
                                    }
                                }
                             },
                             headers={"authorization": create_jwt()})
    print(response.url, response.status_code, response.text)

def consent_deny(context_id):
    response = requests.post("https://test.trunomi.com/ledger/context/" + context_id + "/" + "consent-deny",
                             json={"payload": {
                                 "consentDefinitionId": 0,
                                 "customData": "string",
                                 "moc": "string",
                                 "genericFields": {
                                     "products": [
                                         "string"
                                     ],
                                     "dataController": "string",
                                     "jurisdiction": "string",
                                     "preferences": [
                                         "string"
                                     ]
                                 },
                             }
                             },
                             headers={"authorization": create_jwt()})
    print(response.url, response.status_code, response.text)

def consent_grant(context_id):
    response = requests.post("https://test.trunomi.com/ledger/context/" + context_id + "/" + "consent-grant",
                     json={"payload": {
                         "consentDefinitionId": 0,
                         "customData": "string",
                         "moc": "string",
                         "genericFields": {
                             "products": [
                                 "string"
                             ],
                             "dataController": "string",
                             "jurisdiction": "string",
                             "preferences": [
                                 "string"
                             ]
                         },
                         "dataTypeId": "4c0caf30-4c6f-11e7-907c-716e1cb74214"
                     }
                     },
                     headers={"authorization": create_jwt()})
    print(response.url, response.status_code, response.text)


def consent_revoke(context_id):
    response = requests.post("https://test.trunomi.com/ledger/context/" + context_id + "/" + "consent-revoke",
                 json={"payload": {
                     "consentDefinitionId": 0,
                     "customData": "string",
                     "moc": "string",
                     "genericFields": {
                         "products": [
                             "string"
                         ],
                         "dataController": "string",
                         "jurisdiction": "string",
                         "preferences": [
                             "string"
                         ]
                     }
                 }
                 },
                 headers={"authorization": create_jwt()})
    print(response.url, response.status_code, response.text)


@ddt
@file_data('./ids.json')
def consent_rights(data_type_id, context_id):
    response = requests.post("https://test.trunomi.com/rights/query",
                 json={
                  "contextId": context_id,
                  "consentDefinitionId": 0,
                  "dataTypeId": [
                    data_type_id
                  ]
                 },
                 headers={"authorization": create_jwt()})
    print(response.url, response.status_code, response.text)


ledger_list()
consent_last_ledger("77791cf0-4c9a-11e7-83e5-950adef43067")
consent_message("77791cf0-4c9a-11e7-83e5-950adef43067")
consent_deny("77791cf0-4c9a-11e7-83e5-950adef43067")
consent_grant("77791cf0-4c9a-11e7-83e5-950adef43067")
consent_revoke("77791cf0-4c9a-11e7-83e5-950adef43067")
consent_rights("77791cf0-4c9a-11e7-83e5-950adef43067", "4c0caf30-4c6f-11e7-907c-716e1cb74214")
