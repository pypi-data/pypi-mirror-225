# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from lambda_cloud_client.paths.file_systems import Api

from lambda_cloud_client.paths import PathValues

path = PathValues.FILESYSTEMS