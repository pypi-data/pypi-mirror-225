import atexit
from datomizer.utils.interfaces import DatoClientInterface
from datomizer.helpers.authentication.authentication_helper import *
from datomizer.utils.exceptions import InvalidResponse
from datomizer.utils.general import ACCESS_TOKEN, REFRESH_TOKEN, AUTHORIZATION, BEARER_TOKEN, D_REALM
from datomizer.protos.autodiscoveryservice_pb2 import SchemaDiscoveryDTO
from datomizer.helpers.estimation.estimation_helper import estimate_gen


class Datomizer(DatoClientInterface):
    __domain: str
    __realm: str
    __access_token: str
    __refresh_token: str
    __auth_headers: dict

    def __init__(self, username: str, password: str, env: str = 'app'):
        """Create an authentication object and register Datomize on it using the Datomizer constructor

        Args:
            username: your username
            password: your password
        Returns:
            Datomizer Authentication object"""
        self.__domain = get_domain_by_username(username=username, env=env)
        self.__realm = get_realm_by_domain(domain=self.__domain)
        token_response = post_token(realm=self.__realm, domain=self.__domain,
                                    username=username, password=password)
        self.__config_token(token_response)
        atexit.register(self.log_out)

    def __refresh_token_headers(self):
        token_response = post_refresh_token(realm=self.__realm,
                                            domain=self.__domain,
                                            token=self.__refresh_token)
        self.__config_token(token_response)

    def __config_token(self, token_response):
        try:
            self.__access_token = token_response[ACCESS_TOKEN]
            self.__refresh_token = token_response[REFRESH_TOKEN]
            self.__auth_headers = {AUTHORIZATION: BEARER_TOKEN % self.__access_token, D_REALM: self.__realm}
        except Exception as ex:
            print(f"token res:{token_response}")
            raise ex

    def get_response_json(self, method: requests.Request,
                          url: str, headers: {} = {}, url_params: [] = [], **kwargs):
        return self.api_request(method=method, url=url, headers=headers, url_params=url_params, **kwargs).json()

    def api_request(self, method: requests.Request,
                    url: str, headers: {} = {}, url_params: [] = [], **kwargs) -> requests.Response:
        kwargs['url'] = url % (self.__domain, *url_params)

        headers.update(self.__auth_headers)
        kwargs['headers'] = headers
        response: requests.Response = method(**kwargs)

        # refresh token and retry on unauthorized or forbidden request
        if response.status_code in [401, 403]:
            self.__refresh_token_headers()
            headers.update(self.__auth_headers)
            response = method(**kwargs)

        self.validate_response(response)
        return response

    def estimate_gen(self, n_records: int, data_size: float,
                     n_cat_cols: int, n_num_cols: int, n_date_cols: int, n_id_cols: int, n_short_text_cols: int,
                     n_long_text_cols: int, min_categories: int, max_categories: int, sum_unique_cat: int,
                     n_new_columns: int, n_calculations: int, n_constraints: int) -> int:
        return estimate_gen(self, n_records, data_size, n_cat_cols, n_num_cols, n_date_cols, n_id_cols, n_short_text_cols,
                            n_long_text_cols, min_categories, max_categories, sum_unique_cat,
                            n_new_columns, n_calculations, n_constraints)

    def base_validation(self):
        if not (self.__realm and self.__domain):
            raise Exception("missing base properties")

    def next_step_validation(self):
        if not self.__access_token:
            raise Exception("access token is not configured")

    @staticmethod
    def validate_response(response: requests.Response, not_valid_message: str = "Status is not OK"):
        if response.status_code != 200:
            raise InvalidResponse(response, not_valid_message)

    def log_out(self):
        post_log_out(realm=self.__realm, domain=self.__domain,
                     token=self.__access_token, refresh_token=self.__refresh_token)
