import requests
import binascii
import jwt
from api_methods import ApiRequests
from locust import HttpLocust, TaskSet, task


class Helpers(TaskSet):

    # def __init__(self):
    #     super().__init__(self)
    #     self.jwt_user = ApiRequests.create_jwt_for_user(self, "sarah_6@gmail.com",
    #                                                     "358e5e20-4c65-11e7-b640-4be264b2cb75",
    #                                                     "./private_key.txt")

    def on_start(self):
        print("HEllo! 2")

    def copy_all_file_text(self, path):
            with open(path, 'r') as f:
                data = f.read()
            return data

    @task(2)
    def index(self):
        enterprise_id = "358e5e20-4c65-11e7-b640-4be264b2cb75"
        user = "sarah_6@gmail.com"
        path_to_key = "./private_key.txt"
        host_address = "https://perf.trunomi.com"

        payload = {
            "iss": enterprise_id,
            "aud": [
                "Trunomi",
                enterprise_id,
                user
            ],
            "jti": "86869840-1c96-11e8-b7fc-f162c8621d7f",
            "pol": "enterprise on behalf of customer",
            "sub": enterprise_id + "::" + user,
            "iat": 1519923598
        }
        key = self.copy_all_file_text(path_to_key)
        result = jwt.encode(payload, key, algorithm='RS512')
        result = b"Bearer " + result

        self.client.get("/ledger",
                                data={"customerId": user,
                                      "enterpriseId": enterprise_id},
                                headers={"authorization": result})
        # print(response.url, response.status_code)
        print("HEllo!")
        # jwt_user = ApiRequests.create_jwt_for_user(self, "sarah_6@gmail.com",
        #                                            "358e5e20-4c65-11e7-b640-4be264b2cb75",
        #                                            "./private_key.txt")
        # print("TOKEN \n", jwt_user)
        # # ApiRequests.get_ledger(self, "https://perf.trunomi.com", "sarah_6@gmail.com",
        #                        "358e5e20-4c65-11e7-b640-4be264b2cb75", jwt_user)

    @task(1)
    def profile(self):
        enterprise_id = "358e5e20-4c65-11e7-b640-4be264b2cb75"
        user = "sarah_6@gmail.com"
        path_to_key = "./private_key.txt"
        host_address = "https://perf.trunomi.com"

        payload = {
            "iss": enterprise_id,
            "aud": [
                "Trunomi",
                enterprise_id,
                user
            ],
            "jti": "86869840-1c96-11e8-b7fc-f162c8621d7f",
            "pol": "enterprise on behalf of customer",
            "sub": enterprise_id + "::" + user,
            "iat": 1519923598
        }
        key = self.copy_all_file_text(path_to_key)
        result = jwt.encode(payload, key, algorithm='RS512')
        result = b"Bearer " + result

        self.client.post("/ledger/context/" + "76747e30-4c9a-11e7-9100-d3d75d8f7d4f" + "/" + "consent-grant",
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
                                 headers={"authorization": result})
        # print(response.status_code, response.text, response.url)
        # if response.status_code != 200:
        #     raise AssertionError("\x1b[31m Invalid response status code \x1b[0m",
        #                          response.status_code, "\n", response.text)


# class UserBehavior(TaskSet):
#
#     def on_start(self):
#         print("HEllo! 2")
#
#     tasks = {Helpers.index: 2, Helpers.profile: 1}


class MyLocust(HttpLocust):
    task_set = Helpers
    min_wait = 5000
    max_wait = 15000
