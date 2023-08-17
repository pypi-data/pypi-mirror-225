from typing import List, Dict
from os.path import abspath

from pytailor.api.base import APIBase
from pytailor.utils import check_local_files_exist, walk_and_apply


class LocalFiles(APIBase):
    """
    Create a new LOCAL fileset.
    """

    def __init__(self, **files: List[str]):
        self.__files = {}
        self.add(**files)

    def add(self, **files: List[str]):
        """Add files by specifying keyword arguments: tag=[local_path1, local_path2, ...]"""

        check_local_files_exist(files)

        files_abs_path = walk_and_apply(files, val_cond=lambda x: isinstance(x, str), val_apply=abspath)

        self.__files.update(files_abs_path)

    @property
    def files(self) -> Dict[str, List[str]]:
        return self.__files

    @property
    def file_tags(self) -> List[str]:
        return list(self.__files.keys())
