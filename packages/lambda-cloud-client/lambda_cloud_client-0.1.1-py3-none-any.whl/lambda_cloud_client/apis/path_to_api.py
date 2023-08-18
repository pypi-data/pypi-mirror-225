import typing_extensions

from lambda_cloud_client.paths import PathValues
from lambda_cloud_client.apis.paths.instance_types import InstanceTypes
from lambda_cloud_client.apis.paths.instances import Instances
from lambda_cloud_client.apis.paths.instances_id import InstancesId
from lambda_cloud_client.apis.paths.instance_operations_launch import InstanceOperationsLaunch
from lambda_cloud_client.apis.paths.instance_operations_terminate import InstanceOperationsTerminate
from lambda_cloud_client.apis.paths.instance_operations_restart import InstanceOperationsRestart
from lambda_cloud_client.apis.paths.ssh_keys import SshKeys
from lambda_cloud_client.apis.paths.ssh_keys_id import SshKeysId
from lambda_cloud_client.apis.paths.file_systems import FileSystems

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.INSTANCETYPES: InstanceTypes,
        PathValues.INSTANCES: Instances,
        PathValues.INSTANCES_ID: InstancesId,
        PathValues.INSTANCEOPERATIONS_LAUNCH: InstanceOperationsLaunch,
        PathValues.INSTANCEOPERATIONS_TERMINATE: InstanceOperationsTerminate,
        PathValues.INSTANCEOPERATIONS_RESTART: InstanceOperationsRestart,
        PathValues.SSHKEYS: SshKeys,
        PathValues.SSHKEYS_ID: SshKeysId,
        PathValues.FILESYSTEMS: FileSystems,
    }
)

path_to_api = PathToApi(
    {
        PathValues.INSTANCETYPES: InstanceTypes,
        PathValues.INSTANCES: Instances,
        PathValues.INSTANCES_ID: InstancesId,
        PathValues.INSTANCEOPERATIONS_LAUNCH: InstanceOperationsLaunch,
        PathValues.INSTANCEOPERATIONS_TERMINATE: InstanceOperationsTerminate,
        PathValues.INSTANCEOPERATIONS_RESTART: InstanceOperationsRestart,
        PathValues.SSHKEYS: SshKeys,
        PathValues.SSHKEYS_ID: SshKeysId,
        PathValues.FILESYSTEMS: FileSystems,
    }
)
