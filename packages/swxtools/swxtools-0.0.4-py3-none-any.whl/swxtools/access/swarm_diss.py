import os
import glob
import pandas as pd
import numpy as np
import zipfile
import tempfile
# import pysatCDF
from spacepy import pycdf
import astropy.time
from swxtools import download_tools
from swxtools.config import config

gps_epoch_tai = astropy.time.Time("1980-01-06T00:00:00", scale='tai')
gps_epoch_utc = astropy.time.Time("1980-01-06T00:00:00", scale='utc')

sub_urls = {
    'MODx_SC':
        {
            'Swarm A': 'Level1b/Latest_baselines/MODx_SC/Sat_A/',
            'Swarm B': 'Level1b/Latest_baselines/MODx_SC/Sat_B/',
            'Swarm C': 'Level1b/Latest_baselines/MODx_SC/Sat_C/',
        },
    'DNSxPOD':
        {
            'Swarm A': 'Level2daily/Latest_baselines/DNS/POD/Sat_A/',
            'Swarm B': 'Level2daily/Latest_baselines/DNS/POD/Sat_B/',
            'Swarm C': 'Level2daily/Latest_baselines/DNS/POD/Sat_C/',
        },
    'DNSxACC':
        {
            'Swarm A': 'Level2daily/Latest_baselines/DNS/ACC/Sat_A/',
            'Swarm C': 'Level2daily/Latest_baselines/DNS/ACC/Sat_C/',
            'GRACE A': 'Multimission/GRACE/DNS/Sat_1/',
            'GRACE B': 'Multimission/GRACE/DNS/Sat_2/',
            'GRACE C': 'Multimission/GRACE-FO/DNS/Sat_1/',
            'CHAMP': 'Multimission/CHAMP/DNS/',
        },
    'SP3xCOM':
        {
            'Swarm A': 'Level2daily/Latest_baselines/POD/RD/Sat_A/',
            'Swarm B': 'Level2daily/Latest_baselines/POD/RD/Sat_B/',
            'Swarm C': 'Level2daily/Latest_baselines/POD/RD/Sat_C/',
        },
    'IPDxIRR':
        {
            'Swarm A': 'Level2daily/Latest_baselines/IPD/IRR/Sat_A/',
            'Swarm B': 'Level2daily/Latest_baselines/IPD/IRR/Sat_B/',
            'Swarm C': 'Level2daily/Latest_baselines/IPD/IRR/Sat_C/',
        },
    'FACxTMS':
        {
            'Swarm A': 'Level2daily/Latest_baselines/FAC/TMS/Sat_A/',
            'Swarm B': 'Level2daily/Latest_baselines/FAC/TMS/Sat_B/',
            'Swarm C': 'Level2daily/Latest_baselines/FAC/TMS/Sat_C/',
            'Swarm AC': 'Level2daily/Latest_baselines/FAC/TMS/Sat_AC/',
        },
    'NE':
        {
            'GRACE CD': 'MultiMission/GRACE-FO/NE/Dual_Sat/',
        },
    'TEC':
        {
            'GRACE A': 'MultiMission/GRACE/TEC/Sat_1/',
            'GRACE B': 'MultiMission/GRACE/TEC/Sat_2/',
            'GRACE C': 'MultiMission/GRACE-FO/TEC/Sat_1/',
            'GRACE D': 'MultiMission/GRACE-FO/TEC/Sat_2/',
        },
    'EFIx_LP':
        {
            'Swarm A': 'Level1b/Latest_baselines/EFIx_LP/Sat_A/',
            'Swarm B': 'Level1b/Latest_baselines/EFIx_LP/Sat_B/',
            'Swarm C': 'Level1b/Latest_baselines/EFIx_LP/Sat_C/',
        },
    'MAGx_LR':
        {
            'Swarm A': 'Level1b/Latest_baselines/MAGx_LR/Sat_A/',
            'Swarm B': 'Level1b/Latest_baselines/MAGx_LR/Sat_B/',
            'Swarm C': 'Level1b/Latest_baselines/MAGx_LR/Sat_C/',
        }
}


def filelist_to_dataframe(filelist):
    # Collect information from the filenames
    data = []
    for filename in filelist:
        basename = os.path.basename(filename)
        t0 = pd.to_datetime(basename[19:34], utc=True)
        t1 = pd.to_datetime(basename[35:50], utc=True)
        baseline = basename[51:53]
        version = basename[53:55]
        data.append({'t0': t0,
                     't1': t1,
                     'filename': basename,
                     'path': filename,
                     'baseline': int(baseline),
                     'version': int(version)})
    df = pd.DataFrame(data)

    # Keep only the highest version if t0 is the same
    df = df.sort_values('version', ascending=False).drop_duplicates('t0')

    # Set the index to t0, for easy searching
    df.index = df['t0']
    df.sort_index(inplace=True)
    return df


def download(sat='Swarm C', data_type='DNSxPOD', esa_eo_timespan=None, fast=False):
    if fast:
        local_data_dir = f"{config['local_source_data_path']}/swarm-diss_fast/"
        swarm_diss_url = f'ftp://swarm-diss.eo.esa.int/'
        username = 'fast'
        password = '6uDzOhGIdE3n$'

    else:
        local_data_dir = f"{config['local_source_data_path']}/swarm-diss/"
        swarm_diss_url = 'ftp://swarm-diss.eo.esa.int/'
        username = 'anonymous'
        password = ''

    if sat not in sub_urls[data_type]:
        return []

    sub_url = sub_urls[data_type][sat];
    if fast:
        sub_url = sub_url.replace("Latest_baselines/", "")

    print(sub_url)

    downloaded_files = download_tools.mirror(
        base_url=swarm_diss_url,
        sub_url=sub_url,
        local_dir=local_data_dir,
        esa_eo_timespan=esa_eo_timespan,
        username=username,
        password=password
    )
    return downloaded_files

def recurse_dirs(location):
    filelist = []
    listing = os.listdir(location)
    for item in listing:
        item_location = f"{location}/{item}"
        if os.path.isfile(item_location):
            filelist.append(item_location)
        elif os.path.isdir(item_location):
            filelist.extend(recurse_dirs(item_location))
    return filelist

class SwarmFiles():
    def __init__(self, data_type='DNSxPOD', sat='Swarm A', fast=False):
        if data_type not in sub_urls.keys():
            raise KeyError(f"'{data_type}' not in {sub_urls.keys()}")
        if sat not in sub_urls[data_type].keys():
            raise KeyError(f"'{sat}' not in {sub_urls[data_type].keys()}")
        self.data_type = data_type
        self.sat = sat
        if fast:
            # Fast data is in a separate directory which does not contain the Latest_baselines substructure
            self.local_data_dir = f"{config['local_source_data_path']}/swarm-diss_fast/"
            self.file_location = self.local_data_dir + sub_urls[data_type][sat].replace("Latest_baselines/", "")
        else:
            self.local_data_dir = f"{config['local_source_data_path']}/swarm-diss/"
            self.file_location = self.local_data_dir + sub_urls[data_type][sat]
        self.t0 = pd.to_datetime("2013-11-01T00:00:00", utc=True)
        self.t1 = pd.Timestamp.utcnow()
        self.fast = fast
        self.set_filelist()

    def set_filelist(self):
        filelist = filelist_to_dataframe(recurse_dirs(self.file_location))
        filelist = filelist[(filelist['t1'] >= self.t0) &
                            (filelist['t0'] <= self.t1)]
        self.filelist = filelist

    def set_time_interval(self, t0, t1):
        self.t0 = pd.to_datetime(t0, utc=True)
        self.t1 = pd.to_datetime(t1, utc=True)
        self.set_filelist()

    def number_of_files(self):
        return len(self.filelist)

    def download(self):
        download(sat=self.sat,
                 data_type=self.data_type,
                 esa_eo_timespan=[self.t0, self.t1])
        dirlist = [f"{self.file_location}/{filename}"
                   for filename in os.listdir(self.file_location)]
        self.filelist = filelist_to_dataframe(dirlist)

    def file_for_time(self, time):
        t = pd.to_datetime(time, utc=True)
        file_index = self.filelist.index.get_indexer([t], method='ffill')[0]
        file_record = self.filelist.iloc[file_index]
        file_exists = t >= file_record['t0'] and t <= file_record['t1']
        if file_exists:
            return file_record['path']
        else:
            return False

    def to_dataframe(self):
        return swarm_files_to_df(list(self.filelist['path']))

    def to_dataframe_for_file_index(self, index):
        return swarm_files_to_df(list(self.filelist.iloc[index:index+1]['path']))


def download_orbcnt(sat='Swarm A'):
    include_string = {
        'Swarm A': 'SW_OPER_AUXAORBCNT',
        'Swarm B': 'SW_OPER_AUXBORBCNT',
        'Swarm C': 'SW_OPER_AUXCORBCNT'
    }
    local_data_dir = f"{config['local_source_data_path']}/swarm-diss/"
    downloaded_files = download_tools.mirror(
        base_url='ftp://swarm-diss.eo.esa.int/',
        sub_url='Level1b/Latest_baselines/ORBCNT/',
        local_dir=local_data_dir,
        include_strings=[include_string[sat]])
    return downloaded_files


def orbcnt_dataframe(sat='Swarm A', download=False):
    if download:
        filename = download_orbcnt(sat=sat)
    else:
        local_data_dir = f"{config['local_source_data_path']}/swarm-diss/"
        pattern = (f"{local_data_dir}/Level1b/Latest_baselines/ORBCNT/" +
                   f"SW_OPER_AUX{sat[-1]}ORBCNT*")
        filename = sorted(glob.glob(pattern))[-1]
    df = pd.read_table(filename,
                       delim_whitespace=True,
                       index_col='date_UT',
                       parse_dates=[['date', 'UT']]
                       ).rename({"%orbit": "orbit_counter"}, axis=1)
    df.index = df.index.tz_localize('utc')
    return df




# def cdf_to_df_pysatcdf(cdffile):
#     data = {}
#     index = None
#     with pysatCDF.CDF(cdffile) as cdf:
#         # Loop over the keys to access the data and time-index
#         for key in cdf.data.keys():
#             if key in ['time', 'epoch', 'Timestamp']:
#                 index = cdf.data[key]
#                 index_name = key
#             else:
#                 data[key] = cdf.data[key]
#         if index_name == "":
#             print("Have not found timestamp variable in CDF.")
#             print("cdf.data.keys(): ", cdf.data.keys())
#
#         # Create data-frame
#         df = pd.DataFrame(index=index, data=data)
#
#         # Set fill values to NaN
#         for key in cdf.data.keys():
#             if key != index_name and 'FILLVAL' in cdf.meta[key]:
#                 df[key].replace(float(cdf.meta[key]['FILLVAL']),
#                                 np.nan, inplace=True)
#         return df


def cdf_to_df(cdffile):
    data = {}
    index = None
    with pycdf.CDF(cdffile) as cdf:
        # Loop over the keys to access the data and time-index
        for key in cdf.keys():
            if key in ['time', 'epoch', 'Timestamp']:
                index = cdf[key]
                index_name = key
            else:
                dimensions = len(cdf[key][:].shape)
                if dimensions == 1:
                    data[key] = cdf[key][:]
                elif dimensions == 2:
                    for idim in range(0,cdf[key][:].shape[1]):
                        data[f"{key}_{idim+1}"] = cdf[key][:,idim]
        if index_name == "":
            print("Have not found timestamp variable in CDF.")
            print("cdf.keys(): ", cdf.keys())

        # Create data-frame
        df = pd.DataFrame(index=index, data=data)

        # Set fill values to NaN
        for key in cdf.keys():
            if key != index_name and 'FILLVAL' in cdf[key].attrs:
                df[key].replace(float(cdf[key].attrs['FILLVAL']),
                                np.nan, inplace=True)

    df.index = df.index.tz_localize('utc')
    return df

def swarm_files_to_df(downloaded_files):
    dfs = []
    with tempfile.TemporaryDirectory() as tmpdirname:
        for filename in downloaded_files:
            if filename.lower().endswith('.zip'):
                try:
                    with zipfile.ZipFile(filename, "r") as zip_ref:
                        for member in zip_ref.namelist():
                            membername = f"{tmpdirname}/{member}"
                            if member.lower().endswith('cdf'):
                                zip_ref.extract(member, tmpdirname)
                                dfs.append(cdf_to_df(membername))
                            elif member.lower().endswith('.sp3'):
                                zip_ref.extract(member, tmpdirname)
                                dfs.append(sp3_to_itrf_df(membername))

                except zipfile.BadZipFile:
                    print("Bad zip file: " + filename)
            elif filename.lower().endswith('.cdf'):
                dfs.append(cdf_to_df(filename))
            elif filename.lower().endswith('.sp3'):
                dfs.append(sp3_to_itrf_df(filename))

        if len(dfs) == 0:
            print("No Swarm data files available")
            return pd.DataFrame()

        df = pd.concat(dfs, axis=0).sort_index()
    return df


def gps_to_utc(date_time_index):
    return pd.to_datetime(
            (gps_epoch_utc + (astropy.time.Time(date_time_index, scale='tai') -
             gps_epoch_tai)).iso, utc=True
        )


def sp3_to_itrf_df(filename):
    def parse_sp3_epoch(epochline):
        (_, year, month, day, hour, minute, seconds) = epochline.split()
        return {'time_gps': pd.to_datetime(f"{year}-{month}-{day}T" +
                                           f"{hour}:{minute}:{seconds}")}

    def parse_sp3_position(positionline):
        x = positionline[4:18]
        y = positionline[18:32]
        z = positionline[32:46]
        return {'x_itrf': float(x),
                'y_itrf': float(y),
                'z_itrf': float(z)}

    def parse_sp3_velocity(velocityline):
        try:
            vx = velocityline[4:18]
            vy = velocityline[18:32]
            vz = velocityline[32:46]
            return {'vx_itrf': float(vx)/1e4,
                    'vy_itrf': float(vy)/1e4,
                    'vz_itrf': float(vz)/1e4}
        except ValueError:
            print("Error parsing: " + velocityline)

    class FormatError(Exception):
        pass

    data = []
    with open(filename, 'r') as fh:
        lines = fh.readlines()

    # Sanity checking
    num_epochs = int(lines[0][32:39])
    num_satellites = int(lines[2][4:6])
    if num_satellites != 1:
        raise FormatError("Number of satellites in SP3 header is " +
                          f"{num_satellites}. This code can handle only 1.")
    expected_lines = 23 + num_epochs * num_satellites * 3
    if (len(lines) != expected_lines):
        raise FormatError(f"Number of lines in file is {len(lines)}, while " +
                          f"{expected_lines} was expected based on the " +
                          "number of epochs and satellites in the header")

    for i_epoch in range(0, num_epochs):
        epoch_line_number = 22 + i_epoch * num_satellites * 3
        epoch = parse_sp3_epoch(lines[epoch_line_number])
        for i_satellite in range(num_satellites):
            position_line_number = (22 + i_epoch * num_satellites * 3 +
                                    i_satellite * 2 + 1)
            velocity_line_number = (22 + i_epoch * num_satellites * 3 +
                                    i_satellite * 2 + 2)
            position = parse_sp3_position(lines[position_line_number])
            velocity = parse_sp3_velocity(lines[velocity_line_number])
        data.append({**epoch, **position, **velocity})
    df = pd.DataFrame(data)
    df.index = gps_to_utc(df['time_gps'])
    df.index.name = 'time_utc'
    return df


def tudelft_ascii_to_dataframe(filename='/Users/eelco/SynologyDrive/' +
                                        'datasets/grace/gracec/GC_NEW_V3.txt'):
    pickle_name = filename.replace(".txt", ".pickle")

    if not os.path.isfile(pickle_name):
        # Read the ASCII file
        print("Reading file: ", filename)
        columns = ["Date",
                   "time",
                   "tsys",
                   "alt",
                   "lon",
                   "lat",
                   "lst",
                   "arglat",
                   "rho_x",
                   "wind_east",
                   "wind_north",
                   "wind_up"]
        df = pd.read_table(filename,
                           delim_whitespace=True,
                           comment='#',
                           names=columns,
                           parse_dates=[['Date', 'time']],
                           index_col='Date_time')

        # Convert GPS to UTC time
        print("Converting GPS time to UTC time")

        df.index = gps_to_utc(df.index)
        df.index.name = "DateTimeUTC"
        df.drop("tsys", axis=1, inplace=True)

        # Save the file
        print("Saving as: ", pickle_name)
        df.to_pickle(pickle_name)
    else:
        print("Reading from pickle: ", pickle_name)
        df = pd.read_pickle(pickle_name)

    return df
