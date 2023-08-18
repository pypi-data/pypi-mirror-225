import typing_extensions

from memas_sdk.paths import PathValues
from memas_sdk.apis.paths.cp_create_user import CpCreateUser
from memas_sdk.apis.paths.cp_create_corpus import CpCreateCorpus

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.CP_CREATE_USER: CpCreateUser,
        PathValues.CP_CREATE_CORPUS: CpCreateCorpus,
    }
)

path_to_api = PathToApi(
    {
        PathValues.CP_CREATE_USER: CpCreateUser,
        PathValues.CP_CREATE_CORPUS: CpCreateCorpus,
    }
)
