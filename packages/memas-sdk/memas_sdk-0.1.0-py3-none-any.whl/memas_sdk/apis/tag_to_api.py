import typing_extensions

from memas_sdk.apis.tags import TagValues
from memas_sdk.apis.tags.cp_api import CpApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.CP: CpApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.CP: CpApi,
    }
)
