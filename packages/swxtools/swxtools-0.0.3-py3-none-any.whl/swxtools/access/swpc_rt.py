import numpy as np
import pandas as pd
import os
import json
import logging
from swxtools import download_tools
from swxtools.config import config


def download_data(datatype='plasma'):
    """
    Download real-time data from NOAA/SWPC in JSON format.

    Args:
        datatype ('plasma', 'mag', 'xrays', 'xray-flares', 'integral-protons',
                  'integral-electrons'): Type of data

    Returns:
        List of downloaded file(s).

    Remarks:
        To keep a record of older real-time data, the current date is appended
          to the local file's basename.
    """
    datestr = pd.Timestamp.utcnow().strftime("%Y-%m-%d")
    if datatype == 'plasma':
        baseurl = 'https://services.swpc.noaa.gov/products/solar-wind/'
        remote_file = 'plasma-7-day.json'
        local_file = f'plasma-7-day_{datestr}.json'
    elif datatype == 'mag':
        baseurl = 'https://services.swpc.noaa.gov/products/solar-wind/'
        remote_file = 'mag-7-day.json'
        local_file = f'mag-7-day_{datestr}.json'
    elif datatype == 'xrays':
        baseurl = 'https://services.swpc.noaa.gov/json/goes/primary/'
        remote_file = 'xrays-7-day.json'
        local_file = f'xrays-7-day_{datestr}.json'
    elif datatype == 'xray-flares':
        baseurl = 'https://services.swpc.noaa.gov/json/goes/primary/'
        remote_file = 'xray-flares-7-day.json'
        local_file = f'xray-flares-7-day_{datestr}.json'
    elif datatype == 'integral-protons':
        baseurl = 'https://services.swpc.noaa.gov/json/goes/primary/'
        remote_file = 'integral-protons-7-day.json'
        local_file = f'integral-protons-7-day_{datestr}.json'
    elif datatype == 'integral-electrons':
        baseurl = 'https://services.swpc.noaa.gov/json/goes/primary/'
        remote_file = 'integral-electrons-7-day.json'
        local_file = f'integral-electrons-7-day_{datestr}.json'
    else:
        logging.error(f"Unknown SWPC realtime data type: {datatype}")
        return []

    files_to_download = []
    local_data_dir = f"{config['local_source_data_path']}/swpc/rt/{datatype}"
    download_tools.ensure_data_dir(local_data_dir)
    local_filename = f"{local_data_dir}/{local_file}"
    url = f"{baseurl}/{remote_file}"
    files_to_download.append({'url': url, 'local_path': local_filename,
                              'max_age': pd.to_timedelta(1, 'min')})
    filenames = download_tools.download_files(files_to_download)

    return filenames


def mark_gaps_in_dataframe(df):
    """
    Look for gaps and add np.nan record to enforce breaks in plotted lines

    Args:
        df: Pandas DataFrame object, must have DatetimeIndex as index

    Returns:
        DataFrame with nan-records appended inside gaps.
    """
    nominal_timedelta = pd.to_timedelta(1, 'min')
    deltas = pd.Series(df.index).diff()[1:]
    gaps = deltas[deltas > nominal_timedelta] / nominal_timedelta
    df_gapfilled = df.copy()

    data_nans = {col: np.nan for col in df.columns}

    for i, gap in gaps.items():
        # Add a np.nan record after the start of each gap,
        # to force breaks in plotted lines
        time_gap_start = df.index[i-1] + nominal_timedelta
        df_new_record = pd.DataFrame(data=data_nans, index=[time_gap_start])
        df_gapfilled = pd.concat([df_gapfilled, df_new_record]).sort_index()

        # For gaps longer than 1 record, also add a np.nan record before the
        # end of the gap
        if gap > 2:
            time_gap_end = df.index[i] - nominal_timedelta
            df_new_record = pd.DataFrame(data=data_nans, index=[time_gap_end])
            df_gapfilled = pd.concat([df_gapfilled,
                                      df_new_record]).sort_index()

    return df_gapfilled


def json_to_dataframe(filename, mark_gaps=True):
    """
    Reads the real-time data timeseries into a Pandas DataFrame.

    Args:
        filename (string): Name of the .json file

    Returns:
        Pandas DataFrame containing the timeseries data.
    """
    basename = os.path.basename(filename)
    if 'plasma' in filename or 'mag' in basename:
        with open(filename) as fh:
            jsondata = json.load(fh)
        names = jsondata[0][1:]
        data = np.array(jsondata[1:])[:, 1:].astype(float)
        datetimes = pd.to_datetime(np.array(jsondata[1:])[:, 0])
        df = pd.DataFrame(data=data, columns=names, index=datetimes)
        df.replace(0.0, np.nan, inplace=True)
    elif 'xrays' in basename:
        # Real-time X-ray flux data from GOES XRS
        df = pd.read_json(filename)
        df.index = pd.to_datetime(df['time_tag'], utc=True)
        energies = ['0.05-0.4nm', '0.1-0.8nm']
        df_energies = pd.DataFrame()
        for energy in energies:
            df_energies[f'{energy}'] = df[df['energy'] == energy]['flux']
        df = df_energies
    elif 'xray-flares' in basename:
        # Real-time X-ray flare classifications based on GOES XRS data
        df = pd.read_json(filename)
        df.index = pd.to_datetime(df['time_tag'], utc=True)
    elif 'integral-protons' in basename:
        # Real-time integral proton flux from primary GOES satellite
        df = pd.read_json(filename)
        df.index = pd.to_datetime(df['time_tag'], utc=True)
    elif 'integral-electrons' in basename:
        # Real-time integral proton flux from primary GOES satellite
        df = pd.read_json(filename)
        df.index = pd.to_datetime(df['time_tag'], utc=True)
    else:
        logging.error("Unknown SWPC realtime data type: {datatype}")
        return None

    if mark_gaps:
        df = mark_gaps_in_dataframe(df)

    return df


if __name__ == '__main__':
    allowed_types = [
        'plasma',
        'mag',
        'xrays',
        'xray-flares',
        'integral-protons',
        'integral-electrons'
    ]

    for data_type in allowed_types:
        download_data(data_type)
