import json

import requests

from datomizer.utils.constants import DATAPLANE_POST_ESTIMATE_BY_PARAMS, DATAPLANE_POST_ESTIMATE_BY_SCHEMA
from datomizer.utils.interfaces import DatoClientInterface


def estimate_gen(datomizer: DatoClientInterface, n_records: int, data_size: float,
                 n_cat_cols: int, n_num_cols: int, n_date_cols: int, n_id_cols: int, n_short_text_cols: int,
                 n_long_text_cols: int, min_categories: int, max_categories: int, sum_unique_cat: int,
                 n_new_columns: int, n_calculations: int, n_constraints: int) -> int:
    return int(datomizer.api_request(requests.post,
                                     url=DATAPLANE_POST_ESTIMATE_BY_PARAMS,
                                     headers={"Content-Type": "application/json"},
                                     data=json.dumps({"data_size": data_size, "max_categories": max_categories, "min_categories": min_categories,
                                                      "n_calculations": n_calculations, "n_cat_cols": n_cat_cols, "n_constraints": n_constraints,
                                                      "n_date_cols": n_date_cols, "n_id_cols": n_id_cols, "n_long_text_cols": n_long_text_cols,
                                                      "n_new_columns": n_new_columns, "n_num_cols": n_num_cols, "n_records": n_records,
                                                      "n_short_text_cols": n_short_text_cols, "sum_unique_cat": sum_unique_cat})).text)


def estimate_gen_after_discovery(datomizer: DatoClientInterface, project_id: str, flow_id: str) -> int:
    return int(datomizer.api_request(requests.post,
                                     url=DATAPLANE_POST_ESTIMATE_BY_SCHEMA,
                                     headers={"Content-Type": "application/json"},
                                     data=json.dumps({
                                         "projectId": project_id,
                                         "flowId": flow_id
                                     })).text)
