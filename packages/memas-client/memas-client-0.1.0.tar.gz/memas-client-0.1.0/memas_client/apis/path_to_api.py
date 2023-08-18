import typing_extensions

from memas_client.paths import PathValues
from memas_client.apis.paths.dp_remember import DpRemember
from memas_client.apis.paths.dp_recollect import DpRecollect

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.DP_REMEMBER: DpRemember,
        PathValues.DP_RECOLLECT: DpRecollect,
    }
)

path_to_api = PathToApi(
    {
        PathValues.DP_REMEMBER: DpRemember,
        PathValues.DP_RECOLLECT: DpRecollect,
    }
)
