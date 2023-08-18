from lambda_cloud_client.paths.ssh_keys.get import ApiForget
from lambda_cloud_client.paths.ssh_keys.post import ApiForpost


class SshKeys(
    ApiForget,
    ApiForpost,
):
    pass
