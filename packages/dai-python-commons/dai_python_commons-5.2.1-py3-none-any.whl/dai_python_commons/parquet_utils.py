"""Functionality to modify parquet files in an S3 bucket"""
from __future__ import annotations

import gc
import io
import os
from dataclasses import dataclass
from typing import Optional

import boto3
import loguru
import polars as pl

from dai_python_commons.s3_utils import S3Utils


@dataclass
class ParquetFileLocation:
    """
    Class that contains information about parquet files location in S3.

    args:
        source_bucket (str): The bucket where the parquet files to be merged are located.
        source_prefix (str): The prefix (ie 'folder') where the parquet files are located.
        destination_bucket (str): The bucket where the larger parquet file should be located. It can be the same as the
        source bucket.

        destination_prefix (str): The prefix (ie 'folder') where the merged file should be written
        compression (str): Type of compression. Accepted values are 'NONE', 'SNAPPY', 'GZIP', 'BROTLI', 'LZ4', 'ZSTD'
        remove_files_at_destination (bool): whether the files at the destination folder should be removed before
        writing the merged parquet file

        keep_source_files (bool): whether the source files should be kept after merge
        maximum_file_size (int): only parse sets of files which totals (in Bytes) under this limit
    """
    # pylint: disable=R0902
    source_bucket: str
    source_prefix: str
    destination_bucket: str = ""
    destination_prefix: str = ""
    compression: Optional[str] = "SNAPPY"
    remove_files_at_destination: bool = False
    keep_source_files: bool = True
    total_files_size: int = 1024 * 1024 * 1024   # 1GB


class ParquetUtils:
    """
    Class that provides functionality for manipulating parquet files
    """
    # pylint: disable=no-member,too-many-locals
    VALID_COMPRESSION_TYPES = {'none', 'snappy', 'gzip', 'lz4', 'zstd'}

    @staticmethod
    def s3_merge_files_in_place(boto3_session: boto3.Session,
                                parquet_file_location: ParquetFileLocation,
                                logger: loguru.Logger,
                                compression: str = "snappy",
                                keep_source_files: bool = False) -> int:
        """
         Merge many small parquet files into one larger parquet file. In place.

        :param boto3_session: Boto3 session
        :param parquet_file_location: s3 bucket and prefix location where parquet files will be merged
        :param logger: The logger
        :param compression: Type of compression. Accepted values are 'none', 'snappy', 'gzip', 'brotli', 'lz4', 'zstd'
        :param keep_source_files: True to keep the source files, False to delete them.
        :return:
        """
        data_path = f"s3://{parquet_file_location.source_bucket}/{parquet_file_location.source_prefix}"
        logger.info(f"Merging files from {data_path} to {data_path}, compression: {compression}")

        boto_s3_client = boto3_session.client("s3")
        num_rows = 0

        file_paths_iter = S3Utils.iter_file_paths_in_prefix(boto_s3_client=boto_s3_client,
                                                  bucket_name=parquet_file_location.source_bucket,
                                                  prefix=parquet_file_location.source_prefix,
                                                  logger=logger,
                                                  max_size=parquet_file_location.total_files_size)
        for file_paths in file_paths_iter:
            if len(file_paths) <2:
                logger.info(f"file paths is less than 2 files, no reason to merge: {file_paths}")
                continue
            logger.info(f"Reading and merging {file_paths}")

            file_bytes = []
            for file_path in file_paths:
                file = S3Utils.read_s3_file(
                    s3_client=boto_s3_client,
                    bucket_name=parquet_file_location.source_bucket,
                    key=file_path["Key"]
                ).read()
                file_bytes.append(io.BytesIO(file))

            merged_data = pl.read_parquet(file_bytes.pop(0))
            merged_data = merged_data.select(sorted(merged_data.columns))
            for file in file_bytes:
                new_frame = pl.read_parquet(file)
                merged_data.vstack(new_frame.select(sorted(merged_data.columns)), in_place=True)

            num_rows += merged_data.height
            logger.debug(f"Shape of the table {merged_data.shape}")

            logger.debug(f"Writing to the destination {data_path}")
            try:
                with io.BytesIO() as con:
                    merged_data.write_parquet(con, compression=compression.lower())

                    key=os.path.join(parquet_file_location.source_prefix, f"consolidated_rows_{num_rows}.parquet")
                    boto_s3_client.put_object(Body=con.getvalue(), Bucket=parquet_file_location.source_bucket,Key=key)

                logger.info(f"Done merging, {merged_data.height} rows were written at prefix {data_path}")
                if not keep_source_files:
                    logger.info('Removing source files')
                    logger.debug(f'Removing these files {file_paths}')
                    S3Utils.delete_objects(
                        boto_s3_client=boto_s3_client,
                        bucket_name=parquet_file_location.source_bucket,
                        to_delete=file_paths,
                        logger=logger
                    )
            except Exception:
                logger.exception(f'Caught error when trying to merge parquet files: {file_paths}')
                raise

            # Explicitly clear data from memory
            del merged_data
            gc.collect()

        if num_rows == 0:
            logger.warning(f"No files found at {data_path}, nothing to merge")

        return num_rows

    @staticmethod
    def s3_merge_files(boto3_session: boto3.Session, parquet_file_location: ParquetFileLocation,
                       logger: loguru.Logger) -> int:
        """
        Merge many small parquet files into one larger parquet file. From source to destination.
        Exception will be raised if source is equals to destination.

        :param boto3_session: Boto3 session
        :param parquet_file_location: ParquetFileLocation contains info about the files location in the s3 bucket
        :param logger: The logger
        :return: Number of rows in the parquet file
        """
        source_bucket = parquet_file_location.source_bucket
        source_prefix = parquet_file_location.source_prefix
        remove_files_at_destination = parquet_file_location.remove_files_at_destination

        ParquetUtils._source_and_destination_not_same(parquet_file_location)

        source_data_path = f"s3://{parquet_file_location.source_bucket}/{parquet_file_location.source_prefix}"
        destination_data_path = f"s3://{parquet_file_location.destination_bucket}/{parquet_file_location.destination_prefix}"

        logger.info(f"Merging files from {source_data_path} to {destination_data_path},"
                    f" compression: {parquet_file_location.compression}, "
                    f"remove_files_at_destination={parquet_file_location.remove_files_at_destination}")

        # check if there are any files present
        s3_client = boto3_session.client('s3')
        file_paths = S3Utils.file_paths_in_prefix(boto_s3_client=s3_client,
                                                  bucket_name=source_bucket,
                                                  prefix=source_prefix,
                                                  logger=logger)
        if len(file_paths) == 0:
            logger.warning(f"No files found at {source_data_path}, nothing to merge")
            return 0

        if remove_files_at_destination:
            ParquetUtils._remove_files(parquet_file_location, destination_data_path, logger, s3_client)

        logger.debug(f"Reading data from {source_data_path}")

        file_paths = S3Utils.file_paths_in_prefix(boto_s3_client=s3_client,
                                                  bucket_name=parquet_file_location.source_bucket,
                                                  prefix=parquet_file_location.source_prefix,
                                                  logger=logger)

        files = []
        for file_path in file_paths:
            file = S3Utils.read_s3_file(
                s3_client=s3_client,
                bucket_name=parquet_file_location.source_bucket,
                key=file_path["Key"]
            ).read()
            files.append(io.BytesIO(file))

        pq_table = pl.read_parquet(files.pop(0))
        pq_table = pq_table.select(sorted(pq_table.columns))
        for file in files:
            new_frame = pl.read_parquet(file)
            pq_table.vstack(new_frame.select(sorted(pq_table.columns)), in_place=True)

        logger.debug(f"Shape of the table {pq_table.shape}")

        compression = parquet_file_location.compression
        if compression:
            compression = compression.lower()
        else:
            compression = "none"

        try:
            logger.debug(f"Writing to the destination {destination_data_path}")
            with io.BytesIO() as con:
                pq_table.write_parquet(con, compression=compression)

                key=os.path.join(parquet_file_location.destination_prefix, f"consolidated_entries_{pq_table.height}.parquet")
                s3_client.put_object(Body=con.getvalue(), Bucket=parquet_file_location.destination_bucket,Key=key)

            logger.info(f"Done merging, {pq_table.height} rows were written at {destination_data_path}")
            if not parquet_file_location.keep_source_files:
                logger.info('Removing source files')
                logger.debug(f'Removing these files {file_paths}')
                S3Utils.delete_objects(
                    boto_s3_client=s3_client,
                    bucket_name=source_bucket,
                    to_delete=file_paths,
                    logger=logger
                )
        except Exception:
            logger.exception(f'Caught error when trying to merge parquet files: {file_paths}')
            raise

        return pq_table.height

    @staticmethod
    def _remove_files(parquet_file_location, destination_data_path, logger, s3_client):
        """removes files at the destination bucket, assigned in the parquet_file_location"""
        logger.debug(f"Removing all files at {destination_data_path}")
        S3Utils.delete_objects_by_prefix(boto_s3_client=s3_client, bucket_name=parquet_file_location.destination_bucket,
                                         prefix=parquet_file_location.destination_prefix, logger=logger)

    @staticmethod
    def _source_and_destination_not_same(parquet_file_location):
        """checks that source bucket and destination bucket is not the same"""
        if parquet_file_location.source_bucket == parquet_file_location.destination_bucket and \
                parquet_file_location.source_prefix.rstrip('/') == parquet_file_location.destination_prefix.rstrip('/'):
            raise ValueError('Source and destination cannot be the same!')
