from os import makedirs
from os.path import exists,basename
from zipfile import ZipFile
from modules.utils.extend_util import ExtendUtil
from modules.models.download.library_resource import LibraryResource


class ZipUtil():
    @staticmethod
    def game_natives_decompress(directory: str, library_resources: list[LibraryResource]) -> None:
        if(not exists(directory)):
            makedirs(directory)
        ExtendUtil.del_all_files(directory)
        for item in [x for x in library_resources if x.is_enable & x.is_natives]:
            zip_file: ZipFile = ZipFile(item.to_file_info())
            for z in zip_file.namelist():
                if(".dll" in basename(z))|(".so" in basename(z))|(".dylib" in basename(z)):
                    zip_file.extract(z, directory)
            zip_file.close()