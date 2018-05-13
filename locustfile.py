import json
import jwt
from locust import HttpLocust, TaskSet, task
from .base import Base
from .pages import *
from .locators import *


class Helpers(TaskSet, Base):

    def copy_all_file_text(self, path):
            with open(path, 'r') as f:
                data = f.read()
            return data

    def open_data_json(self):
        with open('./data.json', 'r') as f:
            file = json.load(f)
            data = dict(enterprise_id=file['ENTERPRISE_ID'], user=file['CUSTOMER_ID'],
                        host_address=file['HOST_ADDRESS'], path_to_key=file['PATH_TO_KEY'],
                        dt_ids=file['DATA_TYPE_IDS'], context_ids=file['CONTEXT_IDS'],
                        widgets=file['WIDGETS_URL'])
        return data

    def create_jwt(self):
        enterprise = self.open_data_json()["enterprise_id"]
        user = self.open_data_json()["user"]
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
        key = self.copy_all_file_text(self.open_data_json()["path_to_key"])
        result = jwt.encode(payload, key, algorithm='RS512')
        result = b"Bearer " + result
        return result

    def on_start(self):
        print("Hello! 2")

    @task(2)
    def ledger_list(self):
        self.client.get("/ledger",
                        data={"customerId": self.open_data_json()["user"],
                              "enterpriseId": self.open_data_json()["enterprise_id"]},
                        headers={"authorization": self.create_jwt()})
        # print(response.url, response.status_code)

    @task(3)
    def consent_grant_deny(self):
        self.client.get("/ledger/context/" + self.open_data_json()["context_ids"][4] + "/last",
                        data={"customerId": self.open_data_json()["user"],
                              "enterpriseId": self.open_data_json()["enterprise_id"]},
                        headers={"authorization": self.create_jwt()}
                        )
        # print(response.url, response.text)
        self.client.post("/ledger/context/" + self.open_data_json()["context_ids"][4] + "/" + "consent-grant",
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
                         headers={"authorization": self.create_jwt()})

        # self.client.post("/ledger/context/" + self.open_data_json()["context_ids"][4] + "/" + "consent-revoke",
        #                  json={"payload": {
        #                      "consentDefinitionId": 0,
        #                      "customData": "string",
        #                      "moc": "string",
        #                      "genericFields": {
        #                          "products": [
        #                              "string"
        #                          ],
        #                          "dataController": "string",
        #                          "jurisdiction": "string",
        #                          "preferences": [
        #                              "string"
        #                          ]
        #                      },
        #                      "dataTypeId": "4c0caf30-4c6f-11e7-907c-716e1cb74214"
        #                  }
        #                  },
        #                  headers={"authorization": self.create_jwt()})


class MyLocust(HttpLocust):
    task_set = Helpers
    min_wait = 5000
    max_wait = 15000
