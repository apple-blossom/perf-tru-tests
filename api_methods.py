import requests
import binascii
import jwt
import ast


class ApiRequests(object):

    """
    API methods for tests, gets data from ./helpers/debug_data.json,
    For debugging uncomment print() lines
    """

    def copy_all_file_text(self, path):
            with open(path, 'r') as f:
                data = f.read()
            return data

    def generate_basic_token(self, auth_data):
        """
        Generated Basic token with the help of base64 encoding of 'username:password' string
        :param auth_data: a string of username and password separated by colon, 'username:password'
        :return: returns basic token in bytes string
        """
        auth_data = auth_data.encode()
        token = binascii.b2a_base64(auth_data)
        token = b'Basic ' + token
        token = str(token)
        token = token[2:-3]
        return token

    def create_jwt_token_for_admin(self, host_address, username, password, token):
        """
        Generates JWT for admin
        :param host_address: URL for token to be generated on, like "https://test.trunomi.com", string
        :param username: admin username
        :param password: admin password
        :param token: basic token, generated with generate_basic_token()
        :return: returns JWT for admin
        """
        response = requests.post(host_address + "/auth",
                                 data={"username": username,
                                       "password": password},
                                 headers={"authorization": token})
        if response.status_code == 204:
            return response.headers["www-authenticate"]
        else:
            raise AssertionError("\x1b[31m Invalid status code \x1b[0m", response.status_code, "\n", response.text)

    def reset_demo_data_via_api(self, host_address, jwt_token, username, password):
        """
        Resets demo data on portal for certain user, like the Reset demo data button
        :param host_address: URL where the data will be reset, like "https://test.trunomi.com", string
        :param jwt_token: JWT token generated for ADMIN via create_jwt_token_for_admin(), byte string
        :param username: admin username
        :param password: admin password
        :return: status code 204
        """
        response = requests.get(host_address + "/enterprise-portal/stats/reset-demo",
                                data={"username": username,
                                      "password": password},
                                headers={"authorization": jwt_token})
        # print(response.url, response.status_code)
        if response.status_code != 204:
            raise AssertionError("\x1b[31m Invalid status code \x1b[0m", response.status_code, "\n", response.text)

    def create_consent_action_with_api(self, host_address, data_type_id, consent_type, jwt_token, context_id):
        """
        Creates a consent action, like consent-grant
        :param host_address: URL where consent action will be created, like "https://test.trunomi.com", string
        :param data_type_id: DT ID bounded to this context, string
        :param consent_type: consent type like named in Swagger, string
        :param jwt_token: JWT token generated for user with create_jwt_for_user()
        or for admin with create_jwt_token_for_admin(), byte string
        :param context_id: : context (purpose) ID bounded to this DSR, string
        :return: status code 200
        """
        response = requests.post(host_address + "/ledger/context/" + context_id + "/" + consent_type,
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
                                    "dataTypeId": data_type_id
                                 }
                                 },
                                 headers={"authorization": jwt_token})
        # print(response.status_code, response.text, response.url)
        if response.status_code != 200:
            raise AssertionError("\x1b[31m Invalid response status code \x1b[0m",
                                 response.status_code, "\n", response.text)

    def create_jwt_for_user(self, user, enterprise_id, path_to_key):
        """
        :param user: enterprise user, like "sarah_6", stored in data.json
        :param enterprise_id:  enterprise id, stored in data.json
        :param path_to_key:  path to private key
        :return: returns JWT token for user
        """
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
        # print(result)
        return result

    def create_dsrs_with_api(self, host_address, dsr_type, jwt_token, data_type):
        """
        Creates a Data subject request with API - Accept, Rectify, Erase
        :param host_address: URL where DSR will be created, like "https://test.trunomi.com", string
        :param dsr_type: name of DSR as named in Swagger, like "dar", string
        :param jwt_token: JWT token generated for user with create_jwt_for_user()
        or for admin with create_jwt_token_for_admin(), byte string
        :param data_type: data type ID bounded to this DSR, string
        """
        response = requests.post(host_address + "/ledger/context/" + data_type + "/" + dsr_type,
                                 json={"payload": {
                                        "customData": "string",
                                        "reasons": [
                                            "string"
                                          ],
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
        # print(response.url, response.status_code)
        if response.status_code != 200:
            raise AssertionError("\x1b[31m Invalid response status code \x1b[0m",
                                 response.status_code, "\n", response.text, response.url)

    def create_dsr_actions_with_api(self, host_address, dsr_type, jwt_token, data_type_id, message="string"):
        """
        Creates DSR ACTION with API after data subject request is created, like Dar-Access, Dar-Decline
        :param host_address: URL where DST action will be created, like "https://test.trunomi.com", string
        :param dsr_type: name of DSR action as named in Swagger, like "dar-accept", string
        :param jwt_token: JWT token generated for user with create_jwt_for_user()
        or for admin with create_jwt_token_for_admin(), byte string
        :param data_type_id: data type ID bounded to this DSR, string
        :param message: the DSR reason message, string
        """
        response = requests.post(host_address + "/ledger/context/" + data_type_id + "/" + dsr_type,
                                 json={"payload": {
                                    "customData": "string",
                                    "reasons": [
                                        "string"
                                      ],
                                    "message": message,
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
        # print(response.url, response.status_code)
        if response.status_code != 200:
            raise AssertionError("\x1b[31m Invalid response status code \x1b[0m",
                                 response.status_code, "\n", response.text, response.url)

    def get_ledger(self, host_address, jwt, customer_id, enterprise_id):
        print("DATA\n", host_address, jwt, customer_id, enterprise_id)
        response = requests.get(host_address + "/ledger",
                                data={"customerId": customer_id,
                                      "enterpriseId": enterprise_id},
                                headers={"authorization": jwt})
        print(response.url, response.status_code, response.text)
