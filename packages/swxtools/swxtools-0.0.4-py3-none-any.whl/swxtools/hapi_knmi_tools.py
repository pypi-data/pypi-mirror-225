import re

# Helper functions for parsing the HAPI catalog
def is_iso_duration(duration_string):
    regex = '^[-+]?P(?!$)(([-+]?\d+Y)|([-+]?\d+\.\d+Y$))?(([-+]?\d+M)|([-+]?\d+\.\d+M$))?(([-+]?\d+W)|([-+]?\d+\.\d+W$))?(([-+]?\d+D)|([-+]?\d+\.\d+D$))?(T(?=[\d+-])(([-+]?\d+H)|([-+]?\d+\.\d+H$))?(([-+]?\d+M)|([-+]?\d+\.\d+M$))?([-+]?\d+(\.\d+)?S)?)??$'
    return re.fullmatch(regex, duration_string) is not None

def dataset_split_root_and_cadence(dataset_id):
    parts = dataset_id.split('_')
    if is_iso_duration(parts[-1]):
        cadence_str = parts[-1]
        cadence_sec = pd.to_timedelta(cadence_str)/pd.to_timedelta(1, 'sec')
        return {'dataset': dataset_id, 'root': "_".join(parts[0:-1]), 'cadence_iso': parts[-1], 'cadence_sec': cadence_sec}
    elif parts[-1].endswith('Hz'):
        freq_str = parts[-1]
        cadence_sec = 1/float(freq_str[0:-2])
        return {'dataset': dataset_id, 'root': "_".join(parts[0:-1]), 'cadence_iso': freq_str, 'cadence_sec': cadence_sec}
    else:
        return {'dataset': dataset_id, 'root': dataset_id}


# Add routines here to check whether datasets on HAPI server and python metadata match

# catalog_dataset_ids = list(map(lambda x: x['id'], catalog_request['catalog']))
# parsed_catalog = list(map(dataset_split_root_and_cadence, catalog_dataset_ids))
# dataset_cadences = sorted(list(filter(lambda x: x['root'] == parsed_dataset['root'], parsed_catalog)), key=lambda x: x['cadence_sec'])
# dataset_cadence_isostrings = list(map(lambda x: x['cadence_iso'], dataset_cadences))
