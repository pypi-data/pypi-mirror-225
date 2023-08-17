import datetime
from typing import Dict, List, Union, Callable
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests
from pytailor.models import FileSet
import shutil
import os

from pytailor.utils import get_logger

logger = get_logger("FileClient")


class FileClient(requests.Session):
    def upload_files(self, file_paths: Dict[str, List[Union[str, Path]]], fileset: FileSet):

        # TODO: support files larger than 5GB
        # https://dev.to/traindex/multipart-upload-for-large-files-using-pre-signed-urls-aws-4hg4

        for file_paths, fileset_links in zip(file_paths.values(), fileset.tags):
            for file_path, fileset_link in zip(file_paths, fileset_links.links):
                if os.stat(file_path).st_size == 0:
                    response = requests.put(fileset_link.url, data=b"")
                else:
                    with open(file_path, "rb") as f:
                        response = self.put(fileset_link.url, data=f)
                if not response.status_code == requests.codes.OK:
                    response.raise_for_status()

    def download_files(
        self,
        fileset_or_callable: Union[FileSet, Callable[[], FileSet]],
        use_storage_dirs: bool = True,
    ):

        if callable(fileset_or_callable):
            fileset = fileset_or_callable()
        else:
            fileset = fileset_or_callable

        # we loop on indices instead of fileset.tags and fileset_links.links
        # so that we can update the fileset if the links have expired
        indices = []
        for i, fileset_links in enumerate(fileset.tags):
            indices_j = []
            for j, fileset_link in enumerate(fileset_links.links):
                indices_j.append(j)
            indices.append(indices_j)

        for i, indices_j in enumerate(indices):
            for j in indices_j:
                fileset_links = fileset.tags[i]
                fileset_link = fileset_links.links[j]
                expiration = datetime.datetime.utcfromtimestamp(
                    int(parse_qs(urlparse(fileset_link.url).query)["Expires"][0])
                )
                if expiration < datetime.datetime.utcnow() + datetime.timedelta(minutes=5):
                    if callable(fileset_or_callable):
                        fileset = fileset_or_callable()
                        logger.info("The download links have expired. Renewed the links.")
                        fileset_links = fileset.tags[i]
                        fileset_link = fileset_links.links[j]
                    else:
                        raise ValueError("The download links have expired.")
                path = Path(fileset_link.filename)
                if use_storage_dirs:
                    local_filename = str(path)
                    path.parent.mkdir(parents=True, exist_ok=True)
                else:
                    local_filename = path.name
                with self.get(fileset_link.url, stream=True) as r:
                    with open(local_filename, "wb") as f:
                        shutil.copyfileobj(r.raw, f)
                logger.info(f"Downloaded file {local_filename}")
