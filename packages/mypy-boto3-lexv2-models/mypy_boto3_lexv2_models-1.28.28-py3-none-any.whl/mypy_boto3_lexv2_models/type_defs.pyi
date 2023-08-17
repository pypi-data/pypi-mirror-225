"""
Type annotations for lexv2-models service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lexv2_models/type_defs/)

Usage::

    ```python
    from mypy_boto3_lexv2_models.type_defs import ActiveContextTypeDef

    data: ActiveContextTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AggregatedUtterancesFilterOperatorType,
    AggregatedUtterancesSortAttributeType,
    AnalyticsBinByNameType,
    AnalyticsCommonFilterNameType,
    AnalyticsFilterOperatorType,
    AnalyticsIntentFieldType,
    AnalyticsIntentFilterNameType,
    AnalyticsIntentMetricNameType,
    AnalyticsIntentStageFieldType,
    AnalyticsIntentStageFilterNameType,
    AnalyticsIntentStageMetricNameType,
    AnalyticsIntervalType,
    AnalyticsMetricStatisticType,
    AnalyticsModalityType,
    AnalyticsNodeTypeType,
    AnalyticsSessionFieldType,
    AnalyticsSessionFilterNameType,
    AnalyticsSessionMetricNameType,
    AnalyticsSessionSortByNameType,
    AnalyticsSortOrderType,
    AnalyticsUtteranceFieldType,
    AnalyticsUtteranceFilterNameType,
    AnalyticsUtteranceMetricNameType,
    AssociatedTranscriptFilterNameType,
    BotAliasStatusType,
    BotFilterNameType,
    BotFilterOperatorType,
    BotLocaleFilterOperatorType,
    BotLocaleStatusType,
    BotRecommendationStatusType,
    BotStatusType,
    BotTypeType,
    ConversationEndStateType,
    ConversationLogsInputModeFilterType,
    CustomVocabularyStatusType,
    DialogActionTypeType,
    EffectType,
    ErrorCodeType,
    ExportFilterOperatorType,
    ExportStatusType,
    ImportExportFileFormatType,
    ImportFilterOperatorType,
    ImportResourceTypeType,
    ImportStatusType,
    IntentFilterOperatorType,
    IntentSortAttributeType,
    IntentStateType,
    MergeStrategyType,
    MessageSelectionStrategyType,
    ObfuscationSettingTypeType,
    PromptAttemptType,
    SearchOrderType,
    SlotConstraintType,
    SlotFilterOperatorType,
    SlotShapeType,
    SlotSortAttributeType,
    SlotTypeCategoryType,
    SlotTypeFilterNameType,
    SlotTypeFilterOperatorType,
    SlotTypeSortAttributeType,
    SlotValueResolutionStrategyType,
    SortOrderType,
    TestExecutionApiModeType,
    TestExecutionModalityType,
    TestExecutionSortAttributeType,
    TestExecutionStatusType,
    TestResultMatchStatusType,
    TestResultTypeFilterType,
    TestSetDiscrepancyReportStatusType,
    TestSetGenerationStatusType,
    TestSetModalityType,
    TestSetSortAttributeType,
    TestSetStatusType,
    TimeDimensionType,
    UtteranceContentTypeType,
    VoiceEngineType,
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
    "ActiveContextTypeDef",
    "AdvancedRecognitionSettingTypeDef",
    "ExecutionErrorDetailsTypeDef",
    "AgentTurnSpecificationTypeDef",
    "AggregatedUtterancesFilterTypeDef",
    "AggregatedUtterancesSortByTypeDef",
    "AggregatedUtterancesSummaryTypeDef",
    "AllowedInputTypesTypeDef",
    "AnalyticsBinBySpecificationTypeDef",
    "AnalyticsBinKeyTypeDef",
    "AnalyticsIntentFilterTypeDef",
    "AnalyticsIntentGroupByKeyTypeDef",
    "AnalyticsIntentGroupBySpecificationTypeDef",
    "AnalyticsIntentMetricResultTypeDef",
    "AnalyticsIntentMetricTypeDef",
    "AnalyticsIntentNodeSummaryTypeDef",
    "AnalyticsIntentStageFilterTypeDef",
    "AnalyticsIntentStageGroupByKeyTypeDef",
    "AnalyticsIntentStageGroupBySpecificationTypeDef",
    "AnalyticsIntentStageMetricResultTypeDef",
    "AnalyticsIntentStageMetricTypeDef",
    "AnalyticsPathFilterTypeDef",
    "AnalyticsSessionFilterTypeDef",
    "AnalyticsSessionGroupByKeyTypeDef",
    "AnalyticsSessionGroupBySpecificationTypeDef",
    "AnalyticsSessionMetricResultTypeDef",
    "AnalyticsSessionMetricTypeDef",
    "AnalyticsUtteranceAttributeResultTypeDef",
    "AnalyticsUtteranceAttributeTypeDef",
    "AnalyticsUtteranceFilterTypeDef",
    "AnalyticsUtteranceGroupByKeyTypeDef",
    "AnalyticsUtteranceGroupBySpecificationTypeDef",
    "AnalyticsUtteranceMetricResultTypeDef",
    "AnalyticsUtteranceMetricTypeDef",
    "AssociatedTranscriptFilterTypeDef",
    "AssociatedTranscriptTypeDef",
    "AudioSpecificationTypeDef",
    "DTMFSpecificationTypeDef",
    "S3BucketLogDestinationTypeDef",
    "NewCustomVocabularyItemTypeDef",
    "CustomVocabularyItemTypeDef",
    "FailedCustomVocabularyItemTypeDef",
    "ResponseMetadataTypeDef",
    "CustomVocabularyEntryIdTypeDef",
    "BotAliasHistoryEventTypeDef",
    "BotAliasSummaryTypeDef",
    "BotAliasTestExecutionTargetTypeDef",
    "BotExportSpecificationTypeDef",
    "BotFilterTypeDef",
    "DataPrivacyTypeDef",
    "BotLocaleExportSpecificationTypeDef",
    "BotLocaleFilterTypeDef",
    "BotLocaleHistoryEventTypeDef",
    "VoiceSettingsTypeDef",
    "BotLocaleSortByTypeDef",
    "BotLocaleSummaryTypeDef",
    "BotMemberTypeDef",
    "IntentStatisticsTypeDef",
    "SlotTypeStatisticsTypeDef",
    "BotRecommendationSummaryTypeDef",
    "BotSortByTypeDef",
    "BotSummaryTypeDef",
    "BotVersionLocaleDetailsTypeDef",
    "BotVersionSortByTypeDef",
    "BotVersionSummaryTypeDef",
    "BuildBotLocaleRequestRequestTypeDef",
    "BuiltInIntentSortByTypeDef",
    "BuiltInIntentSummaryTypeDef",
    "BuiltInSlotTypeSortByTypeDef",
    "BuiltInSlotTypeSummaryTypeDef",
    "ButtonTypeDef",
    "CloudWatchLogGroupLogDestinationTypeDef",
    "LambdaCodeHookTypeDef",
    "SubSlotTypeCompositionTypeDef",
    "ConditionTypeDef",
    "ConversationLevelIntentClassificationResultItemTypeDef",
    "ConversationLevelResultDetailTypeDef",
    "ConversationLevelSlotResolutionResultItemTypeDef",
    "ConversationLevelTestResultsFilterByTypeDef",
    "ConversationLogsDataSourceFilterByTypeDef",
    "SentimentAnalysisSettingsTypeDef",
    "DialogCodeHookSettingsTypeDef",
    "InputContextTypeDef",
    "KendraConfigurationTypeDef",
    "OutputContextTypeDef",
    "SampleUtteranceTypeDef",
    "CreateResourcePolicyRequestRequestTypeDef",
    "PrincipalTypeDef",
    "MultipleValuesSettingTypeDef",
    "ObfuscationSettingTypeDef",
    "CustomPayloadTypeDef",
    "CustomVocabularyExportSpecificationTypeDef",
    "CustomVocabularyImportSpecificationTypeDef",
    "DateRangeFilterTypeDef",
    "DeleteBotAliasRequestRequestTypeDef",
    "DeleteBotLocaleRequestRequestTypeDef",
    "DeleteBotRequestRequestTypeDef",
    "DeleteBotVersionRequestRequestTypeDef",
    "DeleteCustomVocabularyRequestRequestTypeDef",
    "DeleteExportRequestRequestTypeDef",
    "DeleteImportRequestRequestTypeDef",
    "DeleteIntentRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteResourcePolicyStatementRequestRequestTypeDef",
    "DeleteSlotRequestRequestTypeDef",
    "DeleteSlotTypeRequestRequestTypeDef",
    "DeleteTestSetRequestRequestTypeDef",
    "DeleteUtterancesRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeBotAliasRequestRequestTypeDef",
    "ParentBotNetworkTypeDef",
    "DescribeBotLocaleRequestRequestTypeDef",
    "DescribeBotRecommendationRequestRequestTypeDef",
    "EncryptionSettingTypeDef",
    "DescribeBotRequestRequestTypeDef",
    "DescribeBotVersionRequestRequestTypeDef",
    "DescribeCustomVocabularyMetadataRequestRequestTypeDef",
    "DescribeExportRequestRequestTypeDef",
    "DescribeImportRequestRequestTypeDef",
    "DescribeIntentRequestRequestTypeDef",
    "SlotPriorityTypeDef",
    "DescribeResourcePolicyRequestRequestTypeDef",
    "DescribeSlotRequestRequestTypeDef",
    "DescribeSlotTypeRequestRequestTypeDef",
    "DescribeTestExecutionRequestRequestTypeDef",
    "DescribeTestSetDiscrepancyReportRequestRequestTypeDef",
    "DescribeTestSetGenerationRequestRequestTypeDef",
    "TestSetStorageLocationTypeDef",
    "DescribeTestSetRequestRequestTypeDef",
    "DialogActionTypeDef",
    "IntentOverrideTypeDef",
    "ElicitationCodeHookInvocationSettingTypeDef",
    "ExportFilterTypeDef",
    "TestSetExportSpecificationTypeDef",
    "ExportSortByTypeDef",
    "GetTestExecutionArtifactsUrlRequestRequestTypeDef",
    "GrammarSlotTypeSourceTypeDef",
    "ImportFilterTypeDef",
    "ImportSortByTypeDef",
    "ImportSummaryTypeDef",
    "RuntimeHintsTypeDef",
    "IntentClassificationTestResultItemCountsTypeDef",
    "IntentFilterTypeDef",
    "IntentSortByTypeDef",
    "InvokedIntentSampleTypeDef",
    "ListBotAliasesRequestRequestTypeDef",
    "ListBotRecommendationsRequestRequestTypeDef",
    "ListCustomVocabularyItemsRequestRequestTypeDef",
    "TimestampTypeDef",
    "ListRecommendedIntentsRequestRequestTypeDef",
    "RecommendedIntentSummaryTypeDef",
    "SessionDataSortByTypeDef",
    "SlotTypeFilterTypeDef",
    "SlotTypeSortByTypeDef",
    "SlotTypeSummaryTypeDef",
    "SlotFilterTypeDef",
    "SlotSortByTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TestExecutionSortByTypeDef",
    "ListTestSetRecordsRequestRequestTypeDef",
    "TestSetSortByTypeDef",
    "UtteranceDataSortByTypeDef",
    "PlainTextMessageTypeDef",
    "SSMLMessageTypeDef",
    "OverallTestResultItemTypeDef",
    "PathFormatTypeDef",
    "TextInputSpecificationTypeDef",
    "RelativeAggregationDurationTypeDef",
    "RuntimeHintValueTypeDef",
    "SampleValueTypeDef",
    "SlotDefaultValueTypeDef",
    "SlotResolutionTestResultItemCountsTypeDef",
    "SlotValueTypeDef",
    "SlotValueRegexFilterTypeDef",
    "StopBotRecommendationRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TestSetIntentDiscrepancyItemTypeDef",
    "TestSetSlotDiscrepancyItemTypeDef",
    "TestSetDiscrepancyReportBotAliasTargetTypeDef",
    "TestSetImportInputLocationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateExportRequestRequestTypeDef",
    "UpdateResourcePolicyRequestRequestTypeDef",
    "UpdateTestSetRequestRequestTypeDef",
    "UserTurnIntentOutputTypeDef",
    "UserTurnSlotOutputTypeDef",
    "UtteranceAudioInputSpecificationTypeDef",
    "AgentTurnResultTypeDef",
    "AnalyticsIntentResultTypeDef",
    "AnalyticsIntentStageResultTypeDef",
    "AnalyticsSessionResultTypeDef",
    "AnalyticsUtteranceResultTypeDef",
    "SearchAssociatedTranscriptsRequestRequestTypeDef",
    "AudioAndDTMFInputSpecificationTypeDef",
    "AudioLogDestinationTypeDef",
    "BatchCreateCustomVocabularyItemRequestRequestTypeDef",
    "BatchUpdateCustomVocabularyItemRequestRequestTypeDef",
    "BatchCreateCustomVocabularyItemResponseTypeDef",
    "BatchDeleteCustomVocabularyItemResponseTypeDef",
    "BatchUpdateCustomVocabularyItemResponseTypeDef",
    "BuildBotLocaleResponseTypeDef",
    "CreateResourcePolicyResponseTypeDef",
    "CreateResourcePolicyStatementResponseTypeDef",
    "CreateUploadUrlResponseTypeDef",
    "DeleteBotAliasResponseTypeDef",
    "DeleteBotLocaleResponseTypeDef",
    "DeleteBotResponseTypeDef",
    "DeleteBotVersionResponseTypeDef",
    "DeleteCustomVocabularyResponseTypeDef",
    "DeleteExportResponseTypeDef",
    "DeleteImportResponseTypeDef",
    "DeleteResourcePolicyResponseTypeDef",
    "DeleteResourcePolicyStatementResponseTypeDef",
    "DescribeCustomVocabularyMetadataResponseTypeDef",
    "DescribeResourcePolicyResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetTestExecutionArtifactsUrlResponseTypeDef",
    "ListCustomVocabularyItemsResponseTypeDef",
    "ListIntentPathsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SearchAssociatedTranscriptsResponseTypeDef",
    "StopBotRecommendationResponseTypeDef",
    "UpdateResourcePolicyResponseTypeDef",
    "BatchDeleteCustomVocabularyItemRequestRequestTypeDef",
    "ListBotAliasesResponseTypeDef",
    "TestExecutionTargetTypeDef",
    "BotImportSpecificationTypeDef",
    "BotLocaleImportSpecificationTypeDef",
    "CreateBotLocaleRequestRequestTypeDef",
    "CreateBotLocaleResponseTypeDef",
    "DescribeBotLocaleResponseTypeDef",
    "UpdateBotLocaleRequestRequestTypeDef",
    "UpdateBotLocaleResponseTypeDef",
    "ListBotLocalesRequestRequestTypeDef",
    "ListBotLocalesResponseTypeDef",
    "CreateBotRequestRequestTypeDef",
    "CreateBotResponseTypeDef",
    "DescribeBotResponseTypeDef",
    "UpdateBotRequestRequestTypeDef",
    "UpdateBotResponseTypeDef",
    "BotRecommendationResultStatisticsTypeDef",
    "ListBotRecommendationsResponseTypeDef",
    "ListBotsRequestRequestTypeDef",
    "ListBotsResponseTypeDef",
    "CreateBotVersionRequestRequestTypeDef",
    "CreateBotVersionResponseTypeDef",
    "ListBotVersionsRequestRequestTypeDef",
    "ListBotVersionsResponseTypeDef",
    "ListBuiltInIntentsRequestRequestTypeDef",
    "ListBuiltInIntentsResponseTypeDef",
    "ListBuiltInSlotTypesRequestRequestTypeDef",
    "ListBuiltInSlotTypesResponseTypeDef",
    "ImageResponseCardTypeDef",
    "TextLogDestinationTypeDef",
    "CodeHookSpecificationTypeDef",
    "CompositeSlotTypeSettingTypeDef",
    "ConversationLevelTestResultItemTypeDef",
    "TestExecutionResultFilterByTypeDef",
    "ConversationLogsDataSourceTypeDef",
    "IntentSummaryTypeDef",
    "CreateResourcePolicyStatementRequestRequestTypeDef",
    "LexTranscriptFilterTypeDef",
    "DescribeBotAliasRequestBotAliasAvailableWaitTypeDef",
    "DescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef",
    "DescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef",
    "DescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef",
    "DescribeBotRequestBotAvailableWaitTypeDef",
    "DescribeBotVersionRequestBotVersionAvailableWaitTypeDef",
    "DescribeExportRequestBotExportCompletedWaitTypeDef",
    "DescribeImportRequestBotImportCompletedWaitTypeDef",
    "DescribeBotVersionResponseTypeDef",
    "UpdateBotRecommendationRequestRequestTypeDef",
    "DescribeTestSetResponseTypeDef",
    "TestSetSummaryTypeDef",
    "UpdateTestSetResponseTypeDef",
    "DialogStateTypeDef",
    "ExportResourceSpecificationTypeDef",
    "ListExportsRequestRequestTypeDef",
    "GrammarSlotTypeSettingTypeDef",
    "ListImportsRequestRequestTypeDef",
    "ListImportsResponseTypeDef",
    "InputSessionStateSpecificationTypeDef",
    "IntentClassificationTestResultItemTypeDef",
    "ListIntentsRequestRequestTypeDef",
    "SessionSpecificationTypeDef",
    "ListIntentMetricsRequestRequestTypeDef",
    "ListIntentPathsRequestRequestTypeDef",
    "ListIntentStageMetricsRequestRequestTypeDef",
    "ListSessionMetricsRequestRequestTypeDef",
    "ListUtteranceMetricsRequestRequestTypeDef",
    "ListRecommendedIntentsResponseTypeDef",
    "ListSessionAnalyticsDataRequestRequestTypeDef",
    "ListSlotTypesRequestRequestTypeDef",
    "ListSlotTypesResponseTypeDef",
    "ListSlotsRequestRequestTypeDef",
    "ListTestExecutionsRequestRequestTypeDef",
    "ListTestSetsRequestRequestTypeDef",
    "ListUtteranceAnalyticsDataRequestRequestTypeDef",
    "OverallTestResultsTypeDef",
    "UtteranceAggregationDurationTypeDef",
    "RuntimeHintDetailsTypeDef",
    "SlotTypeValueTypeDef",
    "SlotDefaultValueSpecificationTypeDef",
    "SlotResolutionTestResultItemTypeDef",
    "SlotValueOverrideTypeDef",
    "SlotValueSelectionSettingTypeDef",
    "TestSetDiscrepancyErrorsTypeDef",
    "TestSetDiscrepancyReportResourceTargetTypeDef",
    "TestSetImportResourceSpecificationTypeDef",
    "UserTurnOutputSpecificationTypeDef",
    "UtteranceInputSpecificationTypeDef",
    "ListIntentMetricsResponseTypeDef",
    "ListIntentStageMetricsResponseTypeDef",
    "ListSessionMetricsResponseTypeDef",
    "ListUtteranceMetricsResponseTypeDef",
    "PromptAttemptSpecificationTypeDef",
    "AudioLogSettingTypeDef",
    "DescribeTestExecutionResponseTypeDef",
    "StartTestExecutionRequestRequestTypeDef",
    "StartTestExecutionResponseTypeDef",
    "TestExecutionSummaryTypeDef",
    "BotRecommendationResultsTypeDef",
    "MessageTypeDef",
    "UtteranceBotResponseTypeDef",
    "TextLogSettingTypeDef",
    "BotAliasLocaleSettingsTypeDef",
    "ConversationLevelTestResultsTypeDef",
    "ListTestExecutionResultItemsRequestRequestTypeDef",
    "TestSetGenerationDataSourceTypeDef",
    "ListIntentsResponseTypeDef",
    "TranscriptFilterTypeDef",
    "ListTestSetsResponseTypeDef",
    "CreateExportRequestRequestTypeDef",
    "CreateExportResponseTypeDef",
    "DescribeExportResponseTypeDef",
    "ExportSummaryTypeDef",
    "UpdateExportResponseTypeDef",
    "ExternalSourceSettingTypeDef",
    "IntentClassificationTestResultsTypeDef",
    "ListSessionAnalyticsDataResponseTypeDef",
    "ListAggregatedUtterancesRequestRequestTypeDef",
    "ListAggregatedUtterancesResponseTypeDef",
    "IntentLevelSlotResolutionTestResultItemTypeDef",
    "CreateTestSetDiscrepancyReportRequestRequestTypeDef",
    "CreateTestSetDiscrepancyReportResponseTypeDef",
    "DescribeTestSetDiscrepancyReportResponseTypeDef",
    "ImportResourceSpecificationTypeDef",
    "UserTurnInputSpecificationTypeDef",
    "ListTestExecutionsResponseTypeDef",
    "MessageGroupTypeDef",
    "UtteranceSpecificationTypeDef",
    "ConversationLogSettingsTypeDef",
    "DescribeTestSetGenerationResponseTypeDef",
    "StartTestSetGenerationRequestRequestTypeDef",
    "StartTestSetGenerationResponseTypeDef",
    "S3BucketTranscriptSourceTypeDef",
    "ListExportsResponseTypeDef",
    "CreateSlotTypeRequestRequestTypeDef",
    "CreateSlotTypeResponseTypeDef",
    "DescribeSlotTypeResponseTypeDef",
    "UpdateSlotTypeRequestRequestTypeDef",
    "UpdateSlotTypeResponseTypeDef",
    "IntentLevelSlotResolutionTestResultsTypeDef",
    "DescribeImportResponseTypeDef",
    "StartImportRequestRequestTypeDef",
    "StartImportResponseTypeDef",
    "UserTurnResultTypeDef",
    "UserTurnSpecificationTypeDef",
    "FulfillmentStartResponseSpecificationTypeDef",
    "FulfillmentUpdateResponseSpecificationTypeDef",
    "PromptSpecificationTypeDef",
    "ResponseSpecificationTypeDef",
    "StillWaitingResponseSpecificationTypeDef",
    "ListUtteranceAnalyticsDataResponseTypeDef",
    "CreateBotAliasRequestRequestTypeDef",
    "CreateBotAliasResponseTypeDef",
    "DescribeBotAliasResponseTypeDef",
    "UpdateBotAliasRequestRequestTypeDef",
    "UpdateBotAliasResponseTypeDef",
    "TranscriptSourceSettingTypeDef",
    "TestSetTurnResultTypeDef",
    "TurnSpecificationTypeDef",
    "FulfillmentUpdatesSpecificationTypeDef",
    "SlotSummaryTypeDef",
    "ConditionalBranchTypeDef",
    "DefaultConditionalBranchTypeDef",
    "WaitAndContinueSpecificationTypeDef",
    "DescribeBotRecommendationResponseTypeDef",
    "StartBotRecommendationRequestRequestTypeDef",
    "StartBotRecommendationResponseTypeDef",
    "UpdateBotRecommendationResponseTypeDef",
    "UtteranceLevelTestResultItemTypeDef",
    "TestSetTurnRecordTypeDef",
    "ListSlotsResponseTypeDef",
    "ConditionalSpecificationTypeDef",
    "SubSlotValueElicitationSettingTypeDef",
    "UtteranceLevelTestResultsTypeDef",
    "ListTestSetRecordsResponseTypeDef",
    "IntentClosingSettingTypeDef",
    "PostDialogCodeHookInvocationSpecificationTypeDef",
    "PostFulfillmentStatusSpecificationTypeDef",
    "SpecificationsTypeDef",
    "TestExecutionResultItemsTypeDef",
    "DialogCodeHookInvocationSettingTypeDef",
    "FulfillmentCodeHookSettingsTypeDef",
    "SubSlotSettingTypeDef",
    "ListTestExecutionResultItemsResponseTypeDef",
    "InitialResponseSettingTypeDef",
    "IntentConfirmationSettingTypeDef",
    "SlotCaptureSettingTypeDef",
    "CreateIntentRequestRequestTypeDef",
    "CreateIntentResponseTypeDef",
    "DescribeIntentResponseTypeDef",
    "UpdateIntentRequestRequestTypeDef",
    "UpdateIntentResponseTypeDef",
    "SlotValueElicitationSettingTypeDef",
    "CreateSlotRequestRequestTypeDef",
    "CreateSlotResponseTypeDef",
    "DescribeSlotResponseTypeDef",
    "UpdateSlotRequestRequestTypeDef",
    "UpdateSlotResponseTypeDef",
)

ActiveContextTypeDef = TypedDict(
    "ActiveContextTypeDef",
    {
        "name": str,
    },
)

AdvancedRecognitionSettingTypeDef = TypedDict(
    "AdvancedRecognitionSettingTypeDef",
    {
        "audioRecognitionStrategy": Literal["UseSlotValuesAsCustomVocabulary"],
    },
    total=False,
)

ExecutionErrorDetailsTypeDef = TypedDict(
    "ExecutionErrorDetailsTypeDef",
    {
        "errorCode": str,
        "errorMessage": str,
    },
)

AgentTurnSpecificationTypeDef = TypedDict(
    "AgentTurnSpecificationTypeDef",
    {
        "agentPrompt": str,
    },
)

AggregatedUtterancesFilterTypeDef = TypedDict(
    "AggregatedUtterancesFilterTypeDef",
    {
        "name": Literal["Utterance"],
        "values": Sequence[str],
        "operator": AggregatedUtterancesFilterOperatorType,
    },
)

AggregatedUtterancesSortByTypeDef = TypedDict(
    "AggregatedUtterancesSortByTypeDef",
    {
        "attribute": AggregatedUtterancesSortAttributeType,
        "order": SortOrderType,
    },
)

AggregatedUtterancesSummaryTypeDef = TypedDict(
    "AggregatedUtterancesSummaryTypeDef",
    {
        "utterance": str,
        "hitCount": int,
        "missedCount": int,
        "utteranceFirstRecordedInAggregationDuration": datetime,
        "utteranceLastRecordedInAggregationDuration": datetime,
        "containsDataFromDeletedResources": bool,
    },
    total=False,
)

AllowedInputTypesTypeDef = TypedDict(
    "AllowedInputTypesTypeDef",
    {
        "allowAudioInput": bool,
        "allowDTMFInput": bool,
    },
)

_RequiredAnalyticsBinBySpecificationTypeDef = TypedDict(
    "_RequiredAnalyticsBinBySpecificationTypeDef",
    {
        "name": AnalyticsBinByNameType,
        "interval": AnalyticsIntervalType,
    },
)
_OptionalAnalyticsBinBySpecificationTypeDef = TypedDict(
    "_OptionalAnalyticsBinBySpecificationTypeDef",
    {
        "order": AnalyticsSortOrderType,
    },
    total=False,
)

class AnalyticsBinBySpecificationTypeDef(
    _RequiredAnalyticsBinBySpecificationTypeDef, _OptionalAnalyticsBinBySpecificationTypeDef
):
    pass

AnalyticsBinKeyTypeDef = TypedDict(
    "AnalyticsBinKeyTypeDef",
    {
        "name": AnalyticsBinByNameType,
        "value": int,
    },
    total=False,
)

AnalyticsIntentFilterTypeDef = TypedDict(
    "AnalyticsIntentFilterTypeDef",
    {
        "name": AnalyticsIntentFilterNameType,
        "operator": AnalyticsFilterOperatorType,
        "values": Sequence[str],
    },
)

AnalyticsIntentGroupByKeyTypeDef = TypedDict(
    "AnalyticsIntentGroupByKeyTypeDef",
    {
        "name": AnalyticsIntentFieldType,
        "value": str,
    },
    total=False,
)

AnalyticsIntentGroupBySpecificationTypeDef = TypedDict(
    "AnalyticsIntentGroupBySpecificationTypeDef",
    {
        "name": AnalyticsIntentFieldType,
    },
)

AnalyticsIntentMetricResultTypeDef = TypedDict(
    "AnalyticsIntentMetricResultTypeDef",
    {
        "name": AnalyticsIntentMetricNameType,
        "statistic": AnalyticsMetricStatisticType,
        "value": float,
    },
    total=False,
)

_RequiredAnalyticsIntentMetricTypeDef = TypedDict(
    "_RequiredAnalyticsIntentMetricTypeDef",
    {
        "name": AnalyticsIntentMetricNameType,
        "statistic": AnalyticsMetricStatisticType,
    },
)
_OptionalAnalyticsIntentMetricTypeDef = TypedDict(
    "_OptionalAnalyticsIntentMetricTypeDef",
    {
        "order": AnalyticsSortOrderType,
    },
    total=False,
)

class AnalyticsIntentMetricTypeDef(
    _RequiredAnalyticsIntentMetricTypeDef, _OptionalAnalyticsIntentMetricTypeDef
):
    pass

AnalyticsIntentNodeSummaryTypeDef = TypedDict(
    "AnalyticsIntentNodeSummaryTypeDef",
    {
        "intentName": str,
        "intentPath": str,
        "intentCount": int,
        "intentLevel": int,
        "nodeType": AnalyticsNodeTypeType,
    },
    total=False,
)

AnalyticsIntentStageFilterTypeDef = TypedDict(
    "AnalyticsIntentStageFilterTypeDef",
    {
        "name": AnalyticsIntentStageFilterNameType,
        "operator": AnalyticsFilterOperatorType,
        "values": Sequence[str],
    },
)

AnalyticsIntentStageGroupByKeyTypeDef = TypedDict(
    "AnalyticsIntentStageGroupByKeyTypeDef",
    {
        "name": AnalyticsIntentStageFieldType,
        "value": str,
    },
    total=False,
)

AnalyticsIntentStageGroupBySpecificationTypeDef = TypedDict(
    "AnalyticsIntentStageGroupBySpecificationTypeDef",
    {
        "name": AnalyticsIntentStageFieldType,
    },
)

AnalyticsIntentStageMetricResultTypeDef = TypedDict(
    "AnalyticsIntentStageMetricResultTypeDef",
    {
        "name": AnalyticsIntentStageMetricNameType,
        "statistic": AnalyticsMetricStatisticType,
        "value": float,
    },
    total=False,
)

_RequiredAnalyticsIntentStageMetricTypeDef = TypedDict(
    "_RequiredAnalyticsIntentStageMetricTypeDef",
    {
        "name": AnalyticsIntentStageMetricNameType,
        "statistic": AnalyticsMetricStatisticType,
    },
)
_OptionalAnalyticsIntentStageMetricTypeDef = TypedDict(
    "_OptionalAnalyticsIntentStageMetricTypeDef",
    {
        "order": AnalyticsSortOrderType,
    },
    total=False,
)

class AnalyticsIntentStageMetricTypeDef(
    _RequiredAnalyticsIntentStageMetricTypeDef, _OptionalAnalyticsIntentStageMetricTypeDef
):
    pass

AnalyticsPathFilterTypeDef = TypedDict(
    "AnalyticsPathFilterTypeDef",
    {
        "name": AnalyticsCommonFilterNameType,
        "operator": AnalyticsFilterOperatorType,
        "values": Sequence[str],
    },
)

AnalyticsSessionFilterTypeDef = TypedDict(
    "AnalyticsSessionFilterTypeDef",
    {
        "name": AnalyticsSessionFilterNameType,
        "operator": AnalyticsFilterOperatorType,
        "values": Sequence[str],
    },
)

AnalyticsSessionGroupByKeyTypeDef = TypedDict(
    "AnalyticsSessionGroupByKeyTypeDef",
    {
        "name": AnalyticsSessionFieldType,
        "value": str,
    },
    total=False,
)

AnalyticsSessionGroupBySpecificationTypeDef = TypedDict(
    "AnalyticsSessionGroupBySpecificationTypeDef",
    {
        "name": AnalyticsSessionFieldType,
    },
)

AnalyticsSessionMetricResultTypeDef = TypedDict(
    "AnalyticsSessionMetricResultTypeDef",
    {
        "name": AnalyticsSessionMetricNameType,
        "statistic": AnalyticsMetricStatisticType,
        "value": float,
    },
    total=False,
)

_RequiredAnalyticsSessionMetricTypeDef = TypedDict(
    "_RequiredAnalyticsSessionMetricTypeDef",
    {
        "name": AnalyticsSessionMetricNameType,
        "statistic": AnalyticsMetricStatisticType,
    },
)
_OptionalAnalyticsSessionMetricTypeDef = TypedDict(
    "_OptionalAnalyticsSessionMetricTypeDef",
    {
        "order": AnalyticsSortOrderType,
    },
    total=False,
)

class AnalyticsSessionMetricTypeDef(
    _RequiredAnalyticsSessionMetricTypeDef, _OptionalAnalyticsSessionMetricTypeDef
):
    pass

AnalyticsUtteranceAttributeResultTypeDef = TypedDict(
    "AnalyticsUtteranceAttributeResultTypeDef",
    {
        "lastUsedIntent": str,
    },
    total=False,
)

AnalyticsUtteranceAttributeTypeDef = TypedDict(
    "AnalyticsUtteranceAttributeTypeDef",
    {
        "name": Literal["LastUsedIntent"],
    },
)

AnalyticsUtteranceFilterTypeDef = TypedDict(
    "AnalyticsUtteranceFilterTypeDef",
    {
        "name": AnalyticsUtteranceFilterNameType,
        "operator": AnalyticsFilterOperatorType,
        "values": Sequence[str],
    },
)

AnalyticsUtteranceGroupByKeyTypeDef = TypedDict(
    "AnalyticsUtteranceGroupByKeyTypeDef",
    {
        "name": AnalyticsUtteranceFieldType,
        "value": str,
    },
    total=False,
)

AnalyticsUtteranceGroupBySpecificationTypeDef = TypedDict(
    "AnalyticsUtteranceGroupBySpecificationTypeDef",
    {
        "name": AnalyticsUtteranceFieldType,
    },
)

AnalyticsUtteranceMetricResultTypeDef = TypedDict(
    "AnalyticsUtteranceMetricResultTypeDef",
    {
        "name": AnalyticsUtteranceMetricNameType,
        "statistic": AnalyticsMetricStatisticType,
        "value": float,
    },
    total=False,
)

_RequiredAnalyticsUtteranceMetricTypeDef = TypedDict(
    "_RequiredAnalyticsUtteranceMetricTypeDef",
    {
        "name": AnalyticsUtteranceMetricNameType,
        "statistic": AnalyticsMetricStatisticType,
    },
)
_OptionalAnalyticsUtteranceMetricTypeDef = TypedDict(
    "_OptionalAnalyticsUtteranceMetricTypeDef",
    {
        "order": AnalyticsSortOrderType,
    },
    total=False,
)

class AnalyticsUtteranceMetricTypeDef(
    _RequiredAnalyticsUtteranceMetricTypeDef, _OptionalAnalyticsUtteranceMetricTypeDef
):
    pass

AssociatedTranscriptFilterTypeDef = TypedDict(
    "AssociatedTranscriptFilterTypeDef",
    {
        "name": AssociatedTranscriptFilterNameType,
        "values": Sequence[str],
    },
)

AssociatedTranscriptTypeDef = TypedDict(
    "AssociatedTranscriptTypeDef",
    {
        "transcript": str,
    },
    total=False,
)

AudioSpecificationTypeDef = TypedDict(
    "AudioSpecificationTypeDef",
    {
        "maxLengthMs": int,
        "endTimeoutMs": int,
    },
)

DTMFSpecificationTypeDef = TypedDict(
    "DTMFSpecificationTypeDef",
    {
        "maxLength": int,
        "endTimeoutMs": int,
        "deletionCharacter": str,
        "endCharacter": str,
    },
)

_RequiredS3BucketLogDestinationTypeDef = TypedDict(
    "_RequiredS3BucketLogDestinationTypeDef",
    {
        "s3BucketArn": str,
        "logPrefix": str,
    },
)
_OptionalS3BucketLogDestinationTypeDef = TypedDict(
    "_OptionalS3BucketLogDestinationTypeDef",
    {
        "kmsKeyArn": str,
    },
    total=False,
)

class S3BucketLogDestinationTypeDef(
    _RequiredS3BucketLogDestinationTypeDef, _OptionalS3BucketLogDestinationTypeDef
):
    pass

_RequiredNewCustomVocabularyItemTypeDef = TypedDict(
    "_RequiredNewCustomVocabularyItemTypeDef",
    {
        "phrase": str,
    },
)
_OptionalNewCustomVocabularyItemTypeDef = TypedDict(
    "_OptionalNewCustomVocabularyItemTypeDef",
    {
        "weight": int,
        "displayAs": str,
    },
    total=False,
)

class NewCustomVocabularyItemTypeDef(
    _RequiredNewCustomVocabularyItemTypeDef, _OptionalNewCustomVocabularyItemTypeDef
):
    pass

_RequiredCustomVocabularyItemTypeDef = TypedDict(
    "_RequiredCustomVocabularyItemTypeDef",
    {
        "itemId": str,
        "phrase": str,
    },
)
_OptionalCustomVocabularyItemTypeDef = TypedDict(
    "_OptionalCustomVocabularyItemTypeDef",
    {
        "weight": int,
        "displayAs": str,
    },
    total=False,
)

class CustomVocabularyItemTypeDef(
    _RequiredCustomVocabularyItemTypeDef, _OptionalCustomVocabularyItemTypeDef
):
    pass

FailedCustomVocabularyItemTypeDef = TypedDict(
    "FailedCustomVocabularyItemTypeDef",
    {
        "itemId": str,
        "errorMessage": str,
        "errorCode": ErrorCodeType,
    },
    total=False,
)

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

CustomVocabularyEntryIdTypeDef = TypedDict(
    "CustomVocabularyEntryIdTypeDef",
    {
        "itemId": str,
    },
)

BotAliasHistoryEventTypeDef = TypedDict(
    "BotAliasHistoryEventTypeDef",
    {
        "botVersion": str,
        "startDate": datetime,
        "endDate": datetime,
    },
    total=False,
)

BotAliasSummaryTypeDef = TypedDict(
    "BotAliasSummaryTypeDef",
    {
        "botAliasId": str,
        "botAliasName": str,
        "description": str,
        "botVersion": str,
        "botAliasStatus": BotAliasStatusType,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

BotAliasTestExecutionTargetTypeDef = TypedDict(
    "BotAliasTestExecutionTargetTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
    },
)

BotExportSpecificationTypeDef = TypedDict(
    "BotExportSpecificationTypeDef",
    {
        "botId": str,
        "botVersion": str,
    },
)

BotFilterTypeDef = TypedDict(
    "BotFilterTypeDef",
    {
        "name": BotFilterNameType,
        "values": Sequence[str],
        "operator": BotFilterOperatorType,
    },
)

DataPrivacyTypeDef = TypedDict(
    "DataPrivacyTypeDef",
    {
        "childDirected": bool,
    },
)

BotLocaleExportSpecificationTypeDef = TypedDict(
    "BotLocaleExportSpecificationTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

BotLocaleFilterTypeDef = TypedDict(
    "BotLocaleFilterTypeDef",
    {
        "name": Literal["BotLocaleName"],
        "values": Sequence[str],
        "operator": BotLocaleFilterOperatorType,
    },
)

BotLocaleHistoryEventTypeDef = TypedDict(
    "BotLocaleHistoryEventTypeDef",
    {
        "event": str,
        "eventDate": datetime,
    },
)

_RequiredVoiceSettingsTypeDef = TypedDict(
    "_RequiredVoiceSettingsTypeDef",
    {
        "voiceId": str,
    },
)
_OptionalVoiceSettingsTypeDef = TypedDict(
    "_OptionalVoiceSettingsTypeDef",
    {
        "engine": VoiceEngineType,
    },
    total=False,
)

class VoiceSettingsTypeDef(_RequiredVoiceSettingsTypeDef, _OptionalVoiceSettingsTypeDef):
    pass

BotLocaleSortByTypeDef = TypedDict(
    "BotLocaleSortByTypeDef",
    {
        "attribute": Literal["BotLocaleName"],
        "order": SortOrderType,
    },
)

BotLocaleSummaryTypeDef = TypedDict(
    "BotLocaleSummaryTypeDef",
    {
        "localeId": str,
        "localeName": str,
        "description": str,
        "botLocaleStatus": BotLocaleStatusType,
        "lastUpdatedDateTime": datetime,
        "lastBuildSubmittedDateTime": datetime,
    },
    total=False,
)

BotMemberTypeDef = TypedDict(
    "BotMemberTypeDef",
    {
        "botMemberId": str,
        "botMemberName": str,
        "botMemberAliasId": str,
        "botMemberAliasName": str,
        "botMemberVersion": str,
    },
)

IntentStatisticsTypeDef = TypedDict(
    "IntentStatisticsTypeDef",
    {
        "discoveredIntentCount": int,
    },
    total=False,
)

SlotTypeStatisticsTypeDef = TypedDict(
    "SlotTypeStatisticsTypeDef",
    {
        "discoveredSlotTypeCount": int,
    },
    total=False,
)

_RequiredBotRecommendationSummaryTypeDef = TypedDict(
    "_RequiredBotRecommendationSummaryTypeDef",
    {
        "botRecommendationStatus": BotRecommendationStatusType,
        "botRecommendationId": str,
    },
)
_OptionalBotRecommendationSummaryTypeDef = TypedDict(
    "_OptionalBotRecommendationSummaryTypeDef",
    {
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

class BotRecommendationSummaryTypeDef(
    _RequiredBotRecommendationSummaryTypeDef, _OptionalBotRecommendationSummaryTypeDef
):
    pass

BotSortByTypeDef = TypedDict(
    "BotSortByTypeDef",
    {
        "attribute": Literal["BotName"],
        "order": SortOrderType,
    },
)

BotSummaryTypeDef = TypedDict(
    "BotSummaryTypeDef",
    {
        "botId": str,
        "botName": str,
        "description": str,
        "botStatus": BotStatusType,
        "latestBotVersion": str,
        "lastUpdatedDateTime": datetime,
        "botType": BotTypeType,
    },
    total=False,
)

BotVersionLocaleDetailsTypeDef = TypedDict(
    "BotVersionLocaleDetailsTypeDef",
    {
        "sourceBotVersion": str,
    },
)

BotVersionSortByTypeDef = TypedDict(
    "BotVersionSortByTypeDef",
    {
        "attribute": Literal["BotVersion"],
        "order": SortOrderType,
    },
)

BotVersionSummaryTypeDef = TypedDict(
    "BotVersionSummaryTypeDef",
    {
        "botName": str,
        "botVersion": str,
        "description": str,
        "botStatus": BotStatusType,
        "creationDateTime": datetime,
    },
    total=False,
)

BuildBotLocaleRequestRequestTypeDef = TypedDict(
    "BuildBotLocaleRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

BuiltInIntentSortByTypeDef = TypedDict(
    "BuiltInIntentSortByTypeDef",
    {
        "attribute": Literal["IntentSignature"],
        "order": SortOrderType,
    },
)

BuiltInIntentSummaryTypeDef = TypedDict(
    "BuiltInIntentSummaryTypeDef",
    {
        "intentSignature": str,
        "description": str,
    },
    total=False,
)

BuiltInSlotTypeSortByTypeDef = TypedDict(
    "BuiltInSlotTypeSortByTypeDef",
    {
        "attribute": Literal["SlotTypeSignature"],
        "order": SortOrderType,
    },
)

BuiltInSlotTypeSummaryTypeDef = TypedDict(
    "BuiltInSlotTypeSummaryTypeDef",
    {
        "slotTypeSignature": str,
        "description": str,
    },
    total=False,
)

ButtonTypeDef = TypedDict(
    "ButtonTypeDef",
    {
        "text": str,
        "value": str,
    },
)

CloudWatchLogGroupLogDestinationTypeDef = TypedDict(
    "CloudWatchLogGroupLogDestinationTypeDef",
    {
        "cloudWatchLogGroupArn": str,
        "logPrefix": str,
    },
)

LambdaCodeHookTypeDef = TypedDict(
    "LambdaCodeHookTypeDef",
    {
        "lambdaARN": str,
        "codeHookInterfaceVersion": str,
    },
)

SubSlotTypeCompositionTypeDef = TypedDict(
    "SubSlotTypeCompositionTypeDef",
    {
        "name": str,
        "slotTypeId": str,
    },
)

ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "expressionString": str,
    },
)

ConversationLevelIntentClassificationResultItemTypeDef = TypedDict(
    "ConversationLevelIntentClassificationResultItemTypeDef",
    {
        "intentName": str,
        "matchResult": TestResultMatchStatusType,
    },
)

_RequiredConversationLevelResultDetailTypeDef = TypedDict(
    "_RequiredConversationLevelResultDetailTypeDef",
    {
        "endToEndResult": TestResultMatchStatusType,
    },
)
_OptionalConversationLevelResultDetailTypeDef = TypedDict(
    "_OptionalConversationLevelResultDetailTypeDef",
    {
        "speechTranscriptionResult": TestResultMatchStatusType,
    },
    total=False,
)

class ConversationLevelResultDetailTypeDef(
    _RequiredConversationLevelResultDetailTypeDef, _OptionalConversationLevelResultDetailTypeDef
):
    pass

ConversationLevelSlotResolutionResultItemTypeDef = TypedDict(
    "ConversationLevelSlotResolutionResultItemTypeDef",
    {
        "intentName": str,
        "slotName": str,
        "matchResult": TestResultMatchStatusType,
    },
)

ConversationLevelTestResultsFilterByTypeDef = TypedDict(
    "ConversationLevelTestResultsFilterByTypeDef",
    {
        "endToEndResult": TestResultMatchStatusType,
    },
    total=False,
)

ConversationLogsDataSourceFilterByTypeDef = TypedDict(
    "ConversationLogsDataSourceFilterByTypeDef",
    {
        "startTime": datetime,
        "endTime": datetime,
        "inputMode": ConversationLogsInputModeFilterType,
    },
)

SentimentAnalysisSettingsTypeDef = TypedDict(
    "SentimentAnalysisSettingsTypeDef",
    {
        "detectSentiment": bool,
    },
)

DialogCodeHookSettingsTypeDef = TypedDict(
    "DialogCodeHookSettingsTypeDef",
    {
        "enabled": bool,
    },
)

InputContextTypeDef = TypedDict(
    "InputContextTypeDef",
    {
        "name": str,
    },
)

_RequiredKendraConfigurationTypeDef = TypedDict(
    "_RequiredKendraConfigurationTypeDef",
    {
        "kendraIndex": str,
    },
)
_OptionalKendraConfigurationTypeDef = TypedDict(
    "_OptionalKendraConfigurationTypeDef",
    {
        "queryFilterStringEnabled": bool,
        "queryFilterString": str,
    },
    total=False,
)

class KendraConfigurationTypeDef(
    _RequiredKendraConfigurationTypeDef, _OptionalKendraConfigurationTypeDef
):
    pass

OutputContextTypeDef = TypedDict(
    "OutputContextTypeDef",
    {
        "name": str,
        "timeToLiveInSeconds": int,
        "turnsToLive": int,
    },
)

SampleUtteranceTypeDef = TypedDict(
    "SampleUtteranceTypeDef",
    {
        "utterance": str,
    },
)

CreateResourcePolicyRequestRequestTypeDef = TypedDict(
    "CreateResourcePolicyRequestRequestTypeDef",
    {
        "resourceArn": str,
        "policy": str,
    },
)

PrincipalTypeDef = TypedDict(
    "PrincipalTypeDef",
    {
        "service": str,
        "arn": str,
    },
    total=False,
)

MultipleValuesSettingTypeDef = TypedDict(
    "MultipleValuesSettingTypeDef",
    {
        "allowMultipleValues": bool,
    },
    total=False,
)

ObfuscationSettingTypeDef = TypedDict(
    "ObfuscationSettingTypeDef",
    {
        "obfuscationSettingType": ObfuscationSettingTypeType,
    },
)

CustomPayloadTypeDef = TypedDict(
    "CustomPayloadTypeDef",
    {
        "value": str,
    },
)

CustomVocabularyExportSpecificationTypeDef = TypedDict(
    "CustomVocabularyExportSpecificationTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

CustomVocabularyImportSpecificationTypeDef = TypedDict(
    "CustomVocabularyImportSpecificationTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

DateRangeFilterTypeDef = TypedDict(
    "DateRangeFilterTypeDef",
    {
        "startDateTime": datetime,
        "endDateTime": datetime,
    },
)

_RequiredDeleteBotAliasRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBotAliasRequestRequestTypeDef",
    {
        "botAliasId": str,
        "botId": str,
    },
)
_OptionalDeleteBotAliasRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBotAliasRequestRequestTypeDef",
    {
        "skipResourceInUseCheck": bool,
    },
    total=False,
)

class DeleteBotAliasRequestRequestTypeDef(
    _RequiredDeleteBotAliasRequestRequestTypeDef, _OptionalDeleteBotAliasRequestRequestTypeDef
):
    pass

DeleteBotLocaleRequestRequestTypeDef = TypedDict(
    "DeleteBotLocaleRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

_RequiredDeleteBotRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBotRequestRequestTypeDef",
    {
        "botId": str,
    },
)
_OptionalDeleteBotRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBotRequestRequestTypeDef",
    {
        "skipResourceInUseCheck": bool,
    },
    total=False,
)

class DeleteBotRequestRequestTypeDef(
    _RequiredDeleteBotRequestRequestTypeDef, _OptionalDeleteBotRequestRequestTypeDef
):
    pass

_RequiredDeleteBotVersionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteBotVersionRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
    },
)
_OptionalDeleteBotVersionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteBotVersionRequestRequestTypeDef",
    {
        "skipResourceInUseCheck": bool,
    },
    total=False,
)

class DeleteBotVersionRequestRequestTypeDef(
    _RequiredDeleteBotVersionRequestRequestTypeDef, _OptionalDeleteBotVersionRequestRequestTypeDef
):
    pass

DeleteCustomVocabularyRequestRequestTypeDef = TypedDict(
    "DeleteCustomVocabularyRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

DeleteExportRequestRequestTypeDef = TypedDict(
    "DeleteExportRequestRequestTypeDef",
    {
        "exportId": str,
    },
)

DeleteImportRequestRequestTypeDef = TypedDict(
    "DeleteImportRequestRequestTypeDef",
    {
        "importId": str,
    },
)

DeleteIntentRequestRequestTypeDef = TypedDict(
    "DeleteIntentRequestRequestTypeDef",
    {
        "intentId": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

_RequiredDeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteResourcePolicyRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalDeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteResourcePolicyRequestRequestTypeDef",
    {
        "expectedRevisionId": str,
    },
    total=False,
)

class DeleteResourcePolicyRequestRequestTypeDef(
    _RequiredDeleteResourcePolicyRequestRequestTypeDef,
    _OptionalDeleteResourcePolicyRequestRequestTypeDef,
):
    pass

_RequiredDeleteResourcePolicyStatementRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteResourcePolicyStatementRequestRequestTypeDef",
    {
        "resourceArn": str,
        "statementId": str,
    },
)
_OptionalDeleteResourcePolicyStatementRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteResourcePolicyStatementRequestRequestTypeDef",
    {
        "expectedRevisionId": str,
    },
    total=False,
)

class DeleteResourcePolicyStatementRequestRequestTypeDef(
    _RequiredDeleteResourcePolicyStatementRequestRequestTypeDef,
    _OptionalDeleteResourcePolicyStatementRequestRequestTypeDef,
):
    pass

DeleteSlotRequestRequestTypeDef = TypedDict(
    "DeleteSlotRequestRequestTypeDef",
    {
        "slotId": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "intentId": str,
    },
)

_RequiredDeleteSlotTypeRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSlotTypeRequestRequestTypeDef",
    {
        "slotTypeId": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalDeleteSlotTypeRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSlotTypeRequestRequestTypeDef",
    {
        "skipResourceInUseCheck": bool,
    },
    total=False,
)

class DeleteSlotTypeRequestRequestTypeDef(
    _RequiredDeleteSlotTypeRequestRequestTypeDef, _OptionalDeleteSlotTypeRequestRequestTypeDef
):
    pass

DeleteTestSetRequestRequestTypeDef = TypedDict(
    "DeleteTestSetRequestRequestTypeDef",
    {
        "testSetId": str,
    },
)

_RequiredDeleteUtterancesRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteUtterancesRequestRequestTypeDef",
    {
        "botId": str,
    },
)
_OptionalDeleteUtterancesRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteUtterancesRequestRequestTypeDef",
    {
        "localeId": str,
        "sessionId": str,
    },
    total=False,
)

class DeleteUtterancesRequestRequestTypeDef(
    _RequiredDeleteUtterancesRequestRequestTypeDef, _OptionalDeleteUtterancesRequestRequestTypeDef
):
    pass

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeBotAliasRequestRequestTypeDef = TypedDict(
    "DescribeBotAliasRequestRequestTypeDef",
    {
        "botAliasId": str,
        "botId": str,
    },
)

ParentBotNetworkTypeDef = TypedDict(
    "ParentBotNetworkTypeDef",
    {
        "botId": str,
        "botVersion": str,
    },
)

DescribeBotLocaleRequestRequestTypeDef = TypedDict(
    "DescribeBotLocaleRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

DescribeBotRecommendationRequestRequestTypeDef = TypedDict(
    "DescribeBotRecommendationRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationId": str,
    },
)

EncryptionSettingTypeDef = TypedDict(
    "EncryptionSettingTypeDef",
    {
        "kmsKeyArn": str,
        "botLocaleExportPassword": str,
        "associatedTranscriptsPassword": str,
    },
    total=False,
)

DescribeBotRequestRequestTypeDef = TypedDict(
    "DescribeBotRequestRequestTypeDef",
    {
        "botId": str,
    },
)

DescribeBotVersionRequestRequestTypeDef = TypedDict(
    "DescribeBotVersionRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
    },
)

DescribeCustomVocabularyMetadataRequestRequestTypeDef = TypedDict(
    "DescribeCustomVocabularyMetadataRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

DescribeExportRequestRequestTypeDef = TypedDict(
    "DescribeExportRequestRequestTypeDef",
    {
        "exportId": str,
    },
)

DescribeImportRequestRequestTypeDef = TypedDict(
    "DescribeImportRequestRequestTypeDef",
    {
        "importId": str,
    },
)

DescribeIntentRequestRequestTypeDef = TypedDict(
    "DescribeIntentRequestRequestTypeDef",
    {
        "intentId": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

SlotPriorityTypeDef = TypedDict(
    "SlotPriorityTypeDef",
    {
        "priority": int,
        "slotId": str,
    },
)

DescribeResourcePolicyRequestRequestTypeDef = TypedDict(
    "DescribeResourcePolicyRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

DescribeSlotRequestRequestTypeDef = TypedDict(
    "DescribeSlotRequestRequestTypeDef",
    {
        "slotId": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "intentId": str,
    },
)

DescribeSlotTypeRequestRequestTypeDef = TypedDict(
    "DescribeSlotTypeRequestRequestTypeDef",
    {
        "slotTypeId": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)

DescribeTestExecutionRequestRequestTypeDef = TypedDict(
    "DescribeTestExecutionRequestRequestTypeDef",
    {
        "testExecutionId": str,
    },
)

DescribeTestSetDiscrepancyReportRequestRequestTypeDef = TypedDict(
    "DescribeTestSetDiscrepancyReportRequestRequestTypeDef",
    {
        "testSetDiscrepancyReportId": str,
    },
)

DescribeTestSetGenerationRequestRequestTypeDef = TypedDict(
    "DescribeTestSetGenerationRequestRequestTypeDef",
    {
        "testSetGenerationId": str,
    },
)

_RequiredTestSetStorageLocationTypeDef = TypedDict(
    "_RequiredTestSetStorageLocationTypeDef",
    {
        "s3BucketName": str,
        "s3Path": str,
    },
)
_OptionalTestSetStorageLocationTypeDef = TypedDict(
    "_OptionalTestSetStorageLocationTypeDef",
    {
        "kmsKeyArn": str,
    },
    total=False,
)

class TestSetStorageLocationTypeDef(
    _RequiredTestSetStorageLocationTypeDef, _OptionalTestSetStorageLocationTypeDef
):
    pass

DescribeTestSetRequestRequestTypeDef = TypedDict(
    "DescribeTestSetRequestRequestTypeDef",
    {
        "testSetId": str,
    },
)

_RequiredDialogActionTypeDef = TypedDict(
    "_RequiredDialogActionTypeDef",
    {
        "type": DialogActionTypeType,
    },
)
_OptionalDialogActionTypeDef = TypedDict(
    "_OptionalDialogActionTypeDef",
    {
        "slotToElicit": str,
        "suppressNextMessage": bool,
    },
    total=False,
)

class DialogActionTypeDef(_RequiredDialogActionTypeDef, _OptionalDialogActionTypeDef):
    pass

IntentOverrideTypeDef = TypedDict(
    "IntentOverrideTypeDef",
    {
        "name": str,
        "slots": Mapping[str, "SlotValueOverrideTypeDef"],
    },
    total=False,
)

_RequiredElicitationCodeHookInvocationSettingTypeDef = TypedDict(
    "_RequiredElicitationCodeHookInvocationSettingTypeDef",
    {
        "enableCodeHookInvocation": bool,
    },
)
_OptionalElicitationCodeHookInvocationSettingTypeDef = TypedDict(
    "_OptionalElicitationCodeHookInvocationSettingTypeDef",
    {
        "invocationLabel": str,
    },
    total=False,
)

class ElicitationCodeHookInvocationSettingTypeDef(
    _RequiredElicitationCodeHookInvocationSettingTypeDef,
    _OptionalElicitationCodeHookInvocationSettingTypeDef,
):
    pass

ExportFilterTypeDef = TypedDict(
    "ExportFilterTypeDef",
    {
        "name": Literal["ExportResourceType"],
        "values": Sequence[str],
        "operator": ExportFilterOperatorType,
    },
)

TestSetExportSpecificationTypeDef = TypedDict(
    "TestSetExportSpecificationTypeDef",
    {
        "testSetId": str,
    },
)

ExportSortByTypeDef = TypedDict(
    "ExportSortByTypeDef",
    {
        "attribute": Literal["LastUpdatedDateTime"],
        "order": SortOrderType,
    },
)

GetTestExecutionArtifactsUrlRequestRequestTypeDef = TypedDict(
    "GetTestExecutionArtifactsUrlRequestRequestTypeDef",
    {
        "testExecutionId": str,
    },
)

_RequiredGrammarSlotTypeSourceTypeDef = TypedDict(
    "_RequiredGrammarSlotTypeSourceTypeDef",
    {
        "s3BucketName": str,
        "s3ObjectKey": str,
    },
)
_OptionalGrammarSlotTypeSourceTypeDef = TypedDict(
    "_OptionalGrammarSlotTypeSourceTypeDef",
    {
        "kmsKeyArn": str,
    },
    total=False,
)

class GrammarSlotTypeSourceTypeDef(
    _RequiredGrammarSlotTypeSourceTypeDef, _OptionalGrammarSlotTypeSourceTypeDef
):
    pass

ImportFilterTypeDef = TypedDict(
    "ImportFilterTypeDef",
    {
        "name": Literal["ImportResourceType"],
        "values": Sequence[str],
        "operator": ImportFilterOperatorType,
    },
)

ImportSortByTypeDef = TypedDict(
    "ImportSortByTypeDef",
    {
        "attribute": Literal["LastUpdatedDateTime"],
        "order": SortOrderType,
    },
)

ImportSummaryTypeDef = TypedDict(
    "ImportSummaryTypeDef",
    {
        "importId": str,
        "importedResourceId": str,
        "importedResourceName": str,
        "importStatus": ImportStatusType,
        "mergeStrategy": MergeStrategyType,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "importedResourceType": ImportResourceTypeType,
    },
    total=False,
)

RuntimeHintsTypeDef = TypedDict(
    "RuntimeHintsTypeDef",
    {
        "slotHints": Dict[str, Dict[str, "RuntimeHintDetailsTypeDef"]],
    },
    total=False,
)

_RequiredIntentClassificationTestResultItemCountsTypeDef = TypedDict(
    "_RequiredIntentClassificationTestResultItemCountsTypeDef",
    {
        "totalResultCount": int,
        "intentMatchResultCounts": Dict[TestResultMatchStatusType, int],
    },
)
_OptionalIntentClassificationTestResultItemCountsTypeDef = TypedDict(
    "_OptionalIntentClassificationTestResultItemCountsTypeDef",
    {
        "speechTranscriptionResultCounts": Dict[TestResultMatchStatusType, int],
    },
    total=False,
)

class IntentClassificationTestResultItemCountsTypeDef(
    _RequiredIntentClassificationTestResultItemCountsTypeDef,
    _OptionalIntentClassificationTestResultItemCountsTypeDef,
):
    pass

IntentFilterTypeDef = TypedDict(
    "IntentFilterTypeDef",
    {
        "name": Literal["IntentName"],
        "values": Sequence[str],
        "operator": IntentFilterOperatorType,
    },
)

IntentSortByTypeDef = TypedDict(
    "IntentSortByTypeDef",
    {
        "attribute": IntentSortAttributeType,
        "order": SortOrderType,
    },
)

InvokedIntentSampleTypeDef = TypedDict(
    "InvokedIntentSampleTypeDef",
    {
        "intentName": str,
    },
    total=False,
)

_RequiredListBotAliasesRequestRequestTypeDef = TypedDict(
    "_RequiredListBotAliasesRequestRequestTypeDef",
    {
        "botId": str,
    },
)
_OptionalListBotAliasesRequestRequestTypeDef = TypedDict(
    "_OptionalListBotAliasesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListBotAliasesRequestRequestTypeDef(
    _RequiredListBotAliasesRequestRequestTypeDef, _OptionalListBotAliasesRequestRequestTypeDef
):
    pass

_RequiredListBotRecommendationsRequestRequestTypeDef = TypedDict(
    "_RequiredListBotRecommendationsRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalListBotRecommendationsRequestRequestTypeDef = TypedDict(
    "_OptionalListBotRecommendationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListBotRecommendationsRequestRequestTypeDef(
    _RequiredListBotRecommendationsRequestRequestTypeDef,
    _OptionalListBotRecommendationsRequestRequestTypeDef,
):
    pass

_RequiredListCustomVocabularyItemsRequestRequestTypeDef = TypedDict(
    "_RequiredListCustomVocabularyItemsRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalListCustomVocabularyItemsRequestRequestTypeDef = TypedDict(
    "_OptionalListCustomVocabularyItemsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListCustomVocabularyItemsRequestRequestTypeDef(
    _RequiredListCustomVocabularyItemsRequestRequestTypeDef,
    _OptionalListCustomVocabularyItemsRequestRequestTypeDef,
):
    pass

TimestampTypeDef = Union[datetime, str]
_RequiredListRecommendedIntentsRequestRequestTypeDef = TypedDict(
    "_RequiredListRecommendedIntentsRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationId": str,
    },
)
_OptionalListRecommendedIntentsRequestRequestTypeDef = TypedDict(
    "_OptionalListRecommendedIntentsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListRecommendedIntentsRequestRequestTypeDef(
    _RequiredListRecommendedIntentsRequestRequestTypeDef,
    _OptionalListRecommendedIntentsRequestRequestTypeDef,
):
    pass

RecommendedIntentSummaryTypeDef = TypedDict(
    "RecommendedIntentSummaryTypeDef",
    {
        "intentId": str,
        "intentName": str,
        "sampleUtterancesCount": int,
    },
    total=False,
)

SessionDataSortByTypeDef = TypedDict(
    "SessionDataSortByTypeDef",
    {
        "name": AnalyticsSessionSortByNameType,
        "order": AnalyticsSortOrderType,
    },
)

SlotTypeFilterTypeDef = TypedDict(
    "SlotTypeFilterTypeDef",
    {
        "name": SlotTypeFilterNameType,
        "values": Sequence[str],
        "operator": SlotTypeFilterOperatorType,
    },
)

SlotTypeSortByTypeDef = TypedDict(
    "SlotTypeSortByTypeDef",
    {
        "attribute": SlotTypeSortAttributeType,
        "order": SortOrderType,
    },
)

SlotTypeSummaryTypeDef = TypedDict(
    "SlotTypeSummaryTypeDef",
    {
        "slotTypeId": str,
        "slotTypeName": str,
        "description": str,
        "parentSlotTypeSignature": str,
        "lastUpdatedDateTime": datetime,
        "slotTypeCategory": SlotTypeCategoryType,
    },
    total=False,
)

SlotFilterTypeDef = TypedDict(
    "SlotFilterTypeDef",
    {
        "name": Literal["SlotName"],
        "values": Sequence[str],
        "operator": SlotFilterOperatorType,
    },
)

SlotSortByTypeDef = TypedDict(
    "SlotSortByTypeDef",
    {
        "attribute": SlotSortAttributeType,
        "order": SortOrderType,
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
    },
)

TestExecutionSortByTypeDef = TypedDict(
    "TestExecutionSortByTypeDef",
    {
        "attribute": TestExecutionSortAttributeType,
        "order": SortOrderType,
    },
)

_RequiredListTestSetRecordsRequestRequestTypeDef = TypedDict(
    "_RequiredListTestSetRecordsRequestRequestTypeDef",
    {
        "testSetId": str,
    },
)
_OptionalListTestSetRecordsRequestRequestTypeDef = TypedDict(
    "_OptionalListTestSetRecordsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListTestSetRecordsRequestRequestTypeDef(
    _RequiredListTestSetRecordsRequestRequestTypeDef,
    _OptionalListTestSetRecordsRequestRequestTypeDef,
):
    pass

TestSetSortByTypeDef = TypedDict(
    "TestSetSortByTypeDef",
    {
        "attribute": TestSetSortAttributeType,
        "order": SortOrderType,
    },
)

UtteranceDataSortByTypeDef = TypedDict(
    "UtteranceDataSortByTypeDef",
    {
        "name": Literal["UtteranceTimestamp"],
        "order": AnalyticsSortOrderType,
    },
)

PlainTextMessageTypeDef = TypedDict(
    "PlainTextMessageTypeDef",
    {
        "value": str,
    },
)

SSMLMessageTypeDef = TypedDict(
    "SSMLMessageTypeDef",
    {
        "value": str,
    },
)

_RequiredOverallTestResultItemTypeDef = TypedDict(
    "_RequiredOverallTestResultItemTypeDef",
    {
        "multiTurnConversation": bool,
        "totalResultCount": int,
        "endToEndResultCounts": Dict[TestResultMatchStatusType, int],
    },
)
_OptionalOverallTestResultItemTypeDef = TypedDict(
    "_OptionalOverallTestResultItemTypeDef",
    {
        "speechTranscriptionResultCounts": Dict[TestResultMatchStatusType, int],
    },
    total=False,
)

class OverallTestResultItemTypeDef(
    _RequiredOverallTestResultItemTypeDef, _OptionalOverallTestResultItemTypeDef
):
    pass

PathFormatTypeDef = TypedDict(
    "PathFormatTypeDef",
    {
        "objectPrefixes": List[str],
    },
    total=False,
)

TextInputSpecificationTypeDef = TypedDict(
    "TextInputSpecificationTypeDef",
    {
        "startTimeoutMs": int,
    },
)

RelativeAggregationDurationTypeDef = TypedDict(
    "RelativeAggregationDurationTypeDef",
    {
        "timeDimension": TimeDimensionType,
        "timeValue": int,
    },
)

RuntimeHintValueTypeDef = TypedDict(
    "RuntimeHintValueTypeDef",
    {
        "phrase": str,
    },
)

SampleValueTypeDef = TypedDict(
    "SampleValueTypeDef",
    {
        "value": str,
    },
)

SlotDefaultValueTypeDef = TypedDict(
    "SlotDefaultValueTypeDef",
    {
        "defaultValue": str,
    },
)

_RequiredSlotResolutionTestResultItemCountsTypeDef = TypedDict(
    "_RequiredSlotResolutionTestResultItemCountsTypeDef",
    {
        "totalResultCount": int,
        "slotMatchResultCounts": Dict[TestResultMatchStatusType, int],
    },
)
_OptionalSlotResolutionTestResultItemCountsTypeDef = TypedDict(
    "_OptionalSlotResolutionTestResultItemCountsTypeDef",
    {
        "speechTranscriptionResultCounts": Dict[TestResultMatchStatusType, int],
    },
    total=False,
)

class SlotResolutionTestResultItemCountsTypeDef(
    _RequiredSlotResolutionTestResultItemCountsTypeDef,
    _OptionalSlotResolutionTestResultItemCountsTypeDef,
):
    pass

SlotValueTypeDef = TypedDict(
    "SlotValueTypeDef",
    {
        "interpretedValue": str,
    },
    total=False,
)

SlotValueRegexFilterTypeDef = TypedDict(
    "SlotValueRegexFilterTypeDef",
    {
        "pattern": str,
    },
)

StopBotRecommendationRequestRequestTypeDef = TypedDict(
    "StopBotRecommendationRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationId": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
        "tags": Mapping[str, str],
    },
)

TestSetIntentDiscrepancyItemTypeDef = TypedDict(
    "TestSetIntentDiscrepancyItemTypeDef",
    {
        "intentName": str,
        "errorMessage": str,
    },
)

TestSetSlotDiscrepancyItemTypeDef = TypedDict(
    "TestSetSlotDiscrepancyItemTypeDef",
    {
        "intentName": str,
        "slotName": str,
        "errorMessage": str,
    },
)

TestSetDiscrepancyReportBotAliasTargetTypeDef = TypedDict(
    "TestSetDiscrepancyReportBotAliasTargetTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
    },
)

TestSetImportInputLocationTypeDef = TypedDict(
    "TestSetImportInputLocationTypeDef",
    {
        "s3BucketName": str,
        "s3Path": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateExportRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateExportRequestRequestTypeDef",
    {
        "exportId": str,
    },
)
_OptionalUpdateExportRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateExportRequestRequestTypeDef",
    {
        "filePassword": str,
    },
    total=False,
)

class UpdateExportRequestRequestTypeDef(
    _RequiredUpdateExportRequestRequestTypeDef, _OptionalUpdateExportRequestRequestTypeDef
):
    pass

_RequiredUpdateResourcePolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateResourcePolicyRequestRequestTypeDef",
    {
        "resourceArn": str,
        "policy": str,
    },
)
_OptionalUpdateResourcePolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateResourcePolicyRequestRequestTypeDef",
    {
        "expectedRevisionId": str,
    },
    total=False,
)

class UpdateResourcePolicyRequestRequestTypeDef(
    _RequiredUpdateResourcePolicyRequestRequestTypeDef,
    _OptionalUpdateResourcePolicyRequestRequestTypeDef,
):
    pass

_RequiredUpdateTestSetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTestSetRequestRequestTypeDef",
    {
        "testSetId": str,
        "testSetName": str,
    },
)
_OptionalUpdateTestSetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTestSetRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)

class UpdateTestSetRequestRequestTypeDef(
    _RequiredUpdateTestSetRequestRequestTypeDef, _OptionalUpdateTestSetRequestRequestTypeDef
):
    pass

_RequiredUserTurnIntentOutputTypeDef = TypedDict(
    "_RequiredUserTurnIntentOutputTypeDef",
    {
        "name": str,
    },
)
_OptionalUserTurnIntentOutputTypeDef = TypedDict(
    "_OptionalUserTurnIntentOutputTypeDef",
    {
        "slots": Dict[str, "UserTurnSlotOutputTypeDef"],
    },
    total=False,
)

class UserTurnIntentOutputTypeDef(
    _RequiredUserTurnIntentOutputTypeDef, _OptionalUserTurnIntentOutputTypeDef
):
    pass

UserTurnSlotOutputTypeDef = TypedDict(
    "UserTurnSlotOutputTypeDef",
    {
        "value": str,
        "values": List[Dict[str, Any]],
        "subSlots": Dict[str, Dict[str, Any]],
    },
    total=False,
)

UtteranceAudioInputSpecificationTypeDef = TypedDict(
    "UtteranceAudioInputSpecificationTypeDef",
    {
        "audioFileS3Location": str,
    },
)

_RequiredAgentTurnResultTypeDef = TypedDict(
    "_RequiredAgentTurnResultTypeDef",
    {
        "expectedAgentPrompt": str,
    },
)
_OptionalAgentTurnResultTypeDef = TypedDict(
    "_OptionalAgentTurnResultTypeDef",
    {
        "actualAgentPrompt": str,
        "errorDetails": ExecutionErrorDetailsTypeDef,
        "actualElicitedSlot": str,
        "actualIntent": str,
    },
    total=False,
)

class AgentTurnResultTypeDef(_RequiredAgentTurnResultTypeDef, _OptionalAgentTurnResultTypeDef):
    pass

AnalyticsIntentResultTypeDef = TypedDict(
    "AnalyticsIntentResultTypeDef",
    {
        "binKeys": List[AnalyticsBinKeyTypeDef],
        "groupByKeys": List[AnalyticsIntentGroupByKeyTypeDef],
        "metricsResults": List[AnalyticsIntentMetricResultTypeDef],
    },
    total=False,
)

AnalyticsIntentStageResultTypeDef = TypedDict(
    "AnalyticsIntentStageResultTypeDef",
    {
        "binKeys": List[AnalyticsBinKeyTypeDef],
        "groupByKeys": List[AnalyticsIntentStageGroupByKeyTypeDef],
        "metricsResults": List[AnalyticsIntentStageMetricResultTypeDef],
    },
    total=False,
)

AnalyticsSessionResultTypeDef = TypedDict(
    "AnalyticsSessionResultTypeDef",
    {
        "binKeys": List[AnalyticsBinKeyTypeDef],
        "groupByKeys": List[AnalyticsSessionGroupByKeyTypeDef],
        "metricsResults": List[AnalyticsSessionMetricResultTypeDef],
    },
    total=False,
)

AnalyticsUtteranceResultTypeDef = TypedDict(
    "AnalyticsUtteranceResultTypeDef",
    {
        "binKeys": List[AnalyticsBinKeyTypeDef],
        "groupByKeys": List[AnalyticsUtteranceGroupByKeyTypeDef],
        "metricsResults": List[AnalyticsUtteranceMetricResultTypeDef],
        "attributeResults": List[AnalyticsUtteranceAttributeResultTypeDef],
    },
    total=False,
)

_RequiredSearchAssociatedTranscriptsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchAssociatedTranscriptsRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationId": str,
        "filters": Sequence[AssociatedTranscriptFilterTypeDef],
    },
)
_OptionalSearchAssociatedTranscriptsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchAssociatedTranscriptsRequestRequestTypeDef",
    {
        "searchOrder": SearchOrderType,
        "maxResults": int,
        "nextIndex": int,
    },
    total=False,
)

class SearchAssociatedTranscriptsRequestRequestTypeDef(
    _RequiredSearchAssociatedTranscriptsRequestRequestTypeDef,
    _OptionalSearchAssociatedTranscriptsRequestRequestTypeDef,
):
    pass

_RequiredAudioAndDTMFInputSpecificationTypeDef = TypedDict(
    "_RequiredAudioAndDTMFInputSpecificationTypeDef",
    {
        "startTimeoutMs": int,
    },
)
_OptionalAudioAndDTMFInputSpecificationTypeDef = TypedDict(
    "_OptionalAudioAndDTMFInputSpecificationTypeDef",
    {
        "audioSpecification": AudioSpecificationTypeDef,
        "dtmfSpecification": DTMFSpecificationTypeDef,
    },
    total=False,
)

class AudioAndDTMFInputSpecificationTypeDef(
    _RequiredAudioAndDTMFInputSpecificationTypeDef, _OptionalAudioAndDTMFInputSpecificationTypeDef
):
    pass

AudioLogDestinationTypeDef = TypedDict(
    "AudioLogDestinationTypeDef",
    {
        "s3Bucket": S3BucketLogDestinationTypeDef,
    },
)

BatchCreateCustomVocabularyItemRequestRequestTypeDef = TypedDict(
    "BatchCreateCustomVocabularyItemRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "customVocabularyItemList": Sequence[NewCustomVocabularyItemTypeDef],
    },
)

BatchUpdateCustomVocabularyItemRequestRequestTypeDef = TypedDict(
    "BatchUpdateCustomVocabularyItemRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "customVocabularyItemList": Sequence[CustomVocabularyItemTypeDef],
    },
)

BatchCreateCustomVocabularyItemResponseTypeDef = TypedDict(
    "BatchCreateCustomVocabularyItemResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "errors": List[FailedCustomVocabularyItemTypeDef],
        "resources": List[CustomVocabularyItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteCustomVocabularyItemResponseTypeDef = TypedDict(
    "BatchDeleteCustomVocabularyItemResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "errors": List[FailedCustomVocabularyItemTypeDef],
        "resources": List[CustomVocabularyItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateCustomVocabularyItemResponseTypeDef = TypedDict(
    "BatchUpdateCustomVocabularyItemResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "errors": List[FailedCustomVocabularyItemTypeDef],
        "resources": List[CustomVocabularyItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BuildBotLocaleResponseTypeDef = TypedDict(
    "BuildBotLocaleResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botLocaleStatus": BotLocaleStatusType,
        "lastBuildSubmittedDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateResourcePolicyResponseTypeDef = TypedDict(
    "CreateResourcePolicyResponseTypeDef",
    {
        "resourceArn": str,
        "revisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateResourcePolicyStatementResponseTypeDef = TypedDict(
    "CreateResourcePolicyStatementResponseTypeDef",
    {
        "resourceArn": str,
        "revisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateUploadUrlResponseTypeDef = TypedDict(
    "CreateUploadUrlResponseTypeDef",
    {
        "importId": str,
        "uploadUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBotAliasResponseTypeDef = TypedDict(
    "DeleteBotAliasResponseTypeDef",
    {
        "botAliasId": str,
        "botId": str,
        "botAliasStatus": BotAliasStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBotLocaleResponseTypeDef = TypedDict(
    "DeleteBotLocaleResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botLocaleStatus": BotLocaleStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBotResponseTypeDef = TypedDict(
    "DeleteBotResponseTypeDef",
    {
        "botId": str,
        "botStatus": BotStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBotVersionResponseTypeDef = TypedDict(
    "DeleteBotVersionResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "botStatus": BotStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCustomVocabularyResponseTypeDef = TypedDict(
    "DeleteCustomVocabularyResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "customVocabularyStatus": CustomVocabularyStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteExportResponseTypeDef = TypedDict(
    "DeleteExportResponseTypeDef",
    {
        "exportId": str,
        "exportStatus": ExportStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteImportResponseTypeDef = TypedDict(
    "DeleteImportResponseTypeDef",
    {
        "importId": str,
        "importStatus": ImportStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteResourcePolicyResponseTypeDef = TypedDict(
    "DeleteResourcePolicyResponseTypeDef",
    {
        "resourceArn": str,
        "revisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteResourcePolicyStatementResponseTypeDef = TypedDict(
    "DeleteResourcePolicyStatementResponseTypeDef",
    {
        "resourceArn": str,
        "revisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCustomVocabularyMetadataResponseTypeDef = TypedDict(
    "DescribeCustomVocabularyMetadataResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "customVocabularyStatus": CustomVocabularyStatusType,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeResourcePolicyResponseTypeDef = TypedDict(
    "DescribeResourcePolicyResponseTypeDef",
    {
        "resourceArn": str,
        "policy": str,
        "revisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTestExecutionArtifactsUrlResponseTypeDef = TypedDict(
    "GetTestExecutionArtifactsUrlResponseTypeDef",
    {
        "testExecutionId": str,
        "downloadArtifactsUrl": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomVocabularyItemsResponseTypeDef = TypedDict(
    "ListCustomVocabularyItemsResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "customVocabularyItems": List[CustomVocabularyItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIntentPathsResponseTypeDef = TypedDict(
    "ListIntentPathsResponseTypeDef",
    {
        "nodeSummaries": List[AnalyticsIntentNodeSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchAssociatedTranscriptsResponseTypeDef = TypedDict(
    "SearchAssociatedTranscriptsResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationId": str,
        "nextIndex": int,
        "associatedTranscripts": List[AssociatedTranscriptTypeDef],
        "totalResults": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopBotRecommendationResponseTypeDef = TypedDict(
    "StopBotRecommendationResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationStatus": BotRecommendationStatusType,
        "botRecommendationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateResourcePolicyResponseTypeDef = TypedDict(
    "UpdateResourcePolicyResponseTypeDef",
    {
        "resourceArn": str,
        "revisionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteCustomVocabularyItemRequestRequestTypeDef = TypedDict(
    "BatchDeleteCustomVocabularyItemRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "customVocabularyItemList": Sequence[CustomVocabularyEntryIdTypeDef],
    },
)

ListBotAliasesResponseTypeDef = TypedDict(
    "ListBotAliasesResponseTypeDef",
    {
        "botAliasSummaries": List[BotAliasSummaryTypeDef],
        "nextToken": str,
        "botId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TestExecutionTargetTypeDef = TypedDict(
    "TestExecutionTargetTypeDef",
    {
        "botAliasTarget": BotAliasTestExecutionTargetTypeDef,
    },
    total=False,
)

_RequiredBotImportSpecificationTypeDef = TypedDict(
    "_RequiredBotImportSpecificationTypeDef",
    {
        "botName": str,
        "roleArn": str,
        "dataPrivacy": DataPrivacyTypeDef,
    },
)
_OptionalBotImportSpecificationTypeDef = TypedDict(
    "_OptionalBotImportSpecificationTypeDef",
    {
        "idleSessionTTLInSeconds": int,
        "botTags": Dict[str, str],
        "testBotAliasTags": Dict[str, str],
    },
    total=False,
)

class BotImportSpecificationTypeDef(
    _RequiredBotImportSpecificationTypeDef, _OptionalBotImportSpecificationTypeDef
):
    pass

_RequiredBotLocaleImportSpecificationTypeDef = TypedDict(
    "_RequiredBotLocaleImportSpecificationTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalBotLocaleImportSpecificationTypeDef = TypedDict(
    "_OptionalBotLocaleImportSpecificationTypeDef",
    {
        "nluIntentConfidenceThreshold": float,
        "voiceSettings": VoiceSettingsTypeDef,
    },
    total=False,
)

class BotLocaleImportSpecificationTypeDef(
    _RequiredBotLocaleImportSpecificationTypeDef, _OptionalBotLocaleImportSpecificationTypeDef
):
    pass

_RequiredCreateBotLocaleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBotLocaleRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "nluIntentConfidenceThreshold": float,
    },
)
_OptionalCreateBotLocaleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBotLocaleRequestRequestTypeDef",
    {
        "description": str,
        "voiceSettings": VoiceSettingsTypeDef,
    },
    total=False,
)

class CreateBotLocaleRequestRequestTypeDef(
    _RequiredCreateBotLocaleRequestRequestTypeDef, _OptionalCreateBotLocaleRequestRequestTypeDef
):
    pass

CreateBotLocaleResponseTypeDef = TypedDict(
    "CreateBotLocaleResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeName": str,
        "localeId": str,
        "description": str,
        "nluIntentConfidenceThreshold": float,
        "voiceSettings": VoiceSettingsTypeDef,
        "botLocaleStatus": BotLocaleStatusType,
        "creationDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBotLocaleResponseTypeDef = TypedDict(
    "DescribeBotLocaleResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "localeName": str,
        "description": str,
        "nluIntentConfidenceThreshold": float,
        "voiceSettings": VoiceSettingsTypeDef,
        "intentsCount": int,
        "slotTypesCount": int,
        "botLocaleStatus": BotLocaleStatusType,
        "failureReasons": List[str],
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "lastBuildSubmittedDateTime": datetime,
        "botLocaleHistoryEvents": List[BotLocaleHistoryEventTypeDef],
        "recommendedActions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateBotLocaleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBotLocaleRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "nluIntentConfidenceThreshold": float,
    },
)
_OptionalUpdateBotLocaleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBotLocaleRequestRequestTypeDef",
    {
        "description": str,
        "voiceSettings": VoiceSettingsTypeDef,
    },
    total=False,
)

class UpdateBotLocaleRequestRequestTypeDef(
    _RequiredUpdateBotLocaleRequestRequestTypeDef, _OptionalUpdateBotLocaleRequestRequestTypeDef
):
    pass

UpdateBotLocaleResponseTypeDef = TypedDict(
    "UpdateBotLocaleResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "localeName": str,
        "description": str,
        "nluIntentConfidenceThreshold": float,
        "voiceSettings": VoiceSettingsTypeDef,
        "botLocaleStatus": BotLocaleStatusType,
        "failureReasons": List[str],
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "recommendedActions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListBotLocalesRequestRequestTypeDef = TypedDict(
    "_RequiredListBotLocalesRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
    },
)
_OptionalListBotLocalesRequestRequestTypeDef = TypedDict(
    "_OptionalListBotLocalesRequestRequestTypeDef",
    {
        "sortBy": BotLocaleSortByTypeDef,
        "filters": Sequence[BotLocaleFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListBotLocalesRequestRequestTypeDef(
    _RequiredListBotLocalesRequestRequestTypeDef, _OptionalListBotLocalesRequestRequestTypeDef
):
    pass

ListBotLocalesResponseTypeDef = TypedDict(
    "ListBotLocalesResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "nextToken": str,
        "botLocaleSummaries": List[BotLocaleSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateBotRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBotRequestRequestTypeDef",
    {
        "botName": str,
        "roleArn": str,
        "dataPrivacy": DataPrivacyTypeDef,
        "idleSessionTTLInSeconds": int,
    },
)
_OptionalCreateBotRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBotRequestRequestTypeDef",
    {
        "description": str,
        "botTags": Mapping[str, str],
        "testBotAliasTags": Mapping[str, str],
        "botType": BotTypeType,
        "botMembers": Sequence[BotMemberTypeDef],
    },
    total=False,
)

class CreateBotRequestRequestTypeDef(
    _RequiredCreateBotRequestRequestTypeDef, _OptionalCreateBotRequestRequestTypeDef
):
    pass

CreateBotResponseTypeDef = TypedDict(
    "CreateBotResponseTypeDef",
    {
        "botId": str,
        "botName": str,
        "description": str,
        "roleArn": str,
        "dataPrivacy": DataPrivacyTypeDef,
        "idleSessionTTLInSeconds": int,
        "botStatus": BotStatusType,
        "creationDateTime": datetime,
        "botTags": Dict[str, str],
        "testBotAliasTags": Dict[str, str],
        "botType": BotTypeType,
        "botMembers": List[BotMemberTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBotResponseTypeDef = TypedDict(
    "DescribeBotResponseTypeDef",
    {
        "botId": str,
        "botName": str,
        "description": str,
        "roleArn": str,
        "dataPrivacy": DataPrivacyTypeDef,
        "idleSessionTTLInSeconds": int,
        "botStatus": BotStatusType,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "botType": BotTypeType,
        "botMembers": List[BotMemberTypeDef],
        "failureReasons": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateBotRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBotRequestRequestTypeDef",
    {
        "botId": str,
        "botName": str,
        "roleArn": str,
        "dataPrivacy": DataPrivacyTypeDef,
        "idleSessionTTLInSeconds": int,
    },
)
_OptionalUpdateBotRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBotRequestRequestTypeDef",
    {
        "description": str,
        "botType": BotTypeType,
        "botMembers": Sequence[BotMemberTypeDef],
    },
    total=False,
)

class UpdateBotRequestRequestTypeDef(
    _RequiredUpdateBotRequestRequestTypeDef, _OptionalUpdateBotRequestRequestTypeDef
):
    pass

UpdateBotResponseTypeDef = TypedDict(
    "UpdateBotResponseTypeDef",
    {
        "botId": str,
        "botName": str,
        "description": str,
        "roleArn": str,
        "dataPrivacy": DataPrivacyTypeDef,
        "idleSessionTTLInSeconds": int,
        "botStatus": BotStatusType,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "botType": BotTypeType,
        "botMembers": List[BotMemberTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BotRecommendationResultStatisticsTypeDef = TypedDict(
    "BotRecommendationResultStatisticsTypeDef",
    {
        "intents": IntentStatisticsTypeDef,
        "slotTypes": SlotTypeStatisticsTypeDef,
    },
    total=False,
)

ListBotRecommendationsResponseTypeDef = TypedDict(
    "ListBotRecommendationsResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationSummaries": List[BotRecommendationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBotsRequestRequestTypeDef = TypedDict(
    "ListBotsRequestRequestTypeDef",
    {
        "sortBy": BotSortByTypeDef,
        "filters": Sequence[BotFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListBotsResponseTypeDef = TypedDict(
    "ListBotsResponseTypeDef",
    {
        "botSummaries": List[BotSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateBotVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBotVersionRequestRequestTypeDef",
    {
        "botId": str,
        "botVersionLocaleSpecification": Mapping[str, BotVersionLocaleDetailsTypeDef],
    },
)
_OptionalCreateBotVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBotVersionRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)

class CreateBotVersionRequestRequestTypeDef(
    _RequiredCreateBotVersionRequestRequestTypeDef, _OptionalCreateBotVersionRequestRequestTypeDef
):
    pass

CreateBotVersionResponseTypeDef = TypedDict(
    "CreateBotVersionResponseTypeDef",
    {
        "botId": str,
        "description": str,
        "botVersion": str,
        "botVersionLocaleSpecification": Dict[str, BotVersionLocaleDetailsTypeDef],
        "botStatus": BotStatusType,
        "creationDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListBotVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListBotVersionsRequestRequestTypeDef",
    {
        "botId": str,
    },
)
_OptionalListBotVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListBotVersionsRequestRequestTypeDef",
    {
        "sortBy": BotVersionSortByTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListBotVersionsRequestRequestTypeDef(
    _RequiredListBotVersionsRequestRequestTypeDef, _OptionalListBotVersionsRequestRequestTypeDef
):
    pass

ListBotVersionsResponseTypeDef = TypedDict(
    "ListBotVersionsResponseTypeDef",
    {
        "botId": str,
        "botVersionSummaries": List[BotVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListBuiltInIntentsRequestRequestTypeDef = TypedDict(
    "_RequiredListBuiltInIntentsRequestRequestTypeDef",
    {
        "localeId": str,
    },
)
_OptionalListBuiltInIntentsRequestRequestTypeDef = TypedDict(
    "_OptionalListBuiltInIntentsRequestRequestTypeDef",
    {
        "sortBy": BuiltInIntentSortByTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListBuiltInIntentsRequestRequestTypeDef(
    _RequiredListBuiltInIntentsRequestRequestTypeDef,
    _OptionalListBuiltInIntentsRequestRequestTypeDef,
):
    pass

ListBuiltInIntentsResponseTypeDef = TypedDict(
    "ListBuiltInIntentsResponseTypeDef",
    {
        "builtInIntentSummaries": List[BuiltInIntentSummaryTypeDef],
        "nextToken": str,
        "localeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListBuiltInSlotTypesRequestRequestTypeDef = TypedDict(
    "_RequiredListBuiltInSlotTypesRequestRequestTypeDef",
    {
        "localeId": str,
    },
)
_OptionalListBuiltInSlotTypesRequestRequestTypeDef = TypedDict(
    "_OptionalListBuiltInSlotTypesRequestRequestTypeDef",
    {
        "sortBy": BuiltInSlotTypeSortByTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListBuiltInSlotTypesRequestRequestTypeDef(
    _RequiredListBuiltInSlotTypesRequestRequestTypeDef,
    _OptionalListBuiltInSlotTypesRequestRequestTypeDef,
):
    pass

ListBuiltInSlotTypesResponseTypeDef = TypedDict(
    "ListBuiltInSlotTypesResponseTypeDef",
    {
        "builtInSlotTypeSummaries": List[BuiltInSlotTypeSummaryTypeDef],
        "nextToken": str,
        "localeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredImageResponseCardTypeDef = TypedDict(
    "_RequiredImageResponseCardTypeDef",
    {
        "title": str,
    },
)
_OptionalImageResponseCardTypeDef = TypedDict(
    "_OptionalImageResponseCardTypeDef",
    {
        "subtitle": str,
        "imageUrl": str,
        "buttons": Sequence[ButtonTypeDef],
    },
    total=False,
)

class ImageResponseCardTypeDef(
    _RequiredImageResponseCardTypeDef, _OptionalImageResponseCardTypeDef
):
    pass

TextLogDestinationTypeDef = TypedDict(
    "TextLogDestinationTypeDef",
    {
        "cloudWatch": CloudWatchLogGroupLogDestinationTypeDef,
    },
)

CodeHookSpecificationTypeDef = TypedDict(
    "CodeHookSpecificationTypeDef",
    {
        "lambdaCodeHook": LambdaCodeHookTypeDef,
    },
)

CompositeSlotTypeSettingTypeDef = TypedDict(
    "CompositeSlotTypeSettingTypeDef",
    {
        "subSlots": Sequence[SubSlotTypeCompositionTypeDef],
    },
    total=False,
)

_RequiredConversationLevelTestResultItemTypeDef = TypedDict(
    "_RequiredConversationLevelTestResultItemTypeDef",
    {
        "conversationId": str,
        "endToEndResult": TestResultMatchStatusType,
        "intentClassificationResults": List[ConversationLevelIntentClassificationResultItemTypeDef],
        "slotResolutionResults": List[ConversationLevelSlotResolutionResultItemTypeDef],
    },
)
_OptionalConversationLevelTestResultItemTypeDef = TypedDict(
    "_OptionalConversationLevelTestResultItemTypeDef",
    {
        "speechTranscriptionResult": TestResultMatchStatusType,
    },
    total=False,
)

class ConversationLevelTestResultItemTypeDef(
    _RequiredConversationLevelTestResultItemTypeDef, _OptionalConversationLevelTestResultItemTypeDef
):
    pass

_RequiredTestExecutionResultFilterByTypeDef = TypedDict(
    "_RequiredTestExecutionResultFilterByTypeDef",
    {
        "resultTypeFilter": TestResultTypeFilterType,
    },
)
_OptionalTestExecutionResultFilterByTypeDef = TypedDict(
    "_OptionalTestExecutionResultFilterByTypeDef",
    {
        "conversationLevelTestResultsFilterBy": ConversationLevelTestResultsFilterByTypeDef,
    },
    total=False,
)

class TestExecutionResultFilterByTypeDef(
    _RequiredTestExecutionResultFilterByTypeDef, _OptionalTestExecutionResultFilterByTypeDef
):
    pass

ConversationLogsDataSourceTypeDef = TypedDict(
    "ConversationLogsDataSourceTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "localeId": str,
        "filter": ConversationLogsDataSourceFilterByTypeDef,
    },
)

IntentSummaryTypeDef = TypedDict(
    "IntentSummaryTypeDef",
    {
        "intentId": str,
        "intentName": str,
        "description": str,
        "parentIntentSignature": str,
        "inputContexts": List[InputContextTypeDef],
        "outputContexts": List[OutputContextTypeDef],
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

_RequiredCreateResourcePolicyStatementRequestRequestTypeDef = TypedDict(
    "_RequiredCreateResourcePolicyStatementRequestRequestTypeDef",
    {
        "resourceArn": str,
        "statementId": str,
        "effect": EffectType,
        "principal": Sequence[PrincipalTypeDef],
        "action": Sequence[str],
    },
)
_OptionalCreateResourcePolicyStatementRequestRequestTypeDef = TypedDict(
    "_OptionalCreateResourcePolicyStatementRequestRequestTypeDef",
    {
        "condition": Mapping[str, Mapping[str, str]],
        "expectedRevisionId": str,
    },
    total=False,
)

class CreateResourcePolicyStatementRequestRequestTypeDef(
    _RequiredCreateResourcePolicyStatementRequestRequestTypeDef,
    _OptionalCreateResourcePolicyStatementRequestRequestTypeDef,
):
    pass

LexTranscriptFilterTypeDef = TypedDict(
    "LexTranscriptFilterTypeDef",
    {
        "dateRangeFilter": DateRangeFilterTypeDef,
    },
    total=False,
)

_RequiredDescribeBotAliasRequestBotAliasAvailableWaitTypeDef = TypedDict(
    "_RequiredDescribeBotAliasRequestBotAliasAvailableWaitTypeDef",
    {
        "botAliasId": str,
        "botId": str,
    },
)
_OptionalDescribeBotAliasRequestBotAliasAvailableWaitTypeDef = TypedDict(
    "_OptionalDescribeBotAliasRequestBotAliasAvailableWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeBotAliasRequestBotAliasAvailableWaitTypeDef(
    _RequiredDescribeBotAliasRequestBotAliasAvailableWaitTypeDef,
    _OptionalDescribeBotAliasRequestBotAliasAvailableWaitTypeDef,
):
    pass

_RequiredDescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef = TypedDict(
    "_RequiredDescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalDescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef = TypedDict(
    "_OptionalDescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef(
    _RequiredDescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef,
    _OptionalDescribeBotLocaleRequestBotLocaleBuiltWaitTypeDef,
):
    pass

_RequiredDescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef = TypedDict(
    "_RequiredDescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalDescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef = TypedDict(
    "_OptionalDescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef(
    _RequiredDescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef,
    _OptionalDescribeBotLocaleRequestBotLocaleCreatedWaitTypeDef,
):
    pass

_RequiredDescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef = TypedDict(
    "_RequiredDescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalDescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef = TypedDict(
    "_OptionalDescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef(
    _RequiredDescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef,
    _OptionalDescribeBotLocaleRequestBotLocaleExpressTestingAvailableWaitTypeDef,
):
    pass

_RequiredDescribeBotRequestBotAvailableWaitTypeDef = TypedDict(
    "_RequiredDescribeBotRequestBotAvailableWaitTypeDef",
    {
        "botId": str,
    },
)
_OptionalDescribeBotRequestBotAvailableWaitTypeDef = TypedDict(
    "_OptionalDescribeBotRequestBotAvailableWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeBotRequestBotAvailableWaitTypeDef(
    _RequiredDescribeBotRequestBotAvailableWaitTypeDef,
    _OptionalDescribeBotRequestBotAvailableWaitTypeDef,
):
    pass

_RequiredDescribeBotVersionRequestBotVersionAvailableWaitTypeDef = TypedDict(
    "_RequiredDescribeBotVersionRequestBotVersionAvailableWaitTypeDef",
    {
        "botId": str,
        "botVersion": str,
    },
)
_OptionalDescribeBotVersionRequestBotVersionAvailableWaitTypeDef = TypedDict(
    "_OptionalDescribeBotVersionRequestBotVersionAvailableWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeBotVersionRequestBotVersionAvailableWaitTypeDef(
    _RequiredDescribeBotVersionRequestBotVersionAvailableWaitTypeDef,
    _OptionalDescribeBotVersionRequestBotVersionAvailableWaitTypeDef,
):
    pass

_RequiredDescribeExportRequestBotExportCompletedWaitTypeDef = TypedDict(
    "_RequiredDescribeExportRequestBotExportCompletedWaitTypeDef",
    {
        "exportId": str,
    },
)
_OptionalDescribeExportRequestBotExportCompletedWaitTypeDef = TypedDict(
    "_OptionalDescribeExportRequestBotExportCompletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeExportRequestBotExportCompletedWaitTypeDef(
    _RequiredDescribeExportRequestBotExportCompletedWaitTypeDef,
    _OptionalDescribeExportRequestBotExportCompletedWaitTypeDef,
):
    pass

_RequiredDescribeImportRequestBotImportCompletedWaitTypeDef = TypedDict(
    "_RequiredDescribeImportRequestBotImportCompletedWaitTypeDef",
    {
        "importId": str,
    },
)
_OptionalDescribeImportRequestBotImportCompletedWaitTypeDef = TypedDict(
    "_OptionalDescribeImportRequestBotImportCompletedWaitTypeDef",
    {
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

class DescribeImportRequestBotImportCompletedWaitTypeDef(
    _RequiredDescribeImportRequestBotImportCompletedWaitTypeDef,
    _OptionalDescribeImportRequestBotImportCompletedWaitTypeDef,
):
    pass

DescribeBotVersionResponseTypeDef = TypedDict(
    "DescribeBotVersionResponseTypeDef",
    {
        "botId": str,
        "botName": str,
        "botVersion": str,
        "description": str,
        "roleArn": str,
        "dataPrivacy": DataPrivacyTypeDef,
        "idleSessionTTLInSeconds": int,
        "botStatus": BotStatusType,
        "failureReasons": List[str],
        "creationDateTime": datetime,
        "parentBotNetworks": List[ParentBotNetworkTypeDef],
        "botType": BotTypeType,
        "botMembers": List[BotMemberTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBotRecommendationRequestRequestTypeDef = TypedDict(
    "UpdateBotRecommendationRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationId": str,
        "encryptionSetting": EncryptionSettingTypeDef,
    },
)

DescribeTestSetResponseTypeDef = TypedDict(
    "DescribeTestSetResponseTypeDef",
    {
        "testSetId": str,
        "testSetName": str,
        "description": str,
        "modality": TestSetModalityType,
        "status": TestSetStatusType,
        "roleArn": str,
        "numTurns": int,
        "storageLocation": TestSetStorageLocationTypeDef,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TestSetSummaryTypeDef = TypedDict(
    "TestSetSummaryTypeDef",
    {
        "testSetId": str,
        "testSetName": str,
        "description": str,
        "modality": TestSetModalityType,
        "status": TestSetStatusType,
        "roleArn": str,
        "numTurns": int,
        "storageLocation": TestSetStorageLocationTypeDef,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

UpdateTestSetResponseTypeDef = TypedDict(
    "UpdateTestSetResponseTypeDef",
    {
        "testSetId": str,
        "testSetName": str,
        "description": str,
        "modality": TestSetModalityType,
        "status": TestSetStatusType,
        "roleArn": str,
        "numTurns": int,
        "storageLocation": TestSetStorageLocationTypeDef,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DialogStateTypeDef = TypedDict(
    "DialogStateTypeDef",
    {
        "dialogAction": DialogActionTypeDef,
        "intent": IntentOverrideTypeDef,
        "sessionAttributes": Mapping[str, str],
    },
    total=False,
)

ExportResourceSpecificationTypeDef = TypedDict(
    "ExportResourceSpecificationTypeDef",
    {
        "botExportSpecification": BotExportSpecificationTypeDef,
        "botLocaleExportSpecification": BotLocaleExportSpecificationTypeDef,
        "customVocabularyExportSpecification": CustomVocabularyExportSpecificationTypeDef,
        "testSetExportSpecification": TestSetExportSpecificationTypeDef,
    },
    total=False,
)

ListExportsRequestRequestTypeDef = TypedDict(
    "ListExportsRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "sortBy": ExportSortByTypeDef,
        "filters": Sequence[ExportFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
        "localeId": str,
    },
    total=False,
)

GrammarSlotTypeSettingTypeDef = TypedDict(
    "GrammarSlotTypeSettingTypeDef",
    {
        "source": GrammarSlotTypeSourceTypeDef,
    },
    total=False,
)

ListImportsRequestRequestTypeDef = TypedDict(
    "ListImportsRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "sortBy": ImportSortByTypeDef,
        "filters": Sequence[ImportFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
        "localeId": str,
    },
    total=False,
)

ListImportsResponseTypeDef = TypedDict(
    "ListImportsResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "importSummaries": List[ImportSummaryTypeDef],
        "nextToken": str,
        "localeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InputSessionStateSpecificationTypeDef = TypedDict(
    "InputSessionStateSpecificationTypeDef",
    {
        "sessionAttributes": Dict[str, str],
        "activeContexts": List[ActiveContextTypeDef],
        "runtimeHints": RuntimeHintsTypeDef,
    },
    total=False,
)

IntentClassificationTestResultItemTypeDef = TypedDict(
    "IntentClassificationTestResultItemTypeDef",
    {
        "intentName": str,
        "multiTurnConversation": bool,
        "resultCounts": IntentClassificationTestResultItemCountsTypeDef,
    },
)

_RequiredListIntentsRequestRequestTypeDef = TypedDict(
    "_RequiredListIntentsRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalListIntentsRequestRequestTypeDef = TypedDict(
    "_OptionalListIntentsRequestRequestTypeDef",
    {
        "sortBy": IntentSortByTypeDef,
        "filters": Sequence[IntentFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListIntentsRequestRequestTypeDef(
    _RequiredListIntentsRequestRequestTypeDef, _OptionalListIntentsRequestRequestTypeDef
):
    pass

SessionSpecificationTypeDef = TypedDict(
    "SessionSpecificationTypeDef",
    {
        "botAliasId": str,
        "botVersion": str,
        "localeId": str,
        "channel": str,
        "sessionId": str,
        "conversationStartTime": datetime,
        "conversationEndTime": datetime,
        "conversationDurationSeconds": int,
        "conversationEndState": ConversationEndStateType,
        "mode": AnalyticsModalityType,
        "numberOfTurns": int,
        "invokedIntentSamples": List[InvokedIntentSampleTypeDef],
        "originatingRequestId": str,
    },
    total=False,
)

_RequiredListIntentMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredListIntentMetricsRequestRequestTypeDef",
    {
        "botId": str,
        "startDateTime": TimestampTypeDef,
        "endDateTime": TimestampTypeDef,
        "metrics": Sequence[AnalyticsIntentMetricTypeDef],
    },
)
_OptionalListIntentMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalListIntentMetricsRequestRequestTypeDef",
    {
        "binBy": Sequence[AnalyticsBinBySpecificationTypeDef],
        "groupBy": Sequence[AnalyticsIntentGroupBySpecificationTypeDef],
        "filters": Sequence[AnalyticsIntentFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListIntentMetricsRequestRequestTypeDef(
    _RequiredListIntentMetricsRequestRequestTypeDef, _OptionalListIntentMetricsRequestRequestTypeDef
):
    pass

_RequiredListIntentPathsRequestRequestTypeDef = TypedDict(
    "_RequiredListIntentPathsRequestRequestTypeDef",
    {
        "botId": str,
        "startDateTime": TimestampTypeDef,
        "endDateTime": TimestampTypeDef,
        "intentPath": str,
    },
)
_OptionalListIntentPathsRequestRequestTypeDef = TypedDict(
    "_OptionalListIntentPathsRequestRequestTypeDef",
    {
        "filters": Sequence[AnalyticsPathFilterTypeDef],
    },
    total=False,
)

class ListIntentPathsRequestRequestTypeDef(
    _RequiredListIntentPathsRequestRequestTypeDef, _OptionalListIntentPathsRequestRequestTypeDef
):
    pass

_RequiredListIntentStageMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredListIntentStageMetricsRequestRequestTypeDef",
    {
        "botId": str,
        "startDateTime": TimestampTypeDef,
        "endDateTime": TimestampTypeDef,
        "metrics": Sequence[AnalyticsIntentStageMetricTypeDef],
    },
)
_OptionalListIntentStageMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalListIntentStageMetricsRequestRequestTypeDef",
    {
        "binBy": Sequence[AnalyticsBinBySpecificationTypeDef],
        "groupBy": Sequence[AnalyticsIntentStageGroupBySpecificationTypeDef],
        "filters": Sequence[AnalyticsIntentStageFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListIntentStageMetricsRequestRequestTypeDef(
    _RequiredListIntentStageMetricsRequestRequestTypeDef,
    _OptionalListIntentStageMetricsRequestRequestTypeDef,
):
    pass

_RequiredListSessionMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredListSessionMetricsRequestRequestTypeDef",
    {
        "botId": str,
        "startDateTime": TimestampTypeDef,
        "endDateTime": TimestampTypeDef,
        "metrics": Sequence[AnalyticsSessionMetricTypeDef],
    },
)
_OptionalListSessionMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalListSessionMetricsRequestRequestTypeDef",
    {
        "binBy": Sequence[AnalyticsBinBySpecificationTypeDef],
        "groupBy": Sequence[AnalyticsSessionGroupBySpecificationTypeDef],
        "filters": Sequence[AnalyticsSessionFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListSessionMetricsRequestRequestTypeDef(
    _RequiredListSessionMetricsRequestRequestTypeDef,
    _OptionalListSessionMetricsRequestRequestTypeDef,
):
    pass

_RequiredListUtteranceMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredListUtteranceMetricsRequestRequestTypeDef",
    {
        "botId": str,
        "startDateTime": TimestampTypeDef,
        "endDateTime": TimestampTypeDef,
        "metrics": Sequence[AnalyticsUtteranceMetricTypeDef],
    },
)
_OptionalListUtteranceMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalListUtteranceMetricsRequestRequestTypeDef",
    {
        "binBy": Sequence[AnalyticsBinBySpecificationTypeDef],
        "groupBy": Sequence[AnalyticsUtteranceGroupBySpecificationTypeDef],
        "attributes": Sequence[AnalyticsUtteranceAttributeTypeDef],
        "filters": Sequence[AnalyticsUtteranceFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListUtteranceMetricsRequestRequestTypeDef(
    _RequiredListUtteranceMetricsRequestRequestTypeDef,
    _OptionalListUtteranceMetricsRequestRequestTypeDef,
):
    pass

ListRecommendedIntentsResponseTypeDef = TypedDict(
    "ListRecommendedIntentsResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationId": str,
        "summaryList": List[RecommendedIntentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListSessionAnalyticsDataRequestRequestTypeDef = TypedDict(
    "_RequiredListSessionAnalyticsDataRequestRequestTypeDef",
    {
        "botId": str,
        "startDateTime": TimestampTypeDef,
        "endDateTime": TimestampTypeDef,
    },
)
_OptionalListSessionAnalyticsDataRequestRequestTypeDef = TypedDict(
    "_OptionalListSessionAnalyticsDataRequestRequestTypeDef",
    {
        "sortBy": SessionDataSortByTypeDef,
        "filters": Sequence[AnalyticsSessionFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListSessionAnalyticsDataRequestRequestTypeDef(
    _RequiredListSessionAnalyticsDataRequestRequestTypeDef,
    _OptionalListSessionAnalyticsDataRequestRequestTypeDef,
):
    pass

_RequiredListSlotTypesRequestRequestTypeDef = TypedDict(
    "_RequiredListSlotTypesRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalListSlotTypesRequestRequestTypeDef = TypedDict(
    "_OptionalListSlotTypesRequestRequestTypeDef",
    {
        "sortBy": SlotTypeSortByTypeDef,
        "filters": Sequence[SlotTypeFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListSlotTypesRequestRequestTypeDef(
    _RequiredListSlotTypesRequestRequestTypeDef, _OptionalListSlotTypesRequestRequestTypeDef
):
    pass

ListSlotTypesResponseTypeDef = TypedDict(
    "ListSlotTypesResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "slotTypeSummaries": List[SlotTypeSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListSlotsRequestRequestTypeDef = TypedDict(
    "_RequiredListSlotsRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "intentId": str,
    },
)
_OptionalListSlotsRequestRequestTypeDef = TypedDict(
    "_OptionalListSlotsRequestRequestTypeDef",
    {
        "sortBy": SlotSortByTypeDef,
        "filters": Sequence[SlotFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListSlotsRequestRequestTypeDef(
    _RequiredListSlotsRequestRequestTypeDef, _OptionalListSlotsRequestRequestTypeDef
):
    pass

ListTestExecutionsRequestRequestTypeDef = TypedDict(
    "ListTestExecutionsRequestRequestTypeDef",
    {
        "sortBy": TestExecutionSortByTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListTestSetsRequestRequestTypeDef = TypedDict(
    "ListTestSetsRequestRequestTypeDef",
    {
        "sortBy": TestSetSortByTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListUtteranceAnalyticsDataRequestRequestTypeDef = TypedDict(
    "_RequiredListUtteranceAnalyticsDataRequestRequestTypeDef",
    {
        "botId": str,
        "startDateTime": TimestampTypeDef,
        "endDateTime": TimestampTypeDef,
    },
)
_OptionalListUtteranceAnalyticsDataRequestRequestTypeDef = TypedDict(
    "_OptionalListUtteranceAnalyticsDataRequestRequestTypeDef",
    {
        "sortBy": UtteranceDataSortByTypeDef,
        "filters": Sequence[AnalyticsUtteranceFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListUtteranceAnalyticsDataRequestRequestTypeDef(
    _RequiredListUtteranceAnalyticsDataRequestRequestTypeDef,
    _OptionalListUtteranceAnalyticsDataRequestRequestTypeDef,
):
    pass

OverallTestResultsTypeDef = TypedDict(
    "OverallTestResultsTypeDef",
    {
        "items": List[OverallTestResultItemTypeDef],
    },
)

UtteranceAggregationDurationTypeDef = TypedDict(
    "UtteranceAggregationDurationTypeDef",
    {
        "relativeAggregationDuration": RelativeAggregationDurationTypeDef,
    },
)

RuntimeHintDetailsTypeDef = TypedDict(
    "RuntimeHintDetailsTypeDef",
    {
        "runtimeHintValues": List[RuntimeHintValueTypeDef],
        "subSlotHints": Dict[str, Dict[str, Any]],
    },
    total=False,
)

SlotTypeValueTypeDef = TypedDict(
    "SlotTypeValueTypeDef",
    {
        "sampleValue": SampleValueTypeDef,
        "synonyms": Sequence[SampleValueTypeDef],
    },
    total=False,
)

SlotDefaultValueSpecificationTypeDef = TypedDict(
    "SlotDefaultValueSpecificationTypeDef",
    {
        "defaultValueList": Sequence[SlotDefaultValueTypeDef],
    },
)

SlotResolutionTestResultItemTypeDef = TypedDict(
    "SlotResolutionTestResultItemTypeDef",
    {
        "slotName": str,
        "resultCounts": SlotResolutionTestResultItemCountsTypeDef,
    },
)

SlotValueOverrideTypeDef = TypedDict(
    "SlotValueOverrideTypeDef",
    {
        "shape": SlotShapeType,
        "value": SlotValueTypeDef,
        "values": Sequence[Dict[str, Any]],
    },
    total=False,
)

_RequiredSlotValueSelectionSettingTypeDef = TypedDict(
    "_RequiredSlotValueSelectionSettingTypeDef",
    {
        "resolutionStrategy": SlotValueResolutionStrategyType,
    },
)
_OptionalSlotValueSelectionSettingTypeDef = TypedDict(
    "_OptionalSlotValueSelectionSettingTypeDef",
    {
        "regexFilter": SlotValueRegexFilterTypeDef,
        "advancedRecognitionSetting": AdvancedRecognitionSettingTypeDef,
    },
    total=False,
)

class SlotValueSelectionSettingTypeDef(
    _RequiredSlotValueSelectionSettingTypeDef, _OptionalSlotValueSelectionSettingTypeDef
):
    pass

TestSetDiscrepancyErrorsTypeDef = TypedDict(
    "TestSetDiscrepancyErrorsTypeDef",
    {
        "intentDiscrepancies": List[TestSetIntentDiscrepancyItemTypeDef],
        "slotDiscrepancies": List[TestSetSlotDiscrepancyItemTypeDef],
    },
)

TestSetDiscrepancyReportResourceTargetTypeDef = TypedDict(
    "TestSetDiscrepancyReportResourceTargetTypeDef",
    {
        "botAliasTarget": TestSetDiscrepancyReportBotAliasTargetTypeDef,
    },
    total=False,
)

_RequiredTestSetImportResourceSpecificationTypeDef = TypedDict(
    "_RequiredTestSetImportResourceSpecificationTypeDef",
    {
        "testSetName": str,
        "roleArn": str,
        "storageLocation": TestSetStorageLocationTypeDef,
        "importInputLocation": TestSetImportInputLocationTypeDef,
        "modality": TestSetModalityType,
    },
)
_OptionalTestSetImportResourceSpecificationTypeDef = TypedDict(
    "_OptionalTestSetImportResourceSpecificationTypeDef",
    {
        "description": str,
        "testSetTags": Dict[str, str],
    },
    total=False,
)

class TestSetImportResourceSpecificationTypeDef(
    _RequiredTestSetImportResourceSpecificationTypeDef,
    _OptionalTestSetImportResourceSpecificationTypeDef,
):
    pass

_RequiredUserTurnOutputSpecificationTypeDef = TypedDict(
    "_RequiredUserTurnOutputSpecificationTypeDef",
    {
        "intent": UserTurnIntentOutputTypeDef,
    },
)
_OptionalUserTurnOutputSpecificationTypeDef = TypedDict(
    "_OptionalUserTurnOutputSpecificationTypeDef",
    {
        "activeContexts": List[ActiveContextTypeDef],
        "transcript": str,
    },
    total=False,
)

class UserTurnOutputSpecificationTypeDef(
    _RequiredUserTurnOutputSpecificationTypeDef, _OptionalUserTurnOutputSpecificationTypeDef
):
    pass

UtteranceInputSpecificationTypeDef = TypedDict(
    "UtteranceInputSpecificationTypeDef",
    {
        "textInput": str,
        "audioInput": UtteranceAudioInputSpecificationTypeDef,
    },
    total=False,
)

ListIntentMetricsResponseTypeDef = TypedDict(
    "ListIntentMetricsResponseTypeDef",
    {
        "botId": str,
        "results": List[AnalyticsIntentResultTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIntentStageMetricsResponseTypeDef = TypedDict(
    "ListIntentStageMetricsResponseTypeDef",
    {
        "botId": str,
        "results": List[AnalyticsIntentStageResultTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSessionMetricsResponseTypeDef = TypedDict(
    "ListSessionMetricsResponseTypeDef",
    {
        "botId": str,
        "results": List[AnalyticsSessionResultTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListUtteranceMetricsResponseTypeDef = TypedDict(
    "ListUtteranceMetricsResponseTypeDef",
    {
        "botId": str,
        "results": List[AnalyticsUtteranceResultTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPromptAttemptSpecificationTypeDef = TypedDict(
    "_RequiredPromptAttemptSpecificationTypeDef",
    {
        "allowedInputTypes": AllowedInputTypesTypeDef,
    },
)
_OptionalPromptAttemptSpecificationTypeDef = TypedDict(
    "_OptionalPromptAttemptSpecificationTypeDef",
    {
        "allowInterrupt": bool,
        "audioAndDTMFInputSpecification": AudioAndDTMFInputSpecificationTypeDef,
        "textInputSpecification": TextInputSpecificationTypeDef,
    },
    total=False,
)

class PromptAttemptSpecificationTypeDef(
    _RequiredPromptAttemptSpecificationTypeDef, _OptionalPromptAttemptSpecificationTypeDef
):
    pass

AudioLogSettingTypeDef = TypedDict(
    "AudioLogSettingTypeDef",
    {
        "enabled": bool,
        "destination": AudioLogDestinationTypeDef,
    },
)

DescribeTestExecutionResponseTypeDef = TypedDict(
    "DescribeTestExecutionResponseTypeDef",
    {
        "testExecutionId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "testExecutionStatus": TestExecutionStatusType,
        "testSetId": str,
        "testSetName": str,
        "target": TestExecutionTargetTypeDef,
        "apiMode": TestExecutionApiModeType,
        "testExecutionModality": TestExecutionModalityType,
        "failureReasons": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartTestExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredStartTestExecutionRequestRequestTypeDef",
    {
        "testSetId": str,
        "target": TestExecutionTargetTypeDef,
        "apiMode": TestExecutionApiModeType,
    },
)
_OptionalStartTestExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalStartTestExecutionRequestRequestTypeDef",
    {
        "testExecutionModality": TestExecutionModalityType,
    },
    total=False,
)

class StartTestExecutionRequestRequestTypeDef(
    _RequiredStartTestExecutionRequestRequestTypeDef,
    _OptionalStartTestExecutionRequestRequestTypeDef,
):
    pass

StartTestExecutionResponseTypeDef = TypedDict(
    "StartTestExecutionResponseTypeDef",
    {
        "testExecutionId": str,
        "creationDateTime": datetime,
        "testSetId": str,
        "target": TestExecutionTargetTypeDef,
        "apiMode": TestExecutionApiModeType,
        "testExecutionModality": TestExecutionModalityType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TestExecutionSummaryTypeDef = TypedDict(
    "TestExecutionSummaryTypeDef",
    {
        "testExecutionId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "testExecutionStatus": TestExecutionStatusType,
        "testSetId": str,
        "testSetName": str,
        "target": TestExecutionTargetTypeDef,
        "apiMode": TestExecutionApiModeType,
        "testExecutionModality": TestExecutionModalityType,
    },
    total=False,
)

BotRecommendationResultsTypeDef = TypedDict(
    "BotRecommendationResultsTypeDef",
    {
        "botLocaleExportUrl": str,
        "associatedTranscriptsUrl": str,
        "statistics": BotRecommendationResultStatisticsTypeDef,
    },
    total=False,
)

MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "plainTextMessage": PlainTextMessageTypeDef,
        "customPayload": CustomPayloadTypeDef,
        "ssmlMessage": SSMLMessageTypeDef,
        "imageResponseCard": ImageResponseCardTypeDef,
    },
    total=False,
)

UtteranceBotResponseTypeDef = TypedDict(
    "UtteranceBotResponseTypeDef",
    {
        "content": str,
        "contentType": UtteranceContentTypeType,
        "imageResponseCard": ImageResponseCardTypeDef,
    },
    total=False,
)

TextLogSettingTypeDef = TypedDict(
    "TextLogSettingTypeDef",
    {
        "enabled": bool,
        "destination": TextLogDestinationTypeDef,
    },
)

_RequiredBotAliasLocaleSettingsTypeDef = TypedDict(
    "_RequiredBotAliasLocaleSettingsTypeDef",
    {
        "enabled": bool,
    },
)
_OptionalBotAliasLocaleSettingsTypeDef = TypedDict(
    "_OptionalBotAliasLocaleSettingsTypeDef",
    {
        "codeHookSpecification": CodeHookSpecificationTypeDef,
    },
    total=False,
)

class BotAliasLocaleSettingsTypeDef(
    _RequiredBotAliasLocaleSettingsTypeDef, _OptionalBotAliasLocaleSettingsTypeDef
):
    pass

ConversationLevelTestResultsTypeDef = TypedDict(
    "ConversationLevelTestResultsTypeDef",
    {
        "items": List[ConversationLevelTestResultItemTypeDef],
    },
)

_RequiredListTestExecutionResultItemsRequestRequestTypeDef = TypedDict(
    "_RequiredListTestExecutionResultItemsRequestRequestTypeDef",
    {
        "testExecutionId": str,
        "resultFilterBy": TestExecutionResultFilterByTypeDef,
    },
)
_OptionalListTestExecutionResultItemsRequestRequestTypeDef = TypedDict(
    "_OptionalListTestExecutionResultItemsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListTestExecutionResultItemsRequestRequestTypeDef(
    _RequiredListTestExecutionResultItemsRequestRequestTypeDef,
    _OptionalListTestExecutionResultItemsRequestRequestTypeDef,
):
    pass

TestSetGenerationDataSourceTypeDef = TypedDict(
    "TestSetGenerationDataSourceTypeDef",
    {
        "conversationLogsDataSource": ConversationLogsDataSourceTypeDef,
    },
    total=False,
)

ListIntentsResponseTypeDef = TypedDict(
    "ListIntentsResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "intentSummaries": List[IntentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TranscriptFilterTypeDef = TypedDict(
    "TranscriptFilterTypeDef",
    {
        "lexTranscriptFilter": LexTranscriptFilterTypeDef,
    },
    total=False,
)

ListTestSetsResponseTypeDef = TypedDict(
    "ListTestSetsResponseTypeDef",
    {
        "testSets": List[TestSetSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateExportRequestRequestTypeDef = TypedDict(
    "_RequiredCreateExportRequestRequestTypeDef",
    {
        "resourceSpecification": ExportResourceSpecificationTypeDef,
        "fileFormat": ImportExportFileFormatType,
    },
)
_OptionalCreateExportRequestRequestTypeDef = TypedDict(
    "_OptionalCreateExportRequestRequestTypeDef",
    {
        "filePassword": str,
    },
    total=False,
)

class CreateExportRequestRequestTypeDef(
    _RequiredCreateExportRequestRequestTypeDef, _OptionalCreateExportRequestRequestTypeDef
):
    pass

CreateExportResponseTypeDef = TypedDict(
    "CreateExportResponseTypeDef",
    {
        "exportId": str,
        "resourceSpecification": ExportResourceSpecificationTypeDef,
        "fileFormat": ImportExportFileFormatType,
        "exportStatus": ExportStatusType,
        "creationDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeExportResponseTypeDef = TypedDict(
    "DescribeExportResponseTypeDef",
    {
        "exportId": str,
        "resourceSpecification": ExportResourceSpecificationTypeDef,
        "fileFormat": ImportExportFileFormatType,
        "exportStatus": ExportStatusType,
        "failureReasons": List[str],
        "downloadUrl": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportSummaryTypeDef = TypedDict(
    "ExportSummaryTypeDef",
    {
        "exportId": str,
        "resourceSpecification": ExportResourceSpecificationTypeDef,
        "fileFormat": ImportExportFileFormatType,
        "exportStatus": ExportStatusType,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

UpdateExportResponseTypeDef = TypedDict(
    "UpdateExportResponseTypeDef",
    {
        "exportId": str,
        "resourceSpecification": ExportResourceSpecificationTypeDef,
        "fileFormat": ImportExportFileFormatType,
        "exportStatus": ExportStatusType,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExternalSourceSettingTypeDef = TypedDict(
    "ExternalSourceSettingTypeDef",
    {
        "grammarSlotTypeSetting": GrammarSlotTypeSettingTypeDef,
    },
    total=False,
)

IntentClassificationTestResultsTypeDef = TypedDict(
    "IntentClassificationTestResultsTypeDef",
    {
        "items": List[IntentClassificationTestResultItemTypeDef],
    },
)

ListSessionAnalyticsDataResponseTypeDef = TypedDict(
    "ListSessionAnalyticsDataResponseTypeDef",
    {
        "botId": str,
        "nextToken": str,
        "sessions": List[SessionSpecificationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListAggregatedUtterancesRequestRequestTypeDef = TypedDict(
    "_RequiredListAggregatedUtterancesRequestRequestTypeDef",
    {
        "botId": str,
        "localeId": str,
        "aggregationDuration": UtteranceAggregationDurationTypeDef,
    },
)
_OptionalListAggregatedUtterancesRequestRequestTypeDef = TypedDict(
    "_OptionalListAggregatedUtterancesRequestRequestTypeDef",
    {
        "botAliasId": str,
        "botVersion": str,
        "sortBy": AggregatedUtterancesSortByTypeDef,
        "filters": Sequence[AggregatedUtterancesFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListAggregatedUtterancesRequestRequestTypeDef(
    _RequiredListAggregatedUtterancesRequestRequestTypeDef,
    _OptionalListAggregatedUtterancesRequestRequestTypeDef,
):
    pass

ListAggregatedUtterancesResponseTypeDef = TypedDict(
    "ListAggregatedUtterancesResponseTypeDef",
    {
        "botId": str,
        "botAliasId": str,
        "botVersion": str,
        "localeId": str,
        "aggregationDuration": UtteranceAggregationDurationTypeDef,
        "aggregationWindowStartTime": datetime,
        "aggregationWindowEndTime": datetime,
        "aggregationLastRefreshedDateTime": datetime,
        "aggregatedUtterancesSummaries": List[AggregatedUtterancesSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IntentLevelSlotResolutionTestResultItemTypeDef = TypedDict(
    "IntentLevelSlotResolutionTestResultItemTypeDef",
    {
        "intentName": str,
        "multiTurnConversation": bool,
        "slotResolutionResults": List[SlotResolutionTestResultItemTypeDef],
    },
)

CreateTestSetDiscrepancyReportRequestRequestTypeDef = TypedDict(
    "CreateTestSetDiscrepancyReportRequestRequestTypeDef",
    {
        "testSetId": str,
        "target": TestSetDiscrepancyReportResourceTargetTypeDef,
    },
)

CreateTestSetDiscrepancyReportResponseTypeDef = TypedDict(
    "CreateTestSetDiscrepancyReportResponseTypeDef",
    {
        "testSetDiscrepancyReportId": str,
        "creationDateTime": datetime,
        "testSetId": str,
        "target": TestSetDiscrepancyReportResourceTargetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTestSetDiscrepancyReportResponseTypeDef = TypedDict(
    "DescribeTestSetDiscrepancyReportResponseTypeDef",
    {
        "testSetDiscrepancyReportId": str,
        "testSetId": str,
        "creationDateTime": datetime,
        "target": TestSetDiscrepancyReportResourceTargetTypeDef,
        "testSetDiscrepancyReportStatus": TestSetDiscrepancyReportStatusType,
        "lastUpdatedDataTime": datetime,
        "testSetDiscrepancyTopErrors": TestSetDiscrepancyErrorsTypeDef,
        "testSetDiscrepancyRawOutputUrl": str,
        "failureReasons": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportResourceSpecificationTypeDef = TypedDict(
    "ImportResourceSpecificationTypeDef",
    {
        "botImportSpecification": BotImportSpecificationTypeDef,
        "botLocaleImportSpecification": BotLocaleImportSpecificationTypeDef,
        "customVocabularyImportSpecification": CustomVocabularyImportSpecificationTypeDef,
        "testSetImportResourceSpecification": TestSetImportResourceSpecificationTypeDef,
    },
    total=False,
)

_RequiredUserTurnInputSpecificationTypeDef = TypedDict(
    "_RequiredUserTurnInputSpecificationTypeDef",
    {
        "utteranceInput": UtteranceInputSpecificationTypeDef,
    },
)
_OptionalUserTurnInputSpecificationTypeDef = TypedDict(
    "_OptionalUserTurnInputSpecificationTypeDef",
    {
        "requestAttributes": Dict[str, str],
        "sessionState": InputSessionStateSpecificationTypeDef,
    },
    total=False,
)

class UserTurnInputSpecificationTypeDef(
    _RequiredUserTurnInputSpecificationTypeDef, _OptionalUserTurnInputSpecificationTypeDef
):
    pass

ListTestExecutionsResponseTypeDef = TypedDict(
    "ListTestExecutionsResponseTypeDef",
    {
        "testExecutions": List[TestExecutionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredMessageGroupTypeDef = TypedDict(
    "_RequiredMessageGroupTypeDef",
    {
        "message": MessageTypeDef,
    },
)
_OptionalMessageGroupTypeDef = TypedDict(
    "_OptionalMessageGroupTypeDef",
    {
        "variations": Sequence[MessageTypeDef],
    },
    total=False,
)

class MessageGroupTypeDef(_RequiredMessageGroupTypeDef, _OptionalMessageGroupTypeDef):
    pass

UtteranceSpecificationTypeDef = TypedDict(
    "UtteranceSpecificationTypeDef",
    {
        "botAliasId": str,
        "botVersion": str,
        "localeId": str,
        "sessionId": str,
        "channel": str,
        "mode": AnalyticsModalityType,
        "conversationStartTime": datetime,
        "conversationEndTime": datetime,
        "utterance": str,
        "utteranceTimestamp": datetime,
        "audioVoiceDurationMillis": int,
        "utteranceUnderstood": bool,
        "inputType": str,
        "outputType": str,
        "associatedIntentName": str,
        "associatedSlotName": str,
        "intentState": IntentStateType,
        "dialogActionType": str,
        "botResponseAudioVoiceId": str,
        "slotsFilledInSession": str,
        "utteranceRequestId": str,
        "botResponses": List[UtteranceBotResponseTypeDef],
    },
    total=False,
)

ConversationLogSettingsTypeDef = TypedDict(
    "ConversationLogSettingsTypeDef",
    {
        "textLogSettings": Sequence[TextLogSettingTypeDef],
        "audioLogSettings": Sequence[AudioLogSettingTypeDef],
    },
    total=False,
)

DescribeTestSetGenerationResponseTypeDef = TypedDict(
    "DescribeTestSetGenerationResponseTypeDef",
    {
        "testSetGenerationId": str,
        "testSetGenerationStatus": TestSetGenerationStatusType,
        "failureReasons": List[str],
        "testSetId": str,
        "testSetName": str,
        "description": str,
        "storageLocation": TestSetStorageLocationTypeDef,
        "generationDataSource": TestSetGenerationDataSourceTypeDef,
        "roleArn": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartTestSetGenerationRequestRequestTypeDef = TypedDict(
    "_RequiredStartTestSetGenerationRequestRequestTypeDef",
    {
        "testSetName": str,
        "storageLocation": TestSetStorageLocationTypeDef,
        "generationDataSource": TestSetGenerationDataSourceTypeDef,
        "roleArn": str,
    },
)
_OptionalStartTestSetGenerationRequestRequestTypeDef = TypedDict(
    "_OptionalStartTestSetGenerationRequestRequestTypeDef",
    {
        "description": str,
        "testSetTags": Mapping[str, str],
    },
    total=False,
)

class StartTestSetGenerationRequestRequestTypeDef(
    _RequiredStartTestSetGenerationRequestRequestTypeDef,
    _OptionalStartTestSetGenerationRequestRequestTypeDef,
):
    pass

StartTestSetGenerationResponseTypeDef = TypedDict(
    "StartTestSetGenerationResponseTypeDef",
    {
        "testSetGenerationId": str,
        "creationDateTime": datetime,
        "testSetGenerationStatus": TestSetGenerationStatusType,
        "testSetName": str,
        "description": str,
        "storageLocation": TestSetStorageLocationTypeDef,
        "generationDataSource": TestSetGenerationDataSourceTypeDef,
        "roleArn": str,
        "testSetTags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredS3BucketTranscriptSourceTypeDef = TypedDict(
    "_RequiredS3BucketTranscriptSourceTypeDef",
    {
        "s3BucketName": str,
        "transcriptFormat": Literal["Lex"],
    },
)
_OptionalS3BucketTranscriptSourceTypeDef = TypedDict(
    "_OptionalS3BucketTranscriptSourceTypeDef",
    {
        "pathFormat": PathFormatTypeDef,
        "transcriptFilter": TranscriptFilterTypeDef,
        "kmsKeyArn": str,
    },
    total=False,
)

class S3BucketTranscriptSourceTypeDef(
    _RequiredS3BucketTranscriptSourceTypeDef, _OptionalS3BucketTranscriptSourceTypeDef
):
    pass

ListExportsResponseTypeDef = TypedDict(
    "ListExportsResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "exportSummaries": List[ExportSummaryTypeDef],
        "nextToken": str,
        "localeId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateSlotTypeRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSlotTypeRequestRequestTypeDef",
    {
        "slotTypeName": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalCreateSlotTypeRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSlotTypeRequestRequestTypeDef",
    {
        "description": str,
        "slotTypeValues": Sequence[SlotTypeValueTypeDef],
        "valueSelectionSetting": SlotValueSelectionSettingTypeDef,
        "parentSlotTypeSignature": str,
        "externalSourceSetting": ExternalSourceSettingTypeDef,
        "compositeSlotTypeSetting": CompositeSlotTypeSettingTypeDef,
    },
    total=False,
)

class CreateSlotTypeRequestRequestTypeDef(
    _RequiredCreateSlotTypeRequestRequestTypeDef, _OptionalCreateSlotTypeRequestRequestTypeDef
):
    pass

CreateSlotTypeResponseTypeDef = TypedDict(
    "CreateSlotTypeResponseTypeDef",
    {
        "slotTypeId": str,
        "slotTypeName": str,
        "description": str,
        "slotTypeValues": List[SlotTypeValueTypeDef],
        "valueSelectionSetting": SlotValueSelectionSettingTypeDef,
        "parentSlotTypeSignature": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "creationDateTime": datetime,
        "externalSourceSetting": ExternalSourceSettingTypeDef,
        "compositeSlotTypeSetting": CompositeSlotTypeSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSlotTypeResponseTypeDef = TypedDict(
    "DescribeSlotTypeResponseTypeDef",
    {
        "slotTypeId": str,
        "slotTypeName": str,
        "description": str,
        "slotTypeValues": List[SlotTypeValueTypeDef],
        "valueSelectionSetting": SlotValueSelectionSettingTypeDef,
        "parentSlotTypeSignature": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "externalSourceSetting": ExternalSourceSettingTypeDef,
        "compositeSlotTypeSetting": CompositeSlotTypeSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateSlotTypeRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSlotTypeRequestRequestTypeDef",
    {
        "slotTypeId": str,
        "slotTypeName": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalUpdateSlotTypeRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSlotTypeRequestRequestTypeDef",
    {
        "description": str,
        "slotTypeValues": Sequence[SlotTypeValueTypeDef],
        "valueSelectionSetting": SlotValueSelectionSettingTypeDef,
        "parentSlotTypeSignature": str,
        "externalSourceSetting": ExternalSourceSettingTypeDef,
        "compositeSlotTypeSetting": CompositeSlotTypeSettingTypeDef,
    },
    total=False,
)

class UpdateSlotTypeRequestRequestTypeDef(
    _RequiredUpdateSlotTypeRequestRequestTypeDef, _OptionalUpdateSlotTypeRequestRequestTypeDef
):
    pass

UpdateSlotTypeResponseTypeDef = TypedDict(
    "UpdateSlotTypeResponseTypeDef",
    {
        "slotTypeId": str,
        "slotTypeName": str,
        "description": str,
        "slotTypeValues": List[SlotTypeValueTypeDef],
        "valueSelectionSetting": SlotValueSelectionSettingTypeDef,
        "parentSlotTypeSignature": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "externalSourceSetting": ExternalSourceSettingTypeDef,
        "compositeSlotTypeSetting": CompositeSlotTypeSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IntentLevelSlotResolutionTestResultsTypeDef = TypedDict(
    "IntentLevelSlotResolutionTestResultsTypeDef",
    {
        "items": List[IntentLevelSlotResolutionTestResultItemTypeDef],
    },
)

DescribeImportResponseTypeDef = TypedDict(
    "DescribeImportResponseTypeDef",
    {
        "importId": str,
        "resourceSpecification": ImportResourceSpecificationTypeDef,
        "importedResourceId": str,
        "importedResourceName": str,
        "mergeStrategy": MergeStrategyType,
        "importStatus": ImportStatusType,
        "failureReasons": List[str],
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartImportRequestRequestTypeDef = TypedDict(
    "_RequiredStartImportRequestRequestTypeDef",
    {
        "importId": str,
        "resourceSpecification": ImportResourceSpecificationTypeDef,
        "mergeStrategy": MergeStrategyType,
    },
)
_OptionalStartImportRequestRequestTypeDef = TypedDict(
    "_OptionalStartImportRequestRequestTypeDef",
    {
        "filePassword": str,
    },
    total=False,
)

class StartImportRequestRequestTypeDef(
    _RequiredStartImportRequestRequestTypeDef, _OptionalStartImportRequestRequestTypeDef
):
    pass

StartImportResponseTypeDef = TypedDict(
    "StartImportResponseTypeDef",
    {
        "importId": str,
        "resourceSpecification": ImportResourceSpecificationTypeDef,
        "mergeStrategy": MergeStrategyType,
        "importStatus": ImportStatusType,
        "creationDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUserTurnResultTypeDef = TypedDict(
    "_RequiredUserTurnResultTypeDef",
    {
        "input": UserTurnInputSpecificationTypeDef,
        "expectedOutput": UserTurnOutputSpecificationTypeDef,
    },
)
_OptionalUserTurnResultTypeDef = TypedDict(
    "_OptionalUserTurnResultTypeDef",
    {
        "actualOutput": UserTurnOutputSpecificationTypeDef,
        "errorDetails": ExecutionErrorDetailsTypeDef,
        "endToEndResult": TestResultMatchStatusType,
        "intentMatchResult": TestResultMatchStatusType,
        "slotMatchResult": TestResultMatchStatusType,
        "speechTranscriptionResult": TestResultMatchStatusType,
        "conversationLevelResult": ConversationLevelResultDetailTypeDef,
    },
    total=False,
)

class UserTurnResultTypeDef(_RequiredUserTurnResultTypeDef, _OptionalUserTurnResultTypeDef):
    pass

UserTurnSpecificationTypeDef = TypedDict(
    "UserTurnSpecificationTypeDef",
    {
        "input": UserTurnInputSpecificationTypeDef,
        "expected": UserTurnOutputSpecificationTypeDef,
    },
)

_RequiredFulfillmentStartResponseSpecificationTypeDef = TypedDict(
    "_RequiredFulfillmentStartResponseSpecificationTypeDef",
    {
        "delayInSeconds": int,
        "messageGroups": Sequence[MessageGroupTypeDef],
    },
)
_OptionalFulfillmentStartResponseSpecificationTypeDef = TypedDict(
    "_OptionalFulfillmentStartResponseSpecificationTypeDef",
    {
        "allowInterrupt": bool,
    },
    total=False,
)

class FulfillmentStartResponseSpecificationTypeDef(
    _RequiredFulfillmentStartResponseSpecificationTypeDef,
    _OptionalFulfillmentStartResponseSpecificationTypeDef,
):
    pass

_RequiredFulfillmentUpdateResponseSpecificationTypeDef = TypedDict(
    "_RequiredFulfillmentUpdateResponseSpecificationTypeDef",
    {
        "frequencyInSeconds": int,
        "messageGroups": Sequence[MessageGroupTypeDef],
    },
)
_OptionalFulfillmentUpdateResponseSpecificationTypeDef = TypedDict(
    "_OptionalFulfillmentUpdateResponseSpecificationTypeDef",
    {
        "allowInterrupt": bool,
    },
    total=False,
)

class FulfillmentUpdateResponseSpecificationTypeDef(
    _RequiredFulfillmentUpdateResponseSpecificationTypeDef,
    _OptionalFulfillmentUpdateResponseSpecificationTypeDef,
):
    pass

_RequiredPromptSpecificationTypeDef = TypedDict(
    "_RequiredPromptSpecificationTypeDef",
    {
        "messageGroups": Sequence[MessageGroupTypeDef],
        "maxRetries": int,
    },
)
_OptionalPromptSpecificationTypeDef = TypedDict(
    "_OptionalPromptSpecificationTypeDef",
    {
        "allowInterrupt": bool,
        "messageSelectionStrategy": MessageSelectionStrategyType,
        "promptAttemptsSpecification": Mapping[
            PromptAttemptType, PromptAttemptSpecificationTypeDef
        ],
    },
    total=False,
)

class PromptSpecificationTypeDef(
    _RequiredPromptSpecificationTypeDef, _OptionalPromptSpecificationTypeDef
):
    pass

_RequiredResponseSpecificationTypeDef = TypedDict(
    "_RequiredResponseSpecificationTypeDef",
    {
        "messageGroups": Sequence[MessageGroupTypeDef],
    },
)
_OptionalResponseSpecificationTypeDef = TypedDict(
    "_OptionalResponseSpecificationTypeDef",
    {
        "allowInterrupt": bool,
    },
    total=False,
)

class ResponseSpecificationTypeDef(
    _RequiredResponseSpecificationTypeDef, _OptionalResponseSpecificationTypeDef
):
    pass

_RequiredStillWaitingResponseSpecificationTypeDef = TypedDict(
    "_RequiredStillWaitingResponseSpecificationTypeDef",
    {
        "messageGroups": Sequence[MessageGroupTypeDef],
        "frequencyInSeconds": int,
        "timeoutInSeconds": int,
    },
)
_OptionalStillWaitingResponseSpecificationTypeDef = TypedDict(
    "_OptionalStillWaitingResponseSpecificationTypeDef",
    {
        "allowInterrupt": bool,
    },
    total=False,
)

class StillWaitingResponseSpecificationTypeDef(
    _RequiredStillWaitingResponseSpecificationTypeDef,
    _OptionalStillWaitingResponseSpecificationTypeDef,
):
    pass

ListUtteranceAnalyticsDataResponseTypeDef = TypedDict(
    "ListUtteranceAnalyticsDataResponseTypeDef",
    {
        "botId": str,
        "nextToken": str,
        "utterances": List[UtteranceSpecificationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateBotAliasRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBotAliasRequestRequestTypeDef",
    {
        "botAliasName": str,
        "botId": str,
    },
)
_OptionalCreateBotAliasRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBotAliasRequestRequestTypeDef",
    {
        "description": str,
        "botVersion": str,
        "botAliasLocaleSettings": Mapping[str, BotAliasLocaleSettingsTypeDef],
        "conversationLogSettings": ConversationLogSettingsTypeDef,
        "sentimentAnalysisSettings": SentimentAnalysisSettingsTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateBotAliasRequestRequestTypeDef(
    _RequiredCreateBotAliasRequestRequestTypeDef, _OptionalCreateBotAliasRequestRequestTypeDef
):
    pass

CreateBotAliasResponseTypeDef = TypedDict(
    "CreateBotAliasResponseTypeDef",
    {
        "botAliasId": str,
        "botAliasName": str,
        "description": str,
        "botVersion": str,
        "botAliasLocaleSettings": Dict[str, BotAliasLocaleSettingsTypeDef],
        "conversationLogSettings": ConversationLogSettingsTypeDef,
        "sentimentAnalysisSettings": SentimentAnalysisSettingsTypeDef,
        "botAliasStatus": BotAliasStatusType,
        "botId": str,
        "creationDateTime": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBotAliasResponseTypeDef = TypedDict(
    "DescribeBotAliasResponseTypeDef",
    {
        "botAliasId": str,
        "botAliasName": str,
        "description": str,
        "botVersion": str,
        "botAliasLocaleSettings": Dict[str, BotAliasLocaleSettingsTypeDef],
        "conversationLogSettings": ConversationLogSettingsTypeDef,
        "sentimentAnalysisSettings": SentimentAnalysisSettingsTypeDef,
        "botAliasHistoryEvents": List[BotAliasHistoryEventTypeDef],
        "botAliasStatus": BotAliasStatusType,
        "botId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "parentBotNetworks": List[ParentBotNetworkTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateBotAliasRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateBotAliasRequestRequestTypeDef",
    {
        "botAliasId": str,
        "botAliasName": str,
        "botId": str,
    },
)
_OptionalUpdateBotAliasRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateBotAliasRequestRequestTypeDef",
    {
        "description": str,
        "botVersion": str,
        "botAliasLocaleSettings": Mapping[str, BotAliasLocaleSettingsTypeDef],
        "conversationLogSettings": ConversationLogSettingsTypeDef,
        "sentimentAnalysisSettings": SentimentAnalysisSettingsTypeDef,
    },
    total=False,
)

class UpdateBotAliasRequestRequestTypeDef(
    _RequiredUpdateBotAliasRequestRequestTypeDef, _OptionalUpdateBotAliasRequestRequestTypeDef
):
    pass

UpdateBotAliasResponseTypeDef = TypedDict(
    "UpdateBotAliasResponseTypeDef",
    {
        "botAliasId": str,
        "botAliasName": str,
        "description": str,
        "botVersion": str,
        "botAliasLocaleSettings": Dict[str, BotAliasLocaleSettingsTypeDef],
        "conversationLogSettings": ConversationLogSettingsTypeDef,
        "sentimentAnalysisSettings": SentimentAnalysisSettingsTypeDef,
        "botAliasStatus": BotAliasStatusType,
        "botId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TranscriptSourceSettingTypeDef = TypedDict(
    "TranscriptSourceSettingTypeDef",
    {
        "s3BucketTranscriptSource": S3BucketTranscriptSourceTypeDef,
    },
    total=False,
)

TestSetTurnResultTypeDef = TypedDict(
    "TestSetTurnResultTypeDef",
    {
        "agent": AgentTurnResultTypeDef,
        "user": UserTurnResultTypeDef,
    },
    total=False,
)

TurnSpecificationTypeDef = TypedDict(
    "TurnSpecificationTypeDef",
    {
        "agentTurn": AgentTurnSpecificationTypeDef,
        "userTurn": UserTurnSpecificationTypeDef,
    },
    total=False,
)

_RequiredFulfillmentUpdatesSpecificationTypeDef = TypedDict(
    "_RequiredFulfillmentUpdatesSpecificationTypeDef",
    {
        "active": bool,
    },
)
_OptionalFulfillmentUpdatesSpecificationTypeDef = TypedDict(
    "_OptionalFulfillmentUpdatesSpecificationTypeDef",
    {
        "startResponse": FulfillmentStartResponseSpecificationTypeDef,
        "updateResponse": FulfillmentUpdateResponseSpecificationTypeDef,
        "timeoutInSeconds": int,
    },
    total=False,
)

class FulfillmentUpdatesSpecificationTypeDef(
    _RequiredFulfillmentUpdatesSpecificationTypeDef, _OptionalFulfillmentUpdatesSpecificationTypeDef
):
    pass

SlotSummaryTypeDef = TypedDict(
    "SlotSummaryTypeDef",
    {
        "slotId": str,
        "slotName": str,
        "description": str,
        "slotConstraint": SlotConstraintType,
        "slotTypeId": str,
        "valueElicitationPromptSpecification": PromptSpecificationTypeDef,
        "lastUpdatedDateTime": datetime,
    },
    total=False,
)

_RequiredConditionalBranchTypeDef = TypedDict(
    "_RequiredConditionalBranchTypeDef",
    {
        "name": str,
        "condition": ConditionTypeDef,
        "nextStep": DialogStateTypeDef,
    },
)
_OptionalConditionalBranchTypeDef = TypedDict(
    "_OptionalConditionalBranchTypeDef",
    {
        "response": ResponseSpecificationTypeDef,
    },
    total=False,
)

class ConditionalBranchTypeDef(
    _RequiredConditionalBranchTypeDef, _OptionalConditionalBranchTypeDef
):
    pass

DefaultConditionalBranchTypeDef = TypedDict(
    "DefaultConditionalBranchTypeDef",
    {
        "nextStep": DialogStateTypeDef,
        "response": ResponseSpecificationTypeDef,
    },
    total=False,
)

_RequiredWaitAndContinueSpecificationTypeDef = TypedDict(
    "_RequiredWaitAndContinueSpecificationTypeDef",
    {
        "waitingResponse": ResponseSpecificationTypeDef,
        "continueResponse": ResponseSpecificationTypeDef,
    },
)
_OptionalWaitAndContinueSpecificationTypeDef = TypedDict(
    "_OptionalWaitAndContinueSpecificationTypeDef",
    {
        "stillWaitingResponse": StillWaitingResponseSpecificationTypeDef,
        "active": bool,
    },
    total=False,
)

class WaitAndContinueSpecificationTypeDef(
    _RequiredWaitAndContinueSpecificationTypeDef, _OptionalWaitAndContinueSpecificationTypeDef
):
    pass

DescribeBotRecommendationResponseTypeDef = TypedDict(
    "DescribeBotRecommendationResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationStatus": BotRecommendationStatusType,
        "botRecommendationId": str,
        "failureReasons": List[str],
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "transcriptSourceSetting": TranscriptSourceSettingTypeDef,
        "encryptionSetting": EncryptionSettingTypeDef,
        "botRecommendationResults": BotRecommendationResultsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartBotRecommendationRequestRequestTypeDef = TypedDict(
    "_RequiredStartBotRecommendationRequestRequestTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "transcriptSourceSetting": TranscriptSourceSettingTypeDef,
    },
)
_OptionalStartBotRecommendationRequestRequestTypeDef = TypedDict(
    "_OptionalStartBotRecommendationRequestRequestTypeDef",
    {
        "encryptionSetting": EncryptionSettingTypeDef,
    },
    total=False,
)

class StartBotRecommendationRequestRequestTypeDef(
    _RequiredStartBotRecommendationRequestRequestTypeDef,
    _OptionalStartBotRecommendationRequestRequestTypeDef,
):
    pass

StartBotRecommendationResponseTypeDef = TypedDict(
    "StartBotRecommendationResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationStatus": BotRecommendationStatusType,
        "botRecommendationId": str,
        "creationDateTime": datetime,
        "transcriptSourceSetting": TranscriptSourceSettingTypeDef,
        "encryptionSetting": EncryptionSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBotRecommendationResponseTypeDef = TypedDict(
    "UpdateBotRecommendationResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "botRecommendationStatus": BotRecommendationStatusType,
        "botRecommendationId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "transcriptSourceSetting": TranscriptSourceSettingTypeDef,
        "encryptionSetting": EncryptionSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUtteranceLevelTestResultItemTypeDef = TypedDict(
    "_RequiredUtteranceLevelTestResultItemTypeDef",
    {
        "recordNumber": int,
        "turnResult": TestSetTurnResultTypeDef,
    },
)
_OptionalUtteranceLevelTestResultItemTypeDef = TypedDict(
    "_OptionalUtteranceLevelTestResultItemTypeDef",
    {
        "conversationId": str,
    },
    total=False,
)

class UtteranceLevelTestResultItemTypeDef(
    _RequiredUtteranceLevelTestResultItemTypeDef, _OptionalUtteranceLevelTestResultItemTypeDef
):
    pass

_RequiredTestSetTurnRecordTypeDef = TypedDict(
    "_RequiredTestSetTurnRecordTypeDef",
    {
        "recordNumber": int,
        "turnSpecification": TurnSpecificationTypeDef,
    },
)
_OptionalTestSetTurnRecordTypeDef = TypedDict(
    "_OptionalTestSetTurnRecordTypeDef",
    {
        "conversationId": str,
        "turnNumber": int,
    },
    total=False,
)

class TestSetTurnRecordTypeDef(
    _RequiredTestSetTurnRecordTypeDef, _OptionalTestSetTurnRecordTypeDef
):
    pass

ListSlotsResponseTypeDef = TypedDict(
    "ListSlotsResponseTypeDef",
    {
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "intentId": str,
        "slotSummaries": List[SlotSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ConditionalSpecificationTypeDef = TypedDict(
    "ConditionalSpecificationTypeDef",
    {
        "active": bool,
        "conditionalBranches": Sequence[ConditionalBranchTypeDef],
        "defaultBranch": DefaultConditionalBranchTypeDef,
    },
)

_RequiredSubSlotValueElicitationSettingTypeDef = TypedDict(
    "_RequiredSubSlotValueElicitationSettingTypeDef",
    {
        "promptSpecification": PromptSpecificationTypeDef,
    },
)
_OptionalSubSlotValueElicitationSettingTypeDef = TypedDict(
    "_OptionalSubSlotValueElicitationSettingTypeDef",
    {
        "defaultValueSpecification": SlotDefaultValueSpecificationTypeDef,
        "sampleUtterances": Sequence[SampleUtteranceTypeDef],
        "waitAndContinueSpecification": WaitAndContinueSpecificationTypeDef,
    },
    total=False,
)

class SubSlotValueElicitationSettingTypeDef(
    _RequiredSubSlotValueElicitationSettingTypeDef, _OptionalSubSlotValueElicitationSettingTypeDef
):
    pass

UtteranceLevelTestResultsTypeDef = TypedDict(
    "UtteranceLevelTestResultsTypeDef",
    {
        "items": List[UtteranceLevelTestResultItemTypeDef],
    },
)

ListTestSetRecordsResponseTypeDef = TypedDict(
    "ListTestSetRecordsResponseTypeDef",
    {
        "testSetRecords": List[TestSetTurnRecordTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

IntentClosingSettingTypeDef = TypedDict(
    "IntentClosingSettingTypeDef",
    {
        "closingResponse": ResponseSpecificationTypeDef,
        "active": bool,
        "nextStep": DialogStateTypeDef,
        "conditional": ConditionalSpecificationTypeDef,
    },
    total=False,
)

PostDialogCodeHookInvocationSpecificationTypeDef = TypedDict(
    "PostDialogCodeHookInvocationSpecificationTypeDef",
    {
        "successResponse": ResponseSpecificationTypeDef,
        "successNextStep": DialogStateTypeDef,
        "successConditional": ConditionalSpecificationTypeDef,
        "failureResponse": ResponseSpecificationTypeDef,
        "failureNextStep": DialogStateTypeDef,
        "failureConditional": ConditionalSpecificationTypeDef,
        "timeoutResponse": ResponseSpecificationTypeDef,
        "timeoutNextStep": DialogStateTypeDef,
        "timeoutConditional": ConditionalSpecificationTypeDef,
    },
    total=False,
)

PostFulfillmentStatusSpecificationTypeDef = TypedDict(
    "PostFulfillmentStatusSpecificationTypeDef",
    {
        "successResponse": ResponseSpecificationTypeDef,
        "failureResponse": ResponseSpecificationTypeDef,
        "timeoutResponse": ResponseSpecificationTypeDef,
        "successNextStep": DialogStateTypeDef,
        "successConditional": ConditionalSpecificationTypeDef,
        "failureNextStep": DialogStateTypeDef,
        "failureConditional": ConditionalSpecificationTypeDef,
        "timeoutNextStep": DialogStateTypeDef,
        "timeoutConditional": ConditionalSpecificationTypeDef,
    },
    total=False,
)

SpecificationsTypeDef = TypedDict(
    "SpecificationsTypeDef",
    {
        "slotTypeId": str,
        "valueElicitationSetting": SubSlotValueElicitationSettingTypeDef,
    },
)

TestExecutionResultItemsTypeDef = TypedDict(
    "TestExecutionResultItemsTypeDef",
    {
        "overallTestResults": OverallTestResultsTypeDef,
        "conversationLevelTestResults": ConversationLevelTestResultsTypeDef,
        "intentClassificationTestResults": IntentClassificationTestResultsTypeDef,
        "intentLevelSlotResolutionTestResults": IntentLevelSlotResolutionTestResultsTypeDef,
        "utteranceLevelTestResults": UtteranceLevelTestResultsTypeDef,
    },
    total=False,
)

_RequiredDialogCodeHookInvocationSettingTypeDef = TypedDict(
    "_RequiredDialogCodeHookInvocationSettingTypeDef",
    {
        "enableCodeHookInvocation": bool,
        "active": bool,
        "postCodeHookSpecification": PostDialogCodeHookInvocationSpecificationTypeDef,
    },
)
_OptionalDialogCodeHookInvocationSettingTypeDef = TypedDict(
    "_OptionalDialogCodeHookInvocationSettingTypeDef",
    {
        "invocationLabel": str,
    },
    total=False,
)

class DialogCodeHookInvocationSettingTypeDef(
    _RequiredDialogCodeHookInvocationSettingTypeDef, _OptionalDialogCodeHookInvocationSettingTypeDef
):
    pass

_RequiredFulfillmentCodeHookSettingsTypeDef = TypedDict(
    "_RequiredFulfillmentCodeHookSettingsTypeDef",
    {
        "enabled": bool,
    },
)
_OptionalFulfillmentCodeHookSettingsTypeDef = TypedDict(
    "_OptionalFulfillmentCodeHookSettingsTypeDef",
    {
        "postFulfillmentStatusSpecification": PostFulfillmentStatusSpecificationTypeDef,
        "fulfillmentUpdatesSpecification": FulfillmentUpdatesSpecificationTypeDef,
        "active": bool,
    },
    total=False,
)

class FulfillmentCodeHookSettingsTypeDef(
    _RequiredFulfillmentCodeHookSettingsTypeDef, _OptionalFulfillmentCodeHookSettingsTypeDef
):
    pass

SubSlotSettingTypeDef = TypedDict(
    "SubSlotSettingTypeDef",
    {
        "expression": str,
        "slotSpecifications": Mapping[str, SpecificationsTypeDef],
    },
    total=False,
)

ListTestExecutionResultItemsResponseTypeDef = TypedDict(
    "ListTestExecutionResultItemsResponseTypeDef",
    {
        "testExecutionResults": TestExecutionResultItemsTypeDef,
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InitialResponseSettingTypeDef = TypedDict(
    "InitialResponseSettingTypeDef",
    {
        "initialResponse": ResponseSpecificationTypeDef,
        "nextStep": DialogStateTypeDef,
        "conditional": ConditionalSpecificationTypeDef,
        "codeHook": DialogCodeHookInvocationSettingTypeDef,
    },
    total=False,
)

_RequiredIntentConfirmationSettingTypeDef = TypedDict(
    "_RequiredIntentConfirmationSettingTypeDef",
    {
        "promptSpecification": PromptSpecificationTypeDef,
    },
)
_OptionalIntentConfirmationSettingTypeDef = TypedDict(
    "_OptionalIntentConfirmationSettingTypeDef",
    {
        "declinationResponse": ResponseSpecificationTypeDef,
        "active": bool,
        "confirmationResponse": ResponseSpecificationTypeDef,
        "confirmationNextStep": DialogStateTypeDef,
        "confirmationConditional": ConditionalSpecificationTypeDef,
        "declinationNextStep": DialogStateTypeDef,
        "declinationConditional": ConditionalSpecificationTypeDef,
        "failureResponse": ResponseSpecificationTypeDef,
        "failureNextStep": DialogStateTypeDef,
        "failureConditional": ConditionalSpecificationTypeDef,
        "codeHook": DialogCodeHookInvocationSettingTypeDef,
        "elicitationCodeHook": ElicitationCodeHookInvocationSettingTypeDef,
    },
    total=False,
)

class IntentConfirmationSettingTypeDef(
    _RequiredIntentConfirmationSettingTypeDef, _OptionalIntentConfirmationSettingTypeDef
):
    pass

SlotCaptureSettingTypeDef = TypedDict(
    "SlotCaptureSettingTypeDef",
    {
        "captureResponse": ResponseSpecificationTypeDef,
        "captureNextStep": DialogStateTypeDef,
        "captureConditional": ConditionalSpecificationTypeDef,
        "failureResponse": ResponseSpecificationTypeDef,
        "failureNextStep": DialogStateTypeDef,
        "failureConditional": ConditionalSpecificationTypeDef,
        "codeHook": DialogCodeHookInvocationSettingTypeDef,
        "elicitationCodeHook": ElicitationCodeHookInvocationSettingTypeDef,
    },
    total=False,
)

_RequiredCreateIntentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIntentRequestRequestTypeDef",
    {
        "intentName": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalCreateIntentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIntentRequestRequestTypeDef",
    {
        "description": str,
        "parentIntentSignature": str,
        "sampleUtterances": Sequence[SampleUtteranceTypeDef],
        "dialogCodeHook": DialogCodeHookSettingsTypeDef,
        "fulfillmentCodeHook": FulfillmentCodeHookSettingsTypeDef,
        "intentConfirmationSetting": IntentConfirmationSettingTypeDef,
        "intentClosingSetting": IntentClosingSettingTypeDef,
        "inputContexts": Sequence[InputContextTypeDef],
        "outputContexts": Sequence[OutputContextTypeDef],
        "kendraConfiguration": KendraConfigurationTypeDef,
        "initialResponseSetting": InitialResponseSettingTypeDef,
    },
    total=False,
)

class CreateIntentRequestRequestTypeDef(
    _RequiredCreateIntentRequestRequestTypeDef, _OptionalCreateIntentRequestRequestTypeDef
):
    pass

CreateIntentResponseTypeDef = TypedDict(
    "CreateIntentResponseTypeDef",
    {
        "intentId": str,
        "intentName": str,
        "description": str,
        "parentIntentSignature": str,
        "sampleUtterances": List[SampleUtteranceTypeDef],
        "dialogCodeHook": DialogCodeHookSettingsTypeDef,
        "fulfillmentCodeHook": FulfillmentCodeHookSettingsTypeDef,
        "intentConfirmationSetting": IntentConfirmationSettingTypeDef,
        "intentClosingSetting": IntentClosingSettingTypeDef,
        "inputContexts": List[InputContextTypeDef],
        "outputContexts": List[OutputContextTypeDef],
        "kendraConfiguration": KendraConfigurationTypeDef,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "creationDateTime": datetime,
        "initialResponseSetting": InitialResponseSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeIntentResponseTypeDef = TypedDict(
    "DescribeIntentResponseTypeDef",
    {
        "intentId": str,
        "intentName": str,
        "description": str,
        "parentIntentSignature": str,
        "sampleUtterances": List[SampleUtteranceTypeDef],
        "dialogCodeHook": DialogCodeHookSettingsTypeDef,
        "fulfillmentCodeHook": FulfillmentCodeHookSettingsTypeDef,
        "slotPriorities": List[SlotPriorityTypeDef],
        "intentConfirmationSetting": IntentConfirmationSettingTypeDef,
        "intentClosingSetting": IntentClosingSettingTypeDef,
        "inputContexts": List[InputContextTypeDef],
        "outputContexts": List[OutputContextTypeDef],
        "kendraConfiguration": KendraConfigurationTypeDef,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "initialResponseSetting": InitialResponseSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateIntentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateIntentRequestRequestTypeDef",
    {
        "intentId": str,
        "intentName": str,
        "botId": str,
        "botVersion": str,
        "localeId": str,
    },
)
_OptionalUpdateIntentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateIntentRequestRequestTypeDef",
    {
        "description": str,
        "parentIntentSignature": str,
        "sampleUtterances": Sequence[SampleUtteranceTypeDef],
        "dialogCodeHook": DialogCodeHookSettingsTypeDef,
        "fulfillmentCodeHook": FulfillmentCodeHookSettingsTypeDef,
        "slotPriorities": Sequence[SlotPriorityTypeDef],
        "intentConfirmationSetting": IntentConfirmationSettingTypeDef,
        "intentClosingSetting": IntentClosingSettingTypeDef,
        "inputContexts": Sequence[InputContextTypeDef],
        "outputContexts": Sequence[OutputContextTypeDef],
        "kendraConfiguration": KendraConfigurationTypeDef,
        "initialResponseSetting": InitialResponseSettingTypeDef,
    },
    total=False,
)

class UpdateIntentRequestRequestTypeDef(
    _RequiredUpdateIntentRequestRequestTypeDef, _OptionalUpdateIntentRequestRequestTypeDef
):
    pass

UpdateIntentResponseTypeDef = TypedDict(
    "UpdateIntentResponseTypeDef",
    {
        "intentId": str,
        "intentName": str,
        "description": str,
        "parentIntentSignature": str,
        "sampleUtterances": List[SampleUtteranceTypeDef],
        "dialogCodeHook": DialogCodeHookSettingsTypeDef,
        "fulfillmentCodeHook": FulfillmentCodeHookSettingsTypeDef,
        "slotPriorities": List[SlotPriorityTypeDef],
        "intentConfirmationSetting": IntentConfirmationSettingTypeDef,
        "intentClosingSetting": IntentClosingSettingTypeDef,
        "inputContexts": List[InputContextTypeDef],
        "outputContexts": List[OutputContextTypeDef],
        "kendraConfiguration": KendraConfigurationTypeDef,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "initialResponseSetting": InitialResponseSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredSlotValueElicitationSettingTypeDef = TypedDict(
    "_RequiredSlotValueElicitationSettingTypeDef",
    {
        "slotConstraint": SlotConstraintType,
    },
)
_OptionalSlotValueElicitationSettingTypeDef = TypedDict(
    "_OptionalSlotValueElicitationSettingTypeDef",
    {
        "defaultValueSpecification": SlotDefaultValueSpecificationTypeDef,
        "promptSpecification": PromptSpecificationTypeDef,
        "sampleUtterances": Sequence[SampleUtteranceTypeDef],
        "waitAndContinueSpecification": WaitAndContinueSpecificationTypeDef,
        "slotCaptureSetting": SlotCaptureSettingTypeDef,
    },
    total=False,
)

class SlotValueElicitationSettingTypeDef(
    _RequiredSlotValueElicitationSettingTypeDef, _OptionalSlotValueElicitationSettingTypeDef
):
    pass

_RequiredCreateSlotRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSlotRequestRequestTypeDef",
    {
        "slotName": str,
        "valueElicitationSetting": SlotValueElicitationSettingTypeDef,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "intentId": str,
    },
)
_OptionalCreateSlotRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSlotRequestRequestTypeDef",
    {
        "description": str,
        "slotTypeId": str,
        "obfuscationSetting": ObfuscationSettingTypeDef,
        "multipleValuesSetting": MultipleValuesSettingTypeDef,
        "subSlotSetting": SubSlotSettingTypeDef,
    },
    total=False,
)

class CreateSlotRequestRequestTypeDef(
    _RequiredCreateSlotRequestRequestTypeDef, _OptionalCreateSlotRequestRequestTypeDef
):
    pass

CreateSlotResponseTypeDef = TypedDict(
    "CreateSlotResponseTypeDef",
    {
        "slotId": str,
        "slotName": str,
        "description": str,
        "slotTypeId": str,
        "valueElicitationSetting": SlotValueElicitationSettingTypeDef,
        "obfuscationSetting": ObfuscationSettingTypeDef,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "intentId": str,
        "creationDateTime": datetime,
        "multipleValuesSetting": MultipleValuesSettingTypeDef,
        "subSlotSetting": SubSlotSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSlotResponseTypeDef = TypedDict(
    "DescribeSlotResponseTypeDef",
    {
        "slotId": str,
        "slotName": str,
        "description": str,
        "slotTypeId": str,
        "valueElicitationSetting": SlotValueElicitationSettingTypeDef,
        "obfuscationSetting": ObfuscationSettingTypeDef,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "intentId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "multipleValuesSetting": MultipleValuesSettingTypeDef,
        "subSlotSetting": SubSlotSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateSlotRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSlotRequestRequestTypeDef",
    {
        "slotId": str,
        "slotName": str,
        "valueElicitationSetting": SlotValueElicitationSettingTypeDef,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "intentId": str,
    },
)
_OptionalUpdateSlotRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSlotRequestRequestTypeDef",
    {
        "description": str,
        "slotTypeId": str,
        "obfuscationSetting": ObfuscationSettingTypeDef,
        "multipleValuesSetting": MultipleValuesSettingTypeDef,
        "subSlotSetting": SubSlotSettingTypeDef,
    },
    total=False,
)

class UpdateSlotRequestRequestTypeDef(
    _RequiredUpdateSlotRequestRequestTypeDef, _OptionalUpdateSlotRequestRequestTypeDef
):
    pass

UpdateSlotResponseTypeDef = TypedDict(
    "UpdateSlotResponseTypeDef",
    {
        "slotId": str,
        "slotName": str,
        "description": str,
        "slotTypeId": str,
        "valueElicitationSetting": SlotValueElicitationSettingTypeDef,
        "obfuscationSetting": ObfuscationSettingTypeDef,
        "botId": str,
        "botVersion": str,
        "localeId": str,
        "intentId": str,
        "creationDateTime": datetime,
        "lastUpdatedDateTime": datetime,
        "multipleValuesSetting": MultipleValuesSettingTypeDef,
        "subSlotSetting": SubSlotSettingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
