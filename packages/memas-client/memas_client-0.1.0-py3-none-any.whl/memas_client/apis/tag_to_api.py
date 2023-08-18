import typing_extensions

from memas_client.apis.tags import TagValues
from memas_client.apis.tags.dp_api import DpApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.DP: DpApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.DP: DpApi,
    }
)
