import numpy as np
import pandas as pd
from swxtools.config import config
from swxtools import download_tools


def download(filetype='all'):
    local_dir = config['local_source_data_path'] + "/silso"
    download_tools.ensure_data_dir(local_dir)
    files_to_download = []
    if filetype == 'total' or filetype == 'all':
        files_to_download.append(
            {'url': 'https://www.sidc.be/silso/DATA/SN_d_tot_V2.0.txt',
             'local_path': f'{local_dir}/SN_d_tot_V2.0.txt',
             'max_age': pd.to_timedelta(7, 'D')}
        )
    if filetype == 'current' or filetype == 'all':
        files_to_download.append(
            {'url': 'https://www.sidc.be/silso/DATA/EISN/EISN_current.txt',
             'local_path': f'{local_dir}/EISN_current.txt',
             'max_age': pd.to_timedelta(3, 'H')}
        )
    downloaded_files = download_tools.download_files(files_to_download)
    return downloaded_files


def txt_to_dataframe(filename, convert_column_names=False):
    if 'SN_d_tot_V2.0' in filename:
        columns = [
            "Year",
            "Month",
            "Day",
            "Decimal date",
            "Daily sunspot number",
            "Standard deviation",
            "Number of observations",
            "Star",
        ]
    elif "EISN_current" in filename:
        columns = [
            "Year",
            "Month",
            "Day",
            "Decimal date",
            "Estimated Sunspot Number",
            "Estimated Standard Deviation",
            "Number of Stations calculated",
            "Number of Stations available ",
        ]
    df = pd.read_csv(filename, delim_whitespace=True, names=columns,
                     parse_dates={'DateTime': ['Year', 'Month', 'Day']},
                     index_col='DateTime').replace(-1, np.nan)

    if convert_column_names:
        df.rename({'Daily sunspot number': 'sunspot_number',
                   'Estimated Sunspot Number': 'sunspot_number',
                   'Estimated Standard Deviation': 'standard_deviation'},
                  axis=1, inplace=True)
    return df
