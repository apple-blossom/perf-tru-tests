import jwt
from locust import HttpLocust, TaskSet, task
from base import Base
from test_widgets import TestWidgets
# from pages import *
# from locators import *
# from api_methods import ApiRequests


class LoadTest(TaskSet, Base):

    RAND_ID = Base.random_user_id()

    def create_jwt(self):
        enterprise = self.open_data_json()["enterprise_id"]
        user = self.RAND_ID
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

    @task(1)
    def ledger_list(self):
        self.client.get("/ledger",
                                data={"customerId": self.RAND_ID,
                                      "enterpriseId": self.open_data_json()["enterprise_id"]},
                                headers={"authorization": self.create_jwt()})

    # @task(1)
    # def consent_last_ledger(self):
    #     self.client.get("https://test.trunomi.com/ledger/context/" + self.open_data_json()["context_ids"][0] + "/last",
    #                             data={"customerId": self.RAND_ID,
    #                                   "enterpriseId": self.open_data_json()["enterprise_id"]},
    #                             headers={"authorization": self.create_jwt()}
    #                             )

    @task(2)
    def consent_message(self):
        res = self.client.post("/ledger/context/" + self.open_data_json()["context_ids"][0] + "/" + "message",
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
                                 headers={"authorization": self.create_jwt()})
        print(res.content)

    def consent_deny(self, context_id):
        self.client.post("/ledger/context/" + context_id + "/" + "consent-deny",
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
                         headers={"authorization": self.create_jwt()})
        print(res.content)

    def consent_grant(self, context_id):
        res = self.client.post("/ledger/context/" + context_id + "/" + "consent-grant",
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
        print(res.content)

    def consent_revoke(self, context_id):
        res = self.client.post("/ledger/context/" + context_id + "/" + "consent-revoke",
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
                         headers={"authorization": self.create_jwt()})
        print(res.content)

    def consent_rights(self, data_type_id, context_id):
        res = self.client.post("/rights/query",
                         json={
                             "contextId": context_id,
                             "consentDefinitionId": 0,
                             "dataTypeId": [
                                 data_type_id
                             ]
                         },
                         headers={"authorization": self.create_jwt()})
        print(res.content)

    @task(2)
    def grant_revoke_get_rights(self):
        count = 0
        for el in self.open_ids_json():
            # self.consent_deny(el["context_id"])
            print(el, count)
            self.consent_grant(el["context_id"])
            self.consent_revoke(el["context_id"])
            self.consent_rights(el["data_type_id"], el["context_id"])
            count += 1


class MyLocust(HttpLocust):
    task_set = LoadTest
    min_wait = 5000
    max_wait = 15000
