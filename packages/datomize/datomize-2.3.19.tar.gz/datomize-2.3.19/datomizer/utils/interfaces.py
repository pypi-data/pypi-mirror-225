import requests


class DatoClientInterface(object):
    def api_request(self, method: requests.Request,
                    url: str, headers: {} = {}, url_params: [] = [], **kwargs) -> requests.Response:
        pass

    def get_response_json(self, method: requests.Request,
                          url: str, headers: {} = {}, url_params: [] = [], **kwargs):
        pass


class DatoCommonInterface(object):
    def wait(self):
        pass

    def list_tables(self):
        pass


class DatoGenInterface(DatoCommonInterface):
    def get_generated_data(self):
        pass

    def get_generated_data_csv(self, table_name: str = None):
        pass
