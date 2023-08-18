# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from lambda_cloud_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    INSTANCETYPES = "/instance-types"
    INSTANCES = "/instances"
    INSTANCES_ID = "/instances/{id}"
    INSTANCEOPERATIONS_LAUNCH = "/instance-operations/launch"
    INSTANCEOPERATIONS_TERMINATE = "/instance-operations/terminate"
    INSTANCEOPERATIONS_RESTART = "/instance-operations/restart"
    SSHKEYS = "/ssh-keys"
    SSHKEYS_ID = "/ssh-keys/{id}"
    FILESYSTEMS = "/file-systems"
