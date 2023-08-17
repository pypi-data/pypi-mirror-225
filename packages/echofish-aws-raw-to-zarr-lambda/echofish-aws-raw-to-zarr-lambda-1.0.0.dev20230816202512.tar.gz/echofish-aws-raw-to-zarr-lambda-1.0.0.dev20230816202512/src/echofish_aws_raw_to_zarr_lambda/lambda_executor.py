# lambda_executor.py
import os
import glob
import shutil
import echopype as ep
import numpy as np
import pandas as pd
import geopandas
import json
from datetime import datetime

TEMPDIR = "/tmp"


class LambdaExecutor:

    ############################################################################
    def __init__(
            self,
            s3_operations,
            dynamo_operations,
            sns_operations,
            input_bucket,
            output_bucket,
            table_name,
            output_bucket_access_key,
            output_bucket_secret_access_key,
            done_topic_arn,
    ):
        self.__s3 = s3_operations
        self.__dynamo = dynamo_operations
        self.__sns_operations = sns_operations
        self.__input_bucket = input_bucket
        self.__output_bucket = output_bucket
        self.__table_name = table_name
        self.__output_bucket_access_key = output_bucket_access_key
        self.__output_bucket_secret_access_key = output_bucket_secret_access_key
        self.__done_topic_arn = done_topic_arn

    ############################################################################
    def __delete_all_local_raw_and_zarr_files(self):  # good
        """Used to clean up any residual files from warm lambdas
        to keep the storage footprint below the 512 MB allocation.

        Returns
        -------
        None : None
            No return value.
        """
        print('Deleting all local raw and zarr files')
        for i in ['*.raw*', '*.zarr']:
            for j in glob.glob(i):
                # print(f'Deleting {j}')
                if os.path.isdir(j):
                    shutil.rmtree(j, ignore_errors=True)
                elif os.path.isfile(j):
                    os.remove(j)

    ############################################################################
    def __set_processing_status(
            self,
            ship_name: str,
            cruise_name: str,
            sensor_name: str,
            file_name: str,
            new_status: str
    ):
        # Updates PIPELINE_STATUS via new_status value
        # HASH: FILE_NAME, RANGE: SENSOR_NAME
        self.__dynamo.put_item(
            table_name=self.__table_name,
            item={
                'FILE_NAME': {'S': file_name},  # HASH
                'SHIP_NAME': {'S': ship_name},
                'CRUISE_NAME': {'S': cruise_name},
                'SENSOR_NAME': {'S': sensor_name},  # RANGE
                'PIPELINE_TIME': {'S': datetime.now().isoformat(timespec="seconds") + "Z"},
                'PIPELINE_STATUS': {'S': new_status},
            }
        )

    ############################################################################
    def __update_processing_status(
            self,
            cruise_name,
            file_name,
            new_status
    ):
        self.__dynamo.update_item(
            table_name=self.__table_name,
            key={
                'FILE_NAME': {'S': file_name},  # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key
            },
            expression='SET #PS = :ps',
            attribute_names={
                '#PS': 'PIPELINE_STATUS'
            },
            attribute_values={
                ':ps': {
                    'S': new_status
                }
            }
        )

    ############################################################################
    def __get_processing_status(
            self,
            file_name,
            cruise_name
    ):
        # HASH: FILE_NAME, RANGE: SENSOR_NAME
        item = self.__dynamo.get_item(
            TableName=self.__table_name,
            Key={
                'FILE_NAME': {'S': file_name},  # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key
            })
        if item is None:
            return 'NONE'
        return item['PIPELINE_STATUS']['S']

    ############################################################################
    def __zarr_info_to_table(
            self,
            cruise_name,
            file_name,
            zarr_path,
            min_echo_range,
            max_echo_range,
            num_ping_time_dropna,
            start_time,
            end_time,
            frequencies,
            channels
    ):
        self.__dynamo.update_item(
            table_name=self.__table_name,
            key={
                'FILE_NAME': {'S': file_name},  # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key # TODO: should be FILE_NAME & SENSOR_NAME so they are truely unique for when two sensors are processed within one cruise
            },
            expression='SET #ZB = :zb, #ZP = :zp, #MINER = :miner, #MAXER = :maxer, #P = :p, #ST = :st, #ET = :et, #F = :f, #C = :c',
            attribute_names={
                '#ZB': 'ZARR_BUCKET',
                '#ZP': 'ZARR_PATH',
                '#MINER': 'MIN_ECHO_RANGE',
                '#MAXER': 'MAX_ECHO_RANGE',
                '#P': 'NUM_PING_TIME_DROPNA',
                '#ST': 'START_TIME',
                '#ET': 'END_TIME',
                '#F': 'FREQUENCIES',
                '#C': 'CHANNELS',
                ### TODO: don't actually need to do with "update_item" operation ###
                # SHIP_NAME,SENSOR_NAME,PIPELINE_TIME,PIPELINE_STATUS
            },
            attribute_values={
                ':zb': {
                    'S': self.__output_bucket
                },
                ':zp': {
                    'S': zarr_path
                },
                ':miner': {
                    'N': str(np.round(min_echo_range, 4))
                },
                ':maxer': {
                    'N': str(np.round(max_echo_range, 4))
                },
                ':p': {
                    'N': str(num_ping_time_dropna)
                },
                ':st': {
                    'S': start_time
                },
                ':et': {
                    'S': end_time
                },
                ':f': {
                    'L': [{'N': str(i)} for i in frequencies]
                },
                ':c': {
                    'L': [{'S': i} for i in channels]
                }
            }
        )

    ############################################################################
    def __get_gps_data(
            self,
            echodata: ep.echodata.echodata.EchoData
    ) -> tuple:
        assert(
                'latitude' in echodata.platform.variables and 'longitude' in echodata.platform.variables
        ), "Problem: GPS coordinates not found in echodata."
        latitude = echodata.platform.latitude.values
        longitude = echodata.platform.longitude.values  # len(longitude) == 14691
        # RE: time coordinates: https://github.com/OSOceanAcoustics/echopype/issues/656#issue-1219104771
        assert(
                'time1' in echodata.platform.variables and 'time1' in echodata.environment.variables
        ), "Problem: Time coordinate not found in echodata."
        # 'nmea_times' are times from the nmea datalogger associated with GPS
        nmea_times = echodata.platform.time1.values
        # 'time1' are times from the echosounder associated with transducer measurement
        time1 = echodata.environment.time1.values
        # Align 'sv_times' to 'nmea_times'
        assert(
                np.all(time1[:-1] <= time1[1:]) and np.all(nmea_times[:-1] <= nmea_times[1:])
        ), "Problem: NMEA time stamps are not sorted."
        # Finds the indices where 'v' can be inserted into 'a'
        indices = np.searchsorted(a=nmea_times, v=time1, side="right") - 1
        #
        lat = latitude[indices]
        lat[indices < 0] = np.nan  # values recorded before indexing are set to nan
        lon = longitude[indices]
        lon[indices < 0] = np.nan
        assert(
                np.all(lat[~np.isnan(lat)] >= -90.) and np.all(lat[~np.isnan(lat)] <= 90.)
        ), "Problem: Data falls outside GPS bounds!"
        # https://osoceanacoustics.github.io/echopype-examples/echopype_tour.html
        gps_df = pd.DataFrame({
            'latitude': lat,
            'longitude': lon,
            'time1': time1
        }).set_index(['time1'])
        gps_gdf = geopandas.GeoDataFrame(
            gps_df,
            geometry=geopandas.points_from_xy(gps_df['longitude'], gps_df['latitude']),
            crs="epsg:4326"  # TODO: does this sound right?
        )
        # GeoJSON FeatureCollection with IDs as "time1"
        geo_json = gps_gdf.to_json()
        return geo_json, lat, lon

    ############################################################################
    def __write_geojson_to_file(
            self,
            store_name,
            data
    ) -> None:
        """Write the GeoJSON file inside the Zarr store folder. Note that the
        file is not a technical part of the store, this is more of a hack
        to help pass the data along to the next processing step.

        Parameters
        ----------
        path : str
            The path to a local Zarr store where the file will be written.
        data : str
            A GeoJSON Feature Collection to be written to output file.

        Returns
        -------
        None : None
            No return value.
        """
        with open(os.path.join(store_name, 'geo.json'), "w") as outfile:
            outfile.write(data)

    ############################################################################
    def __create_local_zarr_store(
            self,
            raw_file_name,
            cruise_name,
            sensor_name,
            output_zarr_prefix,
            store_name
    ):
        print(f'Opening raw: {raw_file_name}')
        # TODO: surround with try-catch
        echodata = ep.open_raw(raw_file_name, sonar_model=sensor_name)
        print('Compute volume backscattering strength (Sv) from raw data.')
        ds_sv = ep.calibrate.compute_Sv(echodata)
        frequencies = echodata.environment.frequency_nominal.values
        #################################################################
        # Get GPS coordinates
        gps_data, lat, lon = self.__get_gps_data(echodata=echodata)
        #################################################################
        # Technically the min_echo_range would be 0 m.
        min_echo_range = np.nanmin(np.diff(ds_sv.echo_range.values))  # TODO: this var name is supposed to represent minimum resolution of depth measurements
        max_echo_range = float(np.nanmax(ds_sv.echo_range))
        #
        num_ping_time_dropna = lat[~np.isnan(lat)].shape[0]  # symmetric to lon
        #
        start_time = np.datetime_as_string(ds_sv.ping_time.values[0], unit='ms') + "Z"
        end_time = np.datetime_as_string(ds_sv.ping_time.values[-1], unit='ms') + "Z"
        channels = list(ds_sv.channel.values)
        #
        #################################################################
        # Create the zarr store
        ds_sv.to_zarr(store=store_name)
        #################################################################
        print('Note: Adding GeoJSON inside Zarr store')
        self.__write_geojson_to_file(store_name=store_name, data=gps_data)
        #################################################################
        self.__zarr_info_to_table(
            cruise_name=cruise_name,
            file_name=raw_file_name,
            zarr_path=os.path.join(output_zarr_prefix, store_name),
            min_echo_range=min_echo_range,
            max_echo_range=max_echo_range,
            num_ping_time_dropna=num_ping_time_dropna,
            start_time=start_time,
            end_time=end_time,
            frequencies=frequencies,
            channels=channels
        )

    ############################################################################
    # def __remove_existing_s3_objects(
    #         self,
    #         prefix
    # ):
    #     print(f'Removing existing s3 objects from: {self.__output_bucket} with prefix {prefix}')
    #     keys = self.__s3.list_objects(
    #         bucket_name=self.__output_bucket,
    #         prefix=prefix,
    #         access_key_id=self.__output_bucket_access_key,
    #         secret_access_key=self.__output_bucket_secret_access_key
    #     )
    #     for key in keys:
    #         self.__s3.delete_object(
    #             bucket_name=self.__output_bucket,
    #             key=key,
    #             access_key_id=self.__output_bucket_access_key,
    #             secret_access_key=self.__output_bucket_secret_access_key
    #         )
    #     print('Removing existing s3 objects done')

    ############################################################################
    def __upload_files(
            self,
            local_directory,
            object_prefix
    ):
        print('Uploading files')
        for subdir, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(subdir, file)
                # print(local_path)
                s3_key = os.path.join(object_prefix, local_path)
                self.__s3.upload_file(
                    file_name=local_path,
                    bucket_name=self.__output_bucket,
                    key=s3_key,
                    access_key_id=self.__output_bucket_access_key,
                    secret_access_key=self.__output_bucket_secret_access_key
                )
        # print('Done uploading files')


    ############################################################################
    def __publish_done_message(self, message):
        print("Sending done message")
        self.__sns_operations.publish(self.__done_topic_arn, json.dumps(message))

    ############################################################################
    def execute(self, message):
        ship_name = message['shipName']
        cruise_name = message['cruiseName']
        sensor_name = message['sensorName']
        input_file_name = message['fileName']
        #
        store_name = f"{os.path.splitext(input_file_name)[0]}.zarr"
        output_zarr_prefix = f"level_1/{ship_name}/{cruise_name}/{sensor_name}"
        bucket_key = f"data/raw/{ship_name}/{cruise_name}/{sensor_name}/{input_file_name}"
        #
        os.chdir(TEMPDIR)
        #
        # TODO: Change "put_item" to "update_item"
        self.__set_processing_status(
            ship_name=ship_name,
            cruise_name=cruise_name,
            sensor_name=sensor_name,
            file_name=input_file_name,
            new_status="PROCESSING"
        )
        #
        self.__delete_all_local_raw_and_zarr_files()
        #
        self.__s3.download_file(
            bucket_name=self.__input_bucket,
            key=bucket_key,
            file_name=input_file_name
        )
        self.__create_local_zarr_store(
            raw_file_name=input_file_name,
            cruise_name=cruise_name,
            sensor_name=sensor_name,
            output_zarr_prefix=output_zarr_prefix,
            store_name=store_name
        )
        #################################################################
        zarr_prefix = os.path.join("level_1", ship_name, cruise_name, sensor_name)
        #
        child_objects = self.__s3.get_child_objects(
            bucket_name=self.__output_bucket,
            sub_prefix=zarr_prefix,
            access_key_id=self.__output_bucket_access_key,
            secret_access_key=self.__output_bucket_secret_access_key
        )
        if len(child_objects) > 0:
            self.__s3.delete_objects(
                bucket_name=self.__output_bucket,
                objects=child_objects,
                access_key_id=self.__output_bucket_access_key,
                secret_access_key=self.__output_bucket_secret_access_key
            )
        # self.__remove_existing_s3_objects(
        #     prefix=os.path.join(output_zarr_prefix, store_name)
        # )
        #################################################################
        self.__upload_files(store_name, output_zarr_prefix)
        self.__update_processing_status(
            cruise_name=cruise_name,
            file_name=input_file_name,
            new_status='SUCCESS'
        )
        self.__delete_all_local_raw_and_zarr_files()
        #
        self.__publish_done_message(message)
        print(f'Done processing {input_file_name}')

