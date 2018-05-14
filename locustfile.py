import jwt
from locust import HttpLocust, TaskSet, task
from base import Base
from test_widgets import TestWidgets
# from pages import *
# from locators import *
# from api_methods import ApiRequests


class LoadTest(TaskSet, Base):

    def create_jwt(self):
        enterprise = self.open_data_json()["enterprise_id"]
        user = self.random_user_id()
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

    @task(1)
    def ledger_list(self):
        self.client.get("/ledger",
                                data={"customerId": self.random_user_id(),
                                      "enterpriseId": self.open_data_json()["enterprise_id"]},
                                headers={"authorization": self.create_jwt()})

    @task(2)
    def consent_message(self):
        self.client.post("/ledger/context/" + self.open_data_json()["context_ids"][0] + "/" + "message",
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

    def consent_deny(self, context_id, jwt_token):
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
                         headers={"authorization": jwt_token})

    def consent_grant(self, context_id, dt, jwt_token):
        res = self.client.post("/ledger/context/" + context_id + "/" + "consent-grant",
                         json={"payload": {
                             "consentDefinitionId": 0, #add this!
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
                             "dataTypeId": dt
                         }
                         },
                         headers={"authorization": jwt_token})
        if res.status_code != 200:
            print(res.content, res.url, dt, context_id)

    def consent_revoke(self, context_id, jwt_token):
        self.client.post("/ledger/context/" + context_id + "/" + "consent-revoke",
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
                         headers={"authorization": jwt_token})

    def consent_rights(self, data_type_id, context_id, jwt_token):
        self.client.post("/rights/query",
                         json={
                             "contextId": context_id,
                             "consentDefinitionId": 0,
                             "dataTypeId": [
                                 data_type_id
                             ]
                         },
                         headers={"authorization": jwt_token})

    @task(2)
    def grant_revoke_get_rights(self):
        jwt_token = self.create_jwt()
        for el in self.open_ids_json():
            # print(el["context_id"], el["data_type_id"])
            self.consent_grant(el["context_id"], el["data_type_id"], jwt_token)
            self.consent_revoke(el["context_id"], jwt_token)
            self.consent_rights(el["data_type_id"], el["context_id"], jwt_token)


class MyLocust(HttpLocust):
    task_set = LoadTest
    min_wait = 5000
    max_wait = 15000
