import requests
import json
import pandas as pd
import logging
import sys

class APIError(Exception):
    pass


def create_dataset(server, key, dataset_metadata):
    url = f'{server}/api/datasets?key={key}'
    logging.info(f"Adding new dataset using POST to url: {url}")
    r = requests.post(url=url, json=dataset_metadata)
    if not r.ok:
        raise APIError(json.loads(r.content))


def delete_dataset(server, key, dataset_id):
    print("This does not work right now, check again after knmi-hapi-server updates")
    r = requests.delete(url=f'{server}/api/dataset?key={key}&id={dataset_id}')
    if not r.ok:
        raise APIError(json.loads(r.content))


def add_data(server, key, dataset_id, dataframe):
    # print("Shape: ", dataframe.shape)
    N_ROWS = 100000  # number of rows in chunk
    list_dataframes = [dataframe.iloc[i:i+N_ROWS] for i in range(0,dataframe.shape[0],N_ROWS)]
    url = f'{server}/api/dataset?key={key}'
    for i_df, df in enumerate(list_dataframes):
        data_obj = {'id': dataset_id,
                    'parameters': list(df.columns),
                    'data': df.values.tolist()}
        data_obj['id'] = dataset_id
        logging.info(f"Sending {sys.getsizeof(json.dumps(data_obj))} bytes of JSON data for block {i_df+1}/{len(list_dataframes)} using POST to url: {url} for table {dataset_id}.")
        r = requests.post(url, json=data_obj)
        if not r.ok:
            raise APIError(json.loads(r.content))


def get_hapi_catalog(server):
    r = requests.get(url=f'{server}/hapi/catalog')
    if not r.ok:
        raise APIError(r.content)
    else:
        return json.loads(r.content)


def get_hapi_info(server, dataset_id):
    r = requests.get(url=f'{server}/hapi/info?id={dataset_id}')
    # if not r.ok:
    #    raise APIError(json.loads(r.content))
    return json.loads(r.content)
