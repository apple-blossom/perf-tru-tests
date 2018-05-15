import jwt
# import unittest

from locust import HttpLocust, TaskSet, task

from base import Base
import test_widgets


class LoadTest(TaskSet, Base):

    def create_jwt(self, user):
        enterprise = self.open_data_json()["enterprise_id"]
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

    @task(2)
    def ledger_list(self):
        user = self.random_user_id()
        self.client.get("/ledger",
                                data={"customerId": self.random_user_id(),
                                      "enterpriseId": self.open_data_json()["enterprise_id"]},
                                headers={"authorization": self.create_jwt(user)})

    def consent_message(self, context_id, consent_id, jwt_token):
        res = self.client.post("/ledger/context/" + context_id + "/" + "message",
                                 json={
                                     "payload": {
                                         "consentDefinitionId": consent_id,
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
                                 headers={"authorization": jwt_token})
        if res.status_code != 200:
            print(res.content, res.url, context_id)

    def consent_deny(self, context_id, consent_id, jwt_token):
        res = self.client.post("/ledger/context/" + context_id + "/" + "consent-deny",
                         json={"payload": {
                             "consentDefinitionId": consent_id,
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
        if res.status_code != 200:
            print(res.content, res.url, context_id)

    def consent_grant(self, context_id, consent_id, dt, jwt_token):
        res = self.client.post("/ledger/context/" + context_id + "/" + "consent-grant",
                         json={"payload": {
                             "consentDefinitionId": consent_id,
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

    def consent_revoke(self, context_id, consent_id, jwt_token):
        res = self.client.post("/ledger/context/" + context_id + "/" + "consent-revoke",
                         json={"payload": {
                             "consentDefinitionId": consent_id,
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
        if res.status_code != 200:
            print(res.content, res.url, context_id)

    def consent_rights(self,context_id, consent_id,  data_type_id, jwt_token):
        res = self.client.post("/rights/query",
                         json={
                             "contextId": context_id,
                             "consentDefinitionId": consent_id,
                             "dataTypeId": [
                                 data_type_id
                             ]
                         },
                         headers={"authorization": jwt_token})
        if res.status_code != 200:
            print(res.content, res.url, data_type_id, context_id)

    @task(4)
    def grant_revoke_get_rights(self):
        user = self.random_user_id()
        # print("USER", user)
        jwt_token = self.create_jwt(user)
        for el in self.open_ids_json():
            # print(el["context_id"], el["data_type_id"])
            self.consent_grant(el["context_id"], el["consent_id"], el["data_type_id"], jwt_token)
            self.consent_revoke(el["context_id"], el["consent_id"],  jwt_token)
            self.consent_rights(el["context_id"],  el["consent_id"], el["data_type_id"], jwt_token)

    @task(8)
    def message_deny_get_rights(self):
        user = self.random_user_id()
        print("USER", user)
        jwt_token = self.create_jwt(user)
        for el in self.open_ids_json():
            # self.consent_deny(el["context_id"],  el["consent_id"], jwt_token)
            self.consent_message(el["context_id"], el["consent_id"], jwt_token)
            self.consent_rights(el["context_id"],  el["consent_id"], el["data_type_id"], jwt_token)

    # @task(1)
    # def run_selenium_test(self):
    #     test_widgets.unittest.main()


class MyLocust(HttpLocust):
    task_set = LoadTest
    min_wait = 5000
    max_wait = 15000
