"""
Type annotations for pi service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pi/type_defs/)

Usage::

    ```python
    from mypy_boto3_pi.type_defs import TagTypeDef

    data: TagTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AnalysisStatusType,
    ContextTypeType,
    DetailStatusType,
    FeatureStatusType,
    PeriodAlignmentType,
    ServiceTypeType,
    SeverityType,
    TextFormatType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "TagTypeDef",
    "AnalysisReportTypeDef",
    "TimestampTypeDef",
    "ResponseMetadataTypeDef",
    "DataPointTypeDef",
    "PerformanceInsightsMetricTypeDef",
    "DeletePerformanceAnalysisReportRequestRequestTypeDef",
    "DimensionGroupTypeDef",
    "DimensionKeyDescriptionTypeDef",
    "ResponsePartitionKeyTypeDef",
    "DimensionDetailTypeDef",
    "DimensionKeyDetailTypeDef",
    "FeatureMetadataTypeDef",
    "GetDimensionKeyDetailsRequestRequestTypeDef",
    "GetPerformanceAnalysisReportRequestRequestTypeDef",
    "GetResourceMetadataRequestRequestTypeDef",
    "RecommendationTypeDef",
    "ListAvailableResourceDimensionsRequestRequestTypeDef",
    "ListAvailableResourceMetricsRequestRequestTypeDef",
    "ResponseResourceMetricTypeDef",
    "ListPerformanceAnalysisReportsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ResponseResourceMetricKeyTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AnalysisReportSummaryTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreatePerformanceAnalysisReportRequestRequestTypeDef",
    "CreatePerformanceAnalysisReportResponseTypeDef",
    "GetPerformanceAnalysisReportResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "DataTypeDef",
    "DescribeDimensionKeysRequestRequestTypeDef",
    "MetricQueryTypeDef",
    "DescribeDimensionKeysResponseTypeDef",
    "DimensionGroupDetailTypeDef",
    "GetDimensionKeyDetailsResponseTypeDef",
    "GetResourceMetadataResponseTypeDef",
    "ListAvailableResourceMetricsResponseTypeDef",
    "MetricKeyDataPointsTypeDef",
    "ListPerformanceAnalysisReportsResponseTypeDef",
    "InsightTypeDef",
    "GetResourceMetricsRequestRequestTypeDef",
    "MetricDimensionGroupsTypeDef",
    "GetResourceMetricsResponseTypeDef",
    "ListAvailableResourceDimensionsResponseTypeDef",
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredAnalysisReportTypeDef = TypedDict(
    "_RequiredAnalysisReportTypeDef",
    {
        "AnalysisReportId": str,
    },
)
_OptionalAnalysisReportTypeDef = TypedDict(
    "_OptionalAnalysisReportTypeDef",
    {
        "Identifier": str,
        "ServiceType": ServiceTypeType,
        "CreateTime": datetime,
        "StartTime": datetime,
        "EndTime": datetime,
        "Status": AnalysisStatusType,
        "Insights": List["InsightTypeDef"],
    },
    total=False,
)


class AnalysisReportTypeDef(_RequiredAnalysisReportTypeDef, _OptionalAnalysisReportTypeDef):
    pass


TimestampTypeDef = Union[datetime, str]
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

DataPointTypeDef = TypedDict(
    "DataPointTypeDef",
    {
        "Timestamp": datetime,
        "Value": float,
    },
)

PerformanceInsightsMetricTypeDef = TypedDict(
    "PerformanceInsightsMetricTypeDef",
    {
        "Metric": str,
        "DisplayName": str,
        "Dimensions": Dict[str, str],
        "Value": float,
    },
    total=False,
)

DeletePerformanceAnalysisReportRequestRequestTypeDef = TypedDict(
    "DeletePerformanceAnalysisReportRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "AnalysisReportId": str,
    },
)

_RequiredDimensionGroupTypeDef = TypedDict(
    "_RequiredDimensionGroupTypeDef",
    {
        "Group": str,
    },
)
_OptionalDimensionGroupTypeDef = TypedDict(
    "_OptionalDimensionGroupTypeDef",
    {
        "Dimensions": Sequence[str],
        "Limit": int,
    },
    total=False,
)


class DimensionGroupTypeDef(_RequiredDimensionGroupTypeDef, _OptionalDimensionGroupTypeDef):
    pass


DimensionKeyDescriptionTypeDef = TypedDict(
    "DimensionKeyDescriptionTypeDef",
    {
        "Dimensions": Dict[str, str],
        "Total": float,
        "AdditionalMetrics": Dict[str, float],
        "Partitions": List[float],
    },
    total=False,
)

ResponsePartitionKeyTypeDef = TypedDict(
    "ResponsePartitionKeyTypeDef",
    {
        "Dimensions": Dict[str, str],
    },
)

DimensionDetailTypeDef = TypedDict(
    "DimensionDetailTypeDef",
    {
        "Identifier": str,
    },
    total=False,
)

DimensionKeyDetailTypeDef = TypedDict(
    "DimensionKeyDetailTypeDef",
    {
        "Value": str,
        "Dimension": str,
        "Status": DetailStatusType,
    },
    total=False,
)

FeatureMetadataTypeDef = TypedDict(
    "FeatureMetadataTypeDef",
    {
        "Status": FeatureStatusType,
    },
    total=False,
)

_RequiredGetDimensionKeyDetailsRequestRequestTypeDef = TypedDict(
    "_RequiredGetDimensionKeyDetailsRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "Group": str,
        "GroupIdentifier": str,
    },
)
_OptionalGetDimensionKeyDetailsRequestRequestTypeDef = TypedDict(
    "_OptionalGetDimensionKeyDetailsRequestRequestTypeDef",
    {
        "RequestedDimensions": Sequence[str],
    },
    total=False,
)


class GetDimensionKeyDetailsRequestRequestTypeDef(
    _RequiredGetDimensionKeyDetailsRequestRequestTypeDef,
    _OptionalGetDimensionKeyDetailsRequestRequestTypeDef,
):
    pass


_RequiredGetPerformanceAnalysisReportRequestRequestTypeDef = TypedDict(
    "_RequiredGetPerformanceAnalysisReportRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "AnalysisReportId": str,
    },
)
_OptionalGetPerformanceAnalysisReportRequestRequestTypeDef = TypedDict(
    "_OptionalGetPerformanceAnalysisReportRequestRequestTypeDef",
    {
        "TextFormat": TextFormatType,
        "AcceptLanguage": Literal["EN_US"],
    },
    total=False,
)


class GetPerformanceAnalysisReportRequestRequestTypeDef(
    _RequiredGetPerformanceAnalysisReportRequestRequestTypeDef,
    _OptionalGetPerformanceAnalysisReportRequestRequestTypeDef,
):
    pass


GetResourceMetadataRequestRequestTypeDef = TypedDict(
    "GetResourceMetadataRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
    },
)

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "RecommendationId": str,
        "RecommendationDescription": str,
    },
    total=False,
)

_RequiredListAvailableResourceDimensionsRequestRequestTypeDef = TypedDict(
    "_RequiredListAvailableResourceDimensionsRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "Metrics": Sequence[str],
    },
)
_OptionalListAvailableResourceDimensionsRequestRequestTypeDef = TypedDict(
    "_OptionalListAvailableResourceDimensionsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAvailableResourceDimensionsRequestRequestTypeDef(
    _RequiredListAvailableResourceDimensionsRequestRequestTypeDef,
    _OptionalListAvailableResourceDimensionsRequestRequestTypeDef,
):
    pass


_RequiredListAvailableResourceMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredListAvailableResourceMetricsRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "MetricTypes": Sequence[str],
    },
)
_OptionalListAvailableResourceMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalListAvailableResourceMetricsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListAvailableResourceMetricsRequestRequestTypeDef(
    _RequiredListAvailableResourceMetricsRequestRequestTypeDef,
    _OptionalListAvailableResourceMetricsRequestRequestTypeDef,
):
    pass


ResponseResourceMetricTypeDef = TypedDict(
    "ResponseResourceMetricTypeDef",
    {
        "Metric": str,
        "Description": str,
        "Unit": str,
    },
    total=False,
)

_RequiredListPerformanceAnalysisReportsRequestRequestTypeDef = TypedDict(
    "_RequiredListPerformanceAnalysisReportsRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
    },
)
_OptionalListPerformanceAnalysisReportsRequestRequestTypeDef = TypedDict(
    "_OptionalListPerformanceAnalysisReportsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ListTags": bool,
    },
    total=False,
)


class ListPerformanceAnalysisReportsRequestRequestTypeDef(
    _RequiredListPerformanceAnalysisReportsRequestRequestTypeDef,
    _OptionalListPerformanceAnalysisReportsRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "ResourceARN": str,
    },
)

_RequiredResponseResourceMetricKeyTypeDef = TypedDict(
    "_RequiredResponseResourceMetricKeyTypeDef",
    {
        "Metric": str,
    },
)
_OptionalResponseResourceMetricKeyTypeDef = TypedDict(
    "_OptionalResponseResourceMetricKeyTypeDef",
    {
        "Dimensions": Dict[str, str],
    },
    total=False,
)


class ResponseResourceMetricKeyTypeDef(
    _RequiredResponseResourceMetricKeyTypeDef, _OptionalResponseResourceMetricKeyTypeDef
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

AnalysisReportSummaryTypeDef = TypedDict(
    "AnalysisReportSummaryTypeDef",
    {
        "AnalysisReportId": str,
        "CreateTime": datetime,
        "StartTime": datetime,
        "EndTime": datetime,
        "Status": AnalysisStatusType,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCreatePerformanceAnalysisReportRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePerformanceAnalysisReportRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
    },
)
_OptionalCreatePerformanceAnalysisReportRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePerformanceAnalysisReportRequestRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreatePerformanceAnalysisReportRequestRequestTypeDef(
    _RequiredCreatePerformanceAnalysisReportRequestRequestTypeDef,
    _OptionalCreatePerformanceAnalysisReportRequestRequestTypeDef,
):
    pass


CreatePerformanceAnalysisReportResponseTypeDef = TypedDict(
    "CreatePerformanceAnalysisReportResponseTypeDef",
    {
        "AnalysisReportId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPerformanceAnalysisReportResponseTypeDef = TypedDict(
    "GetPerformanceAnalysisReportResponseTypeDef",
    {
        "AnalysisReport": AnalysisReportTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DataTypeDef = TypedDict(
    "DataTypeDef",
    {
        "PerformanceInsightsMetric": PerformanceInsightsMetricTypeDef,
    },
    total=False,
)

_RequiredDescribeDimensionKeysRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDimensionKeysRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "Metric": str,
        "GroupBy": DimensionGroupTypeDef,
    },
)
_OptionalDescribeDimensionKeysRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDimensionKeysRequestRequestTypeDef",
    {
        "PeriodInSeconds": int,
        "AdditionalMetrics": Sequence[str],
        "PartitionBy": DimensionGroupTypeDef,
        "Filter": Mapping[str, str],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeDimensionKeysRequestRequestTypeDef(
    _RequiredDescribeDimensionKeysRequestRequestTypeDef,
    _OptionalDescribeDimensionKeysRequestRequestTypeDef,
):
    pass


_RequiredMetricQueryTypeDef = TypedDict(
    "_RequiredMetricQueryTypeDef",
    {
        "Metric": str,
    },
)
_OptionalMetricQueryTypeDef = TypedDict(
    "_OptionalMetricQueryTypeDef",
    {
        "GroupBy": DimensionGroupTypeDef,
        "Filter": Mapping[str, str],
    },
    total=False,
)


class MetricQueryTypeDef(_RequiredMetricQueryTypeDef, _OptionalMetricQueryTypeDef):
    pass


DescribeDimensionKeysResponseTypeDef = TypedDict(
    "DescribeDimensionKeysResponseTypeDef",
    {
        "AlignedStartTime": datetime,
        "AlignedEndTime": datetime,
        "PartitionKeys": List[ResponsePartitionKeyTypeDef],
        "Keys": List[DimensionKeyDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DimensionGroupDetailTypeDef = TypedDict(
    "DimensionGroupDetailTypeDef",
    {
        "Group": str,
        "Dimensions": List[DimensionDetailTypeDef],
    },
    total=False,
)

GetDimensionKeyDetailsResponseTypeDef = TypedDict(
    "GetDimensionKeyDetailsResponseTypeDef",
    {
        "Dimensions": List[DimensionKeyDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourceMetadataResponseTypeDef = TypedDict(
    "GetResourceMetadataResponseTypeDef",
    {
        "Identifier": str,
        "Features": Dict[str, FeatureMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAvailableResourceMetricsResponseTypeDef = TypedDict(
    "ListAvailableResourceMetricsResponseTypeDef",
    {
        "Metrics": List[ResponseResourceMetricTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MetricKeyDataPointsTypeDef = TypedDict(
    "MetricKeyDataPointsTypeDef",
    {
        "Key": ResponseResourceMetricKeyTypeDef,
        "DataPoints": List[DataPointTypeDef],
    },
    total=False,
)

ListPerformanceAnalysisReportsResponseTypeDef = TypedDict(
    "ListPerformanceAnalysisReportsResponseTypeDef",
    {
        "AnalysisReports": List[AnalysisReportSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredInsightTypeDef = TypedDict(
    "_RequiredInsightTypeDef",
    {
        "InsightId": str,
    },
)
_OptionalInsightTypeDef = TypedDict(
    "_OptionalInsightTypeDef",
    {
        "InsightType": str,
        "Context": ContextTypeType,
        "StartTime": datetime,
        "EndTime": datetime,
        "Severity": SeverityType,
        "SupportingInsights": List[Dict[str, Any]],
        "Description": str,
        "Recommendations": List[RecommendationTypeDef],
        "InsightData": List[DataTypeDef],
        "BaselineData": List[DataTypeDef],
    },
    total=False,
)


class InsightTypeDef(_RequiredInsightTypeDef, _OptionalInsightTypeDef):
    pass


_RequiredGetResourceMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredGetResourceMetricsRequestRequestTypeDef",
    {
        "ServiceType": ServiceTypeType,
        "Identifier": str,
        "MetricQueries": Sequence[MetricQueryTypeDef],
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
    },
)
_OptionalGetResourceMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalGetResourceMetricsRequestRequestTypeDef",
    {
        "PeriodInSeconds": int,
        "MaxResults": int,
        "NextToken": str,
        "PeriodAlignment": PeriodAlignmentType,
    },
    total=False,
)


class GetResourceMetricsRequestRequestTypeDef(
    _RequiredGetResourceMetricsRequestRequestTypeDef,
    _OptionalGetResourceMetricsRequestRequestTypeDef,
):
    pass


MetricDimensionGroupsTypeDef = TypedDict(
    "MetricDimensionGroupsTypeDef",
    {
        "Metric": str,
        "Groups": List[DimensionGroupDetailTypeDef],
    },
    total=False,
)

GetResourceMetricsResponseTypeDef = TypedDict(
    "GetResourceMetricsResponseTypeDef",
    {
        "AlignedStartTime": datetime,
        "AlignedEndTime": datetime,
        "Identifier": str,
        "MetricList": List[MetricKeyDataPointsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAvailableResourceDimensionsResponseTypeDef = TypedDict(
    "ListAvailableResourceDimensionsResponseTypeDef",
    {
        "MetricDimensions": List[MetricDimensionGroupsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
