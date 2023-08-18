###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

from abc import ABC, abstractmethod
import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)


class Storage(ABC):
    # @abstractmethod
    def __init__(self, defs):
        self.type = defs.get('type')
        self.options = defs.get('options')

    @abstractmethod
    def save(self, data: bytes, filename: Path) -> bool:
        """
        Save data to storage

        :param data: `byte` of data
        :param filename: `str` of filename

        :returns: `bool` of save result
        """

        pass


class FileSystem(Storage):
    def save(self, data: bytes, filename: Path) -> bool:

        filepath = Path(self.options['path']) / filename

        LOGGER.debug(f'Creating directory {filepath.parent}')
        filepath.parent.mkdir(parents=True, exist_ok=True)

        LOGGER.debug(f'Saving data to {filepath}')
        with filepath.open('wb') as fh:
            fh.write(data)

        LOGGER.info(f'Data saved to {filepath}')

        return True


class S3(Storage):
    def save(self, data: bytes, filename: Path) -> bool:

        import boto3
        from botocore.exceptions import ClientError

        s3_url = self.options['url']
        s3_bucket = self.options['bucket']

        s3_client = boto3.client('s3', endpoint_url=s3_url)

        try:
            s3_client.put_object(Body=data, Bucket=s3_bucket, Key=filename)
        except ClientError as err:
            LOGGER.error(err)
            return False

        LOGGER.info(f'Data saved to {filename}')

        return True


STORAGES = {
    'fs': FileSystem,
    'S3': S3
}
