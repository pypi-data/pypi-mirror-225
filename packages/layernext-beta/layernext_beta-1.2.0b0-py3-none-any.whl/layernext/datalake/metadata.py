import json
from typing import TYPE_CHECKING

from layernext.datalake.constants import MetadataUploadType
from .keys import COLLECTION_NAME, FILES, IMAGES, IS_APPLY_TO_ALL_FILES, METADATA, OBJECT_TYPE

if TYPE_CHECKING:
    from . import DatalakeClient


class Metadata:
    
    def __init__(self, client:"DatalakeClient"):
        self._client = client

    """"
    Uploads metadata to the datalake by passing a json file (load json file and pass it as a parameter)
    """
    def upload_metadata_json(self, storage_base_path: str,object_type:str, file_path: str):
        
        # load json file
        file = open(file_path)
        annotation_data = json.load(file)
        file.close()

        metaData_json_array = annotation_data[FILES]

        if len(metaData_json_array) > 0:

            payload = {
                COLLECTION_NAME: storage_base_path,
                OBJECT_TYPE: object_type,
                METADATA: metaData_json_array
            }

            meta_data_updates = self._client.datalake_interface.upload_metadata(payload, MetadataUploadType.BY_JSON)
            return meta_data_updates
        

    """
    Uploads metadata to the datalake by passing a metadata object
    """
    def upload_metadata_object(
            self,
            collection_name: str,
            object_type: str,
            metadata_object: dict,
            is_apply_to_all_files: bool
    ):
        payload = {
            COLLECTION_NAME: collection_name,
            OBJECT_TYPE: object_type,
            METADATA: metadata_object,
            IS_APPLY_TO_ALL_FILES: is_apply_to_all_files
        }

        meta_data_updates = self._client.datalake_interface.upload_metadata(payload, MetadataUploadType.BY_META_OBJECT)
        return meta_data_updates
                
    
