import json
import jwt
import requests


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
    user = "sarah_6@gmail.com"
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
                            data={"customerId": open_data_json()["user"],
                                  "enterpriseId": open_data_json()["enterprise_id"]},
                            headers={"authorization": create_jwt()})
    print(response.url, response.status_code)

def consent_last_ledger():
    response = requests.get("https://test.trunomi.com/ledger/context/" + open_data_json()["context_ids"][4] + "/last",
                 data={"customerId": "ererer",
                       "enterpriseId": open_data_json()["enterprise_id"]},
                 headers={"authorization": create_jwt()}
                 )
    print(response.url, response.status_code)

def consent_message():
    response = requests.post("https://test.trunomi.com/ledger/context/" + open_data_json()["context_ids"][4] + "/" + "message",
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

def consent_deny():
    response = requests.post("https://test.trunomi.com/ledger/context/" + open_data_json()["context_ids"][4] + "/" + "consent-deny",
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

def consent_grant():
    response = requests.post("https://test.trunomi.com/ledger/context/" + open_data_json()["context_ids"][4] + "/" + "consent-grant",
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
    # print(response.url, response.status_code, response.text)


def consent_revoke():
    response = requests.post("https://test.trunomi.com/ledger/context/" + open_data_json()["context_ids"][4] + "/" + "consent-revoke",
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
    # print(response.url, response.status_code, response.text)

def consent_rights():
    response = requests.post("https://test.trunomi.com/rights/query",
                 json={
                  "contextId": "string",
                  "consentDefinitionId": 0,
                  "dataTypeId": [
                    "string"
                  ]
                 },
                 headers={"authorization": create_jwt()})
    print(response.url, response.status_code, response.text)


# ledger_list()
# consent_last_ledger()
# consent_message()
# consent_deny()
# consent_grant()
# consent_revoke()
consent_rights()
