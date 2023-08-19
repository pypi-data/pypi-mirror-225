import typing_extensions

from fuse_client.apis.tags import TagValues
from fuse_client.apis.tags.fuse_api import FuseApi
from fuse_client.apis.tags.risk_report_api import RiskReportApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.FUSE: FuseApi,
        TagValues.RISK_REPORT: RiskReportApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.FUSE: FuseApi,
        TagValues.RISK_REPORT: RiskReportApi,
    }
)
