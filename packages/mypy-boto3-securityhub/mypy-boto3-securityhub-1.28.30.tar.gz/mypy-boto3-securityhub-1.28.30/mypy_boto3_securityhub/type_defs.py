"""
Type annotations for securityhub service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/type_defs/)

Usage::

    ```python
    from mypy_boto3_securityhub.type_defs import AcceptAdministratorInvitationRequestRequestTypeDef

    data: AcceptAdministratorInvitationRequestRequestTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AdminStatusType,
    AssociationStatusType,
    AutoEnableStandardsType,
    AwsIamAccessKeyStatusType,
    AwsS3BucketNotificationConfigurationS3KeyFilterRuleNameType,
    ComplianceStatusType,
    ControlFindingGeneratorType,
    ControlStatusType,
    FindingHistoryUpdateSourceTypeType,
    IntegrationTypeType,
    MalwareStateType,
    MalwareTypeType,
    MapFilterComparisonType,
    NetworkDirectionType,
    PartitionType,
    RecordStateType,
    RegionAvailabilityStatusType,
    RuleStatusType,
    SeverityLabelType,
    SeverityRatingType,
    SortOrderType,
    StandardsStatusType,
    StatusReasonCodeType,
    StringFilterComparisonType,
    ThreatIntelIndicatorCategoryType,
    ThreatIntelIndicatorTypeType,
    UnprocessedErrorCodeType,
    VerificationStateType,
    VulnerabilityExploitAvailableType,
    VulnerabilityFixAvailableType,
    WorkflowStateType,
    WorkflowStatusType,
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
    "AcceptAdministratorInvitationRequestRequestTypeDef",
    "AcceptInvitationRequestRequestTypeDef",
    "AccountDetailsTypeDef",
    "ActionLocalIpDetailsTypeDef",
    "ActionLocalPortDetailsTypeDef",
    "DnsRequestActionTypeDef",
    "CityTypeDef",
    "CountryTypeDef",
    "GeoLocationTypeDef",
    "IpOrganizationDetailsTypeDef",
    "ActionRemotePortDetailsTypeDef",
    "ActionTargetTypeDef",
    "AdjustmentTypeDef",
    "AdminAccountTypeDef",
    "AssociatedStandardTypeDef",
    "AssociationStateDetailsTypeDef",
    "NoteUpdateTypeDef",
    "RelatedFindingTypeDef",
    "SeverityUpdateTypeDef",
    "WorkflowUpdateTypeDef",
    "MapFilterTypeDef",
    "NumberFilterTypeDef",
    "StringFilterTypeDef",
    "AutomationRulesMetadataTypeDef",
    "AvailabilityZoneTypeDef",
    "AwsAmazonMqBrokerEncryptionOptionsDetailsTypeDef",
    "AwsAmazonMqBrokerLdapServerMetadataDetailsPaginatorTypeDef",
    "AwsAmazonMqBrokerMaintenanceWindowStartTimeDetailsTypeDef",
    "AwsAmazonMqBrokerUsersDetailsTypeDef",
    "AwsAmazonMqBrokerLdapServerMetadataDetailsTypeDef",
    "AwsAmazonMqBrokerLogsPendingDetailsTypeDef",
    "AwsApiCallActionDomainDetailsTypeDef",
    "AwsApiGatewayAccessLogSettingsTypeDef",
    "AwsApiGatewayCanarySettingsPaginatorTypeDef",
    "AwsApiGatewayCanarySettingsTypeDef",
    "AwsApiGatewayEndpointConfigurationPaginatorTypeDef",
    "AwsApiGatewayEndpointConfigurationTypeDef",
    "AwsApiGatewayMethodSettingsTypeDef",
    "AwsCorsConfigurationPaginatorTypeDef",
    "AwsCorsConfigurationTypeDef",
    "AwsApiGatewayV2RouteSettingsTypeDef",
    "AwsAppSyncGraphQlApiLambdaAuthorizerConfigDetailsTypeDef",
    "AwsAppSyncGraphQlApiOpenIdConnectConfigDetailsTypeDef",
    "AwsAppSyncGraphQlApiUserPoolConfigDetailsTypeDef",
    "AwsAppSyncGraphQlApiLogConfigDetailsTypeDef",
    "AwsAthenaWorkGroupConfigurationResultConfigurationEncryptionConfigurationDetailsTypeDef",
    "AwsAutoScalingAutoScalingGroupAvailabilityZonesListDetailsTypeDef",
    "AwsAutoScalingAutoScalingGroupLaunchTemplateLaunchTemplateSpecificationTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyInstancesDistributionDetailsTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateOverridesListDetailsTypeDef",
    "AwsAutoScalingLaunchConfigurationBlockDeviceMappingsEbsDetailsTypeDef",
    "AwsAutoScalingLaunchConfigurationInstanceMonitoringDetailsTypeDef",
    "AwsAutoScalingLaunchConfigurationMetadataOptionsTypeDef",
    "AwsBackupBackupPlanAdvancedBackupSettingsDetailsPaginatorTypeDef",
    "AwsBackupBackupPlanAdvancedBackupSettingsDetailsTypeDef",
    "AwsBackupBackupPlanLifecycleDetailsTypeDef",
    "AwsBackupBackupVaultNotificationsDetailsPaginatorTypeDef",
    "AwsBackupBackupVaultNotificationsDetailsTypeDef",
    "AwsBackupRecoveryPointCalculatedLifecycleDetailsTypeDef",
    "AwsBackupRecoveryPointCreatedByDetailsTypeDef",
    "AwsBackupRecoveryPointLifecycleDetailsTypeDef",
    "AwsCertificateManagerCertificateExtendedKeyUsageTypeDef",
    "AwsCertificateManagerCertificateKeyUsageTypeDef",
    "AwsCertificateManagerCertificateOptionsTypeDef",
    "AwsCertificateManagerCertificateResourceRecordTypeDef",
    "AwsCloudFormationStackDriftInformationDetailsTypeDef",
    "AwsCloudFormationStackOutputsDetailsTypeDef",
    "AwsCloudFrontDistributionCacheBehaviorTypeDef",
    "AwsCloudFrontDistributionDefaultCacheBehaviorTypeDef",
    "AwsCloudFrontDistributionLoggingTypeDef",
    "AwsCloudFrontDistributionViewerCertificateTypeDef",
    "AwsCloudFrontDistributionOriginSslProtocolsPaginatorTypeDef",
    "AwsCloudFrontDistributionOriginSslProtocolsTypeDef",
    "AwsCloudFrontDistributionOriginGroupFailoverStatusCodesPaginatorTypeDef",
    "AwsCloudFrontDistributionOriginGroupFailoverStatusCodesTypeDef",
    "AwsCloudFrontDistributionOriginS3OriginConfigTypeDef",
    "AwsCloudTrailTrailDetailsTypeDef",
    "AwsCloudWatchAlarmDimensionsDetailsTypeDef",
    "AwsCodeBuildProjectArtifactsDetailsTypeDef",
    "AwsCodeBuildProjectSourceTypeDef",
    "AwsCodeBuildProjectVpcConfigPaginatorTypeDef",
    "AwsCodeBuildProjectVpcConfigTypeDef",
    "AwsCodeBuildProjectEnvironmentEnvironmentVariablesDetailsTypeDef",
    "AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef",
    "AwsCodeBuildProjectLogsConfigCloudWatchLogsDetailsTypeDef",
    "AwsCodeBuildProjectLogsConfigS3LogsDetailsTypeDef",
    "AwsDynamoDbTableAttributeDefinitionTypeDef",
    "AwsDynamoDbTableBillingModeSummaryTypeDef",
    "AwsDynamoDbTableKeySchemaTypeDef",
    "AwsDynamoDbTableProvisionedThroughputTypeDef",
    "AwsDynamoDbTableRestoreSummaryTypeDef",
    "AwsDynamoDbTableSseDescriptionTypeDef",
    "AwsDynamoDbTableStreamSpecificationTypeDef",
    "AwsDynamoDbTableProjectionPaginatorTypeDef",
    "AwsDynamoDbTableProjectionTypeDef",
    "AwsDynamoDbTableProvisionedThroughputOverrideTypeDef",
    "AwsEc2EipDetailsTypeDef",
    "AwsEc2InstanceMetadataOptionsTypeDef",
    "AwsEc2InstanceMonitoringDetailsTypeDef",
    "AwsEc2InstanceNetworkInterfacesDetailsTypeDef",
    "AwsEc2LaunchTemplateDataBlockDeviceMappingSetEbsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataCapacityReservationSpecificationCapacityReservationTargetDetailsTypeDef",
    "AwsEc2LaunchTemplateDataCpuOptionsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataCreditSpecificationDetailsTypeDef",
    "AwsEc2LaunchTemplateDataElasticGpuSpecificationSetDetailsTypeDef",
    "AwsEc2LaunchTemplateDataElasticInferenceAcceleratorSetDetailsTypeDef",
    "AwsEc2LaunchTemplateDataEnclaveOptionsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataHibernationOptionsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataIamInstanceProfileDetailsTypeDef",
    "AwsEc2LaunchTemplateDataLicenseSetDetailsTypeDef",
    "AwsEc2LaunchTemplateDataMaintenanceOptionsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataMetadataOptionsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataMonitoringDetailsTypeDef",
    "AwsEc2LaunchTemplateDataPlacementDetailsTypeDef",
    "AwsEc2LaunchTemplateDataPrivateDnsNameOptionsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceMarketOptionsSpotOptionsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceRequirementsAcceleratorCountDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceRequirementsAcceleratorTotalMemoryMiBDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceRequirementsBaselineEbsBandwidthMbpsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceRequirementsMemoryGiBPerVCpuDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceRequirementsMemoryMiBDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceRequirementsNetworkInterfaceCountDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceRequirementsTotalLocalStorageGBDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceRequirementsVCpuCountDetailsTypeDef",
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv4PrefixesDetailsTypeDef",
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv6AddressesDetailsTypeDef",
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv6PrefixesDetailsTypeDef",
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetPrivateIpAddressesDetailsTypeDef",
    "AwsEc2NetworkAclAssociationTypeDef",
    "IcmpTypeCodeTypeDef",
    "PortRangeFromToTypeDef",
    "AwsEc2NetworkInterfaceAttachmentTypeDef",
    "AwsEc2NetworkInterfaceIpV6AddressDetailTypeDef",
    "AwsEc2NetworkInterfacePrivateIpAddressDetailTypeDef",
    "AwsEc2NetworkInterfaceSecurityGroupTypeDef",
    "PropagatingVgwSetDetailsTypeDef",
    "RouteSetDetailsTypeDef",
    "AwsEc2SecurityGroupIpRangeTypeDef",
    "AwsEc2SecurityGroupIpv6RangeTypeDef",
    "AwsEc2SecurityGroupPrefixListIdTypeDef",
    "AwsEc2SecurityGroupUserIdGroupPairTypeDef",
    "Ipv6CidrBlockAssociationTypeDef",
    "AwsEc2TransitGatewayDetailsPaginatorTypeDef",
    "AwsEc2TransitGatewayDetailsTypeDef",
    "AwsEc2VolumeAttachmentTypeDef",
    "CidrBlockAssociationTypeDef",
    "AwsEc2VpcEndpointServiceServiceTypeDetailsTypeDef",
    "AwsEc2VpcPeeringConnectionStatusDetailsTypeDef",
    "VpcInfoCidrBlockSetDetailsTypeDef",
    "VpcInfoIpv6CidrBlockSetDetailsTypeDef",
    "VpcInfoPeeringOptionsDetailsTypeDef",
    "AwsEc2VpnConnectionRoutesDetailsTypeDef",
    "AwsEc2VpnConnectionVgwTelemetryDetailsTypeDef",
    "AwsEc2VpnConnectionOptionsTunnelOptionsDetailsPaginatorTypeDef",
    "AwsEc2VpnConnectionOptionsTunnelOptionsDetailsTypeDef",
    "AwsEcrContainerImageDetailsPaginatorTypeDef",
    "AwsEcrContainerImageDetailsTypeDef",
    "AwsEcrRepositoryImageScanningConfigurationDetailsTypeDef",
    "AwsEcrRepositoryLifecyclePolicyDetailsTypeDef",
    "AwsEcsClusterClusterSettingsDetailsTypeDef",
    "AwsEcsClusterConfigurationExecuteCommandConfigurationLogConfigurationDetailsTypeDef",
    "AwsEcsClusterDefaultCapacityProviderStrategyDetailsTypeDef",
    "AwsMountPointTypeDef",
    "AwsEcsServiceCapacityProviderStrategyDetailsTypeDef",
    "AwsEcsServiceDeploymentConfigurationDeploymentCircuitBreakerDetailsTypeDef",
    "AwsEcsServiceDeploymentControllerDetailsTypeDef",
    "AwsEcsServiceLoadBalancersDetailsTypeDef",
    "AwsEcsServicePlacementConstraintsDetailsTypeDef",
    "AwsEcsServicePlacementStrategiesDetailsTypeDef",
    "AwsEcsServiceServiceRegistriesDetailsTypeDef",
    "AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsPaginatorTypeDef",
    "AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsDependsOnDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsEnvironmentDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsEnvironmentFilesDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsExtraHostsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsMountPointsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsPortMappingsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsRepositoryCredentialsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsResourceRequirementsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsSecretsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsSystemControlsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsUlimitsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsVolumesFromDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationSecretOptionsDetailsTypeDef",
    "AwsEcsTaskDefinitionInferenceAcceleratorsDetailsTypeDef",
    "AwsEcsTaskDefinitionPlacementConstraintsDetailsTypeDef",
    "AwsEcsTaskDefinitionProxyConfigurationProxyConfigurationPropertiesDetailsTypeDef",
    "AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionVolumesHostDetailsTypeDef",
    "AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationAuthorizationConfigDetailsTypeDef",
    "AwsEcsTaskVolumeHostDetailsTypeDef",
    "AwsEfsAccessPointPosixUserDetailsPaginatorTypeDef",
    "AwsEfsAccessPointPosixUserDetailsTypeDef",
    "AwsEfsAccessPointRootDirectoryCreationInfoDetailsTypeDef",
    "AwsEksClusterResourcesVpcConfigDetailsPaginatorTypeDef",
    "AwsEksClusterResourcesVpcConfigDetailsTypeDef",
    "AwsEksClusterLoggingClusterLoggingDetailsPaginatorTypeDef",
    "AwsEksClusterLoggingClusterLoggingDetailsTypeDef",
    "AwsElasticBeanstalkEnvironmentEnvironmentLinkTypeDef",
    "AwsElasticBeanstalkEnvironmentOptionSettingTypeDef",
    "AwsElasticBeanstalkEnvironmentTierTypeDef",
    "AwsElasticsearchDomainDomainEndpointOptionsTypeDef",
    "AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef",
    "AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef",
    "AwsElasticsearchDomainServiceSoftwareOptionsTypeDef",
    "AwsElasticsearchDomainVPCOptionsPaginatorTypeDef",
    "AwsElasticsearchDomainVPCOptionsTypeDef",
    "AwsElasticsearchDomainElasticsearchClusterConfigZoneAwarenessConfigDetailsTypeDef",
    "AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef",
    "AwsElbAppCookieStickinessPolicyTypeDef",
    "AwsElbLbCookieStickinessPolicyTypeDef",
    "AwsElbLoadBalancerAccessLogTypeDef",
    "AwsElbLoadBalancerAdditionalAttributeTypeDef",
    "AwsElbLoadBalancerConnectionDrainingTypeDef",
    "AwsElbLoadBalancerConnectionSettingsTypeDef",
    "AwsElbLoadBalancerCrossZoneLoadBalancingTypeDef",
    "AwsElbLoadBalancerBackendServerDescriptionPaginatorTypeDef",
    "AwsElbLoadBalancerBackendServerDescriptionTypeDef",
    "AwsElbLoadBalancerHealthCheckTypeDef",
    "AwsElbLoadBalancerInstanceTypeDef",
    "AwsElbLoadBalancerSourceSecurityGroupTypeDef",
    "AwsElbLoadBalancerListenerTypeDef",
    "AwsElbv2LoadBalancerAttributeTypeDef",
    "LoadBalancerStateTypeDef",
    "AwsEventSchemasRegistryDetailsTypeDef",
    "AwsGuardDutyDetectorDataSourcesCloudTrailDetailsTypeDef",
    "AwsGuardDutyDetectorDataSourcesDnsLogsDetailsTypeDef",
    "AwsGuardDutyDetectorDataSourcesFlowLogsDetailsTypeDef",
    "AwsGuardDutyDetectorDataSourcesS3LogsDetailsTypeDef",
    "AwsGuardDutyDetectorDataSourcesKubernetesAuditLogsDetailsTypeDef",
    "AwsGuardDutyDetectorDataSourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesDetailsTypeDef",
    "AwsGuardDutyDetectorFeaturesDetailsTypeDef",
    "AwsIamAccessKeySessionContextAttributesTypeDef",
    "AwsIamAccessKeySessionContextSessionIssuerTypeDef",
    "AwsIamAttachedManagedPolicyTypeDef",
    "AwsIamGroupPolicyTypeDef",
    "AwsIamInstanceProfileRolePaginatorTypeDef",
    "DictOrStrTypeDef",
    "AwsIamPermissionsBoundaryTypeDef",
    "AwsIamPolicyVersionTypeDef",
    "AwsIamRolePolicyTypeDef",
    "AwsIamUserPolicyTypeDef",
    "AwsKinesisStreamStreamEncryptionDetailsTypeDef",
    "AwsKmsKeyDetailsTypeDef",
    "AwsLambdaFunctionCodeTypeDef",
    "AwsLambdaFunctionDeadLetterConfigTypeDef",
    "AwsLambdaFunctionLayerTypeDef",
    "AwsLambdaFunctionTracingConfigTypeDef",
    "AwsLambdaFunctionVpcConfigPaginatorTypeDef",
    "AwsLambdaFunctionVpcConfigTypeDef",
    "AwsLambdaFunctionEnvironmentErrorTypeDef",
    "AwsLambdaLayerVersionDetailsPaginatorTypeDef",
    "AwsLambdaLayerVersionDetailsTypeDef",
    "AwsNetworkFirewallFirewallSubnetMappingsDetailsTypeDef",
    "AwsOpenSearchServiceDomainMasterUserOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainClusterConfigZoneAwarenessConfigDetailsTypeDef",
    "AwsOpenSearchServiceDomainDomainEndpointOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainEncryptionAtRestOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainNodeToNodeEncryptionOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainServiceSoftwareOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainVpcOptionsDetailsPaginatorTypeDef",
    "AwsOpenSearchServiceDomainVpcOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainLogPublishingOptionTypeDef",
    "AwsRdsDbClusterAssociatedRoleTypeDef",
    "AwsRdsDbClusterMemberTypeDef",
    "AwsRdsDbClusterOptionGroupMembershipTypeDef",
    "AwsRdsDbDomainMembershipTypeDef",
    "AwsRdsDbInstanceVpcSecurityGroupTypeDef",
    "AwsRdsDbClusterSnapshotDbClusterSnapshotAttributePaginatorTypeDef",
    "AwsRdsDbClusterSnapshotDbClusterSnapshotAttributeTypeDef",
    "AwsRdsDbInstanceAssociatedRoleTypeDef",
    "AwsRdsDbInstanceEndpointTypeDef",
    "AwsRdsDbOptionGroupMembershipTypeDef",
    "AwsRdsDbParameterGroupTypeDef",
    "AwsRdsDbProcessorFeatureTypeDef",
    "AwsRdsDbStatusInfoTypeDef",
    "AwsRdsPendingCloudWatchLogsExportsPaginatorTypeDef",
    "AwsRdsPendingCloudWatchLogsExportsTypeDef",
    "AwsRdsDbSecurityGroupEc2SecurityGroupTypeDef",
    "AwsRdsDbSecurityGroupIpRangeTypeDef",
    "AwsRdsDbSubnetGroupSubnetAvailabilityZoneTypeDef",
    "AwsRdsEventSubscriptionDetailsPaginatorTypeDef",
    "AwsRdsEventSubscriptionDetailsTypeDef",
    "AwsRedshiftClusterClusterNodeTypeDef",
    "AwsRedshiftClusterClusterParameterStatusTypeDef",
    "AwsRedshiftClusterClusterSecurityGroupTypeDef",
    "AwsRedshiftClusterClusterSnapshotCopyStatusTypeDef",
    "AwsRedshiftClusterDeferredMaintenanceWindowTypeDef",
    "AwsRedshiftClusterElasticIpStatusTypeDef",
    "AwsRedshiftClusterEndpointTypeDef",
    "AwsRedshiftClusterHsmStatusTypeDef",
    "AwsRedshiftClusterIamRoleTypeDef",
    "AwsRedshiftClusterLoggingStatusTypeDef",
    "AwsRedshiftClusterPendingModifiedValuesTypeDef",
    "AwsRedshiftClusterResizeInfoTypeDef",
    "AwsRedshiftClusterRestoreStatusTypeDef",
    "AwsRedshiftClusterVpcSecurityGroupTypeDef",
    "AwsS3AccountPublicAccessBlockDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesAbortIncompleteMultipartUploadDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesNoncurrentVersionTransitionsDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesTransitionsDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateTagDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsTagDetailsTypeDef",
    "AwsS3BucketBucketVersioningConfigurationTypeDef",
    "AwsS3BucketLoggingConfigurationTypeDef",
    "AwsS3BucketNotificationConfigurationS3KeyFilterRuleTypeDef",
    "AwsS3BucketObjectLockConfigurationRuleDefaultRetentionDetailsTypeDef",
    "AwsS3BucketServerSideEncryptionByDefaultTypeDef",
    "AwsS3BucketWebsiteConfigurationRedirectToTypeDef",
    "AwsS3BucketWebsiteConfigurationRoutingRuleConditionTypeDef",
    "AwsS3BucketWebsiteConfigurationRoutingRuleRedirectTypeDef",
    "AwsS3ObjectDetailsTypeDef",
    "AwsSageMakerNotebookInstanceMetadataServiceConfigurationDetailsTypeDef",
    "AwsSecretsManagerSecretRotationRulesTypeDef",
    "BooleanFilterTypeDef",
    "IpFilterTypeDef",
    "KeywordFilterTypeDef",
    "AwsSecurityFindingIdentifierTypeDef",
    "GeneratorDetailsPaginatorTypeDef",
    "MalwareTypeDef",
    "NoteTypeDef",
    "PatchSummaryTypeDef",
    "ProcessDetailsTypeDef",
    "SeverityTypeDef",
    "ThreatIntelIndicatorTypeDef",
    "WorkflowTypeDef",
    "GeneratorDetailsTypeDef",
    "AwsSnsTopicSubscriptionTypeDef",
    "AwsSqsQueueDetailsTypeDef",
    "AwsSsmComplianceSummaryTypeDef",
    "AwsStepFunctionStateMachineTracingConfigurationDetailsTypeDef",
    "AwsStepFunctionStateMachineLoggingConfigurationDestinationsCloudWatchLogsLogGroupDetailsTypeDef",
    "AwsWafRateBasedRuleMatchPredicateTypeDef",
    "AwsWafRegionalRateBasedRuleMatchPredicateTypeDef",
    "AwsWafRegionalRulePredicateListDetailsTypeDef",
    "AwsWafRegionalRuleGroupRulesActionDetailsTypeDef",
    "AwsWafRegionalWebAclRulesListActionDetailsTypeDef",
    "AwsWafRegionalWebAclRulesListOverrideActionDetailsTypeDef",
    "AwsWafRulePredicateListDetailsTypeDef",
    "AwsWafRuleGroupRulesActionDetailsTypeDef",
    "WafActionTypeDef",
    "WafExcludedRuleTypeDef",
    "WafOverrideActionTypeDef",
    "AwsWafv2CustomHttpHeaderTypeDef",
    "AwsWafv2VisibilityConfigDetailsTypeDef",
    "AwsWafv2WebAclCaptchaConfigImmunityTimePropertyDetailsTypeDef",
    "AwsXrayEncryptionConfigDetailsTypeDef",
    "BatchDeleteAutomationRulesRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "UnprocessedAutomationRuleTypeDef",
    "BatchDisableStandardsRequestRequestTypeDef",
    "StandardsSubscriptionRequestTypeDef",
    "BatchGetAutomationRulesRequestRequestTypeDef",
    "BatchGetSecurityControlsRequestRequestTypeDef",
    "SecurityControlTypeDef",
    "UnprocessedSecurityControlTypeDef",
    "StandardsControlAssociationIdTypeDef",
    "StandardsControlAssociationDetailTypeDef",
    "ImportFindingsErrorTypeDef",
    "StandardsControlAssociationUpdateTypeDef",
    "CellTypeDef",
    "ClassificationStatusTypeDef",
    "CodeVulnerabilitiesFilePathTypeDef",
    "StatusReasonTypeDef",
    "VolumeMountTypeDef",
    "CreateActionTargetRequestRequestTypeDef",
    "CreateFindingAggregatorRequestRequestTypeDef",
    "ResultTypeDef",
    "DateRangeTypeDef",
    "DeclineInvitationsRequestRequestTypeDef",
    "DeleteActionTargetRequestRequestTypeDef",
    "DeleteFindingAggregatorRequestRequestTypeDef",
    "DeleteInsightRequestRequestTypeDef",
    "DeleteInvitationsRequestRequestTypeDef",
    "DeleteMembersRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeActionTargetsRequestRequestTypeDef",
    "DescribeHubRequestRequestTypeDef",
    "DescribeProductsRequestRequestTypeDef",
    "ProductTypeDef",
    "DescribeStandardsControlsRequestRequestTypeDef",
    "StandardsControlTypeDef",
    "DescribeStandardsRequestRequestTypeDef",
    "DisableImportFindingsForProductRequestRequestTypeDef",
    "DisableOrganizationAdminAccountRequestRequestTypeDef",
    "DisassociateMembersRequestRequestTypeDef",
    "EnableImportFindingsForProductRequestRequestTypeDef",
    "EnableOrganizationAdminAccountRequestRequestTypeDef",
    "EnableSecurityHubRequestRequestTypeDef",
    "FilePathsTypeDef",
    "FindingAggregatorTypeDef",
    "FindingHistoryUpdateSourceTypeDef",
    "FindingHistoryUpdateTypeDef",
    "FindingProviderSeverityTypeDef",
    "FirewallPolicyStatefulRuleGroupReferencesDetailsTypeDef",
    "FirewallPolicyStatelessRuleGroupReferencesDetailsTypeDef",
    "InvitationTypeDef",
    "GetEnabledStandardsRequestRequestTypeDef",
    "GetFindingAggregatorRequestRequestTypeDef",
    "TimestampTypeDef",
    "SortCriterionTypeDef",
    "GetInsightResultsRequestRequestTypeDef",
    "GetInsightsRequestRequestTypeDef",
    "GetMembersRequestRequestTypeDef",
    "MemberTypeDef",
    "InsightResultValueTypeDef",
    "InviteMembersRequestRequestTypeDef",
    "ListAutomationRulesRequestRequestTypeDef",
    "ListEnabledProductsForImportRequestRequestTypeDef",
    "ListFindingAggregatorsRequestRequestTypeDef",
    "ListInvitationsRequestRequestTypeDef",
    "ListMembersRequestRequestTypeDef",
    "ListOrganizationAdminAccountsRequestRequestTypeDef",
    "ListSecurityControlDefinitionsRequestRequestTypeDef",
    "SecurityControlDefinitionTypeDef",
    "ListStandardsControlAssociationsRequestRequestTypeDef",
    "StandardsControlAssociationSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PortRangeTypeDef",
    "RangeTypeDef",
    "RecordTypeDef",
    "RecommendationTypeDef",
    "RuleGroupSourceListDetailsPaginatorTypeDef",
    "RuleGroupSourceListDetailsTypeDef",
    "RuleGroupSourceStatefulRulesHeaderDetailsTypeDef",
    "RuleGroupSourceStatefulRulesOptionsDetailsPaginatorTypeDef",
    "RuleGroupSourceStatefulRulesOptionsDetailsTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesDestinationPortsTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesDestinationsTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesSourcePortsTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesSourcesTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsPaginatorTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsTypeDef",
    "RuleGroupVariablesIpSetsDetailsPaginatorTypeDef",
    "RuleGroupVariablesIpSetsDetailsTypeDef",
    "RuleGroupVariablesPortSetsDetailsPaginatorTypeDef",
    "RuleGroupVariablesPortSetsDetailsTypeDef",
    "SoftwarePackageTypeDef",
    "StandardsManagedByTypeDef",
    "StandardsStatusReasonTypeDef",
    "StatelessCustomPublishMetricActionDimensionTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateActionTargetRequestRequestTypeDef",
    "UpdateFindingAggregatorRequestRequestTypeDef",
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    "UpdateSecurityHubConfigurationRequestRequestTypeDef",
    "UpdateStandardsControlRequestRequestTypeDef",
    "VulnerabilityVendorTypeDef",
    "CreateMembersRequestRequestTypeDef",
    "ActionRemoteIpDetailsTypeDef",
    "CvssPaginatorTypeDef",
    "CvssTypeDef",
    "AssociationSetDetailsTypeDef",
    "AutomationRulesFindingFieldsUpdateTypeDef",
    "AwsAmazonMqBrokerLogsDetailsTypeDef",
    "AwsApiGatewayRestApiDetailsPaginatorTypeDef",
    "AwsApiGatewayRestApiDetailsTypeDef",
    "AwsApiGatewayStageDetailsPaginatorTypeDef",
    "AwsApiGatewayStageDetailsTypeDef",
    "AwsApiGatewayV2ApiDetailsPaginatorTypeDef",
    "AwsApiGatewayV2ApiDetailsTypeDef",
    "AwsApiGatewayV2StageDetailsPaginatorTypeDef",
    "AwsApiGatewayV2StageDetailsTypeDef",
    "AwsAppSyncGraphQlApiAdditionalAuthenticationProvidersDetailsTypeDef",
    "AwsAthenaWorkGroupConfigurationResultConfigurationDetailsTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsPaginatorTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsTypeDef",
    "AwsAutoScalingLaunchConfigurationBlockDeviceMappingsDetailsTypeDef",
    "AwsBackupBackupPlanRuleCopyActionsDetailsTypeDef",
    "AwsBackupBackupVaultDetailsPaginatorTypeDef",
    "AwsBackupBackupVaultDetailsTypeDef",
    "AwsBackupRecoveryPointDetailsTypeDef",
    "AwsCertificateManagerCertificateDomainValidationOptionPaginatorTypeDef",
    "AwsCertificateManagerCertificateDomainValidationOptionTypeDef",
    "AwsCloudFormationStackDetailsPaginatorTypeDef",
    "AwsCloudFormationStackDetailsTypeDef",
    "AwsCloudFrontDistributionCacheBehaviorsPaginatorTypeDef",
    "AwsCloudFrontDistributionCacheBehaviorsTypeDef",
    "AwsCloudFrontDistributionOriginCustomOriginConfigPaginatorTypeDef",
    "AwsCloudFrontDistributionOriginCustomOriginConfigTypeDef",
    "AwsCloudFrontDistributionOriginGroupFailoverPaginatorTypeDef",
    "AwsCloudFrontDistributionOriginGroupFailoverTypeDef",
    "AwsCloudWatchAlarmDetailsPaginatorTypeDef",
    "AwsCloudWatchAlarmDetailsTypeDef",
    "AwsCodeBuildProjectEnvironmentPaginatorTypeDef",
    "AwsCodeBuildProjectEnvironmentTypeDef",
    "AwsCodeBuildProjectLogsConfigDetailsTypeDef",
    "AwsDynamoDbTableGlobalSecondaryIndexPaginatorTypeDef",
    "AwsDynamoDbTableLocalSecondaryIndexPaginatorTypeDef",
    "AwsDynamoDbTableGlobalSecondaryIndexTypeDef",
    "AwsDynamoDbTableLocalSecondaryIndexTypeDef",
    "AwsDynamoDbTableReplicaGlobalSecondaryIndexTypeDef",
    "AwsEc2InstanceDetailsPaginatorTypeDef",
    "AwsEc2InstanceDetailsTypeDef",
    "AwsEc2LaunchTemplateDataBlockDeviceMappingSetDetailsTypeDef",
    "AwsEc2LaunchTemplateDataCapacityReservationSpecificationDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceMarketOptionsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataInstanceRequirementsDetailsPaginatorTypeDef",
    "AwsEc2LaunchTemplateDataInstanceRequirementsDetailsTypeDef",
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetDetailsPaginatorTypeDef",
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetDetailsTypeDef",
    "AwsEc2NetworkAclEntryTypeDef",
    "AwsEc2NetworkInterfaceDetailsPaginatorTypeDef",
    "AwsEc2NetworkInterfaceDetailsTypeDef",
    "AwsEc2SecurityGroupIpPermissionPaginatorTypeDef",
    "AwsEc2SecurityGroupIpPermissionTypeDef",
    "AwsEc2SubnetDetailsPaginatorTypeDef",
    "AwsEc2SubnetDetailsTypeDef",
    "AwsEc2VolumeDetailsPaginatorTypeDef",
    "AwsEc2VolumeDetailsTypeDef",
    "AwsEc2VpcDetailsPaginatorTypeDef",
    "AwsEc2VpcDetailsTypeDef",
    "AwsEc2VpcEndpointServiceDetailsPaginatorTypeDef",
    "AwsEc2VpcEndpointServiceDetailsTypeDef",
    "AwsEc2VpcPeeringConnectionVpcInfoDetailsPaginatorTypeDef",
    "AwsEc2VpcPeeringConnectionVpcInfoDetailsTypeDef",
    "AwsEc2VpnConnectionOptionsDetailsPaginatorTypeDef",
    "AwsEc2VpnConnectionOptionsDetailsTypeDef",
    "AwsEcrRepositoryDetailsTypeDef",
    "AwsEcsClusterConfigurationExecuteCommandConfigurationDetailsTypeDef",
    "AwsEcsContainerDetailsPaginatorTypeDef",
    "AwsEcsContainerDetailsTypeDef",
    "AwsEcsServiceDeploymentConfigurationDetailsTypeDef",
    "AwsEcsServiceNetworkConfigurationDetailsPaginatorTypeDef",
    "AwsEcsServiceNetworkConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionProxyConfigurationDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionProxyConfigurationDetailsTypeDef",
    "AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationDetailsTypeDef",
    "AwsEcsTaskVolumeDetailsTypeDef",
    "AwsEfsAccessPointRootDirectoryDetailsTypeDef",
    "AwsEksClusterLoggingDetailsPaginatorTypeDef",
    "AwsEksClusterLoggingDetailsTypeDef",
    "AwsElasticBeanstalkEnvironmentDetailsPaginatorTypeDef",
    "AwsElasticBeanstalkEnvironmentDetailsTypeDef",
    "AwsElasticsearchDomainElasticsearchClusterConfigDetailsTypeDef",
    "AwsElasticsearchDomainLogPublishingOptionsTypeDef",
    "AwsElbLoadBalancerPoliciesPaginatorTypeDef",
    "AwsElbLoadBalancerPoliciesTypeDef",
    "AwsElbLoadBalancerAttributesPaginatorTypeDef",
    "AwsElbLoadBalancerAttributesTypeDef",
    "AwsElbLoadBalancerListenerDescriptionPaginatorTypeDef",
    "AwsElbLoadBalancerListenerDescriptionTypeDef",
    "AwsElbv2LoadBalancerDetailsPaginatorTypeDef",
    "AwsElbv2LoadBalancerDetailsTypeDef",
    "AwsGuardDutyDetectorDataSourcesKubernetesDetailsTypeDef",
    "AwsGuardDutyDetectorDataSourcesMalwareProtectionScanEc2InstanceWithFindingsDetailsTypeDef",
    "AwsIamAccessKeySessionContextTypeDef",
    "AwsIamGroupDetailsPaginatorTypeDef",
    "AwsIamGroupDetailsTypeDef",
    "AwsIamInstanceProfilePaginatorTypeDef",
    "AwsIamInstanceProfileRoleTypeDef",
    "AwsIamPolicyDetailsPaginatorTypeDef",
    "AwsIamPolicyDetailsTypeDef",
    "AwsIamUserDetailsPaginatorTypeDef",
    "AwsIamUserDetailsTypeDef",
    "AwsKinesisStreamDetailsTypeDef",
    "AwsLambdaFunctionEnvironmentPaginatorTypeDef",
    "AwsLambdaFunctionEnvironmentTypeDef",
    "AwsNetworkFirewallFirewallDetailsPaginatorTypeDef",
    "AwsNetworkFirewallFirewallDetailsTypeDef",
    "AwsOpenSearchServiceDomainAdvancedSecurityOptionsDetailsTypeDef",
    "AwsOpenSearchServiceDomainClusterConfigDetailsTypeDef",
    "AwsOpenSearchServiceDomainLogPublishingOptionsDetailsTypeDef",
    "AwsRdsDbClusterDetailsPaginatorTypeDef",
    "AwsRdsDbClusterDetailsTypeDef",
    "AwsRdsDbClusterSnapshotDetailsPaginatorTypeDef",
    "AwsRdsDbClusterSnapshotDetailsTypeDef",
    "AwsRdsDbSnapshotDetailsPaginatorTypeDef",
    "AwsRdsDbSnapshotDetailsTypeDef",
    "AwsRdsDbPendingModifiedValuesPaginatorTypeDef",
    "AwsRdsDbPendingModifiedValuesTypeDef",
    "AwsRdsDbSecurityGroupDetailsPaginatorTypeDef",
    "AwsRdsDbSecurityGroupDetailsTypeDef",
    "AwsRdsDbSubnetGroupSubnetTypeDef",
    "AwsRedshiftClusterClusterParameterGroupPaginatorTypeDef",
    "AwsRedshiftClusterClusterParameterGroupTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsDetailsTypeDef",
    "AwsS3BucketNotificationConfigurationS3KeyFilterPaginatorTypeDef",
    "AwsS3BucketNotificationConfigurationS3KeyFilterTypeDef",
    "AwsS3BucketObjectLockConfigurationRuleDetailsTypeDef",
    "AwsS3BucketServerSideEncryptionRuleTypeDef",
    "AwsS3BucketWebsiteConfigurationRoutingRuleTypeDef",
    "AwsSageMakerNotebookInstanceDetailsPaginatorTypeDef",
    "AwsSageMakerNotebookInstanceDetailsTypeDef",
    "AwsSecretsManagerSecretDetailsTypeDef",
    "BatchUpdateFindingsRequestRequestTypeDef",
    "BatchUpdateFindingsUnprocessedFindingTypeDef",
    "AwsSnsTopicDetailsPaginatorTypeDef",
    "AwsSnsTopicDetailsTypeDef",
    "AwsSsmPatchTypeDef",
    "AwsStepFunctionStateMachineLoggingConfigurationDestinationsDetailsTypeDef",
    "AwsWafRateBasedRuleDetailsPaginatorTypeDef",
    "AwsWafRateBasedRuleDetailsTypeDef",
    "AwsWafRegionalRateBasedRuleDetailsPaginatorTypeDef",
    "AwsWafRegionalRateBasedRuleDetailsTypeDef",
    "AwsWafRegionalRuleDetailsPaginatorTypeDef",
    "AwsWafRegionalRuleDetailsTypeDef",
    "AwsWafRegionalRuleGroupRulesDetailsTypeDef",
    "AwsWafRegionalWebAclRulesListDetailsTypeDef",
    "AwsWafRuleDetailsPaginatorTypeDef",
    "AwsWafRuleDetailsTypeDef",
    "AwsWafRuleGroupRulesDetailsTypeDef",
    "AwsWafWebAclRulePaginatorTypeDef",
    "AwsWafWebAclRuleTypeDef",
    "AwsWafv2CustomRequestHandlingDetailsPaginatorTypeDef",
    "AwsWafv2CustomRequestHandlingDetailsTypeDef",
    "AwsWafv2CustomResponseDetailsPaginatorTypeDef",
    "AwsWafv2CustomResponseDetailsTypeDef",
    "AwsWafv2WebAclCaptchaConfigDetailsTypeDef",
    "CreateActionTargetResponseTypeDef",
    "CreateAutomationRuleResponseTypeDef",
    "CreateFindingAggregatorResponseTypeDef",
    "CreateInsightResponseTypeDef",
    "DeleteActionTargetResponseTypeDef",
    "DeleteInsightResponseTypeDef",
    "DescribeActionTargetsResponseTypeDef",
    "DescribeHubResponseTypeDef",
    "DescribeOrganizationConfigurationResponseTypeDef",
    "EnableImportFindingsForProductResponseTypeDef",
    "GetFindingAggregatorResponseTypeDef",
    "GetInvitationsCountResponseTypeDef",
    "ListAutomationRulesResponseTypeDef",
    "ListEnabledProductsForImportResponseTypeDef",
    "ListOrganizationAdminAccountsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateFindingAggregatorResponseTypeDef",
    "BatchDeleteAutomationRulesResponseTypeDef",
    "BatchUpdateAutomationRulesResponseTypeDef",
    "BatchEnableStandardsRequestRequestTypeDef",
    "BatchGetSecurityControlsResponseTypeDef",
    "BatchGetStandardsControlAssociationsRequestRequestTypeDef",
    "UnprocessedStandardsControlAssociationTypeDef",
    "BatchImportFindingsResponseTypeDef",
    "BatchUpdateStandardsControlAssociationsRequestRequestTypeDef",
    "UnprocessedStandardsControlAssociationUpdateTypeDef",
    "VulnerabilityCodeVulnerabilitiesPaginatorTypeDef",
    "VulnerabilityCodeVulnerabilitiesTypeDef",
    "CompliancePaginatorTypeDef",
    "ComplianceTypeDef",
    "ContainerDetailsPaginatorTypeDef",
    "ContainerDetailsTypeDef",
    "CreateMembersResponseTypeDef",
    "DeclineInvitationsResponseTypeDef",
    "DeleteInvitationsResponseTypeDef",
    "DeleteMembersResponseTypeDef",
    "InviteMembersResponseTypeDef",
    "DateFilterTypeDef",
    "DescribeActionTargetsRequestDescribeActionTargetsPaginateTypeDef",
    "DescribeProductsRequestDescribeProductsPaginateTypeDef",
    "DescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef",
    "DescribeStandardsRequestDescribeStandardsPaginateTypeDef",
    "GetEnabledStandardsRequestGetEnabledStandardsPaginateTypeDef",
    "GetInsightsRequestGetInsightsPaginateTypeDef",
    "ListEnabledProductsForImportRequestListEnabledProductsForImportPaginateTypeDef",
    "ListFindingAggregatorsRequestListFindingAggregatorsPaginateTypeDef",
    "ListInvitationsRequestListInvitationsPaginateTypeDef",
    "ListMembersRequestListMembersPaginateTypeDef",
    "ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef",
    "ListSecurityControlDefinitionsRequestListSecurityControlDefinitionsPaginateTypeDef",
    "ListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef",
    "DescribeProductsResponseTypeDef",
    "DescribeStandardsControlsResponseTypeDef",
    "ThreatPaginatorTypeDef",
    "ThreatTypeDef",
    "ListFindingAggregatorsResponseTypeDef",
    "FindingHistoryRecordTypeDef",
    "FindingProviderFieldsPaginatorTypeDef",
    "FindingProviderFieldsTypeDef",
    "GetAdministratorAccountResponseTypeDef",
    "GetMasterAccountResponseTypeDef",
    "ListInvitationsResponseTypeDef",
    "GetFindingHistoryRequestGetFindingHistoryPaginateTypeDef",
    "GetFindingHistoryRequestRequestTypeDef",
    "GetMembersResponseTypeDef",
    "ListMembersResponseTypeDef",
    "InsightResultsTypeDef",
    "ListSecurityControlDefinitionsResponseTypeDef",
    "ListStandardsControlAssociationsResponseTypeDef",
    "NetworkPathComponentDetailsPaginatorTypeDef",
    "NetworkPathComponentDetailsTypeDef",
    "NetworkTypeDef",
    "PageTypeDef",
    "RemediationTypeDef",
    "RuleGroupSourceStatefulRulesDetailsPaginatorTypeDef",
    "RuleGroupSourceStatefulRulesDetailsTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesPaginatorTypeDef",
    "RuleGroupSourceStatelessRuleMatchAttributesTypeDef",
    "RuleGroupVariablesPaginatorTypeDef",
    "RuleGroupVariablesTypeDef",
    "StandardTypeDef",
    "StandardsSubscriptionTypeDef",
    "StatelessCustomPublishMetricActionPaginatorTypeDef",
    "StatelessCustomPublishMetricActionTypeDef",
    "AwsApiCallActionPaginatorTypeDef",
    "AwsApiCallActionTypeDef",
    "NetworkConnectionActionTypeDef",
    "PortProbeDetailTypeDef",
    "AwsEc2RouteTableDetailsPaginatorTypeDef",
    "AwsEc2RouteTableDetailsTypeDef",
    "AutomationRulesActionTypeDef",
    "AwsAmazonMqBrokerDetailsPaginatorTypeDef",
    "AwsAmazonMqBrokerDetailsTypeDef",
    "AwsAppSyncGraphQlApiDetailsPaginatorTypeDef",
    "AwsAppSyncGraphQlApiDetailsTypeDef",
    "AwsAthenaWorkGroupConfigurationDetailsTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsPaginatorTypeDef",
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsTypeDef",
    "AwsAutoScalingLaunchConfigurationDetailsPaginatorTypeDef",
    "AwsAutoScalingLaunchConfigurationDetailsTypeDef",
    "AwsBackupBackupPlanRuleDetailsPaginatorTypeDef",
    "AwsBackupBackupPlanRuleDetailsTypeDef",
    "AwsCertificateManagerCertificateRenewalSummaryPaginatorTypeDef",
    "AwsCertificateManagerCertificateRenewalSummaryTypeDef",
    "AwsCloudFrontDistributionOriginItemPaginatorTypeDef",
    "AwsCloudFrontDistributionOriginItemTypeDef",
    "AwsCloudFrontDistributionOriginGroupPaginatorTypeDef",
    "AwsCloudFrontDistributionOriginGroupTypeDef",
    "AwsCodeBuildProjectDetailsPaginatorTypeDef",
    "AwsCodeBuildProjectDetailsTypeDef",
    "AwsDynamoDbTableReplicaPaginatorTypeDef",
    "AwsDynamoDbTableReplicaTypeDef",
    "AwsEc2LaunchTemplateDataDetailsPaginatorTypeDef",
    "AwsEc2LaunchTemplateDataDetailsTypeDef",
    "AwsEc2NetworkAclDetailsPaginatorTypeDef",
    "AwsEc2NetworkAclDetailsTypeDef",
    "AwsEc2SecurityGroupDetailsPaginatorTypeDef",
    "AwsEc2SecurityGroupDetailsTypeDef",
    "AwsEc2VpcPeeringConnectionDetailsPaginatorTypeDef",
    "AwsEc2VpcPeeringConnectionDetailsTypeDef",
    "AwsEc2VpnConnectionDetailsPaginatorTypeDef",
    "AwsEc2VpnConnectionDetailsTypeDef",
    "AwsEcsClusterConfigurationDetailsTypeDef",
    "AwsEcsServiceDetailsPaginatorTypeDef",
    "AwsEcsServiceDetailsTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionContainerDefinitionsDetailsTypeDef",
    "AwsEcsTaskDefinitionVolumesDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionVolumesDetailsTypeDef",
    "AwsEcsTaskDetailsPaginatorTypeDef",
    "AwsEcsTaskDetailsTypeDef",
    "AwsEfsAccessPointDetailsPaginatorTypeDef",
    "AwsEfsAccessPointDetailsTypeDef",
    "AwsEksClusterDetailsPaginatorTypeDef",
    "AwsEksClusterDetailsTypeDef",
    "AwsElasticsearchDomainDetailsPaginatorTypeDef",
    "AwsElasticsearchDomainDetailsTypeDef",
    "AwsElbLoadBalancerDetailsPaginatorTypeDef",
    "AwsElbLoadBalancerDetailsTypeDef",
    "AwsGuardDutyDetectorDataSourcesMalwareProtectionDetailsTypeDef",
    "AwsIamAccessKeyDetailsTypeDef",
    "AwsIamRoleDetailsPaginatorTypeDef",
    "AwsIamInstanceProfileTypeDef",
    "AwsLambdaFunctionDetailsPaginatorTypeDef",
    "AwsLambdaFunctionDetailsTypeDef",
    "AwsOpenSearchServiceDomainDetailsPaginatorTypeDef",
    "AwsOpenSearchServiceDomainDetailsTypeDef",
    "AwsRdsDbSubnetGroupPaginatorTypeDef",
    "AwsRdsDbSubnetGroupTypeDef",
    "AwsRedshiftClusterDetailsPaginatorTypeDef",
    "AwsRedshiftClusterDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsPaginatorTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsTypeDef",
    "AwsS3BucketNotificationConfigurationFilterPaginatorTypeDef",
    "AwsS3BucketNotificationConfigurationFilterTypeDef",
    "AwsS3BucketObjectLockConfigurationTypeDef",
    "AwsS3BucketServerSideEncryptionConfigurationPaginatorTypeDef",
    "AwsS3BucketServerSideEncryptionConfigurationTypeDef",
    "AwsS3BucketWebsiteConfigurationPaginatorTypeDef",
    "AwsS3BucketWebsiteConfigurationTypeDef",
    "BatchUpdateFindingsResponseTypeDef",
    "AwsSsmPatchComplianceDetailsTypeDef",
    "AwsStepFunctionStateMachineLoggingConfigurationDetailsPaginatorTypeDef",
    "AwsStepFunctionStateMachineLoggingConfigurationDetailsTypeDef",
    "AwsWafRegionalRuleGroupDetailsPaginatorTypeDef",
    "AwsWafRegionalRuleGroupDetailsTypeDef",
    "AwsWafRegionalWebAclDetailsPaginatorTypeDef",
    "AwsWafRegionalWebAclDetailsTypeDef",
    "AwsWafRuleGroupDetailsPaginatorTypeDef",
    "AwsWafRuleGroupDetailsTypeDef",
    "AwsWafWebAclDetailsPaginatorTypeDef",
    "AwsWafWebAclDetailsTypeDef",
    "AwsWafv2ActionAllowDetailsPaginatorTypeDef",
    "AwsWafv2RulesActionCaptchaDetailsPaginatorTypeDef",
    "AwsWafv2RulesActionCountDetailsPaginatorTypeDef",
    "AwsWafv2ActionAllowDetailsTypeDef",
    "AwsWafv2RulesActionCaptchaDetailsTypeDef",
    "AwsWafv2RulesActionCountDetailsTypeDef",
    "AwsWafv2ActionBlockDetailsPaginatorTypeDef",
    "AwsWafv2ActionBlockDetailsTypeDef",
    "BatchGetStandardsControlAssociationsResponseTypeDef",
    "BatchUpdateStandardsControlAssociationsResponseTypeDef",
    "VulnerabilityPaginatorTypeDef",
    "VulnerabilityTypeDef",
    "AutomationRulesFindingFiltersTypeDef",
    "AwsSecurityFindingFiltersTypeDef",
    "GetFindingHistoryResponseTypeDef",
    "GetInsightResultsResponseTypeDef",
    "NetworkHeaderPaginatorTypeDef",
    "NetworkHeaderTypeDef",
    "OccurrencesPaginatorTypeDef",
    "OccurrencesTypeDef",
    "RuleGroupSourceStatelessRuleDefinitionPaginatorTypeDef",
    "RuleGroupSourceStatelessRuleDefinitionTypeDef",
    "DescribeStandardsResponseTypeDef",
    "BatchDisableStandardsResponseTypeDef",
    "BatchEnableStandardsResponseTypeDef",
    "GetEnabledStandardsResponseTypeDef",
    "StatelessCustomActionDefinitionPaginatorTypeDef",
    "StatelessCustomActionDefinitionTypeDef",
    "PortProbeActionPaginatorTypeDef",
    "PortProbeActionTypeDef",
    "AwsAthenaWorkGroupDetailsTypeDef",
    "AwsAutoScalingAutoScalingGroupDetailsPaginatorTypeDef",
    "AwsAutoScalingAutoScalingGroupDetailsTypeDef",
    "AwsBackupBackupPlanBackupPlanDetailsPaginatorTypeDef",
    "AwsBackupBackupPlanBackupPlanDetailsTypeDef",
    "AwsCertificateManagerCertificateDetailsPaginatorTypeDef",
    "AwsCertificateManagerCertificateDetailsTypeDef",
    "AwsCloudFrontDistributionOriginsPaginatorTypeDef",
    "AwsCloudFrontDistributionOriginsTypeDef",
    "AwsCloudFrontDistributionOriginGroupsPaginatorTypeDef",
    "AwsCloudFrontDistributionOriginGroupsTypeDef",
    "AwsDynamoDbTableDetailsPaginatorTypeDef",
    "AwsDynamoDbTableDetailsTypeDef",
    "AwsEc2LaunchTemplateDetailsPaginatorTypeDef",
    "AwsEc2LaunchTemplateDetailsTypeDef",
    "AwsEcsClusterDetailsPaginatorTypeDef",
    "AwsEcsClusterDetailsTypeDef",
    "AwsEcsTaskDefinitionDetailsPaginatorTypeDef",
    "AwsEcsTaskDefinitionDetailsTypeDef",
    "AwsGuardDutyDetectorDataSourcesDetailsTypeDef",
    "AwsIamRoleDetailsTypeDef",
    "AwsRdsDbInstanceDetailsPaginatorTypeDef",
    "AwsRdsDbInstanceDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsPaginatorTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsTypeDef",
    "AwsS3BucketNotificationConfigurationDetailPaginatorTypeDef",
    "AwsS3BucketNotificationConfigurationDetailTypeDef",
    "AwsStepFunctionStateMachineDetailsPaginatorTypeDef",
    "AwsStepFunctionStateMachineDetailsTypeDef",
    "AwsWafv2RulesActionDetailsPaginatorTypeDef",
    "AwsWafv2WebAclActionDetailsPaginatorTypeDef",
    "AwsWafv2RulesActionDetailsTypeDef",
    "AwsWafv2WebAclActionDetailsTypeDef",
    "AutomationRulesConfigTypeDef",
    "CreateAutomationRuleRequestRequestTypeDef",
    "UpdateAutomationRulesRequestItemTypeDef",
    "CreateInsightRequestRequestTypeDef",
    "GetFindingsRequestGetFindingsPaginateTypeDef",
    "GetFindingsRequestRequestTypeDef",
    "InsightTypeDef",
    "UpdateFindingsRequestRequestTypeDef",
    "UpdateInsightRequestRequestTypeDef",
    "NetworkPathComponentPaginatorTypeDef",
    "NetworkPathComponentTypeDef",
    "CustomDataIdentifiersDetectionsPaginatorTypeDef",
    "SensitiveDataDetectionsPaginatorTypeDef",
    "CustomDataIdentifiersDetectionsTypeDef",
    "SensitiveDataDetectionsTypeDef",
    "RuleGroupSourceStatelessRulesDetailsPaginatorTypeDef",
    "RuleGroupSourceStatelessRulesDetailsTypeDef",
    "FirewallPolicyStatelessCustomActionsDetailsPaginatorTypeDef",
    "RuleGroupSourceCustomActionsDetailsPaginatorTypeDef",
    "FirewallPolicyStatelessCustomActionsDetailsTypeDef",
    "RuleGroupSourceCustomActionsDetailsTypeDef",
    "ActionPaginatorTypeDef",
    "ActionTypeDef",
    "AwsBackupBackupPlanDetailsPaginatorTypeDef",
    "AwsBackupBackupPlanDetailsTypeDef",
    "AwsCloudFrontDistributionDetailsPaginatorTypeDef",
    "AwsCloudFrontDistributionDetailsTypeDef",
    "AwsGuardDutyDetectorDetailsPaginatorTypeDef",
    "AwsGuardDutyDetectorDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesDetailsPaginatorTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationRulesDetailsTypeDef",
    "AwsS3BucketNotificationConfigurationPaginatorTypeDef",
    "AwsS3BucketNotificationConfigurationTypeDef",
    "AwsWafv2RulesDetailsPaginatorTypeDef",
    "AwsWafv2RulesDetailsTypeDef",
    "BatchGetAutomationRulesResponseTypeDef",
    "BatchUpdateAutomationRulesRequestRequestTypeDef",
    "GetInsightsResponseTypeDef",
    "CustomDataIdentifiersResultPaginatorTypeDef",
    "SensitiveDataResultPaginatorTypeDef",
    "CustomDataIdentifiersResultTypeDef",
    "SensitiveDataResultTypeDef",
    "FirewallPolicyDetailsPaginatorTypeDef",
    "RuleGroupSourceStatelessRulesAndCustomActionsDetailsPaginatorTypeDef",
    "FirewallPolicyDetailsTypeDef",
    "RuleGroupSourceStatelessRulesAndCustomActionsDetailsTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationDetailsPaginatorTypeDef",
    "AwsS3BucketBucketLifecycleConfigurationDetailsTypeDef",
    "AwsWafv2RuleGroupDetailsPaginatorTypeDef",
    "AwsWafv2WebAclDetailsPaginatorTypeDef",
    "AwsWafv2RuleGroupDetailsTypeDef",
    "AwsWafv2WebAclDetailsTypeDef",
    "ClassificationResultPaginatorTypeDef",
    "ClassificationResultTypeDef",
    "AwsNetworkFirewallFirewallPolicyDetailsPaginatorTypeDef",
    "RuleGroupSourcePaginatorTypeDef",
    "AwsNetworkFirewallFirewallPolicyDetailsTypeDef",
    "RuleGroupSourceTypeDef",
    "AwsS3BucketDetailsPaginatorTypeDef",
    "AwsS3BucketDetailsTypeDef",
    "DataClassificationDetailsPaginatorTypeDef",
    "DataClassificationDetailsTypeDef",
    "RuleGroupDetailsPaginatorTypeDef",
    "RuleGroupDetailsTypeDef",
    "AwsNetworkFirewallRuleGroupDetailsPaginatorTypeDef",
    "AwsNetworkFirewallRuleGroupDetailsTypeDef",
    "ResourceDetailsPaginatorTypeDef",
    "ResourceDetailsTypeDef",
    "ResourcePaginatorTypeDef",
    "ResourceTypeDef",
    "AwsSecurityFindingPaginatorTypeDef",
    "AwsSecurityFindingTypeDef",
    "GetFindingsResponsePaginatorTypeDef",
    "BatchImportFindingsRequestRequestTypeDef",
    "GetFindingsResponseTypeDef",
)

AcceptAdministratorInvitationRequestRequestTypeDef = TypedDict(
    "AcceptAdministratorInvitationRequestRequestTypeDef",
    {
        "AdministratorId": str,
        "InvitationId": str,
    },
)

AcceptInvitationRequestRequestTypeDef = TypedDict(
    "AcceptInvitationRequestRequestTypeDef",
    {
        "MasterId": str,
        "InvitationId": str,
    },
)

_RequiredAccountDetailsTypeDef = TypedDict(
    "_RequiredAccountDetailsTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalAccountDetailsTypeDef = TypedDict(
    "_OptionalAccountDetailsTypeDef",
    {
        "Email": str,
    },
    total=False,
)


class AccountDetailsTypeDef(_RequiredAccountDetailsTypeDef, _OptionalAccountDetailsTypeDef):
    pass


ActionLocalIpDetailsTypeDef = TypedDict(
    "ActionLocalIpDetailsTypeDef",
    {
        "IpAddressV4": str,
    },
    total=False,
)

ActionLocalPortDetailsTypeDef = TypedDict(
    "ActionLocalPortDetailsTypeDef",
    {
        "Port": int,
        "PortName": str,
    },
    total=False,
)

DnsRequestActionTypeDef = TypedDict(
    "DnsRequestActionTypeDef",
    {
        "Domain": str,
        "Protocol": str,
        "Blocked": bool,
    },
    total=False,
)

CityTypeDef = TypedDict(
    "CityTypeDef",
    {
        "CityName": str,
    },
    total=False,
)

CountryTypeDef = TypedDict(
    "CountryTypeDef",
    {
        "CountryCode": str,
        "CountryName": str,
    },
    total=False,
)

GeoLocationTypeDef = TypedDict(
    "GeoLocationTypeDef",
    {
        "Lon": float,
        "Lat": float,
    },
    total=False,
)

IpOrganizationDetailsTypeDef = TypedDict(
    "IpOrganizationDetailsTypeDef",
    {
        "Asn": int,
        "AsnOrg": str,
        "Isp": str,
        "Org": str,
    },
    total=False,
)

ActionRemotePortDetailsTypeDef = TypedDict(
    "ActionRemotePortDetailsTypeDef",
    {
        "Port": int,
        "PortName": str,
    },
    total=False,
)

ActionTargetTypeDef = TypedDict(
    "ActionTargetTypeDef",
    {
        "ActionTargetArn": str,
        "Name": str,
        "Description": str,
    },
)

AdjustmentTypeDef = TypedDict(
    "AdjustmentTypeDef",
    {
        "Metric": str,
        "Reason": str,
    },
    total=False,
)

AdminAccountTypeDef = TypedDict(
    "AdminAccountTypeDef",
    {
        "AccountId": str,
        "Status": AdminStatusType,
    },
    total=False,
)

AssociatedStandardTypeDef = TypedDict(
    "AssociatedStandardTypeDef",
    {
        "StandardsId": str,
    },
    total=False,
)

AssociationStateDetailsTypeDef = TypedDict(
    "AssociationStateDetailsTypeDef",
    {
        "State": str,
        "StatusMessage": str,
    },
    total=False,
)

NoteUpdateTypeDef = TypedDict(
    "NoteUpdateTypeDef",
    {
        "Text": str,
        "UpdatedBy": str,
    },
)

RelatedFindingTypeDef = TypedDict(
    "RelatedFindingTypeDef",
    {
        "ProductArn": str,
        "Id": str,
    },
)

SeverityUpdateTypeDef = TypedDict(
    "SeverityUpdateTypeDef",
    {
        "Normalized": int,
        "Product": float,
        "Label": SeverityLabelType,
    },
    total=False,
)

WorkflowUpdateTypeDef = TypedDict(
    "WorkflowUpdateTypeDef",
    {
        "Status": WorkflowStatusType,
    },
    total=False,
)

MapFilterTypeDef = TypedDict(
    "MapFilterTypeDef",
    {
        "Key": str,
        "Value": str,
        "Comparison": MapFilterComparisonType,
    },
    total=False,
)

NumberFilterTypeDef = TypedDict(
    "NumberFilterTypeDef",
    {
        "Gte": float,
        "Lte": float,
        "Eq": float,
    },
    total=False,
)

StringFilterTypeDef = TypedDict(
    "StringFilterTypeDef",
    {
        "Value": str,
        "Comparison": StringFilterComparisonType,
    },
    total=False,
)

AutomationRulesMetadataTypeDef = TypedDict(
    "AutomationRulesMetadataTypeDef",
    {
        "RuleArn": str,
        "RuleStatus": RuleStatusType,
        "RuleOrder": int,
        "RuleName": str,
        "Description": str,
        "IsTerminal": bool,
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "CreatedBy": str,
    },
    total=False,
)

AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "ZoneName": str,
        "SubnetId": str,
    },
    total=False,
)

AwsAmazonMqBrokerEncryptionOptionsDetailsTypeDef = TypedDict(
    "AwsAmazonMqBrokerEncryptionOptionsDetailsTypeDef",
    {
        "KmsKeyId": str,
        "UseAwsOwnedKey": bool,
    },
    total=False,
)

AwsAmazonMqBrokerLdapServerMetadataDetailsPaginatorTypeDef = TypedDict(
    "AwsAmazonMqBrokerLdapServerMetadataDetailsPaginatorTypeDef",
    {
        "Hosts": List[str],
        "RoleBase": str,
        "RoleName": str,
        "RoleSearchMatching": str,
        "RoleSearchSubtree": bool,
        "ServiceAccountUsername": str,
        "UserBase": str,
        "UserRoleName": str,
        "UserSearchMatching": str,
        "UserSearchSubtree": bool,
    },
    total=False,
)

AwsAmazonMqBrokerMaintenanceWindowStartTimeDetailsTypeDef = TypedDict(
    "AwsAmazonMqBrokerMaintenanceWindowStartTimeDetailsTypeDef",
    {
        "DayOfWeek": str,
        "TimeOfDay": str,
        "TimeZone": str,
    },
    total=False,
)

AwsAmazonMqBrokerUsersDetailsTypeDef = TypedDict(
    "AwsAmazonMqBrokerUsersDetailsTypeDef",
    {
        "PendingChange": str,
        "Username": str,
    },
    total=False,
)

AwsAmazonMqBrokerLdapServerMetadataDetailsTypeDef = TypedDict(
    "AwsAmazonMqBrokerLdapServerMetadataDetailsTypeDef",
    {
        "Hosts": Sequence[str],
        "RoleBase": str,
        "RoleName": str,
        "RoleSearchMatching": str,
        "RoleSearchSubtree": bool,
        "ServiceAccountUsername": str,
        "UserBase": str,
        "UserRoleName": str,
        "UserSearchMatching": str,
        "UserSearchSubtree": bool,
    },
    total=False,
)

AwsAmazonMqBrokerLogsPendingDetailsTypeDef = TypedDict(
    "AwsAmazonMqBrokerLogsPendingDetailsTypeDef",
    {
        "Audit": bool,
        "General": bool,
    },
    total=False,
)

AwsApiCallActionDomainDetailsTypeDef = TypedDict(
    "AwsApiCallActionDomainDetailsTypeDef",
    {
        "Domain": str,
    },
    total=False,
)

AwsApiGatewayAccessLogSettingsTypeDef = TypedDict(
    "AwsApiGatewayAccessLogSettingsTypeDef",
    {
        "Format": str,
        "DestinationArn": str,
    },
    total=False,
)

AwsApiGatewayCanarySettingsPaginatorTypeDef = TypedDict(
    "AwsApiGatewayCanarySettingsPaginatorTypeDef",
    {
        "PercentTraffic": float,
        "DeploymentId": str,
        "StageVariableOverrides": Dict[str, str],
        "UseStageCache": bool,
    },
    total=False,
)

AwsApiGatewayCanarySettingsTypeDef = TypedDict(
    "AwsApiGatewayCanarySettingsTypeDef",
    {
        "PercentTraffic": float,
        "DeploymentId": str,
        "StageVariableOverrides": Mapping[str, str],
        "UseStageCache": bool,
    },
    total=False,
)

AwsApiGatewayEndpointConfigurationPaginatorTypeDef = TypedDict(
    "AwsApiGatewayEndpointConfigurationPaginatorTypeDef",
    {
        "Types": List[str],
    },
    total=False,
)

AwsApiGatewayEndpointConfigurationTypeDef = TypedDict(
    "AwsApiGatewayEndpointConfigurationTypeDef",
    {
        "Types": Sequence[str],
    },
    total=False,
)

AwsApiGatewayMethodSettingsTypeDef = TypedDict(
    "AwsApiGatewayMethodSettingsTypeDef",
    {
        "MetricsEnabled": bool,
        "LoggingLevel": str,
        "DataTraceEnabled": bool,
        "ThrottlingBurstLimit": int,
        "ThrottlingRateLimit": float,
        "CachingEnabled": bool,
        "CacheTtlInSeconds": int,
        "CacheDataEncrypted": bool,
        "RequireAuthorizationForCacheControl": bool,
        "UnauthorizedCacheControlHeaderStrategy": str,
        "HttpMethod": str,
        "ResourcePath": str,
    },
    total=False,
)

AwsCorsConfigurationPaginatorTypeDef = TypedDict(
    "AwsCorsConfigurationPaginatorTypeDef",
    {
        "AllowOrigins": List[str],
        "AllowCredentials": bool,
        "ExposeHeaders": List[str],
        "MaxAge": int,
        "AllowMethods": List[str],
        "AllowHeaders": List[str],
    },
    total=False,
)

AwsCorsConfigurationTypeDef = TypedDict(
    "AwsCorsConfigurationTypeDef",
    {
        "AllowOrigins": Sequence[str],
        "AllowCredentials": bool,
        "ExposeHeaders": Sequence[str],
        "MaxAge": int,
        "AllowMethods": Sequence[str],
        "AllowHeaders": Sequence[str],
    },
    total=False,
)

AwsApiGatewayV2RouteSettingsTypeDef = TypedDict(
    "AwsApiGatewayV2RouteSettingsTypeDef",
    {
        "DetailedMetricsEnabled": bool,
        "LoggingLevel": str,
        "DataTraceEnabled": bool,
        "ThrottlingBurstLimit": int,
        "ThrottlingRateLimit": float,
    },
    total=False,
)

AwsAppSyncGraphQlApiLambdaAuthorizerConfigDetailsTypeDef = TypedDict(
    "AwsAppSyncGraphQlApiLambdaAuthorizerConfigDetailsTypeDef",
    {
        "AuthorizerResultTtlInSeconds": int,
        "AuthorizerUri": str,
        "IdentityValidationExpression": str,
    },
    total=False,
)

AwsAppSyncGraphQlApiOpenIdConnectConfigDetailsTypeDef = TypedDict(
    "AwsAppSyncGraphQlApiOpenIdConnectConfigDetailsTypeDef",
    {
        "AuthTtL": int,
        "ClientId": str,
        "IatTtL": int,
        "Issuer": str,
    },
    total=False,
)

AwsAppSyncGraphQlApiUserPoolConfigDetailsTypeDef = TypedDict(
    "AwsAppSyncGraphQlApiUserPoolConfigDetailsTypeDef",
    {
        "AppIdClientRegex": str,
        "AwsRegion": str,
        "DefaultAction": str,
        "UserPoolId": str,
    },
    total=False,
)

AwsAppSyncGraphQlApiLogConfigDetailsTypeDef = TypedDict(
    "AwsAppSyncGraphQlApiLogConfigDetailsTypeDef",
    {
        "CloudWatchLogsRoleArn": str,
        "ExcludeVerboseContent": bool,
        "FieldLogLevel": str,
    },
    total=False,
)

AwsAthenaWorkGroupConfigurationResultConfigurationEncryptionConfigurationDetailsTypeDef = TypedDict(
    "AwsAthenaWorkGroupConfigurationResultConfigurationEncryptionConfigurationDetailsTypeDef",
    {
        "EncryptionOption": str,
        "KmsKey": str,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupAvailabilityZonesListDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupAvailabilityZonesListDetailsTypeDef",
    {
        "Value": str,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupLaunchTemplateLaunchTemplateSpecificationTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupLaunchTemplateLaunchTemplateSpecificationTypeDef",
    {
        "LaunchTemplateId": str,
        "LaunchTemplateName": str,
        "Version": str,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyInstancesDistributionDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyInstancesDistributionDetailsTypeDef",
    {
        "OnDemandAllocationStrategy": str,
        "OnDemandBaseCapacity": int,
        "OnDemandPercentageAboveBaseCapacity": int,
        "SpotAllocationStrategy": str,
        "SpotInstancePools": int,
        "SpotMaxPrice": str,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationTypeDef",
    {
        "LaunchTemplateId": str,
        "LaunchTemplateName": str,
        "Version": str,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateOverridesListDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateOverridesListDetailsTypeDef",
    {
        "InstanceType": str,
        "WeightedCapacity": str,
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationBlockDeviceMappingsEbsDetailsTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationBlockDeviceMappingsEbsDetailsTypeDef",
    {
        "DeleteOnTermination": bool,
        "Encrypted": bool,
        "Iops": int,
        "SnapshotId": str,
        "VolumeSize": int,
        "VolumeType": str,
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationInstanceMonitoringDetailsTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationInstanceMonitoringDetailsTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationMetadataOptionsTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationMetadataOptionsTypeDef",
    {
        "HttpEndpoint": str,
        "HttpPutResponseHopLimit": int,
        "HttpTokens": str,
    },
    total=False,
)

AwsBackupBackupPlanAdvancedBackupSettingsDetailsPaginatorTypeDef = TypedDict(
    "AwsBackupBackupPlanAdvancedBackupSettingsDetailsPaginatorTypeDef",
    {
        "BackupOptions": Dict[str, str],
        "ResourceType": str,
    },
    total=False,
)

AwsBackupBackupPlanAdvancedBackupSettingsDetailsTypeDef = TypedDict(
    "AwsBackupBackupPlanAdvancedBackupSettingsDetailsTypeDef",
    {
        "BackupOptions": Mapping[str, str],
        "ResourceType": str,
    },
    total=False,
)

AwsBackupBackupPlanLifecycleDetailsTypeDef = TypedDict(
    "AwsBackupBackupPlanLifecycleDetailsTypeDef",
    {
        "DeleteAfterDays": int,
        "MoveToColdStorageAfterDays": int,
    },
    total=False,
)

AwsBackupBackupVaultNotificationsDetailsPaginatorTypeDef = TypedDict(
    "AwsBackupBackupVaultNotificationsDetailsPaginatorTypeDef",
    {
        "BackupVaultEvents": List[str],
        "SnsTopicArn": str,
    },
    total=False,
)

AwsBackupBackupVaultNotificationsDetailsTypeDef = TypedDict(
    "AwsBackupBackupVaultNotificationsDetailsTypeDef",
    {
        "BackupVaultEvents": Sequence[str],
        "SnsTopicArn": str,
    },
    total=False,
)

AwsBackupRecoveryPointCalculatedLifecycleDetailsTypeDef = TypedDict(
    "AwsBackupRecoveryPointCalculatedLifecycleDetailsTypeDef",
    {
        "DeleteAt": str,
        "MoveToColdStorageAt": str,
    },
    total=False,
)

AwsBackupRecoveryPointCreatedByDetailsTypeDef = TypedDict(
    "AwsBackupRecoveryPointCreatedByDetailsTypeDef",
    {
        "BackupPlanArn": str,
        "BackupPlanId": str,
        "BackupPlanVersion": str,
        "BackupRuleId": str,
    },
    total=False,
)

AwsBackupRecoveryPointLifecycleDetailsTypeDef = TypedDict(
    "AwsBackupRecoveryPointLifecycleDetailsTypeDef",
    {
        "DeleteAfterDays": int,
        "MoveToColdStorageAfterDays": int,
    },
    total=False,
)

AwsCertificateManagerCertificateExtendedKeyUsageTypeDef = TypedDict(
    "AwsCertificateManagerCertificateExtendedKeyUsageTypeDef",
    {
        "Name": str,
        "OId": str,
    },
    total=False,
)

AwsCertificateManagerCertificateKeyUsageTypeDef = TypedDict(
    "AwsCertificateManagerCertificateKeyUsageTypeDef",
    {
        "Name": str,
    },
    total=False,
)

AwsCertificateManagerCertificateOptionsTypeDef = TypedDict(
    "AwsCertificateManagerCertificateOptionsTypeDef",
    {
        "CertificateTransparencyLoggingPreference": str,
    },
    total=False,
)

AwsCertificateManagerCertificateResourceRecordTypeDef = TypedDict(
    "AwsCertificateManagerCertificateResourceRecordTypeDef",
    {
        "Name": str,
        "Type": str,
        "Value": str,
    },
    total=False,
)

AwsCloudFormationStackDriftInformationDetailsTypeDef = TypedDict(
    "AwsCloudFormationStackDriftInformationDetailsTypeDef",
    {
        "StackDriftStatus": str,
    },
    total=False,
)

AwsCloudFormationStackOutputsDetailsTypeDef = TypedDict(
    "AwsCloudFormationStackOutputsDetailsTypeDef",
    {
        "Description": str,
        "OutputKey": str,
        "OutputValue": str,
    },
    total=False,
)

AwsCloudFrontDistributionCacheBehaviorTypeDef = TypedDict(
    "AwsCloudFrontDistributionCacheBehaviorTypeDef",
    {
        "ViewerProtocolPolicy": str,
    },
    total=False,
)

AwsCloudFrontDistributionDefaultCacheBehaviorTypeDef = TypedDict(
    "AwsCloudFrontDistributionDefaultCacheBehaviorTypeDef",
    {
        "ViewerProtocolPolicy": str,
    },
    total=False,
)

AwsCloudFrontDistributionLoggingTypeDef = TypedDict(
    "AwsCloudFrontDistributionLoggingTypeDef",
    {
        "Bucket": str,
        "Enabled": bool,
        "IncludeCookies": bool,
        "Prefix": str,
    },
    total=False,
)

AwsCloudFrontDistributionViewerCertificateTypeDef = TypedDict(
    "AwsCloudFrontDistributionViewerCertificateTypeDef",
    {
        "AcmCertificateArn": str,
        "Certificate": str,
        "CertificateSource": str,
        "CloudFrontDefaultCertificate": bool,
        "IamCertificateId": str,
        "MinimumProtocolVersion": str,
        "SslSupportMethod": str,
    },
    total=False,
)

AwsCloudFrontDistributionOriginSslProtocolsPaginatorTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginSslProtocolsPaginatorTypeDef",
    {
        "Items": List[str],
        "Quantity": int,
    },
    total=False,
)

AwsCloudFrontDistributionOriginSslProtocolsTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginSslProtocolsTypeDef",
    {
        "Items": Sequence[str],
        "Quantity": int,
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupFailoverStatusCodesPaginatorTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupFailoverStatusCodesPaginatorTypeDef",
    {
        "Items": List[int],
        "Quantity": int,
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupFailoverStatusCodesTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupFailoverStatusCodesTypeDef",
    {
        "Items": Sequence[int],
        "Quantity": int,
    },
    total=False,
)

AwsCloudFrontDistributionOriginS3OriginConfigTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginS3OriginConfigTypeDef",
    {
        "OriginAccessIdentity": str,
    },
    total=False,
)

AwsCloudTrailTrailDetailsTypeDef = TypedDict(
    "AwsCloudTrailTrailDetailsTypeDef",
    {
        "CloudWatchLogsLogGroupArn": str,
        "CloudWatchLogsRoleArn": str,
        "HasCustomEventSelectors": bool,
        "HomeRegion": str,
        "IncludeGlobalServiceEvents": bool,
        "IsMultiRegionTrail": bool,
        "IsOrganizationTrail": bool,
        "KmsKeyId": str,
        "LogFileValidationEnabled": bool,
        "Name": str,
        "S3BucketName": str,
        "S3KeyPrefix": str,
        "SnsTopicArn": str,
        "SnsTopicName": str,
        "TrailArn": str,
    },
    total=False,
)

AwsCloudWatchAlarmDimensionsDetailsTypeDef = TypedDict(
    "AwsCloudWatchAlarmDimensionsDetailsTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AwsCodeBuildProjectArtifactsDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectArtifactsDetailsTypeDef",
    {
        "ArtifactIdentifier": str,
        "EncryptionDisabled": bool,
        "Location": str,
        "Name": str,
        "NamespaceType": str,
        "OverrideArtifactName": bool,
        "Packaging": str,
        "Path": str,
        "Type": str,
    },
    total=False,
)

AwsCodeBuildProjectSourceTypeDef = TypedDict(
    "AwsCodeBuildProjectSourceTypeDef",
    {
        "Type": str,
        "Location": str,
        "GitCloneDepth": int,
        "InsecureSsl": bool,
    },
    total=False,
)

AwsCodeBuildProjectVpcConfigPaginatorTypeDef = TypedDict(
    "AwsCodeBuildProjectVpcConfigPaginatorTypeDef",
    {
        "VpcId": str,
        "Subnets": List[str],
        "SecurityGroupIds": List[str],
    },
    total=False,
)

AwsCodeBuildProjectVpcConfigTypeDef = TypedDict(
    "AwsCodeBuildProjectVpcConfigTypeDef",
    {
        "VpcId": str,
        "Subnets": Sequence[str],
        "SecurityGroupIds": Sequence[str],
    },
    total=False,
)

AwsCodeBuildProjectEnvironmentEnvironmentVariablesDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectEnvironmentEnvironmentVariablesDetailsTypeDef",
    {
        "Name": str,
        "Type": str,
        "Value": str,
    },
    total=False,
)

AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef = TypedDict(
    "AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef",
    {
        "Credential": str,
        "CredentialProvider": str,
    },
    total=False,
)

AwsCodeBuildProjectLogsConfigCloudWatchLogsDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectLogsConfigCloudWatchLogsDetailsTypeDef",
    {
        "GroupName": str,
        "Status": str,
        "StreamName": str,
    },
    total=False,
)

AwsCodeBuildProjectLogsConfigS3LogsDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectLogsConfigS3LogsDetailsTypeDef",
    {
        "EncryptionDisabled": bool,
        "Location": str,
        "Status": str,
    },
    total=False,
)

AwsDynamoDbTableAttributeDefinitionTypeDef = TypedDict(
    "AwsDynamoDbTableAttributeDefinitionTypeDef",
    {
        "AttributeName": str,
        "AttributeType": str,
    },
    total=False,
)

AwsDynamoDbTableBillingModeSummaryTypeDef = TypedDict(
    "AwsDynamoDbTableBillingModeSummaryTypeDef",
    {
        "BillingMode": str,
        "LastUpdateToPayPerRequestDateTime": str,
    },
    total=False,
)

AwsDynamoDbTableKeySchemaTypeDef = TypedDict(
    "AwsDynamoDbTableKeySchemaTypeDef",
    {
        "AttributeName": str,
        "KeyType": str,
    },
    total=False,
)

AwsDynamoDbTableProvisionedThroughputTypeDef = TypedDict(
    "AwsDynamoDbTableProvisionedThroughputTypeDef",
    {
        "LastDecreaseDateTime": str,
        "LastIncreaseDateTime": str,
        "NumberOfDecreasesToday": int,
        "ReadCapacityUnits": int,
        "WriteCapacityUnits": int,
    },
    total=False,
)

AwsDynamoDbTableRestoreSummaryTypeDef = TypedDict(
    "AwsDynamoDbTableRestoreSummaryTypeDef",
    {
        "SourceBackupArn": str,
        "SourceTableArn": str,
        "RestoreDateTime": str,
        "RestoreInProgress": bool,
    },
    total=False,
)

AwsDynamoDbTableSseDescriptionTypeDef = TypedDict(
    "AwsDynamoDbTableSseDescriptionTypeDef",
    {
        "InaccessibleEncryptionDateTime": str,
        "Status": str,
        "SseType": str,
        "KmsMasterKeyArn": str,
    },
    total=False,
)

AwsDynamoDbTableStreamSpecificationTypeDef = TypedDict(
    "AwsDynamoDbTableStreamSpecificationTypeDef",
    {
        "StreamEnabled": bool,
        "StreamViewType": str,
    },
    total=False,
)

AwsDynamoDbTableProjectionPaginatorTypeDef = TypedDict(
    "AwsDynamoDbTableProjectionPaginatorTypeDef",
    {
        "NonKeyAttributes": List[str],
        "ProjectionType": str,
    },
    total=False,
)

AwsDynamoDbTableProjectionTypeDef = TypedDict(
    "AwsDynamoDbTableProjectionTypeDef",
    {
        "NonKeyAttributes": Sequence[str],
        "ProjectionType": str,
    },
    total=False,
)

AwsDynamoDbTableProvisionedThroughputOverrideTypeDef = TypedDict(
    "AwsDynamoDbTableProvisionedThroughputOverrideTypeDef",
    {
        "ReadCapacityUnits": int,
    },
    total=False,
)

AwsEc2EipDetailsTypeDef = TypedDict(
    "AwsEc2EipDetailsTypeDef",
    {
        "InstanceId": str,
        "PublicIp": str,
        "AllocationId": str,
        "AssociationId": str,
        "Domain": str,
        "PublicIpv4Pool": str,
        "NetworkBorderGroup": str,
        "NetworkInterfaceId": str,
        "NetworkInterfaceOwnerId": str,
        "PrivateIpAddress": str,
    },
    total=False,
)

AwsEc2InstanceMetadataOptionsTypeDef = TypedDict(
    "AwsEc2InstanceMetadataOptionsTypeDef",
    {
        "HttpEndpoint": str,
        "HttpProtocolIpv6": str,
        "HttpPutResponseHopLimit": int,
        "HttpTokens": str,
        "InstanceMetadataTags": str,
    },
    total=False,
)

AwsEc2InstanceMonitoringDetailsTypeDef = TypedDict(
    "AwsEc2InstanceMonitoringDetailsTypeDef",
    {
        "State": str,
    },
    total=False,
)

AwsEc2InstanceNetworkInterfacesDetailsTypeDef = TypedDict(
    "AwsEc2InstanceNetworkInterfacesDetailsTypeDef",
    {
        "NetworkInterfaceId": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataBlockDeviceMappingSetEbsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataBlockDeviceMappingSetEbsDetailsTypeDef",
    {
        "DeleteOnTermination": bool,
        "Encrypted": bool,
        "Iops": int,
        "KmsKeyId": str,
        "SnapshotId": str,
        "Throughput": int,
        "VolumeSize": int,
        "VolumeType": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataCapacityReservationSpecificationCapacityReservationTargetDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataCapacityReservationSpecificationCapacityReservationTargetDetailsTypeDef",
    {
        "CapacityReservationId": str,
        "CapacityReservationResourceGroupArn": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataCpuOptionsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataCpuOptionsDetailsTypeDef",
    {
        "CoreCount": int,
        "ThreadsPerCore": int,
    },
    total=False,
)

AwsEc2LaunchTemplateDataCreditSpecificationDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataCreditSpecificationDetailsTypeDef",
    {
        "CpuCredits": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataElasticGpuSpecificationSetDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataElasticGpuSpecificationSetDetailsTypeDef",
    {
        "Type": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataElasticInferenceAcceleratorSetDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataElasticInferenceAcceleratorSetDetailsTypeDef",
    {
        "Count": int,
        "Type": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataEnclaveOptionsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataEnclaveOptionsDetailsTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsEc2LaunchTemplateDataHibernationOptionsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataHibernationOptionsDetailsTypeDef",
    {
        "Configured": bool,
    },
    total=False,
)

AwsEc2LaunchTemplateDataIamInstanceProfileDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataIamInstanceProfileDetailsTypeDef",
    {
        "Arn": str,
        "Name": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataLicenseSetDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataLicenseSetDetailsTypeDef",
    {
        "LicenseConfigurationArn": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataMaintenanceOptionsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataMaintenanceOptionsDetailsTypeDef",
    {
        "AutoRecovery": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataMetadataOptionsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataMetadataOptionsDetailsTypeDef",
    {
        "HttpEndpoint": str,
        "HttpProtocolIpv6": str,
        "HttpTokens": str,
        "HttpPutResponseHopLimit": int,
        "InstanceMetadataTags": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataMonitoringDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataMonitoringDetailsTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsEc2LaunchTemplateDataPlacementDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataPlacementDetailsTypeDef",
    {
        "Affinity": str,
        "AvailabilityZone": str,
        "GroupName": str,
        "HostId": str,
        "HostResourceGroupArn": str,
        "PartitionNumber": int,
        "SpreadDomain": str,
        "Tenancy": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataPrivateDnsNameOptionsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataPrivateDnsNameOptionsDetailsTypeDef",
    {
        "EnableResourceNameDnsAAAARecord": bool,
        "EnableResourceNameDnsARecord": bool,
        "HostnameType": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceMarketOptionsSpotOptionsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceMarketOptionsSpotOptionsDetailsTypeDef",
    {
        "BlockDurationMinutes": int,
        "InstanceInterruptionBehavior": str,
        "MaxPrice": str,
        "SpotInstanceType": str,
        "ValidUntil": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceRequirementsAcceleratorCountDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceRequirementsAcceleratorCountDetailsTypeDef",
    {
        "Max": int,
        "Min": int,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceRequirementsAcceleratorTotalMemoryMiBDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceRequirementsAcceleratorTotalMemoryMiBDetailsTypeDef",
    {
        "Max": int,
        "Min": int,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceRequirementsBaselineEbsBandwidthMbpsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceRequirementsBaselineEbsBandwidthMbpsDetailsTypeDef",
    {
        "Max": int,
        "Min": int,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceRequirementsMemoryGiBPerVCpuDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceRequirementsMemoryGiBPerVCpuDetailsTypeDef",
    {
        "Max": float,
        "Min": float,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceRequirementsMemoryMiBDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceRequirementsMemoryMiBDetailsTypeDef",
    {
        "Max": int,
        "Min": int,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceRequirementsNetworkInterfaceCountDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceRequirementsNetworkInterfaceCountDetailsTypeDef",
    {
        "Max": int,
        "Min": int,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceRequirementsTotalLocalStorageGBDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceRequirementsTotalLocalStorageGBDetailsTypeDef",
    {
        "Max": float,
        "Min": float,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceRequirementsVCpuCountDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceRequirementsVCpuCountDetailsTypeDef",
    {
        "Max": int,
        "Min": int,
    },
    total=False,
)

AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv4PrefixesDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv4PrefixesDetailsTypeDef",
    {
        "Ipv4Prefix": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv6AddressesDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv6AddressesDetailsTypeDef",
    {
        "Ipv6Address": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv6PrefixesDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv6PrefixesDetailsTypeDef",
    {
        "Ipv6Prefix": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataNetworkInterfaceSetPrivateIpAddressesDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetPrivateIpAddressesDetailsTypeDef",
    {
        "Primary": bool,
        "PrivateIpAddress": str,
    },
    total=False,
)

AwsEc2NetworkAclAssociationTypeDef = TypedDict(
    "AwsEc2NetworkAclAssociationTypeDef",
    {
        "NetworkAclAssociationId": str,
        "NetworkAclId": str,
        "SubnetId": str,
    },
    total=False,
)

IcmpTypeCodeTypeDef = TypedDict(
    "IcmpTypeCodeTypeDef",
    {
        "Code": int,
        "Type": int,
    },
    total=False,
)

PortRangeFromToTypeDef = TypedDict(
    "PortRangeFromToTypeDef",
    {
        "From": int,
        "To": int,
    },
    total=False,
)

AwsEc2NetworkInterfaceAttachmentTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceAttachmentTypeDef",
    {
        "AttachTime": str,
        "AttachmentId": str,
        "DeleteOnTermination": bool,
        "DeviceIndex": int,
        "InstanceId": str,
        "InstanceOwnerId": str,
        "Status": str,
    },
    total=False,
)

AwsEc2NetworkInterfaceIpV6AddressDetailTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceIpV6AddressDetailTypeDef",
    {
        "IpV6Address": str,
    },
    total=False,
)

AwsEc2NetworkInterfacePrivateIpAddressDetailTypeDef = TypedDict(
    "AwsEc2NetworkInterfacePrivateIpAddressDetailTypeDef",
    {
        "PrivateIpAddress": str,
        "PrivateDnsName": str,
    },
    total=False,
)

AwsEc2NetworkInterfaceSecurityGroupTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceSecurityGroupTypeDef",
    {
        "GroupName": str,
        "GroupId": str,
    },
    total=False,
)

PropagatingVgwSetDetailsTypeDef = TypedDict(
    "PropagatingVgwSetDetailsTypeDef",
    {
        "GatewayId": str,
    },
    total=False,
)

RouteSetDetailsTypeDef = TypedDict(
    "RouteSetDetailsTypeDef",
    {
        "CarrierGatewayId": str,
        "CoreNetworkArn": str,
        "DestinationCidrBlock": str,
        "DestinationIpv6CidrBlock": str,
        "DestinationPrefixListId": str,
        "EgressOnlyInternetGatewayId": str,
        "GatewayId": str,
        "InstanceId": str,
        "InstanceOwnerId": str,
        "LocalGatewayId": str,
        "NatGatewayId": str,
        "NetworkInterfaceId": str,
        "Origin": str,
        "State": str,
        "TransitGatewayId": str,
        "VpcPeeringConnectionId": str,
    },
    total=False,
)

AwsEc2SecurityGroupIpRangeTypeDef = TypedDict(
    "AwsEc2SecurityGroupIpRangeTypeDef",
    {
        "CidrIp": str,
    },
    total=False,
)

AwsEc2SecurityGroupIpv6RangeTypeDef = TypedDict(
    "AwsEc2SecurityGroupIpv6RangeTypeDef",
    {
        "CidrIpv6": str,
    },
    total=False,
)

AwsEc2SecurityGroupPrefixListIdTypeDef = TypedDict(
    "AwsEc2SecurityGroupPrefixListIdTypeDef",
    {
        "PrefixListId": str,
    },
    total=False,
)

AwsEc2SecurityGroupUserIdGroupPairTypeDef = TypedDict(
    "AwsEc2SecurityGroupUserIdGroupPairTypeDef",
    {
        "GroupId": str,
        "GroupName": str,
        "PeeringStatus": str,
        "UserId": str,
        "VpcId": str,
        "VpcPeeringConnectionId": str,
    },
    total=False,
)

Ipv6CidrBlockAssociationTypeDef = TypedDict(
    "Ipv6CidrBlockAssociationTypeDef",
    {
        "AssociationId": str,
        "Ipv6CidrBlock": str,
        "CidrBlockState": str,
    },
    total=False,
)

AwsEc2TransitGatewayDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2TransitGatewayDetailsPaginatorTypeDef",
    {
        "Id": str,
        "Description": str,
        "DefaultRouteTablePropagation": str,
        "AutoAcceptSharedAttachments": str,
        "DefaultRouteTableAssociation": str,
        "TransitGatewayCidrBlocks": List[str],
        "AssociationDefaultRouteTableId": str,
        "PropagationDefaultRouteTableId": str,
        "VpnEcmpSupport": str,
        "DnsSupport": str,
        "MulticastSupport": str,
        "AmazonSideAsn": int,
    },
    total=False,
)

AwsEc2TransitGatewayDetailsTypeDef = TypedDict(
    "AwsEc2TransitGatewayDetailsTypeDef",
    {
        "Id": str,
        "Description": str,
        "DefaultRouteTablePropagation": str,
        "AutoAcceptSharedAttachments": str,
        "DefaultRouteTableAssociation": str,
        "TransitGatewayCidrBlocks": Sequence[str],
        "AssociationDefaultRouteTableId": str,
        "PropagationDefaultRouteTableId": str,
        "VpnEcmpSupport": str,
        "DnsSupport": str,
        "MulticastSupport": str,
        "AmazonSideAsn": int,
    },
    total=False,
)

AwsEc2VolumeAttachmentTypeDef = TypedDict(
    "AwsEc2VolumeAttachmentTypeDef",
    {
        "AttachTime": str,
        "DeleteOnTermination": bool,
        "InstanceId": str,
        "Status": str,
    },
    total=False,
)

CidrBlockAssociationTypeDef = TypedDict(
    "CidrBlockAssociationTypeDef",
    {
        "AssociationId": str,
        "CidrBlock": str,
        "CidrBlockState": str,
    },
    total=False,
)

AwsEc2VpcEndpointServiceServiceTypeDetailsTypeDef = TypedDict(
    "AwsEc2VpcEndpointServiceServiceTypeDetailsTypeDef",
    {
        "ServiceType": str,
    },
    total=False,
)

AwsEc2VpcPeeringConnectionStatusDetailsTypeDef = TypedDict(
    "AwsEc2VpcPeeringConnectionStatusDetailsTypeDef",
    {
        "Code": str,
        "Message": str,
    },
    total=False,
)

VpcInfoCidrBlockSetDetailsTypeDef = TypedDict(
    "VpcInfoCidrBlockSetDetailsTypeDef",
    {
        "CidrBlock": str,
    },
    total=False,
)

VpcInfoIpv6CidrBlockSetDetailsTypeDef = TypedDict(
    "VpcInfoIpv6CidrBlockSetDetailsTypeDef",
    {
        "Ipv6CidrBlock": str,
    },
    total=False,
)

VpcInfoPeeringOptionsDetailsTypeDef = TypedDict(
    "VpcInfoPeeringOptionsDetailsTypeDef",
    {
        "AllowDnsResolutionFromRemoteVpc": bool,
        "AllowEgressFromLocalClassicLinkToRemoteVpc": bool,
        "AllowEgressFromLocalVpcToRemoteClassicLink": bool,
    },
    total=False,
)

AwsEc2VpnConnectionRoutesDetailsTypeDef = TypedDict(
    "AwsEc2VpnConnectionRoutesDetailsTypeDef",
    {
        "DestinationCidrBlock": str,
        "State": str,
    },
    total=False,
)

AwsEc2VpnConnectionVgwTelemetryDetailsTypeDef = TypedDict(
    "AwsEc2VpnConnectionVgwTelemetryDetailsTypeDef",
    {
        "AcceptedRouteCount": int,
        "CertificateArn": str,
        "LastStatusChange": str,
        "OutsideIpAddress": str,
        "Status": str,
        "StatusMessage": str,
    },
    total=False,
)

AwsEc2VpnConnectionOptionsTunnelOptionsDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2VpnConnectionOptionsTunnelOptionsDetailsPaginatorTypeDef",
    {
        "DpdTimeoutSeconds": int,
        "IkeVersions": List[str],
        "OutsideIpAddress": str,
        "Phase1DhGroupNumbers": List[int],
        "Phase1EncryptionAlgorithms": List[str],
        "Phase1IntegrityAlgorithms": List[str],
        "Phase1LifetimeSeconds": int,
        "Phase2DhGroupNumbers": List[int],
        "Phase2EncryptionAlgorithms": List[str],
        "Phase2IntegrityAlgorithms": List[str],
        "Phase2LifetimeSeconds": int,
        "PreSharedKey": str,
        "RekeyFuzzPercentage": int,
        "RekeyMarginTimeSeconds": int,
        "ReplayWindowSize": int,
        "TunnelInsideCidr": str,
    },
    total=False,
)

AwsEc2VpnConnectionOptionsTunnelOptionsDetailsTypeDef = TypedDict(
    "AwsEc2VpnConnectionOptionsTunnelOptionsDetailsTypeDef",
    {
        "DpdTimeoutSeconds": int,
        "IkeVersions": Sequence[str],
        "OutsideIpAddress": str,
        "Phase1DhGroupNumbers": Sequence[int],
        "Phase1EncryptionAlgorithms": Sequence[str],
        "Phase1IntegrityAlgorithms": Sequence[str],
        "Phase1LifetimeSeconds": int,
        "Phase2DhGroupNumbers": Sequence[int],
        "Phase2EncryptionAlgorithms": Sequence[str],
        "Phase2IntegrityAlgorithms": Sequence[str],
        "Phase2LifetimeSeconds": int,
        "PreSharedKey": str,
        "RekeyFuzzPercentage": int,
        "RekeyMarginTimeSeconds": int,
        "ReplayWindowSize": int,
        "TunnelInsideCidr": str,
    },
    total=False,
)

AwsEcrContainerImageDetailsPaginatorTypeDef = TypedDict(
    "AwsEcrContainerImageDetailsPaginatorTypeDef",
    {
        "RegistryId": str,
        "RepositoryName": str,
        "Architecture": str,
        "ImageDigest": str,
        "ImageTags": List[str],
        "ImagePublishedAt": str,
    },
    total=False,
)

AwsEcrContainerImageDetailsTypeDef = TypedDict(
    "AwsEcrContainerImageDetailsTypeDef",
    {
        "RegistryId": str,
        "RepositoryName": str,
        "Architecture": str,
        "ImageDigest": str,
        "ImageTags": Sequence[str],
        "ImagePublishedAt": str,
    },
    total=False,
)

AwsEcrRepositoryImageScanningConfigurationDetailsTypeDef = TypedDict(
    "AwsEcrRepositoryImageScanningConfigurationDetailsTypeDef",
    {
        "ScanOnPush": bool,
    },
    total=False,
)

AwsEcrRepositoryLifecyclePolicyDetailsTypeDef = TypedDict(
    "AwsEcrRepositoryLifecyclePolicyDetailsTypeDef",
    {
        "LifecyclePolicyText": str,
        "RegistryId": str,
    },
    total=False,
)

AwsEcsClusterClusterSettingsDetailsTypeDef = TypedDict(
    "AwsEcsClusterClusterSettingsDetailsTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AwsEcsClusterConfigurationExecuteCommandConfigurationLogConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsClusterConfigurationExecuteCommandConfigurationLogConfigurationDetailsTypeDef",
    {
        "CloudWatchEncryptionEnabled": bool,
        "CloudWatchLogGroupName": str,
        "S3BucketName": str,
        "S3EncryptionEnabled": bool,
        "S3KeyPrefix": str,
    },
    total=False,
)

AwsEcsClusterDefaultCapacityProviderStrategyDetailsTypeDef = TypedDict(
    "AwsEcsClusterDefaultCapacityProviderStrategyDetailsTypeDef",
    {
        "Base": int,
        "CapacityProvider": str,
        "Weight": int,
    },
    total=False,
)

AwsMountPointTypeDef = TypedDict(
    "AwsMountPointTypeDef",
    {
        "SourceVolume": str,
        "ContainerPath": str,
    },
    total=False,
)

AwsEcsServiceCapacityProviderStrategyDetailsTypeDef = TypedDict(
    "AwsEcsServiceCapacityProviderStrategyDetailsTypeDef",
    {
        "Base": int,
        "CapacityProvider": str,
        "Weight": int,
    },
    total=False,
)

AwsEcsServiceDeploymentConfigurationDeploymentCircuitBreakerDetailsTypeDef = TypedDict(
    "AwsEcsServiceDeploymentConfigurationDeploymentCircuitBreakerDetailsTypeDef",
    {
        "Enable": bool,
        "Rollback": bool,
    },
    total=False,
)

AwsEcsServiceDeploymentControllerDetailsTypeDef = TypedDict(
    "AwsEcsServiceDeploymentControllerDetailsTypeDef",
    {
        "Type": str,
    },
    total=False,
)

AwsEcsServiceLoadBalancersDetailsTypeDef = TypedDict(
    "AwsEcsServiceLoadBalancersDetailsTypeDef",
    {
        "ContainerName": str,
        "ContainerPort": int,
        "LoadBalancerName": str,
        "TargetGroupArn": str,
    },
    total=False,
)

AwsEcsServicePlacementConstraintsDetailsTypeDef = TypedDict(
    "AwsEcsServicePlacementConstraintsDetailsTypeDef",
    {
        "Expression": str,
        "Type": str,
    },
    total=False,
)

AwsEcsServicePlacementStrategiesDetailsTypeDef = TypedDict(
    "AwsEcsServicePlacementStrategiesDetailsTypeDef",
    {
        "Field": str,
        "Type": str,
    },
    total=False,
)

AwsEcsServiceServiceRegistriesDetailsTypeDef = TypedDict(
    "AwsEcsServiceServiceRegistriesDetailsTypeDef",
    {
        "ContainerName": str,
        "ContainerPort": int,
        "Port": int,
        "RegistryArn": str,
    },
    total=False,
)

AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsPaginatorTypeDef",
    {
        "AssignPublicIp": str,
        "SecurityGroups": List[str],
        "Subnets": List[str],
    },
    total=False,
)

AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsTypeDef",
    {
        "AssignPublicIp": str,
        "SecurityGroups": Sequence[str],
        "Subnets": Sequence[str],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsDependsOnDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsDependsOnDetailsTypeDef",
    {
        "Condition": str,
        "ContainerName": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsEnvironmentDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsEnvironmentDetailsTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsEnvironmentFilesDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsEnvironmentFilesDetailsTypeDef",
    {
        "Type": str,
        "Value": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsExtraHostsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsExtraHostsDetailsTypeDef",
    {
        "Hostname": str,
        "IpAddress": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsPaginatorTypeDef",
    {
        "Options": Dict[str, str],
        "Type": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsPaginatorTypeDef",
    {
        "Command": List[str],
        "Interval": int,
        "Retries": int,
        "StartPeriod": int,
        "Timeout": int,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsMountPointsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsMountPointsDetailsTypeDef",
    {
        "ContainerPath": str,
        "ReadOnly": bool,
        "SourceVolume": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsPortMappingsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsPortMappingsDetailsTypeDef",
    {
        "ContainerPort": int,
        "HostPort": int,
        "Protocol": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsRepositoryCredentialsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsRepositoryCredentialsDetailsTypeDef",
    {
        "CredentialsParameter": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsResourceRequirementsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsResourceRequirementsDetailsTypeDef",
    {
        "Type": str,
        "Value": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsSecretsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsSecretsDetailsTypeDef",
    {
        "Name": str,
        "ValueFrom": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsSystemControlsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsSystemControlsDetailsTypeDef",
    {
        "Namespace": str,
        "Value": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsUlimitsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsUlimitsDetailsTypeDef",
    {
        "HardLimit": int,
        "Name": str,
        "SoftLimit": int,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsVolumesFromDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsVolumesFromDetailsTypeDef",
    {
        "ReadOnly": bool,
        "SourceContainer": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsTypeDef",
    {
        "Options": Mapping[str, str],
        "Type": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsTypeDef",
    {
        "Command": Sequence[str],
        "Interval": int,
        "Retries": int,
        "StartPeriod": int,
        "Timeout": int,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsPaginatorTypeDef",
    {
        "Add": List[str],
        "Drop": List[str],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsTypeDef",
    {
        "Add": Sequence[str],
        "Drop": Sequence[str],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsPaginatorTypeDef",
    {
        "ContainerPath": str,
        "HostPath": str,
        "Permissions": List[str],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsPaginatorTypeDef",
    {
        "ContainerPath": str,
        "MountOptions": List[str],
        "Size": int,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsTypeDef",
    {
        "ContainerPath": str,
        "HostPath": str,
        "Permissions": Sequence[str],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsTypeDef",
    {
        "ContainerPath": str,
        "MountOptions": Sequence[str],
        "Size": int,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationSecretOptionsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationSecretOptionsDetailsTypeDef",
    {
        "Name": str,
        "ValueFrom": str,
    },
    total=False,
)

AwsEcsTaskDefinitionInferenceAcceleratorsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionInferenceAcceleratorsDetailsTypeDef",
    {
        "DeviceName": str,
        "DeviceType": str,
    },
    total=False,
)

AwsEcsTaskDefinitionPlacementConstraintsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionPlacementConstraintsDetailsTypeDef",
    {
        "Expression": str,
        "Type": str,
    },
    total=False,
)

AwsEcsTaskDefinitionProxyConfigurationProxyConfigurationPropertiesDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionProxyConfigurationProxyConfigurationPropertiesDetailsTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsPaginatorTypeDef",
    {
        "Autoprovision": bool,
        "Driver": str,
        "DriverOpts": Dict[str, str],
        "Labels": Dict[str, str],
        "Scope": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesHostDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesHostDetailsTypeDef",
    {
        "SourcePath": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsTypeDef",
    {
        "Autoprovision": bool,
        "Driver": str,
        "DriverOpts": Mapping[str, str],
        "Labels": Mapping[str, str],
        "Scope": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationAuthorizationConfigDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationAuthorizationConfigDetailsTypeDef",
    {
        "AccessPointId": str,
        "Iam": str,
    },
    total=False,
)

AwsEcsTaskVolumeHostDetailsTypeDef = TypedDict(
    "AwsEcsTaskVolumeHostDetailsTypeDef",
    {
        "SourcePath": str,
    },
    total=False,
)

AwsEfsAccessPointPosixUserDetailsPaginatorTypeDef = TypedDict(
    "AwsEfsAccessPointPosixUserDetailsPaginatorTypeDef",
    {
        "Gid": str,
        "SecondaryGids": List[str],
        "Uid": str,
    },
    total=False,
)

AwsEfsAccessPointPosixUserDetailsTypeDef = TypedDict(
    "AwsEfsAccessPointPosixUserDetailsTypeDef",
    {
        "Gid": str,
        "SecondaryGids": Sequence[str],
        "Uid": str,
    },
    total=False,
)

AwsEfsAccessPointRootDirectoryCreationInfoDetailsTypeDef = TypedDict(
    "AwsEfsAccessPointRootDirectoryCreationInfoDetailsTypeDef",
    {
        "OwnerGid": str,
        "OwnerUid": str,
        "Permissions": str,
    },
    total=False,
)

AwsEksClusterResourcesVpcConfigDetailsPaginatorTypeDef = TypedDict(
    "AwsEksClusterResourcesVpcConfigDetailsPaginatorTypeDef",
    {
        "SecurityGroupIds": List[str],
        "SubnetIds": List[str],
        "EndpointPublicAccess": bool,
    },
    total=False,
)

AwsEksClusterResourcesVpcConfigDetailsTypeDef = TypedDict(
    "AwsEksClusterResourcesVpcConfigDetailsTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "SubnetIds": Sequence[str],
        "EndpointPublicAccess": bool,
    },
    total=False,
)

AwsEksClusterLoggingClusterLoggingDetailsPaginatorTypeDef = TypedDict(
    "AwsEksClusterLoggingClusterLoggingDetailsPaginatorTypeDef",
    {
        "Enabled": bool,
        "Types": List[str],
    },
    total=False,
)

AwsEksClusterLoggingClusterLoggingDetailsTypeDef = TypedDict(
    "AwsEksClusterLoggingClusterLoggingDetailsTypeDef",
    {
        "Enabled": bool,
        "Types": Sequence[str],
    },
    total=False,
)

AwsElasticBeanstalkEnvironmentEnvironmentLinkTypeDef = TypedDict(
    "AwsElasticBeanstalkEnvironmentEnvironmentLinkTypeDef",
    {
        "EnvironmentName": str,
        "LinkName": str,
    },
    total=False,
)

AwsElasticBeanstalkEnvironmentOptionSettingTypeDef = TypedDict(
    "AwsElasticBeanstalkEnvironmentOptionSettingTypeDef",
    {
        "Namespace": str,
        "OptionName": str,
        "ResourceName": str,
        "Value": str,
    },
    total=False,
)

AwsElasticBeanstalkEnvironmentTierTypeDef = TypedDict(
    "AwsElasticBeanstalkEnvironmentTierTypeDef",
    {
        "Name": str,
        "Type": str,
        "Version": str,
    },
    total=False,
)

AwsElasticsearchDomainDomainEndpointOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainDomainEndpointOptionsTypeDef",
    {
        "EnforceHTTPS": bool,
        "TLSSecurityPolicy": str,
    },
    total=False,
)

AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef",
    {
        "Enabled": bool,
        "KmsKeyId": str,
    },
    total=False,
)

AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsElasticsearchDomainServiceSoftwareOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainServiceSoftwareOptionsTypeDef",
    {
        "AutomatedUpdateDate": str,
        "Cancellable": bool,
        "CurrentVersion": str,
        "Description": str,
        "NewVersion": str,
        "UpdateAvailable": bool,
        "UpdateStatus": str,
    },
    total=False,
)

AwsElasticsearchDomainVPCOptionsPaginatorTypeDef = TypedDict(
    "AwsElasticsearchDomainVPCOptionsPaginatorTypeDef",
    {
        "AvailabilityZones": List[str],
        "SecurityGroupIds": List[str],
        "SubnetIds": List[str],
        "VPCId": str,
    },
    total=False,
)

AwsElasticsearchDomainVPCOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainVPCOptionsTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "SecurityGroupIds": Sequence[str],
        "SubnetIds": Sequence[str],
        "VPCId": str,
    },
    total=False,
)

AwsElasticsearchDomainElasticsearchClusterConfigZoneAwarenessConfigDetailsTypeDef = TypedDict(
    "AwsElasticsearchDomainElasticsearchClusterConfigZoneAwarenessConfigDetailsTypeDef",
    {
        "AvailabilityZoneCount": int,
    },
    total=False,
)

AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef = TypedDict(
    "AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef",
    {
        "CloudWatchLogsLogGroupArn": str,
        "Enabled": bool,
    },
    total=False,
)

AwsElbAppCookieStickinessPolicyTypeDef = TypedDict(
    "AwsElbAppCookieStickinessPolicyTypeDef",
    {
        "CookieName": str,
        "PolicyName": str,
    },
    total=False,
)

AwsElbLbCookieStickinessPolicyTypeDef = TypedDict(
    "AwsElbLbCookieStickinessPolicyTypeDef",
    {
        "CookieExpirationPeriod": int,
        "PolicyName": str,
    },
    total=False,
)

AwsElbLoadBalancerAccessLogTypeDef = TypedDict(
    "AwsElbLoadBalancerAccessLogTypeDef",
    {
        "EmitInterval": int,
        "Enabled": bool,
        "S3BucketName": str,
        "S3BucketPrefix": str,
    },
    total=False,
)

AwsElbLoadBalancerAdditionalAttributeTypeDef = TypedDict(
    "AwsElbLoadBalancerAdditionalAttributeTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

AwsElbLoadBalancerConnectionDrainingTypeDef = TypedDict(
    "AwsElbLoadBalancerConnectionDrainingTypeDef",
    {
        "Enabled": bool,
        "Timeout": int,
    },
    total=False,
)

AwsElbLoadBalancerConnectionSettingsTypeDef = TypedDict(
    "AwsElbLoadBalancerConnectionSettingsTypeDef",
    {
        "IdleTimeout": int,
    },
    total=False,
)

AwsElbLoadBalancerCrossZoneLoadBalancingTypeDef = TypedDict(
    "AwsElbLoadBalancerCrossZoneLoadBalancingTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsElbLoadBalancerBackendServerDescriptionPaginatorTypeDef = TypedDict(
    "AwsElbLoadBalancerBackendServerDescriptionPaginatorTypeDef",
    {
        "InstancePort": int,
        "PolicyNames": List[str],
    },
    total=False,
)

AwsElbLoadBalancerBackendServerDescriptionTypeDef = TypedDict(
    "AwsElbLoadBalancerBackendServerDescriptionTypeDef",
    {
        "InstancePort": int,
        "PolicyNames": Sequence[str],
    },
    total=False,
)

AwsElbLoadBalancerHealthCheckTypeDef = TypedDict(
    "AwsElbLoadBalancerHealthCheckTypeDef",
    {
        "HealthyThreshold": int,
        "Interval": int,
        "Target": str,
        "Timeout": int,
        "UnhealthyThreshold": int,
    },
    total=False,
)

AwsElbLoadBalancerInstanceTypeDef = TypedDict(
    "AwsElbLoadBalancerInstanceTypeDef",
    {
        "InstanceId": str,
    },
    total=False,
)

AwsElbLoadBalancerSourceSecurityGroupTypeDef = TypedDict(
    "AwsElbLoadBalancerSourceSecurityGroupTypeDef",
    {
        "GroupName": str,
        "OwnerAlias": str,
    },
    total=False,
)

AwsElbLoadBalancerListenerTypeDef = TypedDict(
    "AwsElbLoadBalancerListenerTypeDef",
    {
        "InstancePort": int,
        "InstanceProtocol": str,
        "LoadBalancerPort": int,
        "Protocol": str,
        "SslCertificateId": str,
    },
    total=False,
)

AwsElbv2LoadBalancerAttributeTypeDef = TypedDict(
    "AwsElbv2LoadBalancerAttributeTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

LoadBalancerStateTypeDef = TypedDict(
    "LoadBalancerStateTypeDef",
    {
        "Code": str,
        "Reason": str,
    },
    total=False,
)

AwsEventSchemasRegistryDetailsTypeDef = TypedDict(
    "AwsEventSchemasRegistryDetailsTypeDef",
    {
        "Description": str,
        "RegistryArn": str,
        "RegistryName": str,
    },
    total=False,
)

AwsGuardDutyDetectorDataSourcesCloudTrailDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDataSourcesCloudTrailDetailsTypeDef",
    {
        "Status": str,
    },
    total=False,
)

AwsGuardDutyDetectorDataSourcesDnsLogsDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDataSourcesDnsLogsDetailsTypeDef",
    {
        "Status": str,
    },
    total=False,
)

AwsGuardDutyDetectorDataSourcesFlowLogsDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDataSourcesFlowLogsDetailsTypeDef",
    {
        "Status": str,
    },
    total=False,
)

AwsGuardDutyDetectorDataSourcesS3LogsDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDataSourcesS3LogsDetailsTypeDef",
    {
        "Status": str,
    },
    total=False,
)

AwsGuardDutyDetectorDataSourcesKubernetesAuditLogsDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDataSourcesKubernetesAuditLogsDetailsTypeDef",
    {
        "Status": str,
    },
    total=False,
)

AwsGuardDutyDetectorDataSourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDataSourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesDetailsTypeDef",
    {
        "Reason": str,
        "Status": str,
    },
    total=False,
)

AwsGuardDutyDetectorFeaturesDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorFeaturesDetailsTypeDef",
    {
        "Name": str,
        "Status": str,
    },
    total=False,
)

AwsIamAccessKeySessionContextAttributesTypeDef = TypedDict(
    "AwsIamAccessKeySessionContextAttributesTypeDef",
    {
        "MfaAuthenticated": bool,
        "CreationDate": str,
    },
    total=False,
)

AwsIamAccessKeySessionContextSessionIssuerTypeDef = TypedDict(
    "AwsIamAccessKeySessionContextSessionIssuerTypeDef",
    {
        "Type": str,
        "PrincipalId": str,
        "Arn": str,
        "AccountId": str,
        "UserName": str,
    },
    total=False,
)

AwsIamAttachedManagedPolicyTypeDef = TypedDict(
    "AwsIamAttachedManagedPolicyTypeDef",
    {
        "PolicyName": str,
        "PolicyArn": str,
    },
    total=False,
)

AwsIamGroupPolicyTypeDef = TypedDict(
    "AwsIamGroupPolicyTypeDef",
    {
        "PolicyName": str,
    },
    total=False,
)

AwsIamInstanceProfileRolePaginatorTypeDef = TypedDict(
    "AwsIamInstanceProfileRolePaginatorTypeDef",
    {
        "Arn": str,
        "AssumeRolePolicyDocument": Dict[str, Any],
        "CreateDate": str,
        "Path": str,
        "RoleId": str,
        "RoleName": str,
    },
    total=False,
)

DictOrStrTypeDef = Union[str, Dict[str, Any]]
AwsIamPermissionsBoundaryTypeDef = TypedDict(
    "AwsIamPermissionsBoundaryTypeDef",
    {
        "PermissionsBoundaryArn": str,
        "PermissionsBoundaryType": str,
    },
    total=False,
)

AwsIamPolicyVersionTypeDef = TypedDict(
    "AwsIamPolicyVersionTypeDef",
    {
        "VersionId": str,
        "IsDefaultVersion": bool,
        "CreateDate": str,
    },
    total=False,
)

AwsIamRolePolicyTypeDef = TypedDict(
    "AwsIamRolePolicyTypeDef",
    {
        "PolicyName": str,
    },
    total=False,
)

AwsIamUserPolicyTypeDef = TypedDict(
    "AwsIamUserPolicyTypeDef",
    {
        "PolicyName": str,
    },
    total=False,
)

AwsKinesisStreamStreamEncryptionDetailsTypeDef = TypedDict(
    "AwsKinesisStreamStreamEncryptionDetailsTypeDef",
    {
        "EncryptionType": str,
        "KeyId": str,
    },
    total=False,
)

AwsKmsKeyDetailsTypeDef = TypedDict(
    "AwsKmsKeyDetailsTypeDef",
    {
        "AWSAccountId": str,
        "CreationDate": float,
        "KeyId": str,
        "KeyManager": str,
        "KeyState": str,
        "Origin": str,
        "Description": str,
        "KeyRotationStatus": bool,
    },
    total=False,
)

AwsLambdaFunctionCodeTypeDef = TypedDict(
    "AwsLambdaFunctionCodeTypeDef",
    {
        "S3Bucket": str,
        "S3Key": str,
        "S3ObjectVersion": str,
        "ZipFile": str,
    },
    total=False,
)

AwsLambdaFunctionDeadLetterConfigTypeDef = TypedDict(
    "AwsLambdaFunctionDeadLetterConfigTypeDef",
    {
        "TargetArn": str,
    },
    total=False,
)

AwsLambdaFunctionLayerTypeDef = TypedDict(
    "AwsLambdaFunctionLayerTypeDef",
    {
        "Arn": str,
        "CodeSize": int,
    },
    total=False,
)

AwsLambdaFunctionTracingConfigTypeDef = TypedDict(
    "AwsLambdaFunctionTracingConfigTypeDef",
    {
        "Mode": str,
    },
    total=False,
)

AwsLambdaFunctionVpcConfigPaginatorTypeDef = TypedDict(
    "AwsLambdaFunctionVpcConfigPaginatorTypeDef",
    {
        "SecurityGroupIds": List[str],
        "SubnetIds": List[str],
        "VpcId": str,
    },
    total=False,
)

AwsLambdaFunctionVpcConfigTypeDef = TypedDict(
    "AwsLambdaFunctionVpcConfigTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "SubnetIds": Sequence[str],
        "VpcId": str,
    },
    total=False,
)

AwsLambdaFunctionEnvironmentErrorTypeDef = TypedDict(
    "AwsLambdaFunctionEnvironmentErrorTypeDef",
    {
        "ErrorCode": str,
        "Message": str,
    },
    total=False,
)

AwsLambdaLayerVersionDetailsPaginatorTypeDef = TypedDict(
    "AwsLambdaLayerVersionDetailsPaginatorTypeDef",
    {
        "Version": int,
        "CompatibleRuntimes": List[str],
        "CreatedDate": str,
    },
    total=False,
)

AwsLambdaLayerVersionDetailsTypeDef = TypedDict(
    "AwsLambdaLayerVersionDetailsTypeDef",
    {
        "Version": int,
        "CompatibleRuntimes": Sequence[str],
        "CreatedDate": str,
    },
    total=False,
)

AwsNetworkFirewallFirewallSubnetMappingsDetailsTypeDef = TypedDict(
    "AwsNetworkFirewallFirewallSubnetMappingsDetailsTypeDef",
    {
        "SubnetId": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainMasterUserOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainMasterUserOptionsDetailsTypeDef",
    {
        "MasterUserArn": str,
        "MasterUserName": str,
        "MasterUserPassword": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainClusterConfigZoneAwarenessConfigDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainClusterConfigZoneAwarenessConfigDetailsTypeDef",
    {
        "AvailabilityZoneCount": int,
    },
    total=False,
)

AwsOpenSearchServiceDomainDomainEndpointOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainDomainEndpointOptionsDetailsTypeDef",
    {
        "CustomEndpointCertificateArn": str,
        "CustomEndpointEnabled": bool,
        "EnforceHTTPS": bool,
        "CustomEndpoint": str,
        "TLSSecurityPolicy": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainEncryptionAtRestOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainEncryptionAtRestOptionsDetailsTypeDef",
    {
        "Enabled": bool,
        "KmsKeyId": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainNodeToNodeEncryptionOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainNodeToNodeEncryptionOptionsDetailsTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsOpenSearchServiceDomainServiceSoftwareOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainServiceSoftwareOptionsDetailsTypeDef",
    {
        "AutomatedUpdateDate": str,
        "Cancellable": bool,
        "CurrentVersion": str,
        "Description": str,
        "NewVersion": str,
        "UpdateAvailable": bool,
        "UpdateStatus": str,
        "OptionalDeployment": bool,
    },
    total=False,
)

AwsOpenSearchServiceDomainVpcOptionsDetailsPaginatorTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainVpcOptionsDetailsPaginatorTypeDef",
    {
        "SecurityGroupIds": List[str],
        "SubnetIds": List[str],
    },
    total=False,
)

AwsOpenSearchServiceDomainVpcOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainVpcOptionsDetailsTypeDef",
    {
        "SecurityGroupIds": Sequence[str],
        "SubnetIds": Sequence[str],
    },
    total=False,
)

AwsOpenSearchServiceDomainLogPublishingOptionTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainLogPublishingOptionTypeDef",
    {
        "CloudWatchLogsLogGroupArn": str,
        "Enabled": bool,
    },
    total=False,
)

AwsRdsDbClusterAssociatedRoleTypeDef = TypedDict(
    "AwsRdsDbClusterAssociatedRoleTypeDef",
    {
        "RoleArn": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbClusterMemberTypeDef = TypedDict(
    "AwsRdsDbClusterMemberTypeDef",
    {
        "IsClusterWriter": bool,
        "PromotionTier": int,
        "DbInstanceIdentifier": str,
        "DbClusterParameterGroupStatus": str,
    },
    total=False,
)

AwsRdsDbClusterOptionGroupMembershipTypeDef = TypedDict(
    "AwsRdsDbClusterOptionGroupMembershipTypeDef",
    {
        "DbClusterOptionGroupName": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbDomainMembershipTypeDef = TypedDict(
    "AwsRdsDbDomainMembershipTypeDef",
    {
        "Domain": str,
        "Status": str,
        "Fqdn": str,
        "IamRoleName": str,
    },
    total=False,
)

AwsRdsDbInstanceVpcSecurityGroupTypeDef = TypedDict(
    "AwsRdsDbInstanceVpcSecurityGroupTypeDef",
    {
        "VpcSecurityGroupId": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbClusterSnapshotDbClusterSnapshotAttributePaginatorTypeDef = TypedDict(
    "AwsRdsDbClusterSnapshotDbClusterSnapshotAttributePaginatorTypeDef",
    {
        "AttributeName": str,
        "AttributeValues": List[str],
    },
    total=False,
)

AwsRdsDbClusterSnapshotDbClusterSnapshotAttributeTypeDef = TypedDict(
    "AwsRdsDbClusterSnapshotDbClusterSnapshotAttributeTypeDef",
    {
        "AttributeName": str,
        "AttributeValues": Sequence[str],
    },
    total=False,
)

AwsRdsDbInstanceAssociatedRoleTypeDef = TypedDict(
    "AwsRdsDbInstanceAssociatedRoleTypeDef",
    {
        "RoleArn": str,
        "FeatureName": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbInstanceEndpointTypeDef = TypedDict(
    "AwsRdsDbInstanceEndpointTypeDef",
    {
        "Address": str,
        "Port": int,
        "HostedZoneId": str,
    },
    total=False,
)

AwsRdsDbOptionGroupMembershipTypeDef = TypedDict(
    "AwsRdsDbOptionGroupMembershipTypeDef",
    {
        "OptionGroupName": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbParameterGroupTypeDef = TypedDict(
    "AwsRdsDbParameterGroupTypeDef",
    {
        "DbParameterGroupName": str,
        "ParameterApplyStatus": str,
    },
    total=False,
)

AwsRdsDbProcessorFeatureTypeDef = TypedDict(
    "AwsRdsDbProcessorFeatureTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AwsRdsDbStatusInfoTypeDef = TypedDict(
    "AwsRdsDbStatusInfoTypeDef",
    {
        "StatusType": str,
        "Normal": bool,
        "Status": str,
        "Message": str,
    },
    total=False,
)

AwsRdsPendingCloudWatchLogsExportsPaginatorTypeDef = TypedDict(
    "AwsRdsPendingCloudWatchLogsExportsPaginatorTypeDef",
    {
        "LogTypesToEnable": List[str],
        "LogTypesToDisable": List[str],
    },
    total=False,
)

AwsRdsPendingCloudWatchLogsExportsTypeDef = TypedDict(
    "AwsRdsPendingCloudWatchLogsExportsTypeDef",
    {
        "LogTypesToEnable": Sequence[str],
        "LogTypesToDisable": Sequence[str],
    },
    total=False,
)

AwsRdsDbSecurityGroupEc2SecurityGroupTypeDef = TypedDict(
    "AwsRdsDbSecurityGroupEc2SecurityGroupTypeDef",
    {
        "Ec2SecurityGroupId": str,
        "Ec2SecurityGroupName": str,
        "Ec2SecurityGroupOwnerId": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbSecurityGroupIpRangeTypeDef = TypedDict(
    "AwsRdsDbSecurityGroupIpRangeTypeDef",
    {
        "CidrIp": str,
        "Status": str,
    },
    total=False,
)

AwsRdsDbSubnetGroupSubnetAvailabilityZoneTypeDef = TypedDict(
    "AwsRdsDbSubnetGroupSubnetAvailabilityZoneTypeDef",
    {
        "Name": str,
    },
    total=False,
)

AwsRdsEventSubscriptionDetailsPaginatorTypeDef = TypedDict(
    "AwsRdsEventSubscriptionDetailsPaginatorTypeDef",
    {
        "CustSubscriptionId": str,
        "CustomerAwsId": str,
        "Enabled": bool,
        "EventCategoriesList": List[str],
        "EventSubscriptionArn": str,
        "SnsTopicArn": str,
        "SourceIdsList": List[str],
        "SourceType": str,
        "Status": str,
        "SubscriptionCreationTime": str,
    },
    total=False,
)

AwsRdsEventSubscriptionDetailsTypeDef = TypedDict(
    "AwsRdsEventSubscriptionDetailsTypeDef",
    {
        "CustSubscriptionId": str,
        "CustomerAwsId": str,
        "Enabled": bool,
        "EventCategoriesList": Sequence[str],
        "EventSubscriptionArn": str,
        "SnsTopicArn": str,
        "SourceIdsList": Sequence[str],
        "SourceType": str,
        "Status": str,
        "SubscriptionCreationTime": str,
    },
    total=False,
)

AwsRedshiftClusterClusterNodeTypeDef = TypedDict(
    "AwsRedshiftClusterClusterNodeTypeDef",
    {
        "NodeRole": str,
        "PrivateIpAddress": str,
        "PublicIpAddress": str,
    },
    total=False,
)

AwsRedshiftClusterClusterParameterStatusTypeDef = TypedDict(
    "AwsRedshiftClusterClusterParameterStatusTypeDef",
    {
        "ParameterName": str,
        "ParameterApplyStatus": str,
        "ParameterApplyErrorDescription": str,
    },
    total=False,
)

AwsRedshiftClusterClusterSecurityGroupTypeDef = TypedDict(
    "AwsRedshiftClusterClusterSecurityGroupTypeDef",
    {
        "ClusterSecurityGroupName": str,
        "Status": str,
    },
    total=False,
)

AwsRedshiftClusterClusterSnapshotCopyStatusTypeDef = TypedDict(
    "AwsRedshiftClusterClusterSnapshotCopyStatusTypeDef",
    {
        "DestinationRegion": str,
        "ManualSnapshotRetentionPeriod": int,
        "RetentionPeriod": int,
        "SnapshotCopyGrantName": str,
    },
    total=False,
)

AwsRedshiftClusterDeferredMaintenanceWindowTypeDef = TypedDict(
    "AwsRedshiftClusterDeferredMaintenanceWindowTypeDef",
    {
        "DeferMaintenanceEndTime": str,
        "DeferMaintenanceIdentifier": str,
        "DeferMaintenanceStartTime": str,
    },
    total=False,
)

AwsRedshiftClusterElasticIpStatusTypeDef = TypedDict(
    "AwsRedshiftClusterElasticIpStatusTypeDef",
    {
        "ElasticIp": str,
        "Status": str,
    },
    total=False,
)

AwsRedshiftClusterEndpointTypeDef = TypedDict(
    "AwsRedshiftClusterEndpointTypeDef",
    {
        "Address": str,
        "Port": int,
    },
    total=False,
)

AwsRedshiftClusterHsmStatusTypeDef = TypedDict(
    "AwsRedshiftClusterHsmStatusTypeDef",
    {
        "HsmClientCertificateIdentifier": str,
        "HsmConfigurationIdentifier": str,
        "Status": str,
    },
    total=False,
)

AwsRedshiftClusterIamRoleTypeDef = TypedDict(
    "AwsRedshiftClusterIamRoleTypeDef",
    {
        "ApplyStatus": str,
        "IamRoleArn": str,
    },
    total=False,
)

AwsRedshiftClusterLoggingStatusTypeDef = TypedDict(
    "AwsRedshiftClusterLoggingStatusTypeDef",
    {
        "BucketName": str,
        "LastFailureMessage": str,
        "LastFailureTime": str,
        "LastSuccessfulDeliveryTime": str,
        "LoggingEnabled": bool,
        "S3KeyPrefix": str,
    },
    total=False,
)

AwsRedshiftClusterPendingModifiedValuesTypeDef = TypedDict(
    "AwsRedshiftClusterPendingModifiedValuesTypeDef",
    {
        "AutomatedSnapshotRetentionPeriod": int,
        "ClusterIdentifier": str,
        "ClusterType": str,
        "ClusterVersion": str,
        "EncryptionType": str,
        "EnhancedVpcRouting": bool,
        "MaintenanceTrackName": str,
        "MasterUserPassword": str,
        "NodeType": str,
        "NumberOfNodes": int,
        "PubliclyAccessible": bool,
    },
    total=False,
)

AwsRedshiftClusterResizeInfoTypeDef = TypedDict(
    "AwsRedshiftClusterResizeInfoTypeDef",
    {
        "AllowCancelResize": bool,
        "ResizeType": str,
    },
    total=False,
)

AwsRedshiftClusterRestoreStatusTypeDef = TypedDict(
    "AwsRedshiftClusterRestoreStatusTypeDef",
    {
        "CurrentRestoreRateInMegaBytesPerSecond": float,
        "ElapsedTimeInSeconds": int,
        "EstimatedTimeToCompletionInSeconds": int,
        "ProgressInMegaBytes": int,
        "SnapshotSizeInMegaBytes": int,
        "Status": str,
    },
    total=False,
)

AwsRedshiftClusterVpcSecurityGroupTypeDef = TypedDict(
    "AwsRedshiftClusterVpcSecurityGroupTypeDef",
    {
        "Status": str,
        "VpcSecurityGroupId": str,
    },
    total=False,
)

AwsS3AccountPublicAccessBlockDetailsTypeDef = TypedDict(
    "AwsS3AccountPublicAccessBlockDetailsTypeDef",
    {
        "BlockPublicAcls": bool,
        "BlockPublicPolicy": bool,
        "IgnorePublicAcls": bool,
        "RestrictPublicBuckets": bool,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesAbortIncompleteMultipartUploadDetailsTypeDef = (
    TypedDict(
        "AwsS3BucketBucketLifecycleConfigurationRulesAbortIncompleteMultipartUploadDetailsTypeDef",
        {
            "DaysAfterInitiation": int,
        },
        total=False,
    )
)

AwsS3BucketBucketLifecycleConfigurationRulesNoncurrentVersionTransitionsDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesNoncurrentVersionTransitionsDetailsTypeDef",
    {
        "Days": int,
        "StorageClass": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesTransitionsDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesTransitionsDetailsTypeDef",
    {
        "Date": str,
        "Days": int,
        "StorageClass": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateTagDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateTagDetailsTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsTagDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsTagDetailsTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

AwsS3BucketBucketVersioningConfigurationTypeDef = TypedDict(
    "AwsS3BucketBucketVersioningConfigurationTypeDef",
    {
        "IsMfaDeleteEnabled": bool,
        "Status": str,
    },
    total=False,
)

AwsS3BucketLoggingConfigurationTypeDef = TypedDict(
    "AwsS3BucketLoggingConfigurationTypeDef",
    {
        "DestinationBucketName": str,
        "LogFilePrefix": str,
    },
    total=False,
)

AwsS3BucketNotificationConfigurationS3KeyFilterRuleTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationS3KeyFilterRuleTypeDef",
    {
        "Name": AwsS3BucketNotificationConfigurationS3KeyFilterRuleNameType,
        "Value": str,
    },
    total=False,
)

AwsS3BucketObjectLockConfigurationRuleDefaultRetentionDetailsTypeDef = TypedDict(
    "AwsS3BucketObjectLockConfigurationRuleDefaultRetentionDetailsTypeDef",
    {
        "Days": int,
        "Mode": str,
        "Years": int,
    },
    total=False,
)

AwsS3BucketServerSideEncryptionByDefaultTypeDef = TypedDict(
    "AwsS3BucketServerSideEncryptionByDefaultTypeDef",
    {
        "SSEAlgorithm": str,
        "KMSMasterKeyID": str,
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationRedirectToTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationRedirectToTypeDef",
    {
        "Hostname": str,
        "Protocol": str,
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationRoutingRuleConditionTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationRoutingRuleConditionTypeDef",
    {
        "HttpErrorCodeReturnedEquals": str,
        "KeyPrefixEquals": str,
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationRoutingRuleRedirectTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationRoutingRuleRedirectTypeDef",
    {
        "Hostname": str,
        "HttpRedirectCode": str,
        "Protocol": str,
        "ReplaceKeyPrefixWith": str,
        "ReplaceKeyWith": str,
    },
    total=False,
)

AwsS3ObjectDetailsTypeDef = TypedDict(
    "AwsS3ObjectDetailsTypeDef",
    {
        "LastModified": str,
        "ETag": str,
        "VersionId": str,
        "ContentType": str,
        "ServerSideEncryption": str,
        "SSEKMSKeyId": str,
    },
    total=False,
)

AwsSageMakerNotebookInstanceMetadataServiceConfigurationDetailsTypeDef = TypedDict(
    "AwsSageMakerNotebookInstanceMetadataServiceConfigurationDetailsTypeDef",
    {
        "MinimumInstanceMetadataServiceVersion": str,
    },
    total=False,
)

AwsSecretsManagerSecretRotationRulesTypeDef = TypedDict(
    "AwsSecretsManagerSecretRotationRulesTypeDef",
    {
        "AutomaticallyAfterDays": int,
    },
    total=False,
)

BooleanFilterTypeDef = TypedDict(
    "BooleanFilterTypeDef",
    {
        "Value": bool,
    },
    total=False,
)

IpFilterTypeDef = TypedDict(
    "IpFilterTypeDef",
    {
        "Cidr": str,
    },
    total=False,
)

KeywordFilterTypeDef = TypedDict(
    "KeywordFilterTypeDef",
    {
        "Value": str,
    },
    total=False,
)

AwsSecurityFindingIdentifierTypeDef = TypedDict(
    "AwsSecurityFindingIdentifierTypeDef",
    {
        "Id": str,
        "ProductArn": str,
    },
)

GeneratorDetailsPaginatorTypeDef = TypedDict(
    "GeneratorDetailsPaginatorTypeDef",
    {
        "Name": str,
        "Description": str,
        "Labels": List[str],
    },
    total=False,
)

_RequiredMalwareTypeDef = TypedDict(
    "_RequiredMalwareTypeDef",
    {
        "Name": str,
    },
)
_OptionalMalwareTypeDef = TypedDict(
    "_OptionalMalwareTypeDef",
    {
        "Type": MalwareTypeType,
        "Path": str,
        "State": MalwareStateType,
    },
    total=False,
)


class MalwareTypeDef(_RequiredMalwareTypeDef, _OptionalMalwareTypeDef):
    pass


NoteTypeDef = TypedDict(
    "NoteTypeDef",
    {
        "Text": str,
        "UpdatedBy": str,
        "UpdatedAt": str,
    },
)

_RequiredPatchSummaryTypeDef = TypedDict(
    "_RequiredPatchSummaryTypeDef",
    {
        "Id": str,
    },
)
_OptionalPatchSummaryTypeDef = TypedDict(
    "_OptionalPatchSummaryTypeDef",
    {
        "InstalledCount": int,
        "MissingCount": int,
        "FailedCount": int,
        "InstalledOtherCount": int,
        "InstalledRejectedCount": int,
        "InstalledPendingReboot": int,
        "OperationStartTime": str,
        "OperationEndTime": str,
        "RebootOption": str,
        "Operation": str,
    },
    total=False,
)


class PatchSummaryTypeDef(_RequiredPatchSummaryTypeDef, _OptionalPatchSummaryTypeDef):
    pass


ProcessDetailsTypeDef = TypedDict(
    "ProcessDetailsTypeDef",
    {
        "Name": str,
        "Path": str,
        "Pid": int,
        "ParentPid": int,
        "LaunchedAt": str,
        "TerminatedAt": str,
    },
    total=False,
)

SeverityTypeDef = TypedDict(
    "SeverityTypeDef",
    {
        "Product": float,
        "Label": SeverityLabelType,
        "Normalized": int,
        "Original": str,
    },
    total=False,
)

ThreatIntelIndicatorTypeDef = TypedDict(
    "ThreatIntelIndicatorTypeDef",
    {
        "Type": ThreatIntelIndicatorTypeType,
        "Value": str,
        "Category": ThreatIntelIndicatorCategoryType,
        "LastObservedAt": str,
        "Source": str,
        "SourceUrl": str,
    },
    total=False,
)

WorkflowTypeDef = TypedDict(
    "WorkflowTypeDef",
    {
        "Status": WorkflowStatusType,
    },
    total=False,
)

GeneratorDetailsTypeDef = TypedDict(
    "GeneratorDetailsTypeDef",
    {
        "Name": str,
        "Description": str,
        "Labels": Sequence[str],
    },
    total=False,
)

AwsSnsTopicSubscriptionTypeDef = TypedDict(
    "AwsSnsTopicSubscriptionTypeDef",
    {
        "Endpoint": str,
        "Protocol": str,
    },
    total=False,
)

AwsSqsQueueDetailsTypeDef = TypedDict(
    "AwsSqsQueueDetailsTypeDef",
    {
        "KmsDataKeyReusePeriodSeconds": int,
        "KmsMasterKeyId": str,
        "QueueName": str,
        "DeadLetterTargetArn": str,
    },
    total=False,
)

AwsSsmComplianceSummaryTypeDef = TypedDict(
    "AwsSsmComplianceSummaryTypeDef",
    {
        "Status": str,
        "CompliantCriticalCount": int,
        "CompliantHighCount": int,
        "CompliantMediumCount": int,
        "ExecutionType": str,
        "NonCompliantCriticalCount": int,
        "CompliantInformationalCount": int,
        "NonCompliantInformationalCount": int,
        "CompliantUnspecifiedCount": int,
        "NonCompliantLowCount": int,
        "NonCompliantHighCount": int,
        "CompliantLowCount": int,
        "ComplianceType": str,
        "PatchBaselineId": str,
        "OverallSeverity": str,
        "NonCompliantMediumCount": int,
        "NonCompliantUnspecifiedCount": int,
        "PatchGroup": str,
    },
    total=False,
)

AwsStepFunctionStateMachineTracingConfigurationDetailsTypeDef = TypedDict(
    "AwsStepFunctionStateMachineTracingConfigurationDetailsTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

AwsStepFunctionStateMachineLoggingConfigurationDestinationsCloudWatchLogsLogGroupDetailsTypeDef = TypedDict(
    "AwsStepFunctionStateMachineLoggingConfigurationDestinationsCloudWatchLogsLogGroupDetailsTypeDef",
    {
        "LogGroupArn": str,
    },
    total=False,
)

AwsWafRateBasedRuleMatchPredicateTypeDef = TypedDict(
    "AwsWafRateBasedRuleMatchPredicateTypeDef",
    {
        "DataId": str,
        "Negated": bool,
        "Type": str,
    },
    total=False,
)

AwsWafRegionalRateBasedRuleMatchPredicateTypeDef = TypedDict(
    "AwsWafRegionalRateBasedRuleMatchPredicateTypeDef",
    {
        "DataId": str,
        "Negated": bool,
        "Type": str,
    },
    total=False,
)

AwsWafRegionalRulePredicateListDetailsTypeDef = TypedDict(
    "AwsWafRegionalRulePredicateListDetailsTypeDef",
    {
        "DataId": str,
        "Negated": bool,
        "Type": str,
    },
    total=False,
)

AwsWafRegionalRuleGroupRulesActionDetailsTypeDef = TypedDict(
    "AwsWafRegionalRuleGroupRulesActionDetailsTypeDef",
    {
        "Type": str,
    },
    total=False,
)

AwsWafRegionalWebAclRulesListActionDetailsTypeDef = TypedDict(
    "AwsWafRegionalWebAclRulesListActionDetailsTypeDef",
    {
        "Type": str,
    },
    total=False,
)

AwsWafRegionalWebAclRulesListOverrideActionDetailsTypeDef = TypedDict(
    "AwsWafRegionalWebAclRulesListOverrideActionDetailsTypeDef",
    {
        "Type": str,
    },
    total=False,
)

AwsWafRulePredicateListDetailsTypeDef = TypedDict(
    "AwsWafRulePredicateListDetailsTypeDef",
    {
        "DataId": str,
        "Negated": bool,
        "Type": str,
    },
    total=False,
)

AwsWafRuleGroupRulesActionDetailsTypeDef = TypedDict(
    "AwsWafRuleGroupRulesActionDetailsTypeDef",
    {
        "Type": str,
    },
    total=False,
)

WafActionTypeDef = TypedDict(
    "WafActionTypeDef",
    {
        "Type": str,
    },
    total=False,
)

WafExcludedRuleTypeDef = TypedDict(
    "WafExcludedRuleTypeDef",
    {
        "RuleId": str,
    },
    total=False,
)

WafOverrideActionTypeDef = TypedDict(
    "WafOverrideActionTypeDef",
    {
        "Type": str,
    },
    total=False,
)

AwsWafv2CustomHttpHeaderTypeDef = TypedDict(
    "AwsWafv2CustomHttpHeaderTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

AwsWafv2VisibilityConfigDetailsTypeDef = TypedDict(
    "AwsWafv2VisibilityConfigDetailsTypeDef",
    {
        "CloudWatchMetricsEnabled": bool,
        "MetricName": str,
        "SampledRequestsEnabled": bool,
    },
    total=False,
)

AwsWafv2WebAclCaptchaConfigImmunityTimePropertyDetailsTypeDef = TypedDict(
    "AwsWafv2WebAclCaptchaConfigImmunityTimePropertyDetailsTypeDef",
    {
        "ImmunityTime": int,
    },
    total=False,
)

AwsXrayEncryptionConfigDetailsTypeDef = TypedDict(
    "AwsXrayEncryptionConfigDetailsTypeDef",
    {
        "KeyId": str,
        "Status": str,
        "Type": str,
    },
    total=False,
)

BatchDeleteAutomationRulesRequestRequestTypeDef = TypedDict(
    "BatchDeleteAutomationRulesRequestRequestTypeDef",
    {
        "AutomationRulesArns": Sequence[str],
    },
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

UnprocessedAutomationRuleTypeDef = TypedDict(
    "UnprocessedAutomationRuleTypeDef",
    {
        "RuleArn": str,
        "ErrorCode": int,
        "ErrorMessage": str,
    },
    total=False,
)

BatchDisableStandardsRequestRequestTypeDef = TypedDict(
    "BatchDisableStandardsRequestRequestTypeDef",
    {
        "StandardsSubscriptionArns": Sequence[str],
    },
)

_RequiredStandardsSubscriptionRequestTypeDef = TypedDict(
    "_RequiredStandardsSubscriptionRequestTypeDef",
    {
        "StandardsArn": str,
    },
)
_OptionalStandardsSubscriptionRequestTypeDef = TypedDict(
    "_OptionalStandardsSubscriptionRequestTypeDef",
    {
        "StandardsInput": Mapping[str, str],
    },
    total=False,
)


class StandardsSubscriptionRequestTypeDef(
    _RequiredStandardsSubscriptionRequestTypeDef, _OptionalStandardsSubscriptionRequestTypeDef
):
    pass


BatchGetAutomationRulesRequestRequestTypeDef = TypedDict(
    "BatchGetAutomationRulesRequestRequestTypeDef",
    {
        "AutomationRulesArns": Sequence[str],
    },
)

BatchGetSecurityControlsRequestRequestTypeDef = TypedDict(
    "BatchGetSecurityControlsRequestRequestTypeDef",
    {
        "SecurityControlIds": Sequence[str],
    },
)

SecurityControlTypeDef = TypedDict(
    "SecurityControlTypeDef",
    {
        "SecurityControlId": str,
        "SecurityControlArn": str,
        "Title": str,
        "Description": str,
        "RemediationUrl": str,
        "SeverityRating": SeverityRatingType,
        "SecurityControlStatus": ControlStatusType,
    },
)

_RequiredUnprocessedSecurityControlTypeDef = TypedDict(
    "_RequiredUnprocessedSecurityControlTypeDef",
    {
        "SecurityControlId": str,
        "ErrorCode": UnprocessedErrorCodeType,
    },
)
_OptionalUnprocessedSecurityControlTypeDef = TypedDict(
    "_OptionalUnprocessedSecurityControlTypeDef",
    {
        "ErrorReason": str,
    },
    total=False,
)


class UnprocessedSecurityControlTypeDef(
    _RequiredUnprocessedSecurityControlTypeDef, _OptionalUnprocessedSecurityControlTypeDef
):
    pass


StandardsControlAssociationIdTypeDef = TypedDict(
    "StandardsControlAssociationIdTypeDef",
    {
        "SecurityControlId": str,
        "StandardsArn": str,
    },
)

_RequiredStandardsControlAssociationDetailTypeDef = TypedDict(
    "_RequiredStandardsControlAssociationDetailTypeDef",
    {
        "StandardsArn": str,
        "SecurityControlId": str,
        "SecurityControlArn": str,
        "AssociationStatus": AssociationStatusType,
    },
)
_OptionalStandardsControlAssociationDetailTypeDef = TypedDict(
    "_OptionalStandardsControlAssociationDetailTypeDef",
    {
        "RelatedRequirements": List[str],
        "UpdatedAt": datetime,
        "UpdatedReason": str,
        "StandardsControlTitle": str,
        "StandardsControlDescription": str,
        "StandardsControlArns": List[str],
    },
    total=False,
)


class StandardsControlAssociationDetailTypeDef(
    _RequiredStandardsControlAssociationDetailTypeDef,
    _OptionalStandardsControlAssociationDetailTypeDef,
):
    pass


ImportFindingsErrorTypeDef = TypedDict(
    "ImportFindingsErrorTypeDef",
    {
        "Id": str,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
)

_RequiredStandardsControlAssociationUpdateTypeDef = TypedDict(
    "_RequiredStandardsControlAssociationUpdateTypeDef",
    {
        "StandardsArn": str,
        "SecurityControlId": str,
        "AssociationStatus": AssociationStatusType,
    },
)
_OptionalStandardsControlAssociationUpdateTypeDef = TypedDict(
    "_OptionalStandardsControlAssociationUpdateTypeDef",
    {
        "UpdatedReason": str,
    },
    total=False,
)


class StandardsControlAssociationUpdateTypeDef(
    _RequiredStandardsControlAssociationUpdateTypeDef,
    _OptionalStandardsControlAssociationUpdateTypeDef,
):
    pass


CellTypeDef = TypedDict(
    "CellTypeDef",
    {
        "Column": int,
        "Row": int,
        "ColumnName": str,
        "CellReference": str,
    },
    total=False,
)

ClassificationStatusTypeDef = TypedDict(
    "ClassificationStatusTypeDef",
    {
        "Code": str,
        "Reason": str,
    },
    total=False,
)

CodeVulnerabilitiesFilePathTypeDef = TypedDict(
    "CodeVulnerabilitiesFilePathTypeDef",
    {
        "EndLine": int,
        "FileName": str,
        "FilePath": str,
        "StartLine": int,
    },
    total=False,
)

_RequiredStatusReasonTypeDef = TypedDict(
    "_RequiredStatusReasonTypeDef",
    {
        "ReasonCode": str,
    },
)
_OptionalStatusReasonTypeDef = TypedDict(
    "_OptionalStatusReasonTypeDef",
    {
        "Description": str,
    },
    total=False,
)


class StatusReasonTypeDef(_RequiredStatusReasonTypeDef, _OptionalStatusReasonTypeDef):
    pass


VolumeMountTypeDef = TypedDict(
    "VolumeMountTypeDef",
    {
        "Name": str,
        "MountPath": str,
    },
    total=False,
)

CreateActionTargetRequestRequestTypeDef = TypedDict(
    "CreateActionTargetRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
        "Id": str,
    },
)

_RequiredCreateFindingAggregatorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFindingAggregatorRequestRequestTypeDef",
    {
        "RegionLinkingMode": str,
    },
)
_OptionalCreateFindingAggregatorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFindingAggregatorRequestRequestTypeDef",
    {
        "Regions": Sequence[str],
    },
    total=False,
)


class CreateFindingAggregatorRequestRequestTypeDef(
    _RequiredCreateFindingAggregatorRequestRequestTypeDef,
    _OptionalCreateFindingAggregatorRequestRequestTypeDef,
):
    pass


ResultTypeDef = TypedDict(
    "ResultTypeDef",
    {
        "AccountId": str,
        "ProcessingResult": str,
    },
    total=False,
)

DateRangeTypeDef = TypedDict(
    "DateRangeTypeDef",
    {
        "Value": int,
        "Unit": Literal["DAYS"],
    },
    total=False,
)

DeclineInvitationsRequestRequestTypeDef = TypedDict(
    "DeclineInvitationsRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

DeleteActionTargetRequestRequestTypeDef = TypedDict(
    "DeleteActionTargetRequestRequestTypeDef",
    {
        "ActionTargetArn": str,
    },
)

DeleteFindingAggregatorRequestRequestTypeDef = TypedDict(
    "DeleteFindingAggregatorRequestRequestTypeDef",
    {
        "FindingAggregatorArn": str,
    },
)

DeleteInsightRequestRequestTypeDef = TypedDict(
    "DeleteInsightRequestRequestTypeDef",
    {
        "InsightArn": str,
    },
)

DeleteInvitationsRequestRequestTypeDef = TypedDict(
    "DeleteInvitationsRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

DeleteMembersRequestRequestTypeDef = TypedDict(
    "DeleteMembersRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

DescribeActionTargetsRequestRequestTypeDef = TypedDict(
    "DescribeActionTargetsRequestRequestTypeDef",
    {
        "ActionTargetArns": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DescribeHubRequestRequestTypeDef = TypedDict(
    "DescribeHubRequestRequestTypeDef",
    {
        "HubArn": str,
    },
    total=False,
)

DescribeProductsRequestRequestTypeDef = TypedDict(
    "DescribeProductsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ProductArn": str,
    },
    total=False,
)

_RequiredProductTypeDef = TypedDict(
    "_RequiredProductTypeDef",
    {
        "ProductArn": str,
    },
)
_OptionalProductTypeDef = TypedDict(
    "_OptionalProductTypeDef",
    {
        "ProductName": str,
        "CompanyName": str,
        "Description": str,
        "Categories": List[str],
        "IntegrationTypes": List[IntegrationTypeType],
        "MarketplaceUrl": str,
        "ActivationUrl": str,
        "ProductSubscriptionResourcePolicy": str,
    },
    total=False,
)


class ProductTypeDef(_RequiredProductTypeDef, _OptionalProductTypeDef):
    pass


_RequiredDescribeStandardsControlsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeStandardsControlsRequestRequestTypeDef",
    {
        "StandardsSubscriptionArn": str,
    },
)
_OptionalDescribeStandardsControlsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeStandardsControlsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeStandardsControlsRequestRequestTypeDef(
    _RequiredDescribeStandardsControlsRequestRequestTypeDef,
    _OptionalDescribeStandardsControlsRequestRequestTypeDef,
):
    pass


StandardsControlTypeDef = TypedDict(
    "StandardsControlTypeDef",
    {
        "StandardsControlArn": str,
        "ControlStatus": ControlStatusType,
        "DisabledReason": str,
        "ControlStatusUpdatedAt": datetime,
        "ControlId": str,
        "Title": str,
        "Description": str,
        "RemediationUrl": str,
        "SeverityRating": SeverityRatingType,
        "RelatedRequirements": List[str],
    },
    total=False,
)

DescribeStandardsRequestRequestTypeDef = TypedDict(
    "DescribeStandardsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

DisableImportFindingsForProductRequestRequestTypeDef = TypedDict(
    "DisableImportFindingsForProductRequestRequestTypeDef",
    {
        "ProductSubscriptionArn": str,
    },
)

DisableOrganizationAdminAccountRequestRequestTypeDef = TypedDict(
    "DisableOrganizationAdminAccountRequestRequestTypeDef",
    {
        "AdminAccountId": str,
    },
)

DisassociateMembersRequestRequestTypeDef = TypedDict(
    "DisassociateMembersRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

EnableImportFindingsForProductRequestRequestTypeDef = TypedDict(
    "EnableImportFindingsForProductRequestRequestTypeDef",
    {
        "ProductArn": str,
    },
)

EnableOrganizationAdminAccountRequestRequestTypeDef = TypedDict(
    "EnableOrganizationAdminAccountRequestRequestTypeDef",
    {
        "AdminAccountId": str,
    },
)

EnableSecurityHubRequestRequestTypeDef = TypedDict(
    "EnableSecurityHubRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
        "EnableDefaultStandards": bool,
        "ControlFindingGenerator": ControlFindingGeneratorType,
    },
    total=False,
)

FilePathsTypeDef = TypedDict(
    "FilePathsTypeDef",
    {
        "FilePath": str,
        "FileName": str,
        "ResourceId": str,
        "Hash": str,
    },
    total=False,
)

FindingAggregatorTypeDef = TypedDict(
    "FindingAggregatorTypeDef",
    {
        "FindingAggregatorArn": str,
    },
    total=False,
)

FindingHistoryUpdateSourceTypeDef = TypedDict(
    "FindingHistoryUpdateSourceTypeDef",
    {
        "Type": FindingHistoryUpdateSourceTypeType,
        "Identity": str,
    },
    total=False,
)

FindingHistoryUpdateTypeDef = TypedDict(
    "FindingHistoryUpdateTypeDef",
    {
        "UpdatedField": str,
        "OldValue": str,
        "NewValue": str,
    },
    total=False,
)

FindingProviderSeverityTypeDef = TypedDict(
    "FindingProviderSeverityTypeDef",
    {
        "Label": SeverityLabelType,
        "Original": str,
    },
    total=False,
)

FirewallPolicyStatefulRuleGroupReferencesDetailsTypeDef = TypedDict(
    "FirewallPolicyStatefulRuleGroupReferencesDetailsTypeDef",
    {
        "ResourceArn": str,
    },
    total=False,
)

FirewallPolicyStatelessRuleGroupReferencesDetailsTypeDef = TypedDict(
    "FirewallPolicyStatelessRuleGroupReferencesDetailsTypeDef",
    {
        "Priority": int,
        "ResourceArn": str,
    },
    total=False,
)

InvitationTypeDef = TypedDict(
    "InvitationTypeDef",
    {
        "AccountId": str,
        "InvitationId": str,
        "InvitedAt": datetime,
        "MemberStatus": str,
    },
    total=False,
)

GetEnabledStandardsRequestRequestTypeDef = TypedDict(
    "GetEnabledStandardsRequestRequestTypeDef",
    {
        "StandardsSubscriptionArns": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

GetFindingAggregatorRequestRequestTypeDef = TypedDict(
    "GetFindingAggregatorRequestRequestTypeDef",
    {
        "FindingAggregatorArn": str,
    },
)

TimestampTypeDef = Union[datetime, str]
SortCriterionTypeDef = TypedDict(
    "SortCriterionTypeDef",
    {
        "Field": str,
        "SortOrder": SortOrderType,
    },
    total=False,
)

GetInsightResultsRequestRequestTypeDef = TypedDict(
    "GetInsightResultsRequestRequestTypeDef",
    {
        "InsightArn": str,
    },
)

GetInsightsRequestRequestTypeDef = TypedDict(
    "GetInsightsRequestRequestTypeDef",
    {
        "InsightArns": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

GetMembersRequestRequestTypeDef = TypedDict(
    "GetMembersRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "AccountId": str,
        "Email": str,
        "MasterId": str,
        "AdministratorId": str,
        "MemberStatus": str,
        "InvitedAt": datetime,
        "UpdatedAt": datetime,
    },
    total=False,
)

InsightResultValueTypeDef = TypedDict(
    "InsightResultValueTypeDef",
    {
        "GroupByAttributeValue": str,
        "Count": int,
    },
)

InviteMembersRequestRequestTypeDef = TypedDict(
    "InviteMembersRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

ListAutomationRulesRequestRequestTypeDef = TypedDict(
    "ListAutomationRulesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListEnabledProductsForImportRequestRequestTypeDef = TypedDict(
    "ListEnabledProductsForImportRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListFindingAggregatorsRequestRequestTypeDef = TypedDict(
    "ListFindingAggregatorsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListInvitationsRequestRequestTypeDef = TypedDict(
    "ListInvitationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListMembersRequestRequestTypeDef = TypedDict(
    "ListMembersRequestRequestTypeDef",
    {
        "OnlyAssociated": bool,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListOrganizationAdminAccountsRequestRequestTypeDef = TypedDict(
    "ListOrganizationAdminAccountsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListSecurityControlDefinitionsRequestRequestTypeDef = TypedDict(
    "ListSecurityControlDefinitionsRequestRequestTypeDef",
    {
        "StandardsArn": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

SecurityControlDefinitionTypeDef = TypedDict(
    "SecurityControlDefinitionTypeDef",
    {
        "SecurityControlId": str,
        "Title": str,
        "Description": str,
        "RemediationUrl": str,
        "SeverityRating": SeverityRatingType,
        "CurrentRegionAvailability": RegionAvailabilityStatusType,
    },
)

_RequiredListStandardsControlAssociationsRequestRequestTypeDef = TypedDict(
    "_RequiredListStandardsControlAssociationsRequestRequestTypeDef",
    {
        "SecurityControlId": str,
    },
)
_OptionalListStandardsControlAssociationsRequestRequestTypeDef = TypedDict(
    "_OptionalListStandardsControlAssociationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListStandardsControlAssociationsRequestRequestTypeDef(
    _RequiredListStandardsControlAssociationsRequestRequestTypeDef,
    _OptionalListStandardsControlAssociationsRequestRequestTypeDef,
):
    pass


_RequiredStandardsControlAssociationSummaryTypeDef = TypedDict(
    "_RequiredStandardsControlAssociationSummaryTypeDef",
    {
        "StandardsArn": str,
        "SecurityControlId": str,
        "SecurityControlArn": str,
        "AssociationStatus": AssociationStatusType,
    },
)
_OptionalStandardsControlAssociationSummaryTypeDef = TypedDict(
    "_OptionalStandardsControlAssociationSummaryTypeDef",
    {
        "RelatedRequirements": List[str],
        "UpdatedAt": datetime,
        "UpdatedReason": str,
        "StandardsControlTitle": str,
        "StandardsControlDescription": str,
    },
    total=False,
)


class StandardsControlAssociationSummaryTypeDef(
    _RequiredStandardsControlAssociationSummaryTypeDef,
    _OptionalStandardsControlAssociationSummaryTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "Begin": int,
        "End": int,
    },
    total=False,
)

RangeTypeDef = TypedDict(
    "RangeTypeDef",
    {
        "Start": int,
        "End": int,
        "StartColumn": int,
    },
    total=False,
)

RecordTypeDef = TypedDict(
    "RecordTypeDef",
    {
        "JsonPath": str,
        "RecordIndex": int,
    },
    total=False,
)

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "Text": str,
        "Url": str,
    },
    total=False,
)

RuleGroupSourceListDetailsPaginatorTypeDef = TypedDict(
    "RuleGroupSourceListDetailsPaginatorTypeDef",
    {
        "GeneratedRulesType": str,
        "TargetTypes": List[str],
        "Targets": List[str],
    },
    total=False,
)

RuleGroupSourceListDetailsTypeDef = TypedDict(
    "RuleGroupSourceListDetailsTypeDef",
    {
        "GeneratedRulesType": str,
        "TargetTypes": Sequence[str],
        "Targets": Sequence[str],
    },
    total=False,
)

RuleGroupSourceStatefulRulesHeaderDetailsTypeDef = TypedDict(
    "RuleGroupSourceStatefulRulesHeaderDetailsTypeDef",
    {
        "Destination": str,
        "DestinationPort": str,
        "Direction": str,
        "Protocol": str,
        "Source": str,
        "SourcePort": str,
    },
    total=False,
)

RuleGroupSourceStatefulRulesOptionsDetailsPaginatorTypeDef = TypedDict(
    "RuleGroupSourceStatefulRulesOptionsDetailsPaginatorTypeDef",
    {
        "Keyword": str,
        "Settings": List[str],
    },
    total=False,
)

RuleGroupSourceStatefulRulesOptionsDetailsTypeDef = TypedDict(
    "RuleGroupSourceStatefulRulesOptionsDetailsTypeDef",
    {
        "Keyword": str,
        "Settings": Sequence[str],
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesDestinationPortsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesDestinationPortsTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesDestinationsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesDestinationsTypeDef",
    {
        "AddressDefinition": str,
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesSourcePortsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesSourcePortsTypeDef",
    {
        "FromPort": int,
        "ToPort": int,
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesSourcesTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesSourcesTypeDef",
    {
        "AddressDefinition": str,
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsPaginatorTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsPaginatorTypeDef",
    {
        "Flags": List[str],
        "Masks": List[str],
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsTypeDef",
    {
        "Flags": Sequence[str],
        "Masks": Sequence[str],
    },
    total=False,
)

RuleGroupVariablesIpSetsDetailsPaginatorTypeDef = TypedDict(
    "RuleGroupVariablesIpSetsDetailsPaginatorTypeDef",
    {
        "Definition": List[str],
    },
    total=False,
)

RuleGroupVariablesIpSetsDetailsTypeDef = TypedDict(
    "RuleGroupVariablesIpSetsDetailsTypeDef",
    {
        "Definition": Sequence[str],
    },
    total=False,
)

RuleGroupVariablesPortSetsDetailsPaginatorTypeDef = TypedDict(
    "RuleGroupVariablesPortSetsDetailsPaginatorTypeDef",
    {
        "Definition": List[str],
    },
    total=False,
)

RuleGroupVariablesPortSetsDetailsTypeDef = TypedDict(
    "RuleGroupVariablesPortSetsDetailsTypeDef",
    {
        "Definition": Sequence[str],
    },
    total=False,
)

SoftwarePackageTypeDef = TypedDict(
    "SoftwarePackageTypeDef",
    {
        "Name": str,
        "Version": str,
        "Epoch": str,
        "Release": str,
        "Architecture": str,
        "PackageManager": str,
        "FilePath": str,
        "FixedInVersion": str,
        "Remediation": str,
        "SourceLayerHash": str,
        "SourceLayerArn": str,
    },
    total=False,
)

StandardsManagedByTypeDef = TypedDict(
    "StandardsManagedByTypeDef",
    {
        "Company": str,
        "Product": str,
    },
    total=False,
)

StandardsStatusReasonTypeDef = TypedDict(
    "StandardsStatusReasonTypeDef",
    {
        "StatusReasonCode": StatusReasonCodeType,
    },
)

StatelessCustomPublishMetricActionDimensionTypeDef = TypedDict(
    "StatelessCustomPublishMetricActionDimensionTypeDef",
    {
        "Value": str,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateActionTargetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateActionTargetRequestRequestTypeDef",
    {
        "ActionTargetArn": str,
    },
)
_OptionalUpdateActionTargetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateActionTargetRequestRequestTypeDef",
    {
        "Name": str,
        "Description": str,
    },
    total=False,
)


class UpdateActionTargetRequestRequestTypeDef(
    _RequiredUpdateActionTargetRequestRequestTypeDef,
    _OptionalUpdateActionTargetRequestRequestTypeDef,
):
    pass


_RequiredUpdateFindingAggregatorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFindingAggregatorRequestRequestTypeDef",
    {
        "FindingAggregatorArn": str,
        "RegionLinkingMode": str,
    },
)
_OptionalUpdateFindingAggregatorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFindingAggregatorRequestRequestTypeDef",
    {
        "Regions": Sequence[str],
    },
    total=False,
)


class UpdateFindingAggregatorRequestRequestTypeDef(
    _RequiredUpdateFindingAggregatorRequestRequestTypeDef,
    _OptionalUpdateFindingAggregatorRequestRequestTypeDef,
):
    pass


_RequiredUpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "AutoEnable": bool,
    },
)
_OptionalUpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "AutoEnableStandards": AutoEnableStandardsType,
    },
    total=False,
)


class UpdateOrganizationConfigurationRequestRequestTypeDef(
    _RequiredUpdateOrganizationConfigurationRequestRequestTypeDef,
    _OptionalUpdateOrganizationConfigurationRequestRequestTypeDef,
):
    pass


UpdateSecurityHubConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateSecurityHubConfigurationRequestRequestTypeDef",
    {
        "AutoEnableControls": bool,
        "ControlFindingGenerator": ControlFindingGeneratorType,
    },
    total=False,
)

_RequiredUpdateStandardsControlRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStandardsControlRequestRequestTypeDef",
    {
        "StandardsControlArn": str,
    },
)
_OptionalUpdateStandardsControlRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStandardsControlRequestRequestTypeDef",
    {
        "ControlStatus": ControlStatusType,
        "DisabledReason": str,
    },
    total=False,
)


class UpdateStandardsControlRequestRequestTypeDef(
    _RequiredUpdateStandardsControlRequestRequestTypeDef,
    _OptionalUpdateStandardsControlRequestRequestTypeDef,
):
    pass


_RequiredVulnerabilityVendorTypeDef = TypedDict(
    "_RequiredVulnerabilityVendorTypeDef",
    {
        "Name": str,
    },
)
_OptionalVulnerabilityVendorTypeDef = TypedDict(
    "_OptionalVulnerabilityVendorTypeDef",
    {
        "Url": str,
        "VendorSeverity": str,
        "VendorCreatedAt": str,
        "VendorUpdatedAt": str,
    },
    total=False,
)


class VulnerabilityVendorTypeDef(
    _RequiredVulnerabilityVendorTypeDef, _OptionalVulnerabilityVendorTypeDef
):
    pass


CreateMembersRequestRequestTypeDef = TypedDict(
    "CreateMembersRequestRequestTypeDef",
    {
        "AccountDetails": Sequence[AccountDetailsTypeDef],
    },
)

ActionRemoteIpDetailsTypeDef = TypedDict(
    "ActionRemoteIpDetailsTypeDef",
    {
        "IpAddressV4": str,
        "Organization": IpOrganizationDetailsTypeDef,
        "Country": CountryTypeDef,
        "City": CityTypeDef,
        "GeoLocation": GeoLocationTypeDef,
    },
    total=False,
)

CvssPaginatorTypeDef = TypedDict(
    "CvssPaginatorTypeDef",
    {
        "Version": str,
        "BaseScore": float,
        "BaseVector": str,
        "Source": str,
        "Adjustments": List[AdjustmentTypeDef],
    },
    total=False,
)

CvssTypeDef = TypedDict(
    "CvssTypeDef",
    {
        "Version": str,
        "BaseScore": float,
        "BaseVector": str,
        "Source": str,
        "Adjustments": Sequence[AdjustmentTypeDef],
    },
    total=False,
)

AssociationSetDetailsTypeDef = TypedDict(
    "AssociationSetDetailsTypeDef",
    {
        "AssociationState": AssociationStateDetailsTypeDef,
        "GatewayId": str,
        "Main": bool,
        "RouteTableAssociationId": str,
        "RouteTableId": str,
        "SubnetId": str,
    },
    total=False,
)

AutomationRulesFindingFieldsUpdateTypeDef = TypedDict(
    "AutomationRulesFindingFieldsUpdateTypeDef",
    {
        "Note": NoteUpdateTypeDef,
        "Severity": SeverityUpdateTypeDef,
        "VerificationState": VerificationStateType,
        "Confidence": int,
        "Criticality": int,
        "Types": List[str],
        "UserDefinedFields": Dict[str, str],
        "Workflow": WorkflowUpdateTypeDef,
        "RelatedFindings": List[RelatedFindingTypeDef],
    },
    total=False,
)

AwsAmazonMqBrokerLogsDetailsTypeDef = TypedDict(
    "AwsAmazonMqBrokerLogsDetailsTypeDef",
    {
        "Audit": bool,
        "General": bool,
        "AuditLogGroup": str,
        "GeneralLogGroup": str,
        "Pending": AwsAmazonMqBrokerLogsPendingDetailsTypeDef,
    },
    total=False,
)

AwsApiGatewayRestApiDetailsPaginatorTypeDef = TypedDict(
    "AwsApiGatewayRestApiDetailsPaginatorTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "CreatedDate": str,
        "Version": str,
        "BinaryMediaTypes": List[str],
        "MinimumCompressionSize": int,
        "ApiKeySource": str,
        "EndpointConfiguration": AwsApiGatewayEndpointConfigurationPaginatorTypeDef,
    },
    total=False,
)

AwsApiGatewayRestApiDetailsTypeDef = TypedDict(
    "AwsApiGatewayRestApiDetailsTypeDef",
    {
        "Id": str,
        "Name": str,
        "Description": str,
        "CreatedDate": str,
        "Version": str,
        "BinaryMediaTypes": Sequence[str],
        "MinimumCompressionSize": int,
        "ApiKeySource": str,
        "EndpointConfiguration": AwsApiGatewayEndpointConfigurationTypeDef,
    },
    total=False,
)

AwsApiGatewayStageDetailsPaginatorTypeDef = TypedDict(
    "AwsApiGatewayStageDetailsPaginatorTypeDef",
    {
        "DeploymentId": str,
        "ClientCertificateId": str,
        "StageName": str,
        "Description": str,
        "CacheClusterEnabled": bool,
        "CacheClusterSize": str,
        "CacheClusterStatus": str,
        "MethodSettings": List[AwsApiGatewayMethodSettingsTypeDef],
        "Variables": Dict[str, str],
        "DocumentationVersion": str,
        "AccessLogSettings": AwsApiGatewayAccessLogSettingsTypeDef,
        "CanarySettings": AwsApiGatewayCanarySettingsPaginatorTypeDef,
        "TracingEnabled": bool,
        "CreatedDate": str,
        "LastUpdatedDate": str,
        "WebAclArn": str,
    },
    total=False,
)

AwsApiGatewayStageDetailsTypeDef = TypedDict(
    "AwsApiGatewayStageDetailsTypeDef",
    {
        "DeploymentId": str,
        "ClientCertificateId": str,
        "StageName": str,
        "Description": str,
        "CacheClusterEnabled": bool,
        "CacheClusterSize": str,
        "CacheClusterStatus": str,
        "MethodSettings": Sequence[AwsApiGatewayMethodSettingsTypeDef],
        "Variables": Mapping[str, str],
        "DocumentationVersion": str,
        "AccessLogSettings": AwsApiGatewayAccessLogSettingsTypeDef,
        "CanarySettings": AwsApiGatewayCanarySettingsTypeDef,
        "TracingEnabled": bool,
        "CreatedDate": str,
        "LastUpdatedDate": str,
        "WebAclArn": str,
    },
    total=False,
)

AwsApiGatewayV2ApiDetailsPaginatorTypeDef = TypedDict(
    "AwsApiGatewayV2ApiDetailsPaginatorTypeDef",
    {
        "ApiEndpoint": str,
        "ApiId": str,
        "ApiKeySelectionExpression": str,
        "CreatedDate": str,
        "Description": str,
        "Version": str,
        "Name": str,
        "ProtocolType": str,
        "RouteSelectionExpression": str,
        "CorsConfiguration": AwsCorsConfigurationPaginatorTypeDef,
    },
    total=False,
)

AwsApiGatewayV2ApiDetailsTypeDef = TypedDict(
    "AwsApiGatewayV2ApiDetailsTypeDef",
    {
        "ApiEndpoint": str,
        "ApiId": str,
        "ApiKeySelectionExpression": str,
        "CreatedDate": str,
        "Description": str,
        "Version": str,
        "Name": str,
        "ProtocolType": str,
        "RouteSelectionExpression": str,
        "CorsConfiguration": AwsCorsConfigurationTypeDef,
    },
    total=False,
)

AwsApiGatewayV2StageDetailsPaginatorTypeDef = TypedDict(
    "AwsApiGatewayV2StageDetailsPaginatorTypeDef",
    {
        "ClientCertificateId": str,
        "CreatedDate": str,
        "Description": str,
        "DefaultRouteSettings": AwsApiGatewayV2RouteSettingsTypeDef,
        "DeploymentId": str,
        "LastUpdatedDate": str,
        "RouteSettings": AwsApiGatewayV2RouteSettingsTypeDef,
        "StageName": str,
        "StageVariables": Dict[str, str],
        "AccessLogSettings": AwsApiGatewayAccessLogSettingsTypeDef,
        "AutoDeploy": bool,
        "LastDeploymentStatusMessage": str,
        "ApiGatewayManaged": bool,
    },
    total=False,
)

AwsApiGatewayV2StageDetailsTypeDef = TypedDict(
    "AwsApiGatewayV2StageDetailsTypeDef",
    {
        "ClientCertificateId": str,
        "CreatedDate": str,
        "Description": str,
        "DefaultRouteSettings": AwsApiGatewayV2RouteSettingsTypeDef,
        "DeploymentId": str,
        "LastUpdatedDate": str,
        "RouteSettings": AwsApiGatewayV2RouteSettingsTypeDef,
        "StageName": str,
        "StageVariables": Mapping[str, str],
        "AccessLogSettings": AwsApiGatewayAccessLogSettingsTypeDef,
        "AutoDeploy": bool,
        "LastDeploymentStatusMessage": str,
        "ApiGatewayManaged": bool,
    },
    total=False,
)

AwsAppSyncGraphQlApiAdditionalAuthenticationProvidersDetailsTypeDef = TypedDict(
    "AwsAppSyncGraphQlApiAdditionalAuthenticationProvidersDetailsTypeDef",
    {
        "AuthenticationType": str,
        "LambdaAuthorizerConfig": AwsAppSyncGraphQlApiLambdaAuthorizerConfigDetailsTypeDef,
        "OpenIdConnectConfig": AwsAppSyncGraphQlApiOpenIdConnectConfigDetailsTypeDef,
        "UserPoolConfig": AwsAppSyncGraphQlApiUserPoolConfigDetailsTypeDef,
    },
    total=False,
)

AwsAthenaWorkGroupConfigurationResultConfigurationDetailsTypeDef = TypedDict(
    "AwsAthenaWorkGroupConfigurationResultConfigurationDetailsTypeDef",
    {
        "EncryptionConfiguration": (
            AwsAthenaWorkGroupConfigurationResultConfigurationEncryptionConfigurationDetailsTypeDef
        ),
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsPaginatorTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsPaginatorTypeDef",
    {
        "LaunchTemplateSpecification": AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationTypeDef,
        "Overrides": List[
            AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateOverridesListDetailsTypeDef
        ],
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsTypeDef",
    {
        "LaunchTemplateSpecification": AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateLaunchTemplateSpecificationTypeDef,
        "Overrides": Sequence[
            AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateOverridesListDetailsTypeDef
        ],
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationBlockDeviceMappingsDetailsTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationBlockDeviceMappingsDetailsTypeDef",
    {
        "DeviceName": str,
        "Ebs": AwsAutoScalingLaunchConfigurationBlockDeviceMappingsEbsDetailsTypeDef,
        "NoDevice": bool,
        "VirtualName": str,
    },
    total=False,
)

AwsBackupBackupPlanRuleCopyActionsDetailsTypeDef = TypedDict(
    "AwsBackupBackupPlanRuleCopyActionsDetailsTypeDef",
    {
        "DestinationBackupVaultArn": str,
        "Lifecycle": AwsBackupBackupPlanLifecycleDetailsTypeDef,
    },
    total=False,
)

AwsBackupBackupVaultDetailsPaginatorTypeDef = TypedDict(
    "AwsBackupBackupVaultDetailsPaginatorTypeDef",
    {
        "BackupVaultArn": str,
        "BackupVaultName": str,
        "EncryptionKeyArn": str,
        "Notifications": AwsBackupBackupVaultNotificationsDetailsPaginatorTypeDef,
        "AccessPolicy": str,
    },
    total=False,
)

AwsBackupBackupVaultDetailsTypeDef = TypedDict(
    "AwsBackupBackupVaultDetailsTypeDef",
    {
        "BackupVaultArn": str,
        "BackupVaultName": str,
        "EncryptionKeyArn": str,
        "Notifications": AwsBackupBackupVaultNotificationsDetailsTypeDef,
        "AccessPolicy": str,
    },
    total=False,
)

AwsBackupRecoveryPointDetailsTypeDef = TypedDict(
    "AwsBackupRecoveryPointDetailsTypeDef",
    {
        "BackupSizeInBytes": int,
        "BackupVaultArn": str,
        "BackupVaultName": str,
        "CalculatedLifecycle": AwsBackupRecoveryPointCalculatedLifecycleDetailsTypeDef,
        "CompletionDate": str,
        "CreatedBy": AwsBackupRecoveryPointCreatedByDetailsTypeDef,
        "CreationDate": str,
        "EncryptionKeyArn": str,
        "IamRoleArn": str,
        "IsEncrypted": bool,
        "LastRestoreTime": str,
        "Lifecycle": AwsBackupRecoveryPointLifecycleDetailsTypeDef,
        "RecoveryPointArn": str,
        "ResourceArn": str,
        "ResourceType": str,
        "SourceBackupVaultArn": str,
        "Status": str,
        "StatusMessage": str,
        "StorageClass": str,
    },
    total=False,
)

AwsCertificateManagerCertificateDomainValidationOptionPaginatorTypeDef = TypedDict(
    "AwsCertificateManagerCertificateDomainValidationOptionPaginatorTypeDef",
    {
        "DomainName": str,
        "ResourceRecord": AwsCertificateManagerCertificateResourceRecordTypeDef,
        "ValidationDomain": str,
        "ValidationEmails": List[str],
        "ValidationMethod": str,
        "ValidationStatus": str,
    },
    total=False,
)

AwsCertificateManagerCertificateDomainValidationOptionTypeDef = TypedDict(
    "AwsCertificateManagerCertificateDomainValidationOptionTypeDef",
    {
        "DomainName": str,
        "ResourceRecord": AwsCertificateManagerCertificateResourceRecordTypeDef,
        "ValidationDomain": str,
        "ValidationEmails": Sequence[str],
        "ValidationMethod": str,
        "ValidationStatus": str,
    },
    total=False,
)

AwsCloudFormationStackDetailsPaginatorTypeDef = TypedDict(
    "AwsCloudFormationStackDetailsPaginatorTypeDef",
    {
        "Capabilities": List[str],
        "CreationTime": str,
        "Description": str,
        "DisableRollback": bool,
        "DriftInformation": AwsCloudFormationStackDriftInformationDetailsTypeDef,
        "EnableTerminationProtection": bool,
        "LastUpdatedTime": str,
        "NotificationArns": List[str],
        "Outputs": List[AwsCloudFormationStackOutputsDetailsTypeDef],
        "RoleArn": str,
        "StackId": str,
        "StackName": str,
        "StackStatus": str,
        "StackStatusReason": str,
        "TimeoutInMinutes": int,
    },
    total=False,
)

AwsCloudFormationStackDetailsTypeDef = TypedDict(
    "AwsCloudFormationStackDetailsTypeDef",
    {
        "Capabilities": Sequence[str],
        "CreationTime": str,
        "Description": str,
        "DisableRollback": bool,
        "DriftInformation": AwsCloudFormationStackDriftInformationDetailsTypeDef,
        "EnableTerminationProtection": bool,
        "LastUpdatedTime": str,
        "NotificationArns": Sequence[str],
        "Outputs": Sequence[AwsCloudFormationStackOutputsDetailsTypeDef],
        "RoleArn": str,
        "StackId": str,
        "StackName": str,
        "StackStatus": str,
        "StackStatusReason": str,
        "TimeoutInMinutes": int,
    },
    total=False,
)

AwsCloudFrontDistributionCacheBehaviorsPaginatorTypeDef = TypedDict(
    "AwsCloudFrontDistributionCacheBehaviorsPaginatorTypeDef",
    {
        "Items": List[AwsCloudFrontDistributionCacheBehaviorTypeDef],
    },
    total=False,
)

AwsCloudFrontDistributionCacheBehaviorsTypeDef = TypedDict(
    "AwsCloudFrontDistributionCacheBehaviorsTypeDef",
    {
        "Items": Sequence[AwsCloudFrontDistributionCacheBehaviorTypeDef],
    },
    total=False,
)

AwsCloudFrontDistributionOriginCustomOriginConfigPaginatorTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginCustomOriginConfigPaginatorTypeDef",
    {
        "HttpPort": int,
        "HttpsPort": int,
        "OriginKeepaliveTimeout": int,
        "OriginProtocolPolicy": str,
        "OriginReadTimeout": int,
        "OriginSslProtocols": AwsCloudFrontDistributionOriginSslProtocolsPaginatorTypeDef,
    },
    total=False,
)

AwsCloudFrontDistributionOriginCustomOriginConfigTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginCustomOriginConfigTypeDef",
    {
        "HttpPort": int,
        "HttpsPort": int,
        "OriginKeepaliveTimeout": int,
        "OriginProtocolPolicy": str,
        "OriginReadTimeout": int,
        "OriginSslProtocols": AwsCloudFrontDistributionOriginSslProtocolsTypeDef,
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupFailoverPaginatorTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupFailoverPaginatorTypeDef",
    {
        "StatusCodes": AwsCloudFrontDistributionOriginGroupFailoverStatusCodesPaginatorTypeDef,
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupFailoverTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupFailoverTypeDef",
    {
        "StatusCodes": AwsCloudFrontDistributionOriginGroupFailoverStatusCodesTypeDef,
    },
    total=False,
)

AwsCloudWatchAlarmDetailsPaginatorTypeDef = TypedDict(
    "AwsCloudWatchAlarmDetailsPaginatorTypeDef",
    {
        "ActionsEnabled": bool,
        "AlarmActions": List[str],
        "AlarmArn": str,
        "AlarmConfigurationUpdatedTimestamp": str,
        "AlarmDescription": str,
        "AlarmName": str,
        "ComparisonOperator": str,
        "DatapointsToAlarm": int,
        "Dimensions": List[AwsCloudWatchAlarmDimensionsDetailsTypeDef],
        "EvaluateLowSampleCountPercentile": str,
        "EvaluationPeriods": int,
        "ExtendedStatistic": str,
        "InsufficientDataActions": List[str],
        "MetricName": str,
        "Namespace": str,
        "OkActions": List[str],
        "Period": int,
        "Statistic": str,
        "Threshold": float,
        "ThresholdMetricId": str,
        "TreatMissingData": str,
        "Unit": str,
    },
    total=False,
)

AwsCloudWatchAlarmDetailsTypeDef = TypedDict(
    "AwsCloudWatchAlarmDetailsTypeDef",
    {
        "ActionsEnabled": bool,
        "AlarmActions": Sequence[str],
        "AlarmArn": str,
        "AlarmConfigurationUpdatedTimestamp": str,
        "AlarmDescription": str,
        "AlarmName": str,
        "ComparisonOperator": str,
        "DatapointsToAlarm": int,
        "Dimensions": Sequence[AwsCloudWatchAlarmDimensionsDetailsTypeDef],
        "EvaluateLowSampleCountPercentile": str,
        "EvaluationPeriods": int,
        "ExtendedStatistic": str,
        "InsufficientDataActions": Sequence[str],
        "MetricName": str,
        "Namespace": str,
        "OkActions": Sequence[str],
        "Period": int,
        "Statistic": str,
        "Threshold": float,
        "ThresholdMetricId": str,
        "TreatMissingData": str,
        "Unit": str,
    },
    total=False,
)

AwsCodeBuildProjectEnvironmentPaginatorTypeDef = TypedDict(
    "AwsCodeBuildProjectEnvironmentPaginatorTypeDef",
    {
        "Certificate": str,
        "EnvironmentVariables": List[
            AwsCodeBuildProjectEnvironmentEnvironmentVariablesDetailsTypeDef
        ],
        "PrivilegedMode": bool,
        "ImagePullCredentialsType": str,
        "RegistryCredential": AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef,
        "Type": str,
    },
    total=False,
)

AwsCodeBuildProjectEnvironmentTypeDef = TypedDict(
    "AwsCodeBuildProjectEnvironmentTypeDef",
    {
        "Certificate": str,
        "EnvironmentVariables": Sequence[
            AwsCodeBuildProjectEnvironmentEnvironmentVariablesDetailsTypeDef
        ],
        "PrivilegedMode": bool,
        "ImagePullCredentialsType": str,
        "RegistryCredential": AwsCodeBuildProjectEnvironmentRegistryCredentialTypeDef,
        "Type": str,
    },
    total=False,
)

AwsCodeBuildProjectLogsConfigDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectLogsConfigDetailsTypeDef",
    {
        "CloudWatchLogs": AwsCodeBuildProjectLogsConfigCloudWatchLogsDetailsTypeDef,
        "S3Logs": AwsCodeBuildProjectLogsConfigS3LogsDetailsTypeDef,
    },
    total=False,
)

AwsDynamoDbTableGlobalSecondaryIndexPaginatorTypeDef = TypedDict(
    "AwsDynamoDbTableGlobalSecondaryIndexPaginatorTypeDef",
    {
        "Backfilling": bool,
        "IndexArn": str,
        "IndexName": str,
        "IndexSizeBytes": int,
        "IndexStatus": str,
        "ItemCount": int,
        "KeySchema": List[AwsDynamoDbTableKeySchemaTypeDef],
        "Projection": AwsDynamoDbTableProjectionPaginatorTypeDef,
        "ProvisionedThroughput": AwsDynamoDbTableProvisionedThroughputTypeDef,
    },
    total=False,
)

AwsDynamoDbTableLocalSecondaryIndexPaginatorTypeDef = TypedDict(
    "AwsDynamoDbTableLocalSecondaryIndexPaginatorTypeDef",
    {
        "IndexArn": str,
        "IndexName": str,
        "KeySchema": List[AwsDynamoDbTableKeySchemaTypeDef],
        "Projection": AwsDynamoDbTableProjectionPaginatorTypeDef,
    },
    total=False,
)

AwsDynamoDbTableGlobalSecondaryIndexTypeDef = TypedDict(
    "AwsDynamoDbTableGlobalSecondaryIndexTypeDef",
    {
        "Backfilling": bool,
        "IndexArn": str,
        "IndexName": str,
        "IndexSizeBytes": int,
        "IndexStatus": str,
        "ItemCount": int,
        "KeySchema": Sequence[AwsDynamoDbTableKeySchemaTypeDef],
        "Projection": AwsDynamoDbTableProjectionTypeDef,
        "ProvisionedThroughput": AwsDynamoDbTableProvisionedThroughputTypeDef,
    },
    total=False,
)

AwsDynamoDbTableLocalSecondaryIndexTypeDef = TypedDict(
    "AwsDynamoDbTableLocalSecondaryIndexTypeDef",
    {
        "IndexArn": str,
        "IndexName": str,
        "KeySchema": Sequence[AwsDynamoDbTableKeySchemaTypeDef],
        "Projection": AwsDynamoDbTableProjectionTypeDef,
    },
    total=False,
)

AwsDynamoDbTableReplicaGlobalSecondaryIndexTypeDef = TypedDict(
    "AwsDynamoDbTableReplicaGlobalSecondaryIndexTypeDef",
    {
        "IndexName": str,
        "ProvisionedThroughputOverride": AwsDynamoDbTableProvisionedThroughputOverrideTypeDef,
    },
    total=False,
)

AwsEc2InstanceDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2InstanceDetailsPaginatorTypeDef",
    {
        "Type": str,
        "ImageId": str,
        "IpV4Addresses": List[str],
        "IpV6Addresses": List[str],
        "KeyName": str,
        "IamInstanceProfileArn": str,
        "VpcId": str,
        "SubnetId": str,
        "LaunchedAt": str,
        "NetworkInterfaces": List[AwsEc2InstanceNetworkInterfacesDetailsTypeDef],
        "VirtualizationType": str,
        "MetadataOptions": AwsEc2InstanceMetadataOptionsTypeDef,
        "Monitoring": AwsEc2InstanceMonitoringDetailsTypeDef,
    },
    total=False,
)

AwsEc2InstanceDetailsTypeDef = TypedDict(
    "AwsEc2InstanceDetailsTypeDef",
    {
        "Type": str,
        "ImageId": str,
        "IpV4Addresses": Sequence[str],
        "IpV6Addresses": Sequence[str],
        "KeyName": str,
        "IamInstanceProfileArn": str,
        "VpcId": str,
        "SubnetId": str,
        "LaunchedAt": str,
        "NetworkInterfaces": Sequence[AwsEc2InstanceNetworkInterfacesDetailsTypeDef],
        "VirtualizationType": str,
        "MetadataOptions": AwsEc2InstanceMetadataOptionsTypeDef,
        "Monitoring": AwsEc2InstanceMonitoringDetailsTypeDef,
    },
    total=False,
)

AwsEc2LaunchTemplateDataBlockDeviceMappingSetDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataBlockDeviceMappingSetDetailsTypeDef",
    {
        "DeviceName": str,
        "Ebs": AwsEc2LaunchTemplateDataBlockDeviceMappingSetEbsDetailsTypeDef,
        "NoDevice": str,
        "VirtualName": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataCapacityReservationSpecificationDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataCapacityReservationSpecificationDetailsTypeDef",
    {
        "CapacityReservationPreference": str,
        "CapacityReservationTarget": AwsEc2LaunchTemplateDataCapacityReservationSpecificationCapacityReservationTargetDetailsTypeDef,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceMarketOptionsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceMarketOptionsDetailsTypeDef",
    {
        "MarketType": str,
        "SpotOptions": AwsEc2LaunchTemplateDataInstanceMarketOptionsSpotOptionsDetailsTypeDef,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceRequirementsDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceRequirementsDetailsPaginatorTypeDef",
    {
        "AcceleratorCount": (
            AwsEc2LaunchTemplateDataInstanceRequirementsAcceleratorCountDetailsTypeDef
        ),
        "AcceleratorManufacturers": List[str],
        "AcceleratorNames": List[str],
        "AcceleratorTotalMemoryMiB": (
            AwsEc2LaunchTemplateDataInstanceRequirementsAcceleratorTotalMemoryMiBDetailsTypeDef
        ),
        "AcceleratorTypes": List[str],
        "BareMetal": str,
        "BaselineEbsBandwidthMbps": (
            AwsEc2LaunchTemplateDataInstanceRequirementsBaselineEbsBandwidthMbpsDetailsTypeDef
        ),
        "BurstablePerformance": str,
        "CpuManufacturers": List[str],
        "ExcludedInstanceTypes": List[str],
        "InstanceGenerations": List[str],
        "LocalStorage": str,
        "LocalStorageTypes": List[str],
        "MemoryGiBPerVCpu": (
            AwsEc2LaunchTemplateDataInstanceRequirementsMemoryGiBPerVCpuDetailsTypeDef
        ),
        "MemoryMiB": AwsEc2LaunchTemplateDataInstanceRequirementsMemoryMiBDetailsTypeDef,
        "NetworkInterfaceCount": (
            AwsEc2LaunchTemplateDataInstanceRequirementsNetworkInterfaceCountDetailsTypeDef
        ),
        "OnDemandMaxPricePercentageOverLowestPrice": int,
        "RequireHibernateSupport": bool,
        "SpotMaxPricePercentageOverLowestPrice": int,
        "TotalLocalStorageGB": (
            AwsEc2LaunchTemplateDataInstanceRequirementsTotalLocalStorageGBDetailsTypeDef
        ),
        "VCpuCount": AwsEc2LaunchTemplateDataInstanceRequirementsVCpuCountDetailsTypeDef,
    },
    total=False,
)

AwsEc2LaunchTemplateDataInstanceRequirementsDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataInstanceRequirementsDetailsTypeDef",
    {
        "AcceleratorCount": (
            AwsEc2LaunchTemplateDataInstanceRequirementsAcceleratorCountDetailsTypeDef
        ),
        "AcceleratorManufacturers": Sequence[str],
        "AcceleratorNames": Sequence[str],
        "AcceleratorTotalMemoryMiB": (
            AwsEc2LaunchTemplateDataInstanceRequirementsAcceleratorTotalMemoryMiBDetailsTypeDef
        ),
        "AcceleratorTypes": Sequence[str],
        "BareMetal": str,
        "BaselineEbsBandwidthMbps": (
            AwsEc2LaunchTemplateDataInstanceRequirementsBaselineEbsBandwidthMbpsDetailsTypeDef
        ),
        "BurstablePerformance": str,
        "CpuManufacturers": Sequence[str],
        "ExcludedInstanceTypes": Sequence[str],
        "InstanceGenerations": Sequence[str],
        "LocalStorage": str,
        "LocalStorageTypes": Sequence[str],
        "MemoryGiBPerVCpu": (
            AwsEc2LaunchTemplateDataInstanceRequirementsMemoryGiBPerVCpuDetailsTypeDef
        ),
        "MemoryMiB": AwsEc2LaunchTemplateDataInstanceRequirementsMemoryMiBDetailsTypeDef,
        "NetworkInterfaceCount": (
            AwsEc2LaunchTemplateDataInstanceRequirementsNetworkInterfaceCountDetailsTypeDef
        ),
        "OnDemandMaxPricePercentageOverLowestPrice": int,
        "RequireHibernateSupport": bool,
        "SpotMaxPricePercentageOverLowestPrice": int,
        "TotalLocalStorageGB": (
            AwsEc2LaunchTemplateDataInstanceRequirementsTotalLocalStorageGBDetailsTypeDef
        ),
        "VCpuCount": AwsEc2LaunchTemplateDataInstanceRequirementsVCpuCountDetailsTypeDef,
    },
    total=False,
)

AwsEc2LaunchTemplateDataNetworkInterfaceSetDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetDetailsPaginatorTypeDef",
    {
        "AssociateCarrierIpAddress": bool,
        "AssociatePublicIpAddress": bool,
        "DeleteOnTermination": bool,
        "Description": str,
        "DeviceIndex": int,
        "Groups": List[str],
        "InterfaceType": str,
        "Ipv4PrefixCount": int,
        "Ipv4Prefixes": List[AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv4PrefixesDetailsTypeDef],
        "Ipv6AddressCount": int,
        "Ipv6Addresses": List[
            AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv6AddressesDetailsTypeDef
        ],
        "Ipv6PrefixCount": int,
        "Ipv6Prefixes": List[AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv6PrefixesDetailsTypeDef],
        "NetworkCardIndex": int,
        "NetworkInterfaceId": str,
        "PrivateIpAddress": str,
        "PrivateIpAddresses": List[
            AwsEc2LaunchTemplateDataNetworkInterfaceSetPrivateIpAddressesDetailsTypeDef
        ],
        "SecondaryPrivateIpAddressCount": int,
        "SubnetId": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataNetworkInterfaceSetDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataNetworkInterfaceSetDetailsTypeDef",
    {
        "AssociateCarrierIpAddress": bool,
        "AssociatePublicIpAddress": bool,
        "DeleteOnTermination": bool,
        "Description": str,
        "DeviceIndex": int,
        "Groups": Sequence[str],
        "InterfaceType": str,
        "Ipv4PrefixCount": int,
        "Ipv4Prefixes": Sequence[
            AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv4PrefixesDetailsTypeDef
        ],
        "Ipv6AddressCount": int,
        "Ipv6Addresses": Sequence[
            AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv6AddressesDetailsTypeDef
        ],
        "Ipv6PrefixCount": int,
        "Ipv6Prefixes": Sequence[
            AwsEc2LaunchTemplateDataNetworkInterfaceSetIpv6PrefixesDetailsTypeDef
        ],
        "NetworkCardIndex": int,
        "NetworkInterfaceId": str,
        "PrivateIpAddress": str,
        "PrivateIpAddresses": Sequence[
            AwsEc2LaunchTemplateDataNetworkInterfaceSetPrivateIpAddressesDetailsTypeDef
        ],
        "SecondaryPrivateIpAddressCount": int,
        "SubnetId": str,
    },
    total=False,
)

AwsEc2NetworkAclEntryTypeDef = TypedDict(
    "AwsEc2NetworkAclEntryTypeDef",
    {
        "CidrBlock": str,
        "Egress": bool,
        "IcmpTypeCode": IcmpTypeCodeTypeDef,
        "Ipv6CidrBlock": str,
        "PortRange": PortRangeFromToTypeDef,
        "Protocol": str,
        "RuleAction": str,
        "RuleNumber": int,
    },
    total=False,
)

AwsEc2NetworkInterfaceDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceDetailsPaginatorTypeDef",
    {
        "Attachment": AwsEc2NetworkInterfaceAttachmentTypeDef,
        "NetworkInterfaceId": str,
        "SecurityGroups": List[AwsEc2NetworkInterfaceSecurityGroupTypeDef],
        "SourceDestCheck": bool,
        "IpV6Addresses": List[AwsEc2NetworkInterfaceIpV6AddressDetailTypeDef],
        "PrivateIpAddresses": List[AwsEc2NetworkInterfacePrivateIpAddressDetailTypeDef],
        "PublicDnsName": str,
        "PublicIp": str,
    },
    total=False,
)

AwsEc2NetworkInterfaceDetailsTypeDef = TypedDict(
    "AwsEc2NetworkInterfaceDetailsTypeDef",
    {
        "Attachment": AwsEc2NetworkInterfaceAttachmentTypeDef,
        "NetworkInterfaceId": str,
        "SecurityGroups": Sequence[AwsEc2NetworkInterfaceSecurityGroupTypeDef],
        "SourceDestCheck": bool,
        "IpV6Addresses": Sequence[AwsEc2NetworkInterfaceIpV6AddressDetailTypeDef],
        "PrivateIpAddresses": Sequence[AwsEc2NetworkInterfacePrivateIpAddressDetailTypeDef],
        "PublicDnsName": str,
        "PublicIp": str,
    },
    total=False,
)

AwsEc2SecurityGroupIpPermissionPaginatorTypeDef = TypedDict(
    "AwsEc2SecurityGroupIpPermissionPaginatorTypeDef",
    {
        "IpProtocol": str,
        "FromPort": int,
        "ToPort": int,
        "UserIdGroupPairs": List[AwsEc2SecurityGroupUserIdGroupPairTypeDef],
        "IpRanges": List[AwsEc2SecurityGroupIpRangeTypeDef],
        "Ipv6Ranges": List[AwsEc2SecurityGroupIpv6RangeTypeDef],
        "PrefixListIds": List[AwsEc2SecurityGroupPrefixListIdTypeDef],
    },
    total=False,
)

AwsEc2SecurityGroupIpPermissionTypeDef = TypedDict(
    "AwsEc2SecurityGroupIpPermissionTypeDef",
    {
        "IpProtocol": str,
        "FromPort": int,
        "ToPort": int,
        "UserIdGroupPairs": Sequence[AwsEc2SecurityGroupUserIdGroupPairTypeDef],
        "IpRanges": Sequence[AwsEc2SecurityGroupIpRangeTypeDef],
        "Ipv6Ranges": Sequence[AwsEc2SecurityGroupIpv6RangeTypeDef],
        "PrefixListIds": Sequence[AwsEc2SecurityGroupPrefixListIdTypeDef],
    },
    total=False,
)

AwsEc2SubnetDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2SubnetDetailsPaginatorTypeDef",
    {
        "AssignIpv6AddressOnCreation": bool,
        "AvailabilityZone": str,
        "AvailabilityZoneId": str,
        "AvailableIpAddressCount": int,
        "CidrBlock": str,
        "DefaultForAz": bool,
        "MapPublicIpOnLaunch": bool,
        "OwnerId": str,
        "State": str,
        "SubnetArn": str,
        "SubnetId": str,
        "VpcId": str,
        "Ipv6CidrBlockAssociationSet": List[Ipv6CidrBlockAssociationTypeDef],
    },
    total=False,
)

AwsEc2SubnetDetailsTypeDef = TypedDict(
    "AwsEc2SubnetDetailsTypeDef",
    {
        "AssignIpv6AddressOnCreation": bool,
        "AvailabilityZone": str,
        "AvailabilityZoneId": str,
        "AvailableIpAddressCount": int,
        "CidrBlock": str,
        "DefaultForAz": bool,
        "MapPublicIpOnLaunch": bool,
        "OwnerId": str,
        "State": str,
        "SubnetArn": str,
        "SubnetId": str,
        "VpcId": str,
        "Ipv6CidrBlockAssociationSet": Sequence[Ipv6CidrBlockAssociationTypeDef],
    },
    total=False,
)

AwsEc2VolumeDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2VolumeDetailsPaginatorTypeDef",
    {
        "CreateTime": str,
        "DeviceName": str,
        "Encrypted": bool,
        "Size": int,
        "SnapshotId": str,
        "Status": str,
        "KmsKeyId": str,
        "Attachments": List[AwsEc2VolumeAttachmentTypeDef],
        "VolumeId": str,
        "VolumeType": str,
        "VolumeScanStatus": str,
    },
    total=False,
)

AwsEc2VolumeDetailsTypeDef = TypedDict(
    "AwsEc2VolumeDetailsTypeDef",
    {
        "CreateTime": str,
        "DeviceName": str,
        "Encrypted": bool,
        "Size": int,
        "SnapshotId": str,
        "Status": str,
        "KmsKeyId": str,
        "Attachments": Sequence[AwsEc2VolumeAttachmentTypeDef],
        "VolumeId": str,
        "VolumeType": str,
        "VolumeScanStatus": str,
    },
    total=False,
)

AwsEc2VpcDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2VpcDetailsPaginatorTypeDef",
    {
        "CidrBlockAssociationSet": List[CidrBlockAssociationTypeDef],
        "Ipv6CidrBlockAssociationSet": List[Ipv6CidrBlockAssociationTypeDef],
        "DhcpOptionsId": str,
        "State": str,
    },
    total=False,
)

AwsEc2VpcDetailsTypeDef = TypedDict(
    "AwsEc2VpcDetailsTypeDef",
    {
        "CidrBlockAssociationSet": Sequence[CidrBlockAssociationTypeDef],
        "Ipv6CidrBlockAssociationSet": Sequence[Ipv6CidrBlockAssociationTypeDef],
        "DhcpOptionsId": str,
        "State": str,
    },
    total=False,
)

AwsEc2VpcEndpointServiceDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2VpcEndpointServiceDetailsPaginatorTypeDef",
    {
        "AcceptanceRequired": bool,
        "AvailabilityZones": List[str],
        "BaseEndpointDnsNames": List[str],
        "ManagesVpcEndpoints": bool,
        "GatewayLoadBalancerArns": List[str],
        "NetworkLoadBalancerArns": List[str],
        "PrivateDnsName": str,
        "ServiceId": str,
        "ServiceName": str,
        "ServiceState": str,
        "ServiceType": List[AwsEc2VpcEndpointServiceServiceTypeDetailsTypeDef],
    },
    total=False,
)

AwsEc2VpcEndpointServiceDetailsTypeDef = TypedDict(
    "AwsEc2VpcEndpointServiceDetailsTypeDef",
    {
        "AcceptanceRequired": bool,
        "AvailabilityZones": Sequence[str],
        "BaseEndpointDnsNames": Sequence[str],
        "ManagesVpcEndpoints": bool,
        "GatewayLoadBalancerArns": Sequence[str],
        "NetworkLoadBalancerArns": Sequence[str],
        "PrivateDnsName": str,
        "ServiceId": str,
        "ServiceName": str,
        "ServiceState": str,
        "ServiceType": Sequence[AwsEc2VpcEndpointServiceServiceTypeDetailsTypeDef],
    },
    total=False,
)

AwsEc2VpcPeeringConnectionVpcInfoDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2VpcPeeringConnectionVpcInfoDetailsPaginatorTypeDef",
    {
        "CidrBlock": str,
        "CidrBlockSet": List[VpcInfoCidrBlockSetDetailsTypeDef],
        "Ipv6CidrBlockSet": List[VpcInfoIpv6CidrBlockSetDetailsTypeDef],
        "OwnerId": str,
        "PeeringOptions": VpcInfoPeeringOptionsDetailsTypeDef,
        "Region": str,
        "VpcId": str,
    },
    total=False,
)

AwsEc2VpcPeeringConnectionVpcInfoDetailsTypeDef = TypedDict(
    "AwsEc2VpcPeeringConnectionVpcInfoDetailsTypeDef",
    {
        "CidrBlock": str,
        "CidrBlockSet": Sequence[VpcInfoCidrBlockSetDetailsTypeDef],
        "Ipv6CidrBlockSet": Sequence[VpcInfoIpv6CidrBlockSetDetailsTypeDef],
        "OwnerId": str,
        "PeeringOptions": VpcInfoPeeringOptionsDetailsTypeDef,
        "Region": str,
        "VpcId": str,
    },
    total=False,
)

AwsEc2VpnConnectionOptionsDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2VpnConnectionOptionsDetailsPaginatorTypeDef",
    {
        "StaticRoutesOnly": bool,
        "TunnelOptions": List[AwsEc2VpnConnectionOptionsTunnelOptionsDetailsPaginatorTypeDef],
    },
    total=False,
)

AwsEc2VpnConnectionOptionsDetailsTypeDef = TypedDict(
    "AwsEc2VpnConnectionOptionsDetailsTypeDef",
    {
        "StaticRoutesOnly": bool,
        "TunnelOptions": Sequence[AwsEc2VpnConnectionOptionsTunnelOptionsDetailsTypeDef],
    },
    total=False,
)

AwsEcrRepositoryDetailsTypeDef = TypedDict(
    "AwsEcrRepositoryDetailsTypeDef",
    {
        "Arn": str,
        "ImageScanningConfiguration": AwsEcrRepositoryImageScanningConfigurationDetailsTypeDef,
        "ImageTagMutability": str,
        "LifecyclePolicy": AwsEcrRepositoryLifecyclePolicyDetailsTypeDef,
        "RepositoryName": str,
        "RepositoryPolicyText": str,
    },
    total=False,
)

AwsEcsClusterConfigurationExecuteCommandConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsClusterConfigurationExecuteCommandConfigurationDetailsTypeDef",
    {
        "KmsKeyId": str,
        "LogConfiguration": (
            AwsEcsClusterConfigurationExecuteCommandConfigurationLogConfigurationDetailsTypeDef
        ),
        "Logging": str,
    },
    total=False,
)

AwsEcsContainerDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsContainerDetailsPaginatorTypeDef",
    {
        "Name": str,
        "Image": str,
        "MountPoints": List[AwsMountPointTypeDef],
        "Privileged": bool,
    },
    total=False,
)

AwsEcsContainerDetailsTypeDef = TypedDict(
    "AwsEcsContainerDetailsTypeDef",
    {
        "Name": str,
        "Image": str,
        "MountPoints": Sequence[AwsMountPointTypeDef],
        "Privileged": bool,
    },
    total=False,
)

AwsEcsServiceDeploymentConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsServiceDeploymentConfigurationDetailsTypeDef",
    {
        "DeploymentCircuitBreaker": (
            AwsEcsServiceDeploymentConfigurationDeploymentCircuitBreakerDetailsTypeDef
        ),
        "MaximumPercent": int,
        "MinimumHealthyPercent": int,
    },
    total=False,
)

AwsEcsServiceNetworkConfigurationDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsServiceNetworkConfigurationDetailsPaginatorTypeDef",
    {
        "AwsVpcConfiguration": (
            AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsPaginatorTypeDef
        ),
    },
    total=False,
)

AwsEcsServiceNetworkConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsServiceNetworkConfigurationDetailsTypeDef",
    {
        "AwsVpcConfiguration": AwsEcsServiceNetworkConfigurationAwsVpcConfigurationDetailsTypeDef,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsPaginatorTypeDef",
    {
        "Capabilities": AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsPaginatorTypeDef,
        "Devices": List[
            AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsPaginatorTypeDef
        ],
        "InitProcessEnabled": bool,
        "MaxSwap": int,
        "SharedMemorySize": int,
        "Swappiness": int,
        "Tmpfs": List[
            AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsPaginatorTypeDef
        ],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsTypeDef",
    {
        "Capabilities": (
            AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersCapabilitiesDetailsTypeDef
        ),
        "Devices": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDevicesDetailsTypeDef
        ],
        "InitProcessEnabled": bool,
        "MaxSwap": int,
        "SharedMemorySize": int,
        "Swappiness": int,
        "Tmpfs": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersTmpfsDetailsTypeDef
        ],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsPaginatorTypeDef",
    {
        "LogDriver": str,
        "Options": Dict[str, str],
        "SecretOptions": List[
            AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationSecretOptionsDetailsTypeDef
        ],
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsTypeDef",
    {
        "LogDriver": str,
        "Options": Mapping[str, str],
        "SecretOptions": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationSecretOptionsDetailsTypeDef
        ],
    },
    total=False,
)

AwsEcsTaskDefinitionProxyConfigurationDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionProxyConfigurationDetailsPaginatorTypeDef",
    {
        "ContainerName": str,
        "ProxyConfigurationProperties": List[
            AwsEcsTaskDefinitionProxyConfigurationProxyConfigurationPropertiesDetailsTypeDef
        ],
        "Type": str,
    },
    total=False,
)

AwsEcsTaskDefinitionProxyConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionProxyConfigurationDetailsTypeDef",
    {
        "ContainerName": str,
        "ProxyConfigurationProperties": Sequence[
            AwsEcsTaskDefinitionProxyConfigurationProxyConfigurationPropertiesDetailsTypeDef
        ],
        "Type": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationDetailsTypeDef",
    {
        "AuthorizationConfig": (
            AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationAuthorizationConfigDetailsTypeDef
        ),
        "FilesystemId": str,
        "RootDirectory": str,
        "TransitEncryption": str,
        "TransitEncryptionPort": int,
    },
    total=False,
)

AwsEcsTaskVolumeDetailsTypeDef = TypedDict(
    "AwsEcsTaskVolumeDetailsTypeDef",
    {
        "Name": str,
        "Host": AwsEcsTaskVolumeHostDetailsTypeDef,
    },
    total=False,
)

AwsEfsAccessPointRootDirectoryDetailsTypeDef = TypedDict(
    "AwsEfsAccessPointRootDirectoryDetailsTypeDef",
    {
        "CreationInfo": AwsEfsAccessPointRootDirectoryCreationInfoDetailsTypeDef,
        "Path": str,
    },
    total=False,
)

AwsEksClusterLoggingDetailsPaginatorTypeDef = TypedDict(
    "AwsEksClusterLoggingDetailsPaginatorTypeDef",
    {
        "ClusterLogging": List[AwsEksClusterLoggingClusterLoggingDetailsPaginatorTypeDef],
    },
    total=False,
)

AwsEksClusterLoggingDetailsTypeDef = TypedDict(
    "AwsEksClusterLoggingDetailsTypeDef",
    {
        "ClusterLogging": Sequence[AwsEksClusterLoggingClusterLoggingDetailsTypeDef],
    },
    total=False,
)

AwsElasticBeanstalkEnvironmentDetailsPaginatorTypeDef = TypedDict(
    "AwsElasticBeanstalkEnvironmentDetailsPaginatorTypeDef",
    {
        "ApplicationName": str,
        "Cname": str,
        "DateCreated": str,
        "DateUpdated": str,
        "Description": str,
        "EndpointUrl": str,
        "EnvironmentArn": str,
        "EnvironmentId": str,
        "EnvironmentLinks": List[AwsElasticBeanstalkEnvironmentEnvironmentLinkTypeDef],
        "EnvironmentName": str,
        "OptionSettings": List[AwsElasticBeanstalkEnvironmentOptionSettingTypeDef],
        "PlatformArn": str,
        "SolutionStackName": str,
        "Status": str,
        "Tier": AwsElasticBeanstalkEnvironmentTierTypeDef,
        "VersionLabel": str,
    },
    total=False,
)

AwsElasticBeanstalkEnvironmentDetailsTypeDef = TypedDict(
    "AwsElasticBeanstalkEnvironmentDetailsTypeDef",
    {
        "ApplicationName": str,
        "Cname": str,
        "DateCreated": str,
        "DateUpdated": str,
        "Description": str,
        "EndpointUrl": str,
        "EnvironmentArn": str,
        "EnvironmentId": str,
        "EnvironmentLinks": Sequence[AwsElasticBeanstalkEnvironmentEnvironmentLinkTypeDef],
        "EnvironmentName": str,
        "OptionSettings": Sequence[AwsElasticBeanstalkEnvironmentOptionSettingTypeDef],
        "PlatformArn": str,
        "SolutionStackName": str,
        "Status": str,
        "Tier": AwsElasticBeanstalkEnvironmentTierTypeDef,
        "VersionLabel": str,
    },
    total=False,
)

AwsElasticsearchDomainElasticsearchClusterConfigDetailsTypeDef = TypedDict(
    "AwsElasticsearchDomainElasticsearchClusterConfigDetailsTypeDef",
    {
        "DedicatedMasterCount": int,
        "DedicatedMasterEnabled": bool,
        "DedicatedMasterType": str,
        "InstanceCount": int,
        "InstanceType": str,
        "ZoneAwarenessConfig": (
            AwsElasticsearchDomainElasticsearchClusterConfigZoneAwarenessConfigDetailsTypeDef
        ),
        "ZoneAwarenessEnabled": bool,
    },
    total=False,
)

AwsElasticsearchDomainLogPublishingOptionsTypeDef = TypedDict(
    "AwsElasticsearchDomainLogPublishingOptionsTypeDef",
    {
        "IndexSlowLogs": AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef,
        "SearchSlowLogs": AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef,
        "AuditLogs": AwsElasticsearchDomainLogPublishingOptionsLogConfigTypeDef,
    },
    total=False,
)

AwsElbLoadBalancerPoliciesPaginatorTypeDef = TypedDict(
    "AwsElbLoadBalancerPoliciesPaginatorTypeDef",
    {
        "AppCookieStickinessPolicies": List[AwsElbAppCookieStickinessPolicyTypeDef],
        "LbCookieStickinessPolicies": List[AwsElbLbCookieStickinessPolicyTypeDef],
        "OtherPolicies": List[str],
    },
    total=False,
)

AwsElbLoadBalancerPoliciesTypeDef = TypedDict(
    "AwsElbLoadBalancerPoliciesTypeDef",
    {
        "AppCookieStickinessPolicies": Sequence[AwsElbAppCookieStickinessPolicyTypeDef],
        "LbCookieStickinessPolicies": Sequence[AwsElbLbCookieStickinessPolicyTypeDef],
        "OtherPolicies": Sequence[str],
    },
    total=False,
)

AwsElbLoadBalancerAttributesPaginatorTypeDef = TypedDict(
    "AwsElbLoadBalancerAttributesPaginatorTypeDef",
    {
        "AccessLog": AwsElbLoadBalancerAccessLogTypeDef,
        "ConnectionDraining": AwsElbLoadBalancerConnectionDrainingTypeDef,
        "ConnectionSettings": AwsElbLoadBalancerConnectionSettingsTypeDef,
        "CrossZoneLoadBalancing": AwsElbLoadBalancerCrossZoneLoadBalancingTypeDef,
        "AdditionalAttributes": List[AwsElbLoadBalancerAdditionalAttributeTypeDef],
    },
    total=False,
)

AwsElbLoadBalancerAttributesTypeDef = TypedDict(
    "AwsElbLoadBalancerAttributesTypeDef",
    {
        "AccessLog": AwsElbLoadBalancerAccessLogTypeDef,
        "ConnectionDraining": AwsElbLoadBalancerConnectionDrainingTypeDef,
        "ConnectionSettings": AwsElbLoadBalancerConnectionSettingsTypeDef,
        "CrossZoneLoadBalancing": AwsElbLoadBalancerCrossZoneLoadBalancingTypeDef,
        "AdditionalAttributes": Sequence[AwsElbLoadBalancerAdditionalAttributeTypeDef],
    },
    total=False,
)

AwsElbLoadBalancerListenerDescriptionPaginatorTypeDef = TypedDict(
    "AwsElbLoadBalancerListenerDescriptionPaginatorTypeDef",
    {
        "Listener": AwsElbLoadBalancerListenerTypeDef,
        "PolicyNames": List[str],
    },
    total=False,
)

AwsElbLoadBalancerListenerDescriptionTypeDef = TypedDict(
    "AwsElbLoadBalancerListenerDescriptionTypeDef",
    {
        "Listener": AwsElbLoadBalancerListenerTypeDef,
        "PolicyNames": Sequence[str],
    },
    total=False,
)

AwsElbv2LoadBalancerDetailsPaginatorTypeDef = TypedDict(
    "AwsElbv2LoadBalancerDetailsPaginatorTypeDef",
    {
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
        "CanonicalHostedZoneId": str,
        "CreatedTime": str,
        "DNSName": str,
        "IpAddressType": str,
        "Scheme": str,
        "SecurityGroups": List[str],
        "State": LoadBalancerStateTypeDef,
        "Type": str,
        "VpcId": str,
        "LoadBalancerAttributes": List[AwsElbv2LoadBalancerAttributeTypeDef],
    },
    total=False,
)

AwsElbv2LoadBalancerDetailsTypeDef = TypedDict(
    "AwsElbv2LoadBalancerDetailsTypeDef",
    {
        "AvailabilityZones": Sequence[AvailabilityZoneTypeDef],
        "CanonicalHostedZoneId": str,
        "CreatedTime": str,
        "DNSName": str,
        "IpAddressType": str,
        "Scheme": str,
        "SecurityGroups": Sequence[str],
        "State": LoadBalancerStateTypeDef,
        "Type": str,
        "VpcId": str,
        "LoadBalancerAttributes": Sequence[AwsElbv2LoadBalancerAttributeTypeDef],
    },
    total=False,
)

AwsGuardDutyDetectorDataSourcesKubernetesDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDataSourcesKubernetesDetailsTypeDef",
    {
        "AuditLogs": AwsGuardDutyDetectorDataSourcesKubernetesAuditLogsDetailsTypeDef,
    },
    total=False,
)

AwsGuardDutyDetectorDataSourcesMalwareProtectionScanEc2InstanceWithFindingsDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDataSourcesMalwareProtectionScanEc2InstanceWithFindingsDetailsTypeDef",
    {
        "EbsVolumes": AwsGuardDutyDetectorDataSourcesMalwareProtectionScanEc2InstanceWithFindingsEbsVolumesDetailsTypeDef,
    },
    total=False,
)

AwsIamAccessKeySessionContextTypeDef = TypedDict(
    "AwsIamAccessKeySessionContextTypeDef",
    {
        "Attributes": AwsIamAccessKeySessionContextAttributesTypeDef,
        "SessionIssuer": AwsIamAccessKeySessionContextSessionIssuerTypeDef,
    },
    total=False,
)

AwsIamGroupDetailsPaginatorTypeDef = TypedDict(
    "AwsIamGroupDetailsPaginatorTypeDef",
    {
        "AttachedManagedPolicies": List[AwsIamAttachedManagedPolicyTypeDef],
        "CreateDate": str,
        "GroupId": str,
        "GroupName": str,
        "GroupPolicyList": List[AwsIamGroupPolicyTypeDef],
        "Path": str,
    },
    total=False,
)

AwsIamGroupDetailsTypeDef = TypedDict(
    "AwsIamGroupDetailsTypeDef",
    {
        "AttachedManagedPolicies": Sequence[AwsIamAttachedManagedPolicyTypeDef],
        "CreateDate": str,
        "GroupId": str,
        "GroupName": str,
        "GroupPolicyList": Sequence[AwsIamGroupPolicyTypeDef],
        "Path": str,
    },
    total=False,
)

AwsIamInstanceProfilePaginatorTypeDef = TypedDict(
    "AwsIamInstanceProfilePaginatorTypeDef",
    {
        "Arn": str,
        "CreateDate": str,
        "InstanceProfileId": str,
        "InstanceProfileName": str,
        "Path": str,
        "Roles": List[AwsIamInstanceProfileRolePaginatorTypeDef],
    },
    total=False,
)

AwsIamInstanceProfileRoleTypeDef = TypedDict(
    "AwsIamInstanceProfileRoleTypeDef",
    {
        "Arn": str,
        "AssumeRolePolicyDocument": DictOrStrTypeDef,
        "CreateDate": str,
        "Path": str,
        "RoleId": str,
        "RoleName": str,
    },
    total=False,
)

AwsIamPolicyDetailsPaginatorTypeDef = TypedDict(
    "AwsIamPolicyDetailsPaginatorTypeDef",
    {
        "AttachmentCount": int,
        "CreateDate": str,
        "DefaultVersionId": str,
        "Description": str,
        "IsAttachable": bool,
        "Path": str,
        "PermissionsBoundaryUsageCount": int,
        "PolicyId": str,
        "PolicyName": str,
        "PolicyVersionList": List[AwsIamPolicyVersionTypeDef],
        "UpdateDate": str,
    },
    total=False,
)

AwsIamPolicyDetailsTypeDef = TypedDict(
    "AwsIamPolicyDetailsTypeDef",
    {
        "AttachmentCount": int,
        "CreateDate": str,
        "DefaultVersionId": str,
        "Description": str,
        "IsAttachable": bool,
        "Path": str,
        "PermissionsBoundaryUsageCount": int,
        "PolicyId": str,
        "PolicyName": str,
        "PolicyVersionList": Sequence[AwsIamPolicyVersionTypeDef],
        "UpdateDate": str,
    },
    total=False,
)

AwsIamUserDetailsPaginatorTypeDef = TypedDict(
    "AwsIamUserDetailsPaginatorTypeDef",
    {
        "AttachedManagedPolicies": List[AwsIamAttachedManagedPolicyTypeDef],
        "CreateDate": str,
        "GroupList": List[str],
        "Path": str,
        "PermissionsBoundary": AwsIamPermissionsBoundaryTypeDef,
        "UserId": str,
        "UserName": str,
        "UserPolicyList": List[AwsIamUserPolicyTypeDef],
    },
    total=False,
)

AwsIamUserDetailsTypeDef = TypedDict(
    "AwsIamUserDetailsTypeDef",
    {
        "AttachedManagedPolicies": Sequence[AwsIamAttachedManagedPolicyTypeDef],
        "CreateDate": str,
        "GroupList": Sequence[str],
        "Path": str,
        "PermissionsBoundary": AwsIamPermissionsBoundaryTypeDef,
        "UserId": str,
        "UserName": str,
        "UserPolicyList": Sequence[AwsIamUserPolicyTypeDef],
    },
    total=False,
)

AwsKinesisStreamDetailsTypeDef = TypedDict(
    "AwsKinesisStreamDetailsTypeDef",
    {
        "Name": str,
        "Arn": str,
        "StreamEncryption": AwsKinesisStreamStreamEncryptionDetailsTypeDef,
        "ShardCount": int,
        "RetentionPeriodHours": int,
    },
    total=False,
)

AwsLambdaFunctionEnvironmentPaginatorTypeDef = TypedDict(
    "AwsLambdaFunctionEnvironmentPaginatorTypeDef",
    {
        "Variables": Dict[str, str],
        "Error": AwsLambdaFunctionEnvironmentErrorTypeDef,
    },
    total=False,
)

AwsLambdaFunctionEnvironmentTypeDef = TypedDict(
    "AwsLambdaFunctionEnvironmentTypeDef",
    {
        "Variables": Mapping[str, str],
        "Error": AwsLambdaFunctionEnvironmentErrorTypeDef,
    },
    total=False,
)

AwsNetworkFirewallFirewallDetailsPaginatorTypeDef = TypedDict(
    "AwsNetworkFirewallFirewallDetailsPaginatorTypeDef",
    {
        "DeleteProtection": bool,
        "Description": str,
        "FirewallArn": str,
        "FirewallId": str,
        "FirewallName": str,
        "FirewallPolicyArn": str,
        "FirewallPolicyChangeProtection": bool,
        "SubnetChangeProtection": bool,
        "SubnetMappings": List[AwsNetworkFirewallFirewallSubnetMappingsDetailsTypeDef],
        "VpcId": str,
    },
    total=False,
)

AwsNetworkFirewallFirewallDetailsTypeDef = TypedDict(
    "AwsNetworkFirewallFirewallDetailsTypeDef",
    {
        "DeleteProtection": bool,
        "Description": str,
        "FirewallArn": str,
        "FirewallId": str,
        "FirewallName": str,
        "FirewallPolicyArn": str,
        "FirewallPolicyChangeProtection": bool,
        "SubnetChangeProtection": bool,
        "SubnetMappings": Sequence[AwsNetworkFirewallFirewallSubnetMappingsDetailsTypeDef],
        "VpcId": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainAdvancedSecurityOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainAdvancedSecurityOptionsDetailsTypeDef",
    {
        "Enabled": bool,
        "InternalUserDatabaseEnabled": bool,
        "MasterUserOptions": AwsOpenSearchServiceDomainMasterUserOptionsDetailsTypeDef,
    },
    total=False,
)

AwsOpenSearchServiceDomainClusterConfigDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainClusterConfigDetailsTypeDef",
    {
        "InstanceCount": int,
        "WarmEnabled": bool,
        "WarmCount": int,
        "DedicatedMasterEnabled": bool,
        "ZoneAwarenessConfig": (
            AwsOpenSearchServiceDomainClusterConfigZoneAwarenessConfigDetailsTypeDef
        ),
        "DedicatedMasterCount": int,
        "InstanceType": str,
        "WarmType": str,
        "ZoneAwarenessEnabled": bool,
        "DedicatedMasterType": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainLogPublishingOptionsDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainLogPublishingOptionsDetailsTypeDef",
    {
        "IndexSlowLogs": AwsOpenSearchServiceDomainLogPublishingOptionTypeDef,
        "SearchSlowLogs": AwsOpenSearchServiceDomainLogPublishingOptionTypeDef,
        "AuditLogs": AwsOpenSearchServiceDomainLogPublishingOptionTypeDef,
    },
    total=False,
)

AwsRdsDbClusterDetailsPaginatorTypeDef = TypedDict(
    "AwsRdsDbClusterDetailsPaginatorTypeDef",
    {
        "AllocatedStorage": int,
        "AvailabilityZones": List[str],
        "BackupRetentionPeriod": int,
        "DatabaseName": str,
        "Status": str,
        "Endpoint": str,
        "ReaderEndpoint": str,
        "CustomEndpoints": List[str],
        "MultiAz": bool,
        "Engine": str,
        "EngineVersion": str,
        "Port": int,
        "MasterUsername": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "ReadReplicaIdentifiers": List[str],
        "VpcSecurityGroups": List[AwsRdsDbInstanceVpcSecurityGroupTypeDef],
        "HostedZoneId": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbClusterResourceId": str,
        "AssociatedRoles": List[AwsRdsDbClusterAssociatedRoleTypeDef],
        "ClusterCreateTime": str,
        "EnabledCloudWatchLogsExports": List[str],
        "EngineMode": str,
        "DeletionProtection": bool,
        "HttpEndpointEnabled": bool,
        "ActivityStreamStatus": str,
        "CopyTagsToSnapshot": bool,
        "CrossAccountClone": bool,
        "DomainMemberships": List[AwsRdsDbDomainMembershipTypeDef],
        "DbClusterParameterGroup": str,
        "DbSubnetGroup": str,
        "DbClusterOptionGroupMemberships": List[AwsRdsDbClusterOptionGroupMembershipTypeDef],
        "DbClusterIdentifier": str,
        "DbClusterMembers": List[AwsRdsDbClusterMemberTypeDef],
        "IamDatabaseAuthenticationEnabled": bool,
    },
    total=False,
)

AwsRdsDbClusterDetailsTypeDef = TypedDict(
    "AwsRdsDbClusterDetailsTypeDef",
    {
        "AllocatedStorage": int,
        "AvailabilityZones": Sequence[str],
        "BackupRetentionPeriod": int,
        "DatabaseName": str,
        "Status": str,
        "Endpoint": str,
        "ReaderEndpoint": str,
        "CustomEndpoints": Sequence[str],
        "MultiAz": bool,
        "Engine": str,
        "EngineVersion": str,
        "Port": int,
        "MasterUsername": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "ReadReplicaIdentifiers": Sequence[str],
        "VpcSecurityGroups": Sequence[AwsRdsDbInstanceVpcSecurityGroupTypeDef],
        "HostedZoneId": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbClusterResourceId": str,
        "AssociatedRoles": Sequence[AwsRdsDbClusterAssociatedRoleTypeDef],
        "ClusterCreateTime": str,
        "EnabledCloudWatchLogsExports": Sequence[str],
        "EngineMode": str,
        "DeletionProtection": bool,
        "HttpEndpointEnabled": bool,
        "ActivityStreamStatus": str,
        "CopyTagsToSnapshot": bool,
        "CrossAccountClone": bool,
        "DomainMemberships": Sequence[AwsRdsDbDomainMembershipTypeDef],
        "DbClusterParameterGroup": str,
        "DbSubnetGroup": str,
        "DbClusterOptionGroupMemberships": Sequence[AwsRdsDbClusterOptionGroupMembershipTypeDef],
        "DbClusterIdentifier": str,
        "DbClusterMembers": Sequence[AwsRdsDbClusterMemberTypeDef],
        "IamDatabaseAuthenticationEnabled": bool,
    },
    total=False,
)

AwsRdsDbClusterSnapshotDetailsPaginatorTypeDef = TypedDict(
    "AwsRdsDbClusterSnapshotDetailsPaginatorTypeDef",
    {
        "AvailabilityZones": List[str],
        "SnapshotCreateTime": str,
        "Engine": str,
        "AllocatedStorage": int,
        "Status": str,
        "Port": int,
        "VpcId": str,
        "ClusterCreateTime": str,
        "MasterUsername": str,
        "EngineVersion": str,
        "LicenseModel": str,
        "SnapshotType": str,
        "PercentProgress": int,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbClusterIdentifier": str,
        "DbClusterSnapshotIdentifier": str,
        "IamDatabaseAuthenticationEnabled": bool,
        "DbClusterSnapshotAttributes": List[
            AwsRdsDbClusterSnapshotDbClusterSnapshotAttributePaginatorTypeDef
        ],
    },
    total=False,
)

AwsRdsDbClusterSnapshotDetailsTypeDef = TypedDict(
    "AwsRdsDbClusterSnapshotDetailsTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "SnapshotCreateTime": str,
        "Engine": str,
        "AllocatedStorage": int,
        "Status": str,
        "Port": int,
        "VpcId": str,
        "ClusterCreateTime": str,
        "MasterUsername": str,
        "EngineVersion": str,
        "LicenseModel": str,
        "SnapshotType": str,
        "PercentProgress": int,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbClusterIdentifier": str,
        "DbClusterSnapshotIdentifier": str,
        "IamDatabaseAuthenticationEnabled": bool,
        "DbClusterSnapshotAttributes": Sequence[
            AwsRdsDbClusterSnapshotDbClusterSnapshotAttributeTypeDef
        ],
    },
    total=False,
)

AwsRdsDbSnapshotDetailsPaginatorTypeDef = TypedDict(
    "AwsRdsDbSnapshotDetailsPaginatorTypeDef",
    {
        "DbSnapshotIdentifier": str,
        "DbInstanceIdentifier": str,
        "SnapshotCreateTime": str,
        "Engine": str,
        "AllocatedStorage": int,
        "Status": str,
        "Port": int,
        "AvailabilityZone": str,
        "VpcId": str,
        "InstanceCreateTime": str,
        "MasterUsername": str,
        "EngineVersion": str,
        "LicenseModel": str,
        "SnapshotType": str,
        "Iops": int,
        "OptionGroupName": str,
        "PercentProgress": int,
        "SourceRegion": str,
        "SourceDbSnapshotIdentifier": str,
        "StorageType": str,
        "TdeCredentialArn": str,
        "Encrypted": bool,
        "KmsKeyId": str,
        "Timezone": str,
        "IamDatabaseAuthenticationEnabled": bool,
        "ProcessorFeatures": List[AwsRdsDbProcessorFeatureTypeDef],
        "DbiResourceId": str,
    },
    total=False,
)

AwsRdsDbSnapshotDetailsTypeDef = TypedDict(
    "AwsRdsDbSnapshotDetailsTypeDef",
    {
        "DbSnapshotIdentifier": str,
        "DbInstanceIdentifier": str,
        "SnapshotCreateTime": str,
        "Engine": str,
        "AllocatedStorage": int,
        "Status": str,
        "Port": int,
        "AvailabilityZone": str,
        "VpcId": str,
        "InstanceCreateTime": str,
        "MasterUsername": str,
        "EngineVersion": str,
        "LicenseModel": str,
        "SnapshotType": str,
        "Iops": int,
        "OptionGroupName": str,
        "PercentProgress": int,
        "SourceRegion": str,
        "SourceDbSnapshotIdentifier": str,
        "StorageType": str,
        "TdeCredentialArn": str,
        "Encrypted": bool,
        "KmsKeyId": str,
        "Timezone": str,
        "IamDatabaseAuthenticationEnabled": bool,
        "ProcessorFeatures": Sequence[AwsRdsDbProcessorFeatureTypeDef],
        "DbiResourceId": str,
    },
    total=False,
)

AwsRdsDbPendingModifiedValuesPaginatorTypeDef = TypedDict(
    "AwsRdsDbPendingModifiedValuesPaginatorTypeDef",
    {
        "DbInstanceClass": str,
        "AllocatedStorage": int,
        "MasterUserPassword": str,
        "Port": int,
        "BackupRetentionPeriod": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "LicenseModel": str,
        "Iops": int,
        "DbInstanceIdentifier": str,
        "StorageType": str,
        "CaCertificateIdentifier": str,
        "DbSubnetGroupName": str,
        "PendingCloudWatchLogsExports": AwsRdsPendingCloudWatchLogsExportsPaginatorTypeDef,
        "ProcessorFeatures": List[AwsRdsDbProcessorFeatureTypeDef],
    },
    total=False,
)

AwsRdsDbPendingModifiedValuesTypeDef = TypedDict(
    "AwsRdsDbPendingModifiedValuesTypeDef",
    {
        "DbInstanceClass": str,
        "AllocatedStorage": int,
        "MasterUserPassword": str,
        "Port": int,
        "BackupRetentionPeriod": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "LicenseModel": str,
        "Iops": int,
        "DbInstanceIdentifier": str,
        "StorageType": str,
        "CaCertificateIdentifier": str,
        "DbSubnetGroupName": str,
        "PendingCloudWatchLogsExports": AwsRdsPendingCloudWatchLogsExportsTypeDef,
        "ProcessorFeatures": Sequence[AwsRdsDbProcessorFeatureTypeDef],
    },
    total=False,
)

AwsRdsDbSecurityGroupDetailsPaginatorTypeDef = TypedDict(
    "AwsRdsDbSecurityGroupDetailsPaginatorTypeDef",
    {
        "DbSecurityGroupArn": str,
        "DbSecurityGroupDescription": str,
        "DbSecurityGroupName": str,
        "Ec2SecurityGroups": List[AwsRdsDbSecurityGroupEc2SecurityGroupTypeDef],
        "IpRanges": List[AwsRdsDbSecurityGroupIpRangeTypeDef],
        "OwnerId": str,
        "VpcId": str,
    },
    total=False,
)

AwsRdsDbSecurityGroupDetailsTypeDef = TypedDict(
    "AwsRdsDbSecurityGroupDetailsTypeDef",
    {
        "DbSecurityGroupArn": str,
        "DbSecurityGroupDescription": str,
        "DbSecurityGroupName": str,
        "Ec2SecurityGroups": Sequence[AwsRdsDbSecurityGroupEc2SecurityGroupTypeDef],
        "IpRanges": Sequence[AwsRdsDbSecurityGroupIpRangeTypeDef],
        "OwnerId": str,
        "VpcId": str,
    },
    total=False,
)

AwsRdsDbSubnetGroupSubnetTypeDef = TypedDict(
    "AwsRdsDbSubnetGroupSubnetTypeDef",
    {
        "SubnetIdentifier": str,
        "SubnetAvailabilityZone": AwsRdsDbSubnetGroupSubnetAvailabilityZoneTypeDef,
        "SubnetStatus": str,
    },
    total=False,
)

AwsRedshiftClusterClusterParameterGroupPaginatorTypeDef = TypedDict(
    "AwsRedshiftClusterClusterParameterGroupPaginatorTypeDef",
    {
        "ClusterParameterStatusList": List[AwsRedshiftClusterClusterParameterStatusTypeDef],
        "ParameterApplyStatus": str,
        "ParameterGroupName": str,
    },
    total=False,
)

AwsRedshiftClusterClusterParameterGroupTypeDef = TypedDict(
    "AwsRedshiftClusterClusterParameterGroupTypeDef",
    {
        "ClusterParameterStatusList": Sequence[AwsRedshiftClusterClusterParameterStatusTypeDef],
        "ParameterApplyStatus": str,
        "ParameterGroupName": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsDetailsTypeDef",
    {
        "Prefix": str,
        "Tag": AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsTagDetailsTypeDef,
        "Type": str,
    },
    total=False,
)

AwsS3BucketNotificationConfigurationS3KeyFilterPaginatorTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationS3KeyFilterPaginatorTypeDef",
    {
        "FilterRules": List[AwsS3BucketNotificationConfigurationS3KeyFilterRuleTypeDef],
    },
    total=False,
)

AwsS3BucketNotificationConfigurationS3KeyFilterTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationS3KeyFilterTypeDef",
    {
        "FilterRules": Sequence[AwsS3BucketNotificationConfigurationS3KeyFilterRuleTypeDef],
    },
    total=False,
)

AwsS3BucketObjectLockConfigurationRuleDetailsTypeDef = TypedDict(
    "AwsS3BucketObjectLockConfigurationRuleDetailsTypeDef",
    {
        "DefaultRetention": AwsS3BucketObjectLockConfigurationRuleDefaultRetentionDetailsTypeDef,
    },
    total=False,
)

AwsS3BucketServerSideEncryptionRuleTypeDef = TypedDict(
    "AwsS3BucketServerSideEncryptionRuleTypeDef",
    {
        "ApplyServerSideEncryptionByDefault": AwsS3BucketServerSideEncryptionByDefaultTypeDef,
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationRoutingRuleTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationRoutingRuleTypeDef",
    {
        "Condition": AwsS3BucketWebsiteConfigurationRoutingRuleConditionTypeDef,
        "Redirect": AwsS3BucketWebsiteConfigurationRoutingRuleRedirectTypeDef,
    },
    total=False,
)

AwsSageMakerNotebookInstanceDetailsPaginatorTypeDef = TypedDict(
    "AwsSageMakerNotebookInstanceDetailsPaginatorTypeDef",
    {
        "AcceleratorTypes": List[str],
        "AdditionalCodeRepositories": List[str],
        "DefaultCodeRepository": str,
        "DirectInternetAccess": str,
        "FailureReason": str,
        "InstanceMetadataServiceConfiguration": (
            AwsSageMakerNotebookInstanceMetadataServiceConfigurationDetailsTypeDef
        ),
        "InstanceType": str,
        "KmsKeyId": str,
        "NetworkInterfaceId": str,
        "NotebookInstanceArn": str,
        "NotebookInstanceLifecycleConfigName": str,
        "NotebookInstanceName": str,
        "NotebookInstanceStatus": str,
        "PlatformIdentifier": str,
        "RoleArn": str,
        "RootAccess": str,
        "SecurityGroups": List[str],
        "SubnetId": str,
        "Url": str,
        "VolumeSizeInGB": int,
    },
    total=False,
)

AwsSageMakerNotebookInstanceDetailsTypeDef = TypedDict(
    "AwsSageMakerNotebookInstanceDetailsTypeDef",
    {
        "AcceleratorTypes": Sequence[str],
        "AdditionalCodeRepositories": Sequence[str],
        "DefaultCodeRepository": str,
        "DirectInternetAccess": str,
        "FailureReason": str,
        "InstanceMetadataServiceConfiguration": (
            AwsSageMakerNotebookInstanceMetadataServiceConfigurationDetailsTypeDef
        ),
        "InstanceType": str,
        "KmsKeyId": str,
        "NetworkInterfaceId": str,
        "NotebookInstanceArn": str,
        "NotebookInstanceLifecycleConfigName": str,
        "NotebookInstanceName": str,
        "NotebookInstanceStatus": str,
        "PlatformIdentifier": str,
        "RoleArn": str,
        "RootAccess": str,
        "SecurityGroups": Sequence[str],
        "SubnetId": str,
        "Url": str,
        "VolumeSizeInGB": int,
    },
    total=False,
)

AwsSecretsManagerSecretDetailsTypeDef = TypedDict(
    "AwsSecretsManagerSecretDetailsTypeDef",
    {
        "RotationRules": AwsSecretsManagerSecretRotationRulesTypeDef,
        "RotationOccurredWithinFrequency": bool,
        "KmsKeyId": str,
        "RotationEnabled": bool,
        "RotationLambdaArn": str,
        "Deleted": bool,
        "Name": str,
        "Description": str,
    },
    total=False,
)

_RequiredBatchUpdateFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredBatchUpdateFindingsRequestRequestTypeDef",
    {
        "FindingIdentifiers": Sequence[AwsSecurityFindingIdentifierTypeDef],
    },
)
_OptionalBatchUpdateFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalBatchUpdateFindingsRequestRequestTypeDef",
    {
        "Note": NoteUpdateTypeDef,
        "Severity": SeverityUpdateTypeDef,
        "VerificationState": VerificationStateType,
        "Confidence": int,
        "Criticality": int,
        "Types": Sequence[str],
        "UserDefinedFields": Mapping[str, str],
        "Workflow": WorkflowUpdateTypeDef,
        "RelatedFindings": Sequence[RelatedFindingTypeDef],
    },
    total=False,
)


class BatchUpdateFindingsRequestRequestTypeDef(
    _RequiredBatchUpdateFindingsRequestRequestTypeDef,
    _OptionalBatchUpdateFindingsRequestRequestTypeDef,
):
    pass


BatchUpdateFindingsUnprocessedFindingTypeDef = TypedDict(
    "BatchUpdateFindingsUnprocessedFindingTypeDef",
    {
        "FindingIdentifier": AwsSecurityFindingIdentifierTypeDef,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
)

AwsSnsTopicDetailsPaginatorTypeDef = TypedDict(
    "AwsSnsTopicDetailsPaginatorTypeDef",
    {
        "KmsMasterKeyId": str,
        "Subscription": List[AwsSnsTopicSubscriptionTypeDef],
        "TopicName": str,
        "Owner": str,
        "SqsSuccessFeedbackRoleArn": str,
        "SqsFailureFeedbackRoleArn": str,
        "ApplicationSuccessFeedbackRoleArn": str,
        "FirehoseSuccessFeedbackRoleArn": str,
        "FirehoseFailureFeedbackRoleArn": str,
        "HttpSuccessFeedbackRoleArn": str,
        "HttpFailureFeedbackRoleArn": str,
    },
    total=False,
)

AwsSnsTopicDetailsTypeDef = TypedDict(
    "AwsSnsTopicDetailsTypeDef",
    {
        "KmsMasterKeyId": str,
        "Subscription": Sequence[AwsSnsTopicSubscriptionTypeDef],
        "TopicName": str,
        "Owner": str,
        "SqsSuccessFeedbackRoleArn": str,
        "SqsFailureFeedbackRoleArn": str,
        "ApplicationSuccessFeedbackRoleArn": str,
        "FirehoseSuccessFeedbackRoleArn": str,
        "FirehoseFailureFeedbackRoleArn": str,
        "HttpSuccessFeedbackRoleArn": str,
        "HttpFailureFeedbackRoleArn": str,
    },
    total=False,
)

AwsSsmPatchTypeDef = TypedDict(
    "AwsSsmPatchTypeDef",
    {
        "ComplianceSummary": AwsSsmComplianceSummaryTypeDef,
    },
    total=False,
)

AwsStepFunctionStateMachineLoggingConfigurationDestinationsDetailsTypeDef = TypedDict(
    "AwsStepFunctionStateMachineLoggingConfigurationDestinationsDetailsTypeDef",
    {
        "CloudWatchLogsLogGroup": AwsStepFunctionStateMachineLoggingConfigurationDestinationsCloudWatchLogsLogGroupDetailsTypeDef,
    },
    total=False,
)

AwsWafRateBasedRuleDetailsPaginatorTypeDef = TypedDict(
    "AwsWafRateBasedRuleDetailsPaginatorTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "RateKey": str,
        "RateLimit": int,
        "RuleId": str,
        "MatchPredicates": List[AwsWafRateBasedRuleMatchPredicateTypeDef],
    },
    total=False,
)

AwsWafRateBasedRuleDetailsTypeDef = TypedDict(
    "AwsWafRateBasedRuleDetailsTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "RateKey": str,
        "RateLimit": int,
        "RuleId": str,
        "MatchPredicates": Sequence[AwsWafRateBasedRuleMatchPredicateTypeDef],
    },
    total=False,
)

AwsWafRegionalRateBasedRuleDetailsPaginatorTypeDef = TypedDict(
    "AwsWafRegionalRateBasedRuleDetailsPaginatorTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "RateKey": str,
        "RateLimit": int,
        "RuleId": str,
        "MatchPredicates": List[AwsWafRegionalRateBasedRuleMatchPredicateTypeDef],
    },
    total=False,
)

AwsWafRegionalRateBasedRuleDetailsTypeDef = TypedDict(
    "AwsWafRegionalRateBasedRuleDetailsTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "RateKey": str,
        "RateLimit": int,
        "RuleId": str,
        "MatchPredicates": Sequence[AwsWafRegionalRateBasedRuleMatchPredicateTypeDef],
    },
    total=False,
)

AwsWafRegionalRuleDetailsPaginatorTypeDef = TypedDict(
    "AwsWafRegionalRuleDetailsPaginatorTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "PredicateList": List[AwsWafRegionalRulePredicateListDetailsTypeDef],
        "RuleId": str,
    },
    total=False,
)

AwsWafRegionalRuleDetailsTypeDef = TypedDict(
    "AwsWafRegionalRuleDetailsTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "PredicateList": Sequence[AwsWafRegionalRulePredicateListDetailsTypeDef],
        "RuleId": str,
    },
    total=False,
)

AwsWafRegionalRuleGroupRulesDetailsTypeDef = TypedDict(
    "AwsWafRegionalRuleGroupRulesDetailsTypeDef",
    {
        "Action": AwsWafRegionalRuleGroupRulesActionDetailsTypeDef,
        "Priority": int,
        "RuleId": str,
        "Type": str,
    },
    total=False,
)

AwsWafRegionalWebAclRulesListDetailsTypeDef = TypedDict(
    "AwsWafRegionalWebAclRulesListDetailsTypeDef",
    {
        "Action": AwsWafRegionalWebAclRulesListActionDetailsTypeDef,
        "OverrideAction": AwsWafRegionalWebAclRulesListOverrideActionDetailsTypeDef,
        "Priority": int,
        "RuleId": str,
        "Type": str,
    },
    total=False,
)

AwsWafRuleDetailsPaginatorTypeDef = TypedDict(
    "AwsWafRuleDetailsPaginatorTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "PredicateList": List[AwsWafRulePredicateListDetailsTypeDef],
        "RuleId": str,
    },
    total=False,
)

AwsWafRuleDetailsTypeDef = TypedDict(
    "AwsWafRuleDetailsTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "PredicateList": Sequence[AwsWafRulePredicateListDetailsTypeDef],
        "RuleId": str,
    },
    total=False,
)

AwsWafRuleGroupRulesDetailsTypeDef = TypedDict(
    "AwsWafRuleGroupRulesDetailsTypeDef",
    {
        "Action": AwsWafRuleGroupRulesActionDetailsTypeDef,
        "Priority": int,
        "RuleId": str,
        "Type": str,
    },
    total=False,
)

AwsWafWebAclRulePaginatorTypeDef = TypedDict(
    "AwsWafWebAclRulePaginatorTypeDef",
    {
        "Action": WafActionTypeDef,
        "ExcludedRules": List[WafExcludedRuleTypeDef],
        "OverrideAction": WafOverrideActionTypeDef,
        "Priority": int,
        "RuleId": str,
        "Type": str,
    },
    total=False,
)

AwsWafWebAclRuleTypeDef = TypedDict(
    "AwsWafWebAclRuleTypeDef",
    {
        "Action": WafActionTypeDef,
        "ExcludedRules": Sequence[WafExcludedRuleTypeDef],
        "OverrideAction": WafOverrideActionTypeDef,
        "Priority": int,
        "RuleId": str,
        "Type": str,
    },
    total=False,
)

AwsWafv2CustomRequestHandlingDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2CustomRequestHandlingDetailsPaginatorTypeDef",
    {
        "InsertHeaders": List[AwsWafv2CustomHttpHeaderTypeDef],
    },
    total=False,
)

AwsWafv2CustomRequestHandlingDetailsTypeDef = TypedDict(
    "AwsWafv2CustomRequestHandlingDetailsTypeDef",
    {
        "InsertHeaders": Sequence[AwsWafv2CustomHttpHeaderTypeDef],
    },
    total=False,
)

AwsWafv2CustomResponseDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2CustomResponseDetailsPaginatorTypeDef",
    {
        "CustomResponseBodyKey": str,
        "ResponseCode": int,
        "ResponseHeaders": List[AwsWafv2CustomHttpHeaderTypeDef],
    },
    total=False,
)

AwsWafv2CustomResponseDetailsTypeDef = TypedDict(
    "AwsWafv2CustomResponseDetailsTypeDef",
    {
        "CustomResponseBodyKey": str,
        "ResponseCode": int,
        "ResponseHeaders": Sequence[AwsWafv2CustomHttpHeaderTypeDef],
    },
    total=False,
)

AwsWafv2WebAclCaptchaConfigDetailsTypeDef = TypedDict(
    "AwsWafv2WebAclCaptchaConfigDetailsTypeDef",
    {
        "ImmunityTimeProperty": AwsWafv2WebAclCaptchaConfigImmunityTimePropertyDetailsTypeDef,
    },
    total=False,
)

CreateActionTargetResponseTypeDef = TypedDict(
    "CreateActionTargetResponseTypeDef",
    {
        "ActionTargetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAutomationRuleResponseTypeDef = TypedDict(
    "CreateAutomationRuleResponseTypeDef",
    {
        "RuleArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFindingAggregatorResponseTypeDef = TypedDict(
    "CreateFindingAggregatorResponseTypeDef",
    {
        "FindingAggregatorArn": str,
        "FindingAggregationRegion": str,
        "RegionLinkingMode": str,
        "Regions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateInsightResponseTypeDef = TypedDict(
    "CreateInsightResponseTypeDef",
    {
        "InsightArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteActionTargetResponseTypeDef = TypedDict(
    "DeleteActionTargetResponseTypeDef",
    {
        "ActionTargetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteInsightResponseTypeDef = TypedDict(
    "DeleteInsightResponseTypeDef",
    {
        "InsightArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeActionTargetsResponseTypeDef = TypedDict(
    "DescribeActionTargetsResponseTypeDef",
    {
        "ActionTargets": List[ActionTargetTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeHubResponseTypeDef = TypedDict(
    "DescribeHubResponseTypeDef",
    {
        "HubArn": str,
        "SubscribedAt": str,
        "AutoEnableControls": bool,
        "ControlFindingGenerator": ControlFindingGeneratorType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOrganizationConfigurationResponseTypeDef = TypedDict(
    "DescribeOrganizationConfigurationResponseTypeDef",
    {
        "AutoEnable": bool,
        "MemberAccountLimitReached": bool,
        "AutoEnableStandards": AutoEnableStandardsType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableImportFindingsForProductResponseTypeDef = TypedDict(
    "EnableImportFindingsForProductResponseTypeDef",
    {
        "ProductSubscriptionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFindingAggregatorResponseTypeDef = TypedDict(
    "GetFindingAggregatorResponseTypeDef",
    {
        "FindingAggregatorArn": str,
        "FindingAggregationRegion": str,
        "RegionLinkingMode": str,
        "Regions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInvitationsCountResponseTypeDef = TypedDict(
    "GetInvitationsCountResponseTypeDef",
    {
        "InvitationsCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAutomationRulesResponseTypeDef = TypedDict(
    "ListAutomationRulesResponseTypeDef",
    {
        "AutomationRulesMetadata": List[AutomationRulesMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEnabledProductsForImportResponseTypeDef = TypedDict(
    "ListEnabledProductsForImportResponseTypeDef",
    {
        "ProductSubscriptions": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOrganizationAdminAccountsResponseTypeDef = TypedDict(
    "ListOrganizationAdminAccountsResponseTypeDef",
    {
        "AdminAccounts": List[AdminAccountTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFindingAggregatorResponseTypeDef = TypedDict(
    "UpdateFindingAggregatorResponseTypeDef",
    {
        "FindingAggregatorArn": str,
        "FindingAggregationRegion": str,
        "RegionLinkingMode": str,
        "Regions": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDeleteAutomationRulesResponseTypeDef = TypedDict(
    "BatchDeleteAutomationRulesResponseTypeDef",
    {
        "ProcessedAutomationRules": List[str],
        "UnprocessedAutomationRules": List[UnprocessedAutomationRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateAutomationRulesResponseTypeDef = TypedDict(
    "BatchUpdateAutomationRulesResponseTypeDef",
    {
        "ProcessedAutomationRules": List[str],
        "UnprocessedAutomationRules": List[UnprocessedAutomationRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchEnableStandardsRequestRequestTypeDef = TypedDict(
    "BatchEnableStandardsRequestRequestTypeDef",
    {
        "StandardsSubscriptionRequests": Sequence[StandardsSubscriptionRequestTypeDef],
    },
)

BatchGetSecurityControlsResponseTypeDef = TypedDict(
    "BatchGetSecurityControlsResponseTypeDef",
    {
        "SecurityControls": List[SecurityControlTypeDef],
        "UnprocessedIds": List[UnprocessedSecurityControlTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetStandardsControlAssociationsRequestRequestTypeDef = TypedDict(
    "BatchGetStandardsControlAssociationsRequestRequestTypeDef",
    {
        "StandardsControlAssociationIds": Sequence[StandardsControlAssociationIdTypeDef],
    },
)

_RequiredUnprocessedStandardsControlAssociationTypeDef = TypedDict(
    "_RequiredUnprocessedStandardsControlAssociationTypeDef",
    {
        "StandardsControlAssociationId": StandardsControlAssociationIdTypeDef,
        "ErrorCode": UnprocessedErrorCodeType,
    },
)
_OptionalUnprocessedStandardsControlAssociationTypeDef = TypedDict(
    "_OptionalUnprocessedStandardsControlAssociationTypeDef",
    {
        "ErrorReason": str,
    },
    total=False,
)


class UnprocessedStandardsControlAssociationTypeDef(
    _RequiredUnprocessedStandardsControlAssociationTypeDef,
    _OptionalUnprocessedStandardsControlAssociationTypeDef,
):
    pass


BatchImportFindingsResponseTypeDef = TypedDict(
    "BatchImportFindingsResponseTypeDef",
    {
        "FailedCount": int,
        "SuccessCount": int,
        "FailedFindings": List[ImportFindingsErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateStandardsControlAssociationsRequestRequestTypeDef = TypedDict(
    "BatchUpdateStandardsControlAssociationsRequestRequestTypeDef",
    {
        "StandardsControlAssociationUpdates": Sequence[StandardsControlAssociationUpdateTypeDef],
    },
)

_RequiredUnprocessedStandardsControlAssociationUpdateTypeDef = TypedDict(
    "_RequiredUnprocessedStandardsControlAssociationUpdateTypeDef",
    {
        "StandardsControlAssociationUpdate": StandardsControlAssociationUpdateTypeDef,
        "ErrorCode": UnprocessedErrorCodeType,
    },
)
_OptionalUnprocessedStandardsControlAssociationUpdateTypeDef = TypedDict(
    "_OptionalUnprocessedStandardsControlAssociationUpdateTypeDef",
    {
        "ErrorReason": str,
    },
    total=False,
)


class UnprocessedStandardsControlAssociationUpdateTypeDef(
    _RequiredUnprocessedStandardsControlAssociationUpdateTypeDef,
    _OptionalUnprocessedStandardsControlAssociationUpdateTypeDef,
):
    pass


VulnerabilityCodeVulnerabilitiesPaginatorTypeDef = TypedDict(
    "VulnerabilityCodeVulnerabilitiesPaginatorTypeDef",
    {
        "Cwes": List[str],
        "FilePath": CodeVulnerabilitiesFilePathTypeDef,
        "SourceArn": str,
    },
    total=False,
)

VulnerabilityCodeVulnerabilitiesTypeDef = TypedDict(
    "VulnerabilityCodeVulnerabilitiesTypeDef",
    {
        "Cwes": Sequence[str],
        "FilePath": CodeVulnerabilitiesFilePathTypeDef,
        "SourceArn": str,
    },
    total=False,
)

CompliancePaginatorTypeDef = TypedDict(
    "CompliancePaginatorTypeDef",
    {
        "Status": ComplianceStatusType,
        "RelatedRequirements": List[str],
        "StatusReasons": List[StatusReasonTypeDef],
        "SecurityControlId": str,
        "AssociatedStandards": List[AssociatedStandardTypeDef],
    },
    total=False,
)

ComplianceTypeDef = TypedDict(
    "ComplianceTypeDef",
    {
        "Status": ComplianceStatusType,
        "RelatedRequirements": Sequence[str],
        "StatusReasons": Sequence[StatusReasonTypeDef],
        "SecurityControlId": str,
        "AssociatedStandards": Sequence[AssociatedStandardTypeDef],
    },
    total=False,
)

ContainerDetailsPaginatorTypeDef = TypedDict(
    "ContainerDetailsPaginatorTypeDef",
    {
        "ContainerRuntime": str,
        "Name": str,
        "ImageId": str,
        "ImageName": str,
        "LaunchedAt": str,
        "VolumeMounts": List[VolumeMountTypeDef],
        "Privileged": bool,
    },
    total=False,
)

ContainerDetailsTypeDef = TypedDict(
    "ContainerDetailsTypeDef",
    {
        "ContainerRuntime": str,
        "Name": str,
        "ImageId": str,
        "ImageName": str,
        "LaunchedAt": str,
        "VolumeMounts": Sequence[VolumeMountTypeDef],
        "Privileged": bool,
    },
    total=False,
)

CreateMembersResponseTypeDef = TypedDict(
    "CreateMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeclineInvitationsResponseTypeDef = TypedDict(
    "DeclineInvitationsResponseTypeDef",
    {
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteInvitationsResponseTypeDef = TypedDict(
    "DeleteInvitationsResponseTypeDef",
    {
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMembersResponseTypeDef = TypedDict(
    "DeleteMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InviteMembersResponseTypeDef = TypedDict(
    "InviteMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DateFilterTypeDef = TypedDict(
    "DateFilterTypeDef",
    {
        "Start": str,
        "End": str,
        "DateRange": DateRangeTypeDef,
    },
    total=False,
)

DescribeActionTargetsRequestDescribeActionTargetsPaginateTypeDef = TypedDict(
    "DescribeActionTargetsRequestDescribeActionTargetsPaginateTypeDef",
    {
        "ActionTargetArns": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeProductsRequestDescribeProductsPaginateTypeDef = TypedDict(
    "DescribeProductsRequestDescribeProductsPaginateTypeDef",
    {
        "ProductArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef = TypedDict(
    "_RequiredDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef",
    {
        "StandardsSubscriptionArn": str,
    },
)
_OptionalDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef = TypedDict(
    "_OptionalDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef(
    _RequiredDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef,
    _OptionalDescribeStandardsControlsRequestDescribeStandardsControlsPaginateTypeDef,
):
    pass


DescribeStandardsRequestDescribeStandardsPaginateTypeDef = TypedDict(
    "DescribeStandardsRequestDescribeStandardsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetEnabledStandardsRequestGetEnabledStandardsPaginateTypeDef = TypedDict(
    "GetEnabledStandardsRequestGetEnabledStandardsPaginateTypeDef",
    {
        "StandardsSubscriptionArns": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetInsightsRequestGetInsightsPaginateTypeDef = TypedDict(
    "GetInsightsRequestGetInsightsPaginateTypeDef",
    {
        "InsightArns": Sequence[str],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListEnabledProductsForImportRequestListEnabledProductsForImportPaginateTypeDef = TypedDict(
    "ListEnabledProductsForImportRequestListEnabledProductsForImportPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListFindingAggregatorsRequestListFindingAggregatorsPaginateTypeDef = TypedDict(
    "ListFindingAggregatorsRequestListFindingAggregatorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListInvitationsRequestListInvitationsPaginateTypeDef = TypedDict(
    "ListInvitationsRequestListInvitationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListMembersRequestListMembersPaginateTypeDef = TypedDict(
    "ListMembersRequestListMembersPaginateTypeDef",
    {
        "OnlyAssociated": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef = TypedDict(
    "ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSecurityControlDefinitionsRequestListSecurityControlDefinitionsPaginateTypeDef = TypedDict(
    "ListSecurityControlDefinitionsRequestListSecurityControlDefinitionsPaginateTypeDef",
    {
        "StandardsArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef = TypedDict(
    "_RequiredListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef",
    {
        "SecurityControlId": str,
    },
)
_OptionalListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef = TypedDict(
    "_OptionalListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef(
    _RequiredListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef,
    _OptionalListStandardsControlAssociationsRequestListStandardsControlAssociationsPaginateTypeDef,
):
    pass


DescribeProductsResponseTypeDef = TypedDict(
    "DescribeProductsResponseTypeDef",
    {
        "Products": List[ProductTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStandardsControlsResponseTypeDef = TypedDict(
    "DescribeStandardsControlsResponseTypeDef",
    {
        "Controls": List[StandardsControlTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ThreatPaginatorTypeDef = TypedDict(
    "ThreatPaginatorTypeDef",
    {
        "Name": str,
        "Severity": str,
        "ItemCount": int,
        "FilePaths": List[FilePathsTypeDef],
    },
    total=False,
)

ThreatTypeDef = TypedDict(
    "ThreatTypeDef",
    {
        "Name": str,
        "Severity": str,
        "ItemCount": int,
        "FilePaths": Sequence[FilePathsTypeDef],
    },
    total=False,
)

ListFindingAggregatorsResponseTypeDef = TypedDict(
    "ListFindingAggregatorsResponseTypeDef",
    {
        "FindingAggregators": List[FindingAggregatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FindingHistoryRecordTypeDef = TypedDict(
    "FindingHistoryRecordTypeDef",
    {
        "FindingIdentifier": AwsSecurityFindingIdentifierTypeDef,
        "UpdateTime": datetime,
        "FindingCreated": bool,
        "UpdateSource": FindingHistoryUpdateSourceTypeDef,
        "Updates": List[FindingHistoryUpdateTypeDef],
        "NextToken": str,
    },
    total=False,
)

FindingProviderFieldsPaginatorTypeDef = TypedDict(
    "FindingProviderFieldsPaginatorTypeDef",
    {
        "Confidence": int,
        "Criticality": int,
        "RelatedFindings": List[RelatedFindingTypeDef],
        "Severity": FindingProviderSeverityTypeDef,
        "Types": List[str],
    },
    total=False,
)

FindingProviderFieldsTypeDef = TypedDict(
    "FindingProviderFieldsTypeDef",
    {
        "Confidence": int,
        "Criticality": int,
        "RelatedFindings": Sequence[RelatedFindingTypeDef],
        "Severity": FindingProviderSeverityTypeDef,
        "Types": Sequence[str],
    },
    total=False,
)

GetAdministratorAccountResponseTypeDef = TypedDict(
    "GetAdministratorAccountResponseTypeDef",
    {
        "Administrator": InvitationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMasterAccountResponseTypeDef = TypedDict(
    "GetMasterAccountResponseTypeDef",
    {
        "Master": InvitationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInvitationsResponseTypeDef = TypedDict(
    "ListInvitationsResponseTypeDef",
    {
        "Invitations": List[InvitationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetFindingHistoryRequestGetFindingHistoryPaginateTypeDef = TypedDict(
    "_RequiredGetFindingHistoryRequestGetFindingHistoryPaginateTypeDef",
    {
        "FindingIdentifier": AwsSecurityFindingIdentifierTypeDef,
    },
)
_OptionalGetFindingHistoryRequestGetFindingHistoryPaginateTypeDef = TypedDict(
    "_OptionalGetFindingHistoryRequestGetFindingHistoryPaginateTypeDef",
    {
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetFindingHistoryRequestGetFindingHistoryPaginateTypeDef(
    _RequiredGetFindingHistoryRequestGetFindingHistoryPaginateTypeDef,
    _OptionalGetFindingHistoryRequestGetFindingHistoryPaginateTypeDef,
):
    pass


_RequiredGetFindingHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredGetFindingHistoryRequestRequestTypeDef",
    {
        "FindingIdentifier": AwsSecurityFindingIdentifierTypeDef,
    },
)
_OptionalGetFindingHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalGetFindingHistoryRequestRequestTypeDef",
    {
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class GetFindingHistoryRequestRequestTypeDef(
    _RequiredGetFindingHistoryRequestRequestTypeDef, _OptionalGetFindingHistoryRequestRequestTypeDef
):
    pass


GetMembersResponseTypeDef = TypedDict(
    "GetMembersResponseTypeDef",
    {
        "Members": List[MemberTypeDef],
        "UnprocessedAccounts": List[ResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMembersResponseTypeDef = TypedDict(
    "ListMembersResponseTypeDef",
    {
        "Members": List[MemberTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InsightResultsTypeDef = TypedDict(
    "InsightResultsTypeDef",
    {
        "InsightArn": str,
        "GroupByAttribute": str,
        "ResultValues": List[InsightResultValueTypeDef],
    },
)

ListSecurityControlDefinitionsResponseTypeDef = TypedDict(
    "ListSecurityControlDefinitionsResponseTypeDef",
    {
        "SecurityControlDefinitions": List[SecurityControlDefinitionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStandardsControlAssociationsResponseTypeDef = TypedDict(
    "ListStandardsControlAssociationsResponseTypeDef",
    {
        "StandardsControlAssociationSummaries": List[StandardsControlAssociationSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NetworkPathComponentDetailsPaginatorTypeDef = TypedDict(
    "NetworkPathComponentDetailsPaginatorTypeDef",
    {
        "Address": List[str],
        "PortRanges": List[PortRangeTypeDef],
    },
    total=False,
)

NetworkPathComponentDetailsTypeDef = TypedDict(
    "NetworkPathComponentDetailsTypeDef",
    {
        "Address": Sequence[str],
        "PortRanges": Sequence[PortRangeTypeDef],
    },
    total=False,
)

NetworkTypeDef = TypedDict(
    "NetworkTypeDef",
    {
        "Direction": NetworkDirectionType,
        "Protocol": str,
        "OpenPortRange": PortRangeTypeDef,
        "SourceIpV4": str,
        "SourceIpV6": str,
        "SourcePort": int,
        "SourceDomain": str,
        "SourceMac": str,
        "DestinationIpV4": str,
        "DestinationIpV6": str,
        "DestinationPort": int,
        "DestinationDomain": str,
    },
    total=False,
)

PageTypeDef = TypedDict(
    "PageTypeDef",
    {
        "PageNumber": int,
        "LineRange": RangeTypeDef,
        "OffsetRange": RangeTypeDef,
    },
    total=False,
)

RemediationTypeDef = TypedDict(
    "RemediationTypeDef",
    {
        "Recommendation": RecommendationTypeDef,
    },
    total=False,
)

RuleGroupSourceStatefulRulesDetailsPaginatorTypeDef = TypedDict(
    "RuleGroupSourceStatefulRulesDetailsPaginatorTypeDef",
    {
        "Action": str,
        "Header": RuleGroupSourceStatefulRulesHeaderDetailsTypeDef,
        "RuleOptions": List[RuleGroupSourceStatefulRulesOptionsDetailsPaginatorTypeDef],
    },
    total=False,
)

RuleGroupSourceStatefulRulesDetailsTypeDef = TypedDict(
    "RuleGroupSourceStatefulRulesDetailsTypeDef",
    {
        "Action": str,
        "Header": RuleGroupSourceStatefulRulesHeaderDetailsTypeDef,
        "RuleOptions": Sequence[RuleGroupSourceStatefulRulesOptionsDetailsTypeDef],
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesPaginatorTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesPaginatorTypeDef",
    {
        "DestinationPorts": List[
            RuleGroupSourceStatelessRuleMatchAttributesDestinationPortsTypeDef
        ],
        "Destinations": List[RuleGroupSourceStatelessRuleMatchAttributesDestinationsTypeDef],
        "Protocols": List[int],
        "SourcePorts": List[RuleGroupSourceStatelessRuleMatchAttributesSourcePortsTypeDef],
        "Sources": List[RuleGroupSourceStatelessRuleMatchAttributesSourcesTypeDef],
        "TcpFlags": List[RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsPaginatorTypeDef],
    },
    total=False,
)

RuleGroupSourceStatelessRuleMatchAttributesTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleMatchAttributesTypeDef",
    {
        "DestinationPorts": Sequence[
            RuleGroupSourceStatelessRuleMatchAttributesDestinationPortsTypeDef
        ],
        "Destinations": Sequence[RuleGroupSourceStatelessRuleMatchAttributesDestinationsTypeDef],
        "Protocols": Sequence[int],
        "SourcePorts": Sequence[RuleGroupSourceStatelessRuleMatchAttributesSourcePortsTypeDef],
        "Sources": Sequence[RuleGroupSourceStatelessRuleMatchAttributesSourcesTypeDef],
        "TcpFlags": Sequence[RuleGroupSourceStatelessRuleMatchAttributesTcpFlagsTypeDef],
    },
    total=False,
)

RuleGroupVariablesPaginatorTypeDef = TypedDict(
    "RuleGroupVariablesPaginatorTypeDef",
    {
        "IpSets": RuleGroupVariablesIpSetsDetailsPaginatorTypeDef,
        "PortSets": RuleGroupVariablesPortSetsDetailsPaginatorTypeDef,
    },
    total=False,
)

RuleGroupVariablesTypeDef = TypedDict(
    "RuleGroupVariablesTypeDef",
    {
        "IpSets": RuleGroupVariablesIpSetsDetailsTypeDef,
        "PortSets": RuleGroupVariablesPortSetsDetailsTypeDef,
    },
    total=False,
)

StandardTypeDef = TypedDict(
    "StandardTypeDef",
    {
        "StandardsArn": str,
        "Name": str,
        "Description": str,
        "EnabledByDefault": bool,
        "StandardsManagedBy": StandardsManagedByTypeDef,
    },
    total=False,
)

_RequiredStandardsSubscriptionTypeDef = TypedDict(
    "_RequiredStandardsSubscriptionTypeDef",
    {
        "StandardsSubscriptionArn": str,
        "StandardsArn": str,
        "StandardsInput": Dict[str, str],
        "StandardsStatus": StandardsStatusType,
    },
)
_OptionalStandardsSubscriptionTypeDef = TypedDict(
    "_OptionalStandardsSubscriptionTypeDef",
    {
        "StandardsStatusReason": StandardsStatusReasonTypeDef,
    },
    total=False,
)


class StandardsSubscriptionTypeDef(
    _RequiredStandardsSubscriptionTypeDef, _OptionalStandardsSubscriptionTypeDef
):
    pass


StatelessCustomPublishMetricActionPaginatorTypeDef = TypedDict(
    "StatelessCustomPublishMetricActionPaginatorTypeDef",
    {
        "Dimensions": List[StatelessCustomPublishMetricActionDimensionTypeDef],
    },
    total=False,
)

StatelessCustomPublishMetricActionTypeDef = TypedDict(
    "StatelessCustomPublishMetricActionTypeDef",
    {
        "Dimensions": Sequence[StatelessCustomPublishMetricActionDimensionTypeDef],
    },
    total=False,
)

AwsApiCallActionPaginatorTypeDef = TypedDict(
    "AwsApiCallActionPaginatorTypeDef",
    {
        "Api": str,
        "ServiceName": str,
        "CallerType": str,
        "RemoteIpDetails": ActionRemoteIpDetailsTypeDef,
        "DomainDetails": AwsApiCallActionDomainDetailsTypeDef,
        "AffectedResources": Dict[str, str],
        "FirstSeen": str,
        "LastSeen": str,
    },
    total=False,
)

AwsApiCallActionTypeDef = TypedDict(
    "AwsApiCallActionTypeDef",
    {
        "Api": str,
        "ServiceName": str,
        "CallerType": str,
        "RemoteIpDetails": ActionRemoteIpDetailsTypeDef,
        "DomainDetails": AwsApiCallActionDomainDetailsTypeDef,
        "AffectedResources": Mapping[str, str],
        "FirstSeen": str,
        "LastSeen": str,
    },
    total=False,
)

NetworkConnectionActionTypeDef = TypedDict(
    "NetworkConnectionActionTypeDef",
    {
        "ConnectionDirection": str,
        "RemoteIpDetails": ActionRemoteIpDetailsTypeDef,
        "RemotePortDetails": ActionRemotePortDetailsTypeDef,
        "LocalPortDetails": ActionLocalPortDetailsTypeDef,
        "Protocol": str,
        "Blocked": bool,
    },
    total=False,
)

PortProbeDetailTypeDef = TypedDict(
    "PortProbeDetailTypeDef",
    {
        "LocalPortDetails": ActionLocalPortDetailsTypeDef,
        "LocalIpDetails": ActionLocalIpDetailsTypeDef,
        "RemoteIpDetails": ActionRemoteIpDetailsTypeDef,
    },
    total=False,
)

AwsEc2RouteTableDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2RouteTableDetailsPaginatorTypeDef",
    {
        "AssociationSet": List[AssociationSetDetailsTypeDef],
        "OwnerId": str,
        "PropagatingVgwSet": List[PropagatingVgwSetDetailsTypeDef],
        "RouteTableId": str,
        "RouteSet": List[RouteSetDetailsTypeDef],
        "VpcId": str,
    },
    total=False,
)

AwsEc2RouteTableDetailsTypeDef = TypedDict(
    "AwsEc2RouteTableDetailsTypeDef",
    {
        "AssociationSet": Sequence[AssociationSetDetailsTypeDef],
        "OwnerId": str,
        "PropagatingVgwSet": Sequence[PropagatingVgwSetDetailsTypeDef],
        "RouteTableId": str,
        "RouteSet": Sequence[RouteSetDetailsTypeDef],
        "VpcId": str,
    },
    total=False,
)

AutomationRulesActionTypeDef = TypedDict(
    "AutomationRulesActionTypeDef",
    {
        "Type": Literal["FINDING_FIELDS_UPDATE"],
        "FindingFieldsUpdate": AutomationRulesFindingFieldsUpdateTypeDef,
    },
    total=False,
)

AwsAmazonMqBrokerDetailsPaginatorTypeDef = TypedDict(
    "AwsAmazonMqBrokerDetailsPaginatorTypeDef",
    {
        "AuthenticationStrategy": str,
        "AutoMinorVersionUpgrade": bool,
        "BrokerArn": str,
        "BrokerName": str,
        "DeploymentMode": str,
        "EncryptionOptions": AwsAmazonMqBrokerEncryptionOptionsDetailsTypeDef,
        "EngineType": str,
        "EngineVersion": str,
        "HostInstanceType": str,
        "BrokerId": str,
        "LdapServerMetadata": AwsAmazonMqBrokerLdapServerMetadataDetailsPaginatorTypeDef,
        "Logs": AwsAmazonMqBrokerLogsDetailsTypeDef,
        "MaintenanceWindowStartTime": AwsAmazonMqBrokerMaintenanceWindowStartTimeDetailsTypeDef,
        "PubliclyAccessible": bool,
        "SecurityGroups": List[str],
        "StorageType": str,
        "SubnetIds": List[str],
        "Users": List[AwsAmazonMqBrokerUsersDetailsTypeDef],
    },
    total=False,
)

AwsAmazonMqBrokerDetailsTypeDef = TypedDict(
    "AwsAmazonMqBrokerDetailsTypeDef",
    {
        "AuthenticationStrategy": str,
        "AutoMinorVersionUpgrade": bool,
        "BrokerArn": str,
        "BrokerName": str,
        "DeploymentMode": str,
        "EncryptionOptions": AwsAmazonMqBrokerEncryptionOptionsDetailsTypeDef,
        "EngineType": str,
        "EngineVersion": str,
        "HostInstanceType": str,
        "BrokerId": str,
        "LdapServerMetadata": AwsAmazonMqBrokerLdapServerMetadataDetailsTypeDef,
        "Logs": AwsAmazonMqBrokerLogsDetailsTypeDef,
        "MaintenanceWindowStartTime": AwsAmazonMqBrokerMaintenanceWindowStartTimeDetailsTypeDef,
        "PubliclyAccessible": bool,
        "SecurityGroups": Sequence[str],
        "StorageType": str,
        "SubnetIds": Sequence[str],
        "Users": Sequence[AwsAmazonMqBrokerUsersDetailsTypeDef],
    },
    total=False,
)

AwsAppSyncGraphQlApiDetailsPaginatorTypeDef = TypedDict(
    "AwsAppSyncGraphQlApiDetailsPaginatorTypeDef",
    {
        "ApiId": str,
        "Id": str,
        "OpenIdConnectConfig": AwsAppSyncGraphQlApiOpenIdConnectConfigDetailsTypeDef,
        "Name": str,
        "LambdaAuthorizerConfig": AwsAppSyncGraphQlApiLambdaAuthorizerConfigDetailsTypeDef,
        "XrayEnabled": bool,
        "Arn": str,
        "UserPoolConfig": AwsAppSyncGraphQlApiUserPoolConfigDetailsTypeDef,
        "AuthenticationType": str,
        "LogConfig": AwsAppSyncGraphQlApiLogConfigDetailsTypeDef,
        "AdditionalAuthenticationProviders": List[
            AwsAppSyncGraphQlApiAdditionalAuthenticationProvidersDetailsTypeDef
        ],
        "WafWebAclArn": str,
    },
    total=False,
)

AwsAppSyncGraphQlApiDetailsTypeDef = TypedDict(
    "AwsAppSyncGraphQlApiDetailsTypeDef",
    {
        "ApiId": str,
        "Id": str,
        "OpenIdConnectConfig": AwsAppSyncGraphQlApiOpenIdConnectConfigDetailsTypeDef,
        "Name": str,
        "LambdaAuthorizerConfig": AwsAppSyncGraphQlApiLambdaAuthorizerConfigDetailsTypeDef,
        "XrayEnabled": bool,
        "Arn": str,
        "UserPoolConfig": AwsAppSyncGraphQlApiUserPoolConfigDetailsTypeDef,
        "AuthenticationType": str,
        "LogConfig": AwsAppSyncGraphQlApiLogConfigDetailsTypeDef,
        "AdditionalAuthenticationProviders": Sequence[
            AwsAppSyncGraphQlApiAdditionalAuthenticationProvidersDetailsTypeDef
        ],
        "WafWebAclArn": str,
    },
    total=False,
)

AwsAthenaWorkGroupConfigurationDetailsTypeDef = TypedDict(
    "AwsAthenaWorkGroupConfigurationDetailsTypeDef",
    {
        "ResultConfiguration": AwsAthenaWorkGroupConfigurationResultConfigurationDetailsTypeDef,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsPaginatorTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsPaginatorTypeDef",
    {
        "InstancesDistribution": (
            AwsAutoScalingAutoScalingGroupMixedInstancesPolicyInstancesDistributionDetailsTypeDef
        ),
        "LaunchTemplate": (
            AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsPaginatorTypeDef
        ),
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsTypeDef",
    {
        "InstancesDistribution": (
            AwsAutoScalingAutoScalingGroupMixedInstancesPolicyInstancesDistributionDetailsTypeDef
        ),
        "LaunchTemplate": (
            AwsAutoScalingAutoScalingGroupMixedInstancesPolicyLaunchTemplateDetailsTypeDef
        ),
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationDetailsPaginatorTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationDetailsPaginatorTypeDef",
    {
        "AssociatePublicIpAddress": bool,
        "BlockDeviceMappings": List[
            AwsAutoScalingLaunchConfigurationBlockDeviceMappingsDetailsTypeDef
        ],
        "ClassicLinkVpcId": str,
        "ClassicLinkVpcSecurityGroups": List[str],
        "CreatedTime": str,
        "EbsOptimized": bool,
        "IamInstanceProfile": str,
        "ImageId": str,
        "InstanceMonitoring": AwsAutoScalingLaunchConfigurationInstanceMonitoringDetailsTypeDef,
        "InstanceType": str,
        "KernelId": str,
        "KeyName": str,
        "LaunchConfigurationName": str,
        "PlacementTenancy": str,
        "RamdiskId": str,
        "SecurityGroups": List[str],
        "SpotPrice": str,
        "UserData": str,
        "MetadataOptions": AwsAutoScalingLaunchConfigurationMetadataOptionsTypeDef,
    },
    total=False,
)

AwsAutoScalingLaunchConfigurationDetailsTypeDef = TypedDict(
    "AwsAutoScalingLaunchConfigurationDetailsTypeDef",
    {
        "AssociatePublicIpAddress": bool,
        "BlockDeviceMappings": Sequence[
            AwsAutoScalingLaunchConfigurationBlockDeviceMappingsDetailsTypeDef
        ],
        "ClassicLinkVpcId": str,
        "ClassicLinkVpcSecurityGroups": Sequence[str],
        "CreatedTime": str,
        "EbsOptimized": bool,
        "IamInstanceProfile": str,
        "ImageId": str,
        "InstanceMonitoring": AwsAutoScalingLaunchConfigurationInstanceMonitoringDetailsTypeDef,
        "InstanceType": str,
        "KernelId": str,
        "KeyName": str,
        "LaunchConfigurationName": str,
        "PlacementTenancy": str,
        "RamdiskId": str,
        "SecurityGroups": Sequence[str],
        "SpotPrice": str,
        "UserData": str,
        "MetadataOptions": AwsAutoScalingLaunchConfigurationMetadataOptionsTypeDef,
    },
    total=False,
)

AwsBackupBackupPlanRuleDetailsPaginatorTypeDef = TypedDict(
    "AwsBackupBackupPlanRuleDetailsPaginatorTypeDef",
    {
        "TargetBackupVault": str,
        "StartWindowMinutes": int,
        "ScheduleExpression": str,
        "RuleName": str,
        "RuleId": str,
        "EnableContinuousBackup": bool,
        "CompletionWindowMinutes": int,
        "CopyActions": List[AwsBackupBackupPlanRuleCopyActionsDetailsTypeDef],
        "Lifecycle": AwsBackupBackupPlanLifecycleDetailsTypeDef,
    },
    total=False,
)

AwsBackupBackupPlanRuleDetailsTypeDef = TypedDict(
    "AwsBackupBackupPlanRuleDetailsTypeDef",
    {
        "TargetBackupVault": str,
        "StartWindowMinutes": int,
        "ScheduleExpression": str,
        "RuleName": str,
        "RuleId": str,
        "EnableContinuousBackup": bool,
        "CompletionWindowMinutes": int,
        "CopyActions": Sequence[AwsBackupBackupPlanRuleCopyActionsDetailsTypeDef],
        "Lifecycle": AwsBackupBackupPlanLifecycleDetailsTypeDef,
    },
    total=False,
)

AwsCertificateManagerCertificateRenewalSummaryPaginatorTypeDef = TypedDict(
    "AwsCertificateManagerCertificateRenewalSummaryPaginatorTypeDef",
    {
        "DomainValidationOptions": List[
            AwsCertificateManagerCertificateDomainValidationOptionPaginatorTypeDef
        ],
        "RenewalStatus": str,
        "RenewalStatusReason": str,
        "UpdatedAt": str,
    },
    total=False,
)

AwsCertificateManagerCertificateRenewalSummaryTypeDef = TypedDict(
    "AwsCertificateManagerCertificateRenewalSummaryTypeDef",
    {
        "DomainValidationOptions": Sequence[
            AwsCertificateManagerCertificateDomainValidationOptionTypeDef
        ],
        "RenewalStatus": str,
        "RenewalStatusReason": str,
        "UpdatedAt": str,
    },
    total=False,
)

AwsCloudFrontDistributionOriginItemPaginatorTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginItemPaginatorTypeDef",
    {
        "DomainName": str,
        "Id": str,
        "OriginPath": str,
        "S3OriginConfig": AwsCloudFrontDistributionOriginS3OriginConfigTypeDef,
        "CustomOriginConfig": AwsCloudFrontDistributionOriginCustomOriginConfigPaginatorTypeDef,
    },
    total=False,
)

AwsCloudFrontDistributionOriginItemTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginItemTypeDef",
    {
        "DomainName": str,
        "Id": str,
        "OriginPath": str,
        "S3OriginConfig": AwsCloudFrontDistributionOriginS3OriginConfigTypeDef,
        "CustomOriginConfig": AwsCloudFrontDistributionOriginCustomOriginConfigTypeDef,
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupPaginatorTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupPaginatorTypeDef",
    {
        "FailoverCriteria": AwsCloudFrontDistributionOriginGroupFailoverPaginatorTypeDef,
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupTypeDef",
    {
        "FailoverCriteria": AwsCloudFrontDistributionOriginGroupFailoverTypeDef,
    },
    total=False,
)

AwsCodeBuildProjectDetailsPaginatorTypeDef = TypedDict(
    "AwsCodeBuildProjectDetailsPaginatorTypeDef",
    {
        "EncryptionKey": str,
        "Artifacts": List[AwsCodeBuildProjectArtifactsDetailsTypeDef],
        "Environment": AwsCodeBuildProjectEnvironmentPaginatorTypeDef,
        "Name": str,
        "Source": AwsCodeBuildProjectSourceTypeDef,
        "ServiceRole": str,
        "LogsConfig": AwsCodeBuildProjectLogsConfigDetailsTypeDef,
        "VpcConfig": AwsCodeBuildProjectVpcConfigPaginatorTypeDef,
        "SecondaryArtifacts": List[AwsCodeBuildProjectArtifactsDetailsTypeDef],
    },
    total=False,
)

AwsCodeBuildProjectDetailsTypeDef = TypedDict(
    "AwsCodeBuildProjectDetailsTypeDef",
    {
        "EncryptionKey": str,
        "Artifacts": Sequence[AwsCodeBuildProjectArtifactsDetailsTypeDef],
        "Environment": AwsCodeBuildProjectEnvironmentTypeDef,
        "Name": str,
        "Source": AwsCodeBuildProjectSourceTypeDef,
        "ServiceRole": str,
        "LogsConfig": AwsCodeBuildProjectLogsConfigDetailsTypeDef,
        "VpcConfig": AwsCodeBuildProjectVpcConfigTypeDef,
        "SecondaryArtifacts": Sequence[AwsCodeBuildProjectArtifactsDetailsTypeDef],
    },
    total=False,
)

AwsDynamoDbTableReplicaPaginatorTypeDef = TypedDict(
    "AwsDynamoDbTableReplicaPaginatorTypeDef",
    {
        "GlobalSecondaryIndexes": List[AwsDynamoDbTableReplicaGlobalSecondaryIndexTypeDef],
        "KmsMasterKeyId": str,
        "ProvisionedThroughputOverride": AwsDynamoDbTableProvisionedThroughputOverrideTypeDef,
        "RegionName": str,
        "ReplicaStatus": str,
        "ReplicaStatusDescription": str,
    },
    total=False,
)

AwsDynamoDbTableReplicaTypeDef = TypedDict(
    "AwsDynamoDbTableReplicaTypeDef",
    {
        "GlobalSecondaryIndexes": Sequence[AwsDynamoDbTableReplicaGlobalSecondaryIndexTypeDef],
        "KmsMasterKeyId": str,
        "ProvisionedThroughputOverride": AwsDynamoDbTableProvisionedThroughputOverrideTypeDef,
        "RegionName": str,
        "ReplicaStatus": str,
        "ReplicaStatusDescription": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataDetailsPaginatorTypeDef",
    {
        "BlockDeviceMappingSet": List[AwsEc2LaunchTemplateDataBlockDeviceMappingSetDetailsTypeDef],
        "CapacityReservationSpecification": (
            AwsEc2LaunchTemplateDataCapacityReservationSpecificationDetailsTypeDef
        ),
        "CpuOptions": AwsEc2LaunchTemplateDataCpuOptionsDetailsTypeDef,
        "CreditSpecification": AwsEc2LaunchTemplateDataCreditSpecificationDetailsTypeDef,
        "DisableApiStop": bool,
        "DisableApiTermination": bool,
        "EbsOptimized": bool,
        "ElasticGpuSpecificationSet": List[
            AwsEc2LaunchTemplateDataElasticGpuSpecificationSetDetailsTypeDef
        ],
        "ElasticInferenceAcceleratorSet": List[
            AwsEc2LaunchTemplateDataElasticInferenceAcceleratorSetDetailsTypeDef
        ],
        "EnclaveOptions": AwsEc2LaunchTemplateDataEnclaveOptionsDetailsTypeDef,
        "HibernationOptions": AwsEc2LaunchTemplateDataHibernationOptionsDetailsTypeDef,
        "IamInstanceProfile": AwsEc2LaunchTemplateDataIamInstanceProfileDetailsTypeDef,
        "ImageId": str,
        "InstanceInitiatedShutdownBehavior": str,
        "InstanceMarketOptions": AwsEc2LaunchTemplateDataInstanceMarketOptionsDetailsTypeDef,
        "InstanceRequirements": AwsEc2LaunchTemplateDataInstanceRequirementsDetailsPaginatorTypeDef,
        "InstanceType": str,
        "KernelId": str,
        "KeyName": str,
        "LicenseSet": List[AwsEc2LaunchTemplateDataLicenseSetDetailsTypeDef],
        "MaintenanceOptions": AwsEc2LaunchTemplateDataMaintenanceOptionsDetailsTypeDef,
        "MetadataOptions": AwsEc2LaunchTemplateDataMetadataOptionsDetailsTypeDef,
        "Monitoring": AwsEc2LaunchTemplateDataMonitoringDetailsTypeDef,
        "NetworkInterfaceSet": List[
            AwsEc2LaunchTemplateDataNetworkInterfaceSetDetailsPaginatorTypeDef
        ],
        "Placement": AwsEc2LaunchTemplateDataPlacementDetailsTypeDef,
        "PrivateDnsNameOptions": AwsEc2LaunchTemplateDataPrivateDnsNameOptionsDetailsTypeDef,
        "RamDiskId": str,
        "SecurityGroupIdSet": List[str],
        "SecurityGroupSet": List[str],
        "UserData": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDataDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDataDetailsTypeDef",
    {
        "BlockDeviceMappingSet": Sequence[
            AwsEc2LaunchTemplateDataBlockDeviceMappingSetDetailsTypeDef
        ],
        "CapacityReservationSpecification": (
            AwsEc2LaunchTemplateDataCapacityReservationSpecificationDetailsTypeDef
        ),
        "CpuOptions": AwsEc2LaunchTemplateDataCpuOptionsDetailsTypeDef,
        "CreditSpecification": AwsEc2LaunchTemplateDataCreditSpecificationDetailsTypeDef,
        "DisableApiStop": bool,
        "DisableApiTermination": bool,
        "EbsOptimized": bool,
        "ElasticGpuSpecificationSet": Sequence[
            AwsEc2LaunchTemplateDataElasticGpuSpecificationSetDetailsTypeDef
        ],
        "ElasticInferenceAcceleratorSet": Sequence[
            AwsEc2LaunchTemplateDataElasticInferenceAcceleratorSetDetailsTypeDef
        ],
        "EnclaveOptions": AwsEc2LaunchTemplateDataEnclaveOptionsDetailsTypeDef,
        "HibernationOptions": AwsEc2LaunchTemplateDataHibernationOptionsDetailsTypeDef,
        "IamInstanceProfile": AwsEc2LaunchTemplateDataIamInstanceProfileDetailsTypeDef,
        "ImageId": str,
        "InstanceInitiatedShutdownBehavior": str,
        "InstanceMarketOptions": AwsEc2LaunchTemplateDataInstanceMarketOptionsDetailsTypeDef,
        "InstanceRequirements": AwsEc2LaunchTemplateDataInstanceRequirementsDetailsTypeDef,
        "InstanceType": str,
        "KernelId": str,
        "KeyName": str,
        "LicenseSet": Sequence[AwsEc2LaunchTemplateDataLicenseSetDetailsTypeDef],
        "MaintenanceOptions": AwsEc2LaunchTemplateDataMaintenanceOptionsDetailsTypeDef,
        "MetadataOptions": AwsEc2LaunchTemplateDataMetadataOptionsDetailsTypeDef,
        "Monitoring": AwsEc2LaunchTemplateDataMonitoringDetailsTypeDef,
        "NetworkInterfaceSet": Sequence[AwsEc2LaunchTemplateDataNetworkInterfaceSetDetailsTypeDef],
        "Placement": AwsEc2LaunchTemplateDataPlacementDetailsTypeDef,
        "PrivateDnsNameOptions": AwsEc2LaunchTemplateDataPrivateDnsNameOptionsDetailsTypeDef,
        "RamDiskId": str,
        "SecurityGroupIdSet": Sequence[str],
        "SecurityGroupSet": Sequence[str],
        "UserData": str,
    },
    total=False,
)

AwsEc2NetworkAclDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2NetworkAclDetailsPaginatorTypeDef",
    {
        "IsDefault": bool,
        "NetworkAclId": str,
        "OwnerId": str,
        "VpcId": str,
        "Associations": List[AwsEc2NetworkAclAssociationTypeDef],
        "Entries": List[AwsEc2NetworkAclEntryTypeDef],
    },
    total=False,
)

AwsEc2NetworkAclDetailsTypeDef = TypedDict(
    "AwsEc2NetworkAclDetailsTypeDef",
    {
        "IsDefault": bool,
        "NetworkAclId": str,
        "OwnerId": str,
        "VpcId": str,
        "Associations": Sequence[AwsEc2NetworkAclAssociationTypeDef],
        "Entries": Sequence[AwsEc2NetworkAclEntryTypeDef],
    },
    total=False,
)

AwsEc2SecurityGroupDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2SecurityGroupDetailsPaginatorTypeDef",
    {
        "GroupName": str,
        "GroupId": str,
        "OwnerId": str,
        "VpcId": str,
        "IpPermissions": List[AwsEc2SecurityGroupIpPermissionPaginatorTypeDef],
        "IpPermissionsEgress": List[AwsEc2SecurityGroupIpPermissionPaginatorTypeDef],
    },
    total=False,
)

AwsEc2SecurityGroupDetailsTypeDef = TypedDict(
    "AwsEc2SecurityGroupDetailsTypeDef",
    {
        "GroupName": str,
        "GroupId": str,
        "OwnerId": str,
        "VpcId": str,
        "IpPermissions": Sequence[AwsEc2SecurityGroupIpPermissionTypeDef],
        "IpPermissionsEgress": Sequence[AwsEc2SecurityGroupIpPermissionTypeDef],
    },
    total=False,
)

AwsEc2VpcPeeringConnectionDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2VpcPeeringConnectionDetailsPaginatorTypeDef",
    {
        "AccepterVpcInfo": AwsEc2VpcPeeringConnectionVpcInfoDetailsPaginatorTypeDef,
        "ExpirationTime": str,
        "RequesterVpcInfo": AwsEc2VpcPeeringConnectionVpcInfoDetailsPaginatorTypeDef,
        "Status": AwsEc2VpcPeeringConnectionStatusDetailsTypeDef,
        "VpcPeeringConnectionId": str,
    },
    total=False,
)

AwsEc2VpcPeeringConnectionDetailsTypeDef = TypedDict(
    "AwsEc2VpcPeeringConnectionDetailsTypeDef",
    {
        "AccepterVpcInfo": AwsEc2VpcPeeringConnectionVpcInfoDetailsTypeDef,
        "ExpirationTime": str,
        "RequesterVpcInfo": AwsEc2VpcPeeringConnectionVpcInfoDetailsTypeDef,
        "Status": AwsEc2VpcPeeringConnectionStatusDetailsTypeDef,
        "VpcPeeringConnectionId": str,
    },
    total=False,
)

AwsEc2VpnConnectionDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2VpnConnectionDetailsPaginatorTypeDef",
    {
        "VpnConnectionId": str,
        "State": str,
        "CustomerGatewayId": str,
        "CustomerGatewayConfiguration": str,
        "Type": str,
        "VpnGatewayId": str,
        "Category": str,
        "VgwTelemetry": List[AwsEc2VpnConnectionVgwTelemetryDetailsTypeDef],
        "Options": AwsEc2VpnConnectionOptionsDetailsPaginatorTypeDef,
        "Routes": List[AwsEc2VpnConnectionRoutesDetailsTypeDef],
        "TransitGatewayId": str,
    },
    total=False,
)

AwsEc2VpnConnectionDetailsTypeDef = TypedDict(
    "AwsEc2VpnConnectionDetailsTypeDef",
    {
        "VpnConnectionId": str,
        "State": str,
        "CustomerGatewayId": str,
        "CustomerGatewayConfiguration": str,
        "Type": str,
        "VpnGatewayId": str,
        "Category": str,
        "VgwTelemetry": Sequence[AwsEc2VpnConnectionVgwTelemetryDetailsTypeDef],
        "Options": AwsEc2VpnConnectionOptionsDetailsTypeDef,
        "Routes": Sequence[AwsEc2VpnConnectionRoutesDetailsTypeDef],
        "TransitGatewayId": str,
    },
    total=False,
)

AwsEcsClusterConfigurationDetailsTypeDef = TypedDict(
    "AwsEcsClusterConfigurationDetailsTypeDef",
    {
        "ExecuteCommandConfiguration": (
            AwsEcsClusterConfigurationExecuteCommandConfigurationDetailsTypeDef
        ),
    },
    total=False,
)

AwsEcsServiceDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsServiceDetailsPaginatorTypeDef",
    {
        "CapacityProviderStrategy": List[AwsEcsServiceCapacityProviderStrategyDetailsTypeDef],
        "Cluster": str,
        "DeploymentConfiguration": AwsEcsServiceDeploymentConfigurationDetailsTypeDef,
        "DeploymentController": AwsEcsServiceDeploymentControllerDetailsTypeDef,
        "DesiredCount": int,
        "EnableEcsManagedTags": bool,
        "EnableExecuteCommand": bool,
        "HealthCheckGracePeriodSeconds": int,
        "LaunchType": str,
        "LoadBalancers": List[AwsEcsServiceLoadBalancersDetailsTypeDef],
        "Name": str,
        "NetworkConfiguration": AwsEcsServiceNetworkConfigurationDetailsPaginatorTypeDef,
        "PlacementConstraints": List[AwsEcsServicePlacementConstraintsDetailsTypeDef],
        "PlacementStrategies": List[AwsEcsServicePlacementStrategiesDetailsTypeDef],
        "PlatformVersion": str,
        "PropagateTags": str,
        "Role": str,
        "SchedulingStrategy": str,
        "ServiceArn": str,
        "ServiceName": str,
        "ServiceRegistries": List[AwsEcsServiceServiceRegistriesDetailsTypeDef],
        "TaskDefinition": str,
    },
    total=False,
)

AwsEcsServiceDetailsTypeDef = TypedDict(
    "AwsEcsServiceDetailsTypeDef",
    {
        "CapacityProviderStrategy": Sequence[AwsEcsServiceCapacityProviderStrategyDetailsTypeDef],
        "Cluster": str,
        "DeploymentConfiguration": AwsEcsServiceDeploymentConfigurationDetailsTypeDef,
        "DeploymentController": AwsEcsServiceDeploymentControllerDetailsTypeDef,
        "DesiredCount": int,
        "EnableEcsManagedTags": bool,
        "EnableExecuteCommand": bool,
        "HealthCheckGracePeriodSeconds": int,
        "LaunchType": str,
        "LoadBalancers": Sequence[AwsEcsServiceLoadBalancersDetailsTypeDef],
        "Name": str,
        "NetworkConfiguration": AwsEcsServiceNetworkConfigurationDetailsTypeDef,
        "PlacementConstraints": Sequence[AwsEcsServicePlacementConstraintsDetailsTypeDef],
        "PlacementStrategies": Sequence[AwsEcsServicePlacementStrategiesDetailsTypeDef],
        "PlatformVersion": str,
        "PropagateTags": str,
        "Role": str,
        "SchedulingStrategy": str,
        "ServiceArn": str,
        "ServiceName": str,
        "ServiceRegistries": Sequence[AwsEcsServiceServiceRegistriesDetailsTypeDef],
        "TaskDefinition": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsDetailsPaginatorTypeDef",
    {
        "Command": List[str],
        "Cpu": int,
        "DependsOn": List[AwsEcsTaskDefinitionContainerDefinitionsDependsOnDetailsTypeDef],
        "DisableNetworking": bool,
        "DnsSearchDomains": List[str],
        "DnsServers": List[str],
        "DockerLabels": Dict[str, str],
        "DockerSecurityOptions": List[str],
        "EntryPoint": List[str],
        "Environment": List[AwsEcsTaskDefinitionContainerDefinitionsEnvironmentDetailsTypeDef],
        "EnvironmentFiles": List[
            AwsEcsTaskDefinitionContainerDefinitionsEnvironmentFilesDetailsTypeDef
        ],
        "Essential": bool,
        "ExtraHosts": List[AwsEcsTaskDefinitionContainerDefinitionsExtraHostsDetailsTypeDef],
        "FirelensConfiguration": (
            AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsPaginatorTypeDef
        ),
        "HealthCheck": AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsPaginatorTypeDef,
        "Hostname": str,
        "Image": str,
        "Interactive": bool,
        "Links": List[str],
        "LinuxParameters": (
            AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsPaginatorTypeDef
        ),
        "LogConfiguration": (
            AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsPaginatorTypeDef
        ),
        "Memory": int,
        "MemoryReservation": int,
        "MountPoints": List[AwsEcsTaskDefinitionContainerDefinitionsMountPointsDetailsTypeDef],
        "Name": str,
        "PortMappings": List[AwsEcsTaskDefinitionContainerDefinitionsPortMappingsDetailsTypeDef],
        "Privileged": bool,
        "PseudoTerminal": bool,
        "ReadonlyRootFilesystem": bool,
        "RepositoryCredentials": (
            AwsEcsTaskDefinitionContainerDefinitionsRepositoryCredentialsDetailsTypeDef
        ),
        "ResourceRequirements": List[
            AwsEcsTaskDefinitionContainerDefinitionsResourceRequirementsDetailsTypeDef
        ],
        "Secrets": List[AwsEcsTaskDefinitionContainerDefinitionsSecretsDetailsTypeDef],
        "StartTimeout": int,
        "StopTimeout": int,
        "SystemControls": List[
            AwsEcsTaskDefinitionContainerDefinitionsSystemControlsDetailsTypeDef
        ],
        "Ulimits": List[AwsEcsTaskDefinitionContainerDefinitionsUlimitsDetailsTypeDef],
        "User": str,
        "VolumesFrom": List[AwsEcsTaskDefinitionContainerDefinitionsVolumesFromDetailsTypeDef],
        "WorkingDirectory": str,
    },
    total=False,
)

AwsEcsTaskDefinitionContainerDefinitionsDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionContainerDefinitionsDetailsTypeDef",
    {
        "Command": Sequence[str],
        "Cpu": int,
        "DependsOn": Sequence[AwsEcsTaskDefinitionContainerDefinitionsDependsOnDetailsTypeDef],
        "DisableNetworking": bool,
        "DnsSearchDomains": Sequence[str],
        "DnsServers": Sequence[str],
        "DockerLabels": Mapping[str, str],
        "DockerSecurityOptions": Sequence[str],
        "EntryPoint": Sequence[str],
        "Environment": Sequence[AwsEcsTaskDefinitionContainerDefinitionsEnvironmentDetailsTypeDef],
        "EnvironmentFiles": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsEnvironmentFilesDetailsTypeDef
        ],
        "Essential": bool,
        "ExtraHosts": Sequence[AwsEcsTaskDefinitionContainerDefinitionsExtraHostsDetailsTypeDef],
        "FirelensConfiguration": (
            AwsEcsTaskDefinitionContainerDefinitionsFirelensConfigurationDetailsTypeDef
        ),
        "HealthCheck": AwsEcsTaskDefinitionContainerDefinitionsHealthCheckDetailsTypeDef,
        "Hostname": str,
        "Image": str,
        "Interactive": bool,
        "Links": Sequence[str],
        "LinuxParameters": AwsEcsTaskDefinitionContainerDefinitionsLinuxParametersDetailsTypeDef,
        "LogConfiguration": AwsEcsTaskDefinitionContainerDefinitionsLogConfigurationDetailsTypeDef,
        "Memory": int,
        "MemoryReservation": int,
        "MountPoints": Sequence[AwsEcsTaskDefinitionContainerDefinitionsMountPointsDetailsTypeDef],
        "Name": str,
        "PortMappings": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsPortMappingsDetailsTypeDef
        ],
        "Privileged": bool,
        "PseudoTerminal": bool,
        "ReadonlyRootFilesystem": bool,
        "RepositoryCredentials": (
            AwsEcsTaskDefinitionContainerDefinitionsRepositoryCredentialsDetailsTypeDef
        ),
        "ResourceRequirements": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsResourceRequirementsDetailsTypeDef
        ],
        "Secrets": Sequence[AwsEcsTaskDefinitionContainerDefinitionsSecretsDetailsTypeDef],
        "StartTimeout": int,
        "StopTimeout": int,
        "SystemControls": Sequence[
            AwsEcsTaskDefinitionContainerDefinitionsSystemControlsDetailsTypeDef
        ],
        "Ulimits": Sequence[AwsEcsTaskDefinitionContainerDefinitionsUlimitsDetailsTypeDef],
        "User": str,
        "VolumesFrom": Sequence[AwsEcsTaskDefinitionContainerDefinitionsVolumesFromDetailsTypeDef],
        "WorkingDirectory": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesDetailsPaginatorTypeDef",
    {
        "DockerVolumeConfiguration": (
            AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsPaginatorTypeDef
        ),
        "EfsVolumeConfiguration": AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationDetailsTypeDef,
        "Host": AwsEcsTaskDefinitionVolumesHostDetailsTypeDef,
        "Name": str,
    },
    total=False,
)

AwsEcsTaskDefinitionVolumesDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionVolumesDetailsTypeDef",
    {
        "DockerVolumeConfiguration": (
            AwsEcsTaskDefinitionVolumesDockerVolumeConfigurationDetailsTypeDef
        ),
        "EfsVolumeConfiguration": AwsEcsTaskDefinitionVolumesEfsVolumeConfigurationDetailsTypeDef,
        "Host": AwsEcsTaskDefinitionVolumesHostDetailsTypeDef,
        "Name": str,
    },
    total=False,
)

AwsEcsTaskDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDetailsPaginatorTypeDef",
    {
        "ClusterArn": str,
        "TaskDefinitionArn": str,
        "Version": str,
        "CreatedAt": str,
        "StartedAt": str,
        "StartedBy": str,
        "Group": str,
        "Volumes": List[AwsEcsTaskVolumeDetailsTypeDef],
        "Containers": List[AwsEcsContainerDetailsPaginatorTypeDef],
    },
    total=False,
)

AwsEcsTaskDetailsTypeDef = TypedDict(
    "AwsEcsTaskDetailsTypeDef",
    {
        "ClusterArn": str,
        "TaskDefinitionArn": str,
        "Version": str,
        "CreatedAt": str,
        "StartedAt": str,
        "StartedBy": str,
        "Group": str,
        "Volumes": Sequence[AwsEcsTaskVolumeDetailsTypeDef],
        "Containers": Sequence[AwsEcsContainerDetailsTypeDef],
    },
    total=False,
)

AwsEfsAccessPointDetailsPaginatorTypeDef = TypedDict(
    "AwsEfsAccessPointDetailsPaginatorTypeDef",
    {
        "AccessPointId": str,
        "Arn": str,
        "ClientToken": str,
        "FileSystemId": str,
        "PosixUser": AwsEfsAccessPointPosixUserDetailsPaginatorTypeDef,
        "RootDirectory": AwsEfsAccessPointRootDirectoryDetailsTypeDef,
    },
    total=False,
)

AwsEfsAccessPointDetailsTypeDef = TypedDict(
    "AwsEfsAccessPointDetailsTypeDef",
    {
        "AccessPointId": str,
        "Arn": str,
        "ClientToken": str,
        "FileSystemId": str,
        "PosixUser": AwsEfsAccessPointPosixUserDetailsTypeDef,
        "RootDirectory": AwsEfsAccessPointRootDirectoryDetailsTypeDef,
    },
    total=False,
)

AwsEksClusterDetailsPaginatorTypeDef = TypedDict(
    "AwsEksClusterDetailsPaginatorTypeDef",
    {
        "Arn": str,
        "CertificateAuthorityData": str,
        "ClusterStatus": str,
        "Endpoint": str,
        "Name": str,
        "ResourcesVpcConfig": AwsEksClusterResourcesVpcConfigDetailsPaginatorTypeDef,
        "RoleArn": str,
        "Version": str,
        "Logging": AwsEksClusterLoggingDetailsPaginatorTypeDef,
    },
    total=False,
)

AwsEksClusterDetailsTypeDef = TypedDict(
    "AwsEksClusterDetailsTypeDef",
    {
        "Arn": str,
        "CertificateAuthorityData": str,
        "ClusterStatus": str,
        "Endpoint": str,
        "Name": str,
        "ResourcesVpcConfig": AwsEksClusterResourcesVpcConfigDetailsTypeDef,
        "RoleArn": str,
        "Version": str,
        "Logging": AwsEksClusterLoggingDetailsTypeDef,
    },
    total=False,
)

AwsElasticsearchDomainDetailsPaginatorTypeDef = TypedDict(
    "AwsElasticsearchDomainDetailsPaginatorTypeDef",
    {
        "AccessPolicies": str,
        "DomainEndpointOptions": AwsElasticsearchDomainDomainEndpointOptionsTypeDef,
        "DomainId": str,
        "DomainName": str,
        "Endpoint": str,
        "Endpoints": Dict[str, str],
        "ElasticsearchVersion": str,
        "ElasticsearchClusterConfig": (
            AwsElasticsearchDomainElasticsearchClusterConfigDetailsTypeDef
        ),
        "EncryptionAtRestOptions": AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef,
        "LogPublishingOptions": AwsElasticsearchDomainLogPublishingOptionsTypeDef,
        "NodeToNodeEncryptionOptions": AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef,
        "ServiceSoftwareOptions": AwsElasticsearchDomainServiceSoftwareOptionsTypeDef,
        "VPCOptions": AwsElasticsearchDomainVPCOptionsPaginatorTypeDef,
    },
    total=False,
)

AwsElasticsearchDomainDetailsTypeDef = TypedDict(
    "AwsElasticsearchDomainDetailsTypeDef",
    {
        "AccessPolicies": str,
        "DomainEndpointOptions": AwsElasticsearchDomainDomainEndpointOptionsTypeDef,
        "DomainId": str,
        "DomainName": str,
        "Endpoint": str,
        "Endpoints": Mapping[str, str],
        "ElasticsearchVersion": str,
        "ElasticsearchClusterConfig": (
            AwsElasticsearchDomainElasticsearchClusterConfigDetailsTypeDef
        ),
        "EncryptionAtRestOptions": AwsElasticsearchDomainEncryptionAtRestOptionsTypeDef,
        "LogPublishingOptions": AwsElasticsearchDomainLogPublishingOptionsTypeDef,
        "NodeToNodeEncryptionOptions": AwsElasticsearchDomainNodeToNodeEncryptionOptionsTypeDef,
        "ServiceSoftwareOptions": AwsElasticsearchDomainServiceSoftwareOptionsTypeDef,
        "VPCOptions": AwsElasticsearchDomainVPCOptionsTypeDef,
    },
    total=False,
)

AwsElbLoadBalancerDetailsPaginatorTypeDef = TypedDict(
    "AwsElbLoadBalancerDetailsPaginatorTypeDef",
    {
        "AvailabilityZones": List[str],
        "BackendServerDescriptions": List[
            AwsElbLoadBalancerBackendServerDescriptionPaginatorTypeDef
        ],
        "CanonicalHostedZoneName": str,
        "CanonicalHostedZoneNameID": str,
        "CreatedTime": str,
        "DnsName": str,
        "HealthCheck": AwsElbLoadBalancerHealthCheckTypeDef,
        "Instances": List[AwsElbLoadBalancerInstanceTypeDef],
        "ListenerDescriptions": List[AwsElbLoadBalancerListenerDescriptionPaginatorTypeDef],
        "LoadBalancerAttributes": AwsElbLoadBalancerAttributesPaginatorTypeDef,
        "LoadBalancerName": str,
        "Policies": AwsElbLoadBalancerPoliciesPaginatorTypeDef,
        "Scheme": str,
        "SecurityGroups": List[str],
        "SourceSecurityGroup": AwsElbLoadBalancerSourceSecurityGroupTypeDef,
        "Subnets": List[str],
        "VpcId": str,
    },
    total=False,
)

AwsElbLoadBalancerDetailsTypeDef = TypedDict(
    "AwsElbLoadBalancerDetailsTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "BackendServerDescriptions": Sequence[AwsElbLoadBalancerBackendServerDescriptionTypeDef],
        "CanonicalHostedZoneName": str,
        "CanonicalHostedZoneNameID": str,
        "CreatedTime": str,
        "DnsName": str,
        "HealthCheck": AwsElbLoadBalancerHealthCheckTypeDef,
        "Instances": Sequence[AwsElbLoadBalancerInstanceTypeDef],
        "ListenerDescriptions": Sequence[AwsElbLoadBalancerListenerDescriptionTypeDef],
        "LoadBalancerAttributes": AwsElbLoadBalancerAttributesTypeDef,
        "LoadBalancerName": str,
        "Policies": AwsElbLoadBalancerPoliciesTypeDef,
        "Scheme": str,
        "SecurityGroups": Sequence[str],
        "SourceSecurityGroup": AwsElbLoadBalancerSourceSecurityGroupTypeDef,
        "Subnets": Sequence[str],
        "VpcId": str,
    },
    total=False,
)

AwsGuardDutyDetectorDataSourcesMalwareProtectionDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDataSourcesMalwareProtectionDetailsTypeDef",
    {
        "ScanEc2InstanceWithFindings": AwsGuardDutyDetectorDataSourcesMalwareProtectionScanEc2InstanceWithFindingsDetailsTypeDef,
        "ServiceRole": str,
    },
    total=False,
)

AwsIamAccessKeyDetailsTypeDef = TypedDict(
    "AwsIamAccessKeyDetailsTypeDef",
    {
        "UserName": str,
        "Status": AwsIamAccessKeyStatusType,
        "CreatedAt": str,
        "PrincipalId": str,
        "PrincipalType": str,
        "PrincipalName": str,
        "AccountId": str,
        "AccessKeyId": str,
        "SessionContext": AwsIamAccessKeySessionContextTypeDef,
    },
    total=False,
)

AwsIamRoleDetailsPaginatorTypeDef = TypedDict(
    "AwsIamRoleDetailsPaginatorTypeDef",
    {
        "AssumeRolePolicyDocument": Dict[str, Any],
        "AttachedManagedPolicies": List[AwsIamAttachedManagedPolicyTypeDef],
        "CreateDate": str,
        "InstanceProfileList": List[AwsIamInstanceProfilePaginatorTypeDef],
        "PermissionsBoundary": AwsIamPermissionsBoundaryTypeDef,
        "RoleId": str,
        "RoleName": str,
        "RolePolicyList": List[AwsIamRolePolicyTypeDef],
        "MaxSessionDuration": int,
        "Path": str,
    },
    total=False,
)

AwsIamInstanceProfileTypeDef = TypedDict(
    "AwsIamInstanceProfileTypeDef",
    {
        "Arn": str,
        "CreateDate": str,
        "InstanceProfileId": str,
        "InstanceProfileName": str,
        "Path": str,
        "Roles": Sequence[AwsIamInstanceProfileRoleTypeDef],
    },
    total=False,
)

AwsLambdaFunctionDetailsPaginatorTypeDef = TypedDict(
    "AwsLambdaFunctionDetailsPaginatorTypeDef",
    {
        "Code": AwsLambdaFunctionCodeTypeDef,
        "CodeSha256": str,
        "DeadLetterConfig": AwsLambdaFunctionDeadLetterConfigTypeDef,
        "Environment": AwsLambdaFunctionEnvironmentPaginatorTypeDef,
        "FunctionName": str,
        "Handler": str,
        "KmsKeyArn": str,
        "LastModified": str,
        "Layers": List[AwsLambdaFunctionLayerTypeDef],
        "MasterArn": str,
        "MemorySize": int,
        "RevisionId": str,
        "Role": str,
        "Runtime": str,
        "Timeout": int,
        "TracingConfig": AwsLambdaFunctionTracingConfigTypeDef,
        "VpcConfig": AwsLambdaFunctionVpcConfigPaginatorTypeDef,
        "Version": str,
        "Architectures": List[str],
        "PackageType": str,
    },
    total=False,
)

AwsLambdaFunctionDetailsTypeDef = TypedDict(
    "AwsLambdaFunctionDetailsTypeDef",
    {
        "Code": AwsLambdaFunctionCodeTypeDef,
        "CodeSha256": str,
        "DeadLetterConfig": AwsLambdaFunctionDeadLetterConfigTypeDef,
        "Environment": AwsLambdaFunctionEnvironmentTypeDef,
        "FunctionName": str,
        "Handler": str,
        "KmsKeyArn": str,
        "LastModified": str,
        "Layers": Sequence[AwsLambdaFunctionLayerTypeDef],
        "MasterArn": str,
        "MemorySize": int,
        "RevisionId": str,
        "Role": str,
        "Runtime": str,
        "Timeout": int,
        "TracingConfig": AwsLambdaFunctionTracingConfigTypeDef,
        "VpcConfig": AwsLambdaFunctionVpcConfigTypeDef,
        "Version": str,
        "Architectures": Sequence[str],
        "PackageType": str,
    },
    total=False,
)

AwsOpenSearchServiceDomainDetailsPaginatorTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainDetailsPaginatorTypeDef",
    {
        "Arn": str,
        "AccessPolicies": str,
        "DomainName": str,
        "Id": str,
        "DomainEndpoint": str,
        "EngineVersion": str,
        "EncryptionAtRestOptions": AwsOpenSearchServiceDomainEncryptionAtRestOptionsDetailsTypeDef,
        "NodeToNodeEncryptionOptions": (
            AwsOpenSearchServiceDomainNodeToNodeEncryptionOptionsDetailsTypeDef
        ),
        "ServiceSoftwareOptions": AwsOpenSearchServiceDomainServiceSoftwareOptionsDetailsTypeDef,
        "ClusterConfig": AwsOpenSearchServiceDomainClusterConfigDetailsTypeDef,
        "DomainEndpointOptions": AwsOpenSearchServiceDomainDomainEndpointOptionsDetailsTypeDef,
        "VpcOptions": AwsOpenSearchServiceDomainVpcOptionsDetailsPaginatorTypeDef,
        "LogPublishingOptions": AwsOpenSearchServiceDomainLogPublishingOptionsDetailsTypeDef,
        "DomainEndpoints": Dict[str, str],
        "AdvancedSecurityOptions": AwsOpenSearchServiceDomainAdvancedSecurityOptionsDetailsTypeDef,
    },
    total=False,
)

AwsOpenSearchServiceDomainDetailsTypeDef = TypedDict(
    "AwsOpenSearchServiceDomainDetailsTypeDef",
    {
        "Arn": str,
        "AccessPolicies": str,
        "DomainName": str,
        "Id": str,
        "DomainEndpoint": str,
        "EngineVersion": str,
        "EncryptionAtRestOptions": AwsOpenSearchServiceDomainEncryptionAtRestOptionsDetailsTypeDef,
        "NodeToNodeEncryptionOptions": (
            AwsOpenSearchServiceDomainNodeToNodeEncryptionOptionsDetailsTypeDef
        ),
        "ServiceSoftwareOptions": AwsOpenSearchServiceDomainServiceSoftwareOptionsDetailsTypeDef,
        "ClusterConfig": AwsOpenSearchServiceDomainClusterConfigDetailsTypeDef,
        "DomainEndpointOptions": AwsOpenSearchServiceDomainDomainEndpointOptionsDetailsTypeDef,
        "VpcOptions": AwsOpenSearchServiceDomainVpcOptionsDetailsTypeDef,
        "LogPublishingOptions": AwsOpenSearchServiceDomainLogPublishingOptionsDetailsTypeDef,
        "DomainEndpoints": Mapping[str, str],
        "AdvancedSecurityOptions": AwsOpenSearchServiceDomainAdvancedSecurityOptionsDetailsTypeDef,
    },
    total=False,
)

AwsRdsDbSubnetGroupPaginatorTypeDef = TypedDict(
    "AwsRdsDbSubnetGroupPaginatorTypeDef",
    {
        "DbSubnetGroupName": str,
        "DbSubnetGroupDescription": str,
        "VpcId": str,
        "SubnetGroupStatus": str,
        "Subnets": List[AwsRdsDbSubnetGroupSubnetTypeDef],
        "DbSubnetGroupArn": str,
    },
    total=False,
)

AwsRdsDbSubnetGroupTypeDef = TypedDict(
    "AwsRdsDbSubnetGroupTypeDef",
    {
        "DbSubnetGroupName": str,
        "DbSubnetGroupDescription": str,
        "VpcId": str,
        "SubnetGroupStatus": str,
        "Subnets": Sequence[AwsRdsDbSubnetGroupSubnetTypeDef],
        "DbSubnetGroupArn": str,
    },
    total=False,
)

AwsRedshiftClusterDetailsPaginatorTypeDef = TypedDict(
    "AwsRedshiftClusterDetailsPaginatorTypeDef",
    {
        "AllowVersionUpgrade": bool,
        "AutomatedSnapshotRetentionPeriod": int,
        "AvailabilityZone": str,
        "ClusterAvailabilityStatus": str,
        "ClusterCreateTime": str,
        "ClusterIdentifier": str,
        "ClusterNodes": List[AwsRedshiftClusterClusterNodeTypeDef],
        "ClusterParameterGroups": List[AwsRedshiftClusterClusterParameterGroupPaginatorTypeDef],
        "ClusterPublicKey": str,
        "ClusterRevisionNumber": str,
        "ClusterSecurityGroups": List[AwsRedshiftClusterClusterSecurityGroupTypeDef],
        "ClusterSnapshotCopyStatus": AwsRedshiftClusterClusterSnapshotCopyStatusTypeDef,
        "ClusterStatus": str,
        "ClusterSubnetGroupName": str,
        "ClusterVersion": str,
        "DBName": str,
        "DeferredMaintenanceWindows": List[AwsRedshiftClusterDeferredMaintenanceWindowTypeDef],
        "ElasticIpStatus": AwsRedshiftClusterElasticIpStatusTypeDef,
        "ElasticResizeNumberOfNodeOptions": str,
        "Encrypted": bool,
        "Endpoint": AwsRedshiftClusterEndpointTypeDef,
        "EnhancedVpcRouting": bool,
        "ExpectedNextSnapshotScheduleTime": str,
        "ExpectedNextSnapshotScheduleTimeStatus": str,
        "HsmStatus": AwsRedshiftClusterHsmStatusTypeDef,
        "IamRoles": List[AwsRedshiftClusterIamRoleTypeDef],
        "KmsKeyId": str,
        "MaintenanceTrackName": str,
        "ManualSnapshotRetentionPeriod": int,
        "MasterUsername": str,
        "NextMaintenanceWindowStartTime": str,
        "NodeType": str,
        "NumberOfNodes": int,
        "PendingActions": List[str],
        "PendingModifiedValues": AwsRedshiftClusterPendingModifiedValuesTypeDef,
        "PreferredMaintenanceWindow": str,
        "PubliclyAccessible": bool,
        "ResizeInfo": AwsRedshiftClusterResizeInfoTypeDef,
        "RestoreStatus": AwsRedshiftClusterRestoreStatusTypeDef,
        "SnapshotScheduleIdentifier": str,
        "SnapshotScheduleState": str,
        "VpcId": str,
        "VpcSecurityGroups": List[AwsRedshiftClusterVpcSecurityGroupTypeDef],
        "LoggingStatus": AwsRedshiftClusterLoggingStatusTypeDef,
    },
    total=False,
)

AwsRedshiftClusterDetailsTypeDef = TypedDict(
    "AwsRedshiftClusterDetailsTypeDef",
    {
        "AllowVersionUpgrade": bool,
        "AutomatedSnapshotRetentionPeriod": int,
        "AvailabilityZone": str,
        "ClusterAvailabilityStatus": str,
        "ClusterCreateTime": str,
        "ClusterIdentifier": str,
        "ClusterNodes": Sequence[AwsRedshiftClusterClusterNodeTypeDef],
        "ClusterParameterGroups": Sequence[AwsRedshiftClusterClusterParameterGroupTypeDef],
        "ClusterPublicKey": str,
        "ClusterRevisionNumber": str,
        "ClusterSecurityGroups": Sequence[AwsRedshiftClusterClusterSecurityGroupTypeDef],
        "ClusterSnapshotCopyStatus": AwsRedshiftClusterClusterSnapshotCopyStatusTypeDef,
        "ClusterStatus": str,
        "ClusterSubnetGroupName": str,
        "ClusterVersion": str,
        "DBName": str,
        "DeferredMaintenanceWindows": Sequence[AwsRedshiftClusterDeferredMaintenanceWindowTypeDef],
        "ElasticIpStatus": AwsRedshiftClusterElasticIpStatusTypeDef,
        "ElasticResizeNumberOfNodeOptions": str,
        "Encrypted": bool,
        "Endpoint": AwsRedshiftClusterEndpointTypeDef,
        "EnhancedVpcRouting": bool,
        "ExpectedNextSnapshotScheduleTime": str,
        "ExpectedNextSnapshotScheduleTimeStatus": str,
        "HsmStatus": AwsRedshiftClusterHsmStatusTypeDef,
        "IamRoles": Sequence[AwsRedshiftClusterIamRoleTypeDef],
        "KmsKeyId": str,
        "MaintenanceTrackName": str,
        "ManualSnapshotRetentionPeriod": int,
        "MasterUsername": str,
        "NextMaintenanceWindowStartTime": str,
        "NodeType": str,
        "NumberOfNodes": int,
        "PendingActions": Sequence[str],
        "PendingModifiedValues": AwsRedshiftClusterPendingModifiedValuesTypeDef,
        "PreferredMaintenanceWindow": str,
        "PubliclyAccessible": bool,
        "ResizeInfo": AwsRedshiftClusterResizeInfoTypeDef,
        "RestoreStatus": AwsRedshiftClusterRestoreStatusTypeDef,
        "SnapshotScheduleIdentifier": str,
        "SnapshotScheduleState": str,
        "VpcId": str,
        "VpcSecurityGroups": Sequence[AwsRedshiftClusterVpcSecurityGroupTypeDef],
        "LoggingStatus": AwsRedshiftClusterLoggingStatusTypeDef,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsPaginatorTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsPaginatorTypeDef",
    {
        "Operands": List[
            AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsDetailsTypeDef
        ],
        "Prefix": str,
        "Tag": AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateTagDetailsTypeDef,
        "Type": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsTypeDef",
    {
        "Operands": Sequence[
            AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateOperandsDetailsTypeDef
        ],
        "Prefix": str,
        "Tag": AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateTagDetailsTypeDef,
        "Type": str,
    },
    total=False,
)

AwsS3BucketNotificationConfigurationFilterPaginatorTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationFilterPaginatorTypeDef",
    {
        "S3KeyFilter": AwsS3BucketNotificationConfigurationS3KeyFilterPaginatorTypeDef,
    },
    total=False,
)

AwsS3BucketNotificationConfigurationFilterTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationFilterTypeDef",
    {
        "S3KeyFilter": AwsS3BucketNotificationConfigurationS3KeyFilterTypeDef,
    },
    total=False,
)

AwsS3BucketObjectLockConfigurationTypeDef = TypedDict(
    "AwsS3BucketObjectLockConfigurationTypeDef",
    {
        "ObjectLockEnabled": str,
        "Rule": AwsS3BucketObjectLockConfigurationRuleDetailsTypeDef,
    },
    total=False,
)

AwsS3BucketServerSideEncryptionConfigurationPaginatorTypeDef = TypedDict(
    "AwsS3BucketServerSideEncryptionConfigurationPaginatorTypeDef",
    {
        "Rules": List[AwsS3BucketServerSideEncryptionRuleTypeDef],
    },
    total=False,
)

AwsS3BucketServerSideEncryptionConfigurationTypeDef = TypedDict(
    "AwsS3BucketServerSideEncryptionConfigurationTypeDef",
    {
        "Rules": Sequence[AwsS3BucketServerSideEncryptionRuleTypeDef],
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationPaginatorTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationPaginatorTypeDef",
    {
        "ErrorDocument": str,
        "IndexDocumentSuffix": str,
        "RedirectAllRequestsTo": AwsS3BucketWebsiteConfigurationRedirectToTypeDef,
        "RoutingRules": List[AwsS3BucketWebsiteConfigurationRoutingRuleTypeDef],
    },
    total=False,
)

AwsS3BucketWebsiteConfigurationTypeDef = TypedDict(
    "AwsS3BucketWebsiteConfigurationTypeDef",
    {
        "ErrorDocument": str,
        "IndexDocumentSuffix": str,
        "RedirectAllRequestsTo": AwsS3BucketWebsiteConfigurationRedirectToTypeDef,
        "RoutingRules": Sequence[AwsS3BucketWebsiteConfigurationRoutingRuleTypeDef],
    },
    total=False,
)

BatchUpdateFindingsResponseTypeDef = TypedDict(
    "BatchUpdateFindingsResponseTypeDef",
    {
        "ProcessedFindings": List[AwsSecurityFindingIdentifierTypeDef],
        "UnprocessedFindings": List[BatchUpdateFindingsUnprocessedFindingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AwsSsmPatchComplianceDetailsTypeDef = TypedDict(
    "AwsSsmPatchComplianceDetailsTypeDef",
    {
        "Patch": AwsSsmPatchTypeDef,
    },
    total=False,
)

AwsStepFunctionStateMachineLoggingConfigurationDetailsPaginatorTypeDef = TypedDict(
    "AwsStepFunctionStateMachineLoggingConfigurationDetailsPaginatorTypeDef",
    {
        "Destinations": List[
            AwsStepFunctionStateMachineLoggingConfigurationDestinationsDetailsTypeDef
        ],
        "IncludeExecutionData": bool,
        "Level": str,
    },
    total=False,
)

AwsStepFunctionStateMachineLoggingConfigurationDetailsTypeDef = TypedDict(
    "AwsStepFunctionStateMachineLoggingConfigurationDetailsTypeDef",
    {
        "Destinations": Sequence[
            AwsStepFunctionStateMachineLoggingConfigurationDestinationsDetailsTypeDef
        ],
        "IncludeExecutionData": bool,
        "Level": str,
    },
    total=False,
)

AwsWafRegionalRuleGroupDetailsPaginatorTypeDef = TypedDict(
    "AwsWafRegionalRuleGroupDetailsPaginatorTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "RuleGroupId": str,
        "Rules": List[AwsWafRegionalRuleGroupRulesDetailsTypeDef],
    },
    total=False,
)

AwsWafRegionalRuleGroupDetailsTypeDef = TypedDict(
    "AwsWafRegionalRuleGroupDetailsTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "RuleGroupId": str,
        "Rules": Sequence[AwsWafRegionalRuleGroupRulesDetailsTypeDef],
    },
    total=False,
)

AwsWafRegionalWebAclDetailsPaginatorTypeDef = TypedDict(
    "AwsWafRegionalWebAclDetailsPaginatorTypeDef",
    {
        "DefaultAction": str,
        "MetricName": str,
        "Name": str,
        "RulesList": List[AwsWafRegionalWebAclRulesListDetailsTypeDef],
        "WebAclId": str,
    },
    total=False,
)

AwsWafRegionalWebAclDetailsTypeDef = TypedDict(
    "AwsWafRegionalWebAclDetailsTypeDef",
    {
        "DefaultAction": str,
        "MetricName": str,
        "Name": str,
        "RulesList": Sequence[AwsWafRegionalWebAclRulesListDetailsTypeDef],
        "WebAclId": str,
    },
    total=False,
)

AwsWafRuleGroupDetailsPaginatorTypeDef = TypedDict(
    "AwsWafRuleGroupDetailsPaginatorTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "RuleGroupId": str,
        "Rules": List[AwsWafRuleGroupRulesDetailsTypeDef],
    },
    total=False,
)

AwsWafRuleGroupDetailsTypeDef = TypedDict(
    "AwsWafRuleGroupDetailsTypeDef",
    {
        "MetricName": str,
        "Name": str,
        "RuleGroupId": str,
        "Rules": Sequence[AwsWafRuleGroupRulesDetailsTypeDef],
    },
    total=False,
)

AwsWafWebAclDetailsPaginatorTypeDef = TypedDict(
    "AwsWafWebAclDetailsPaginatorTypeDef",
    {
        "Name": str,
        "DefaultAction": str,
        "Rules": List[AwsWafWebAclRulePaginatorTypeDef],
        "WebAclId": str,
    },
    total=False,
)

AwsWafWebAclDetailsTypeDef = TypedDict(
    "AwsWafWebAclDetailsTypeDef",
    {
        "Name": str,
        "DefaultAction": str,
        "Rules": Sequence[AwsWafWebAclRuleTypeDef],
        "WebAclId": str,
    },
    total=False,
)

AwsWafv2ActionAllowDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2ActionAllowDetailsPaginatorTypeDef",
    {
        "CustomRequestHandling": AwsWafv2CustomRequestHandlingDetailsPaginatorTypeDef,
    },
    total=False,
)

AwsWafv2RulesActionCaptchaDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2RulesActionCaptchaDetailsPaginatorTypeDef",
    {
        "CustomRequestHandling": AwsWafv2CustomRequestHandlingDetailsPaginatorTypeDef,
    },
    total=False,
)

AwsWafv2RulesActionCountDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2RulesActionCountDetailsPaginatorTypeDef",
    {
        "CustomRequestHandling": AwsWafv2CustomRequestHandlingDetailsPaginatorTypeDef,
    },
    total=False,
)

AwsWafv2ActionAllowDetailsTypeDef = TypedDict(
    "AwsWafv2ActionAllowDetailsTypeDef",
    {
        "CustomRequestHandling": AwsWafv2CustomRequestHandlingDetailsTypeDef,
    },
    total=False,
)

AwsWafv2RulesActionCaptchaDetailsTypeDef = TypedDict(
    "AwsWafv2RulesActionCaptchaDetailsTypeDef",
    {
        "CustomRequestHandling": AwsWafv2CustomRequestHandlingDetailsTypeDef,
    },
    total=False,
)

AwsWafv2RulesActionCountDetailsTypeDef = TypedDict(
    "AwsWafv2RulesActionCountDetailsTypeDef",
    {
        "CustomRequestHandling": AwsWafv2CustomRequestHandlingDetailsTypeDef,
    },
    total=False,
)

AwsWafv2ActionBlockDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2ActionBlockDetailsPaginatorTypeDef",
    {
        "CustomResponse": AwsWafv2CustomResponseDetailsPaginatorTypeDef,
    },
    total=False,
)

AwsWafv2ActionBlockDetailsTypeDef = TypedDict(
    "AwsWafv2ActionBlockDetailsTypeDef",
    {
        "CustomResponse": AwsWafv2CustomResponseDetailsTypeDef,
    },
    total=False,
)

BatchGetStandardsControlAssociationsResponseTypeDef = TypedDict(
    "BatchGetStandardsControlAssociationsResponseTypeDef",
    {
        "StandardsControlAssociationDetails": List[StandardsControlAssociationDetailTypeDef],
        "UnprocessedAssociations": List[UnprocessedStandardsControlAssociationTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateStandardsControlAssociationsResponseTypeDef = TypedDict(
    "BatchUpdateStandardsControlAssociationsResponseTypeDef",
    {
        "UnprocessedAssociationUpdates": List[UnprocessedStandardsControlAssociationUpdateTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredVulnerabilityPaginatorTypeDef = TypedDict(
    "_RequiredVulnerabilityPaginatorTypeDef",
    {
        "Id": str,
    },
)
_OptionalVulnerabilityPaginatorTypeDef = TypedDict(
    "_OptionalVulnerabilityPaginatorTypeDef",
    {
        "VulnerablePackages": List[SoftwarePackageTypeDef],
        "Cvss": List[CvssPaginatorTypeDef],
        "RelatedVulnerabilities": List[str],
        "Vendor": VulnerabilityVendorTypeDef,
        "ReferenceUrls": List[str],
        "FixAvailable": VulnerabilityFixAvailableType,
        "EpssScore": float,
        "ExploitAvailable": VulnerabilityExploitAvailableType,
        "CodeVulnerabilities": List[VulnerabilityCodeVulnerabilitiesPaginatorTypeDef],
    },
    total=False,
)


class VulnerabilityPaginatorTypeDef(
    _RequiredVulnerabilityPaginatorTypeDef, _OptionalVulnerabilityPaginatorTypeDef
):
    pass


_RequiredVulnerabilityTypeDef = TypedDict(
    "_RequiredVulnerabilityTypeDef",
    {
        "Id": str,
    },
)
_OptionalVulnerabilityTypeDef = TypedDict(
    "_OptionalVulnerabilityTypeDef",
    {
        "VulnerablePackages": Sequence[SoftwarePackageTypeDef],
        "Cvss": Sequence[CvssTypeDef],
        "RelatedVulnerabilities": Sequence[str],
        "Vendor": VulnerabilityVendorTypeDef,
        "ReferenceUrls": Sequence[str],
        "FixAvailable": VulnerabilityFixAvailableType,
        "EpssScore": float,
        "ExploitAvailable": VulnerabilityExploitAvailableType,
        "CodeVulnerabilities": Sequence[VulnerabilityCodeVulnerabilitiesTypeDef],
    },
    total=False,
)


class VulnerabilityTypeDef(_RequiredVulnerabilityTypeDef, _OptionalVulnerabilityTypeDef):
    pass


AutomationRulesFindingFiltersTypeDef = TypedDict(
    "AutomationRulesFindingFiltersTypeDef",
    {
        "ProductArn": List[StringFilterTypeDef],
        "AwsAccountId": List[StringFilterTypeDef],
        "Id": List[StringFilterTypeDef],
        "GeneratorId": List[StringFilterTypeDef],
        "Type": List[StringFilterTypeDef],
        "FirstObservedAt": List[DateFilterTypeDef],
        "LastObservedAt": List[DateFilterTypeDef],
        "CreatedAt": List[DateFilterTypeDef],
        "UpdatedAt": List[DateFilterTypeDef],
        "Confidence": List[NumberFilterTypeDef],
        "Criticality": List[NumberFilterTypeDef],
        "Title": List[StringFilterTypeDef],
        "Description": List[StringFilterTypeDef],
        "SourceUrl": List[StringFilterTypeDef],
        "ProductName": List[StringFilterTypeDef],
        "CompanyName": List[StringFilterTypeDef],
        "SeverityLabel": List[StringFilterTypeDef],
        "ResourceType": List[StringFilterTypeDef],
        "ResourceId": List[StringFilterTypeDef],
        "ResourcePartition": List[StringFilterTypeDef],
        "ResourceRegion": List[StringFilterTypeDef],
        "ResourceTags": List[MapFilterTypeDef],
        "ResourceDetailsOther": List[MapFilterTypeDef],
        "ComplianceStatus": List[StringFilterTypeDef],
        "ComplianceSecurityControlId": List[StringFilterTypeDef],
        "ComplianceAssociatedStandardsId": List[StringFilterTypeDef],
        "VerificationState": List[StringFilterTypeDef],
        "WorkflowStatus": List[StringFilterTypeDef],
        "RecordState": List[StringFilterTypeDef],
        "RelatedFindingsProductArn": List[StringFilterTypeDef],
        "RelatedFindingsId": List[StringFilterTypeDef],
        "NoteText": List[StringFilterTypeDef],
        "NoteUpdatedAt": List[DateFilterTypeDef],
        "NoteUpdatedBy": List[StringFilterTypeDef],
        "UserDefinedFields": List[MapFilterTypeDef],
    },
    total=False,
)

AwsSecurityFindingFiltersTypeDef = TypedDict(
    "AwsSecurityFindingFiltersTypeDef",
    {
        "ProductArn": Sequence[StringFilterTypeDef],
        "AwsAccountId": Sequence[StringFilterTypeDef],
        "Id": Sequence[StringFilterTypeDef],
        "GeneratorId": Sequence[StringFilterTypeDef],
        "Region": Sequence[StringFilterTypeDef],
        "Type": Sequence[StringFilterTypeDef],
        "FirstObservedAt": Sequence[DateFilterTypeDef],
        "LastObservedAt": Sequence[DateFilterTypeDef],
        "CreatedAt": Sequence[DateFilterTypeDef],
        "UpdatedAt": Sequence[DateFilterTypeDef],
        "SeverityProduct": Sequence[NumberFilterTypeDef],
        "SeverityNormalized": Sequence[NumberFilterTypeDef],
        "SeverityLabel": Sequence[StringFilterTypeDef],
        "Confidence": Sequence[NumberFilterTypeDef],
        "Criticality": Sequence[NumberFilterTypeDef],
        "Title": Sequence[StringFilterTypeDef],
        "Description": Sequence[StringFilterTypeDef],
        "RecommendationText": Sequence[StringFilterTypeDef],
        "SourceUrl": Sequence[StringFilterTypeDef],
        "ProductFields": Sequence[MapFilterTypeDef],
        "ProductName": Sequence[StringFilterTypeDef],
        "CompanyName": Sequence[StringFilterTypeDef],
        "UserDefinedFields": Sequence[MapFilterTypeDef],
        "MalwareName": Sequence[StringFilterTypeDef],
        "MalwareType": Sequence[StringFilterTypeDef],
        "MalwarePath": Sequence[StringFilterTypeDef],
        "MalwareState": Sequence[StringFilterTypeDef],
        "NetworkDirection": Sequence[StringFilterTypeDef],
        "NetworkProtocol": Sequence[StringFilterTypeDef],
        "NetworkSourceIpV4": Sequence[IpFilterTypeDef],
        "NetworkSourceIpV6": Sequence[IpFilterTypeDef],
        "NetworkSourcePort": Sequence[NumberFilterTypeDef],
        "NetworkSourceDomain": Sequence[StringFilterTypeDef],
        "NetworkSourceMac": Sequence[StringFilterTypeDef],
        "NetworkDestinationIpV4": Sequence[IpFilterTypeDef],
        "NetworkDestinationIpV6": Sequence[IpFilterTypeDef],
        "NetworkDestinationPort": Sequence[NumberFilterTypeDef],
        "NetworkDestinationDomain": Sequence[StringFilterTypeDef],
        "ProcessName": Sequence[StringFilterTypeDef],
        "ProcessPath": Sequence[StringFilterTypeDef],
        "ProcessPid": Sequence[NumberFilterTypeDef],
        "ProcessParentPid": Sequence[NumberFilterTypeDef],
        "ProcessLaunchedAt": Sequence[DateFilterTypeDef],
        "ProcessTerminatedAt": Sequence[DateFilterTypeDef],
        "ThreatIntelIndicatorType": Sequence[StringFilterTypeDef],
        "ThreatIntelIndicatorValue": Sequence[StringFilterTypeDef],
        "ThreatIntelIndicatorCategory": Sequence[StringFilterTypeDef],
        "ThreatIntelIndicatorLastObservedAt": Sequence[DateFilterTypeDef],
        "ThreatIntelIndicatorSource": Sequence[StringFilterTypeDef],
        "ThreatIntelIndicatorSourceUrl": Sequence[StringFilterTypeDef],
        "ResourceType": Sequence[StringFilterTypeDef],
        "ResourceId": Sequence[StringFilterTypeDef],
        "ResourcePartition": Sequence[StringFilterTypeDef],
        "ResourceRegion": Sequence[StringFilterTypeDef],
        "ResourceTags": Sequence[MapFilterTypeDef],
        "ResourceAwsEc2InstanceType": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceImageId": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceIpV4Addresses": Sequence[IpFilterTypeDef],
        "ResourceAwsEc2InstanceIpV6Addresses": Sequence[IpFilterTypeDef],
        "ResourceAwsEc2InstanceKeyName": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceIamInstanceProfileArn": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceVpcId": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceSubnetId": Sequence[StringFilterTypeDef],
        "ResourceAwsEc2InstanceLaunchedAt": Sequence[DateFilterTypeDef],
        "ResourceAwsS3BucketOwnerId": Sequence[StringFilterTypeDef],
        "ResourceAwsS3BucketOwnerName": Sequence[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyUserName": Sequence[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyPrincipalName": Sequence[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyStatus": Sequence[StringFilterTypeDef],
        "ResourceAwsIamAccessKeyCreatedAt": Sequence[DateFilterTypeDef],
        "ResourceAwsIamUserUserName": Sequence[StringFilterTypeDef],
        "ResourceContainerName": Sequence[StringFilterTypeDef],
        "ResourceContainerImageId": Sequence[StringFilterTypeDef],
        "ResourceContainerImageName": Sequence[StringFilterTypeDef],
        "ResourceContainerLaunchedAt": Sequence[DateFilterTypeDef],
        "ResourceDetailsOther": Sequence[MapFilterTypeDef],
        "ComplianceStatus": Sequence[StringFilterTypeDef],
        "VerificationState": Sequence[StringFilterTypeDef],
        "WorkflowState": Sequence[StringFilterTypeDef],
        "WorkflowStatus": Sequence[StringFilterTypeDef],
        "RecordState": Sequence[StringFilterTypeDef],
        "RelatedFindingsProductArn": Sequence[StringFilterTypeDef],
        "RelatedFindingsId": Sequence[StringFilterTypeDef],
        "NoteText": Sequence[StringFilterTypeDef],
        "NoteUpdatedAt": Sequence[DateFilterTypeDef],
        "NoteUpdatedBy": Sequence[StringFilterTypeDef],
        "Keyword": Sequence[KeywordFilterTypeDef],
        "FindingProviderFieldsConfidence": Sequence[NumberFilterTypeDef],
        "FindingProviderFieldsCriticality": Sequence[NumberFilterTypeDef],
        "FindingProviderFieldsRelatedFindingsId": Sequence[StringFilterTypeDef],
        "FindingProviderFieldsRelatedFindingsProductArn": Sequence[StringFilterTypeDef],
        "FindingProviderFieldsSeverityLabel": Sequence[StringFilterTypeDef],
        "FindingProviderFieldsSeverityOriginal": Sequence[StringFilterTypeDef],
        "FindingProviderFieldsTypes": Sequence[StringFilterTypeDef],
        "Sample": Sequence[BooleanFilterTypeDef],
        "ComplianceSecurityControlId": Sequence[StringFilterTypeDef],
        "ComplianceAssociatedStandardsId": Sequence[StringFilterTypeDef],
    },
    total=False,
)

GetFindingHistoryResponseTypeDef = TypedDict(
    "GetFindingHistoryResponseTypeDef",
    {
        "Records": List[FindingHistoryRecordTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInsightResultsResponseTypeDef = TypedDict(
    "GetInsightResultsResponseTypeDef",
    {
        "InsightResults": InsightResultsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NetworkHeaderPaginatorTypeDef = TypedDict(
    "NetworkHeaderPaginatorTypeDef",
    {
        "Protocol": str,
        "Destination": NetworkPathComponentDetailsPaginatorTypeDef,
        "Source": NetworkPathComponentDetailsPaginatorTypeDef,
    },
    total=False,
)

NetworkHeaderTypeDef = TypedDict(
    "NetworkHeaderTypeDef",
    {
        "Protocol": str,
        "Destination": NetworkPathComponentDetailsTypeDef,
        "Source": NetworkPathComponentDetailsTypeDef,
    },
    total=False,
)

OccurrencesPaginatorTypeDef = TypedDict(
    "OccurrencesPaginatorTypeDef",
    {
        "LineRanges": List[RangeTypeDef],
        "OffsetRanges": List[RangeTypeDef],
        "Pages": List[PageTypeDef],
        "Records": List[RecordTypeDef],
        "Cells": List[CellTypeDef],
    },
    total=False,
)

OccurrencesTypeDef = TypedDict(
    "OccurrencesTypeDef",
    {
        "LineRanges": Sequence[RangeTypeDef],
        "OffsetRanges": Sequence[RangeTypeDef],
        "Pages": Sequence[PageTypeDef],
        "Records": Sequence[RecordTypeDef],
        "Cells": Sequence[CellTypeDef],
    },
    total=False,
)

RuleGroupSourceStatelessRuleDefinitionPaginatorTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleDefinitionPaginatorTypeDef",
    {
        "Actions": List[str],
        "MatchAttributes": RuleGroupSourceStatelessRuleMatchAttributesPaginatorTypeDef,
    },
    total=False,
)

RuleGroupSourceStatelessRuleDefinitionTypeDef = TypedDict(
    "RuleGroupSourceStatelessRuleDefinitionTypeDef",
    {
        "Actions": Sequence[str],
        "MatchAttributes": RuleGroupSourceStatelessRuleMatchAttributesTypeDef,
    },
    total=False,
)

DescribeStandardsResponseTypeDef = TypedDict(
    "DescribeStandardsResponseTypeDef",
    {
        "Standards": List[StandardTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDisableStandardsResponseTypeDef = TypedDict(
    "BatchDisableStandardsResponseTypeDef",
    {
        "StandardsSubscriptions": List[StandardsSubscriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchEnableStandardsResponseTypeDef = TypedDict(
    "BatchEnableStandardsResponseTypeDef",
    {
        "StandardsSubscriptions": List[StandardsSubscriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEnabledStandardsResponseTypeDef = TypedDict(
    "GetEnabledStandardsResponseTypeDef",
    {
        "StandardsSubscriptions": List[StandardsSubscriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StatelessCustomActionDefinitionPaginatorTypeDef = TypedDict(
    "StatelessCustomActionDefinitionPaginatorTypeDef",
    {
        "PublishMetricAction": StatelessCustomPublishMetricActionPaginatorTypeDef,
    },
    total=False,
)

StatelessCustomActionDefinitionTypeDef = TypedDict(
    "StatelessCustomActionDefinitionTypeDef",
    {
        "PublishMetricAction": StatelessCustomPublishMetricActionTypeDef,
    },
    total=False,
)

PortProbeActionPaginatorTypeDef = TypedDict(
    "PortProbeActionPaginatorTypeDef",
    {
        "PortProbeDetails": List[PortProbeDetailTypeDef],
        "Blocked": bool,
    },
    total=False,
)

PortProbeActionTypeDef = TypedDict(
    "PortProbeActionTypeDef",
    {
        "PortProbeDetails": Sequence[PortProbeDetailTypeDef],
        "Blocked": bool,
    },
    total=False,
)

AwsAthenaWorkGroupDetailsTypeDef = TypedDict(
    "AwsAthenaWorkGroupDetailsTypeDef",
    {
        "Name": str,
        "Description": str,
        "State": str,
        "Configuration": AwsAthenaWorkGroupConfigurationDetailsTypeDef,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupDetailsPaginatorTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupDetailsPaginatorTypeDef",
    {
        "LaunchConfigurationName": str,
        "LoadBalancerNames": List[str],
        "HealthCheckType": str,
        "HealthCheckGracePeriod": int,
        "CreatedTime": str,
        "MixedInstancesPolicy": (
            AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsPaginatorTypeDef
        ),
        "AvailabilityZones": List[
            AwsAutoScalingAutoScalingGroupAvailabilityZonesListDetailsTypeDef
        ],
        "LaunchTemplate": (
            AwsAutoScalingAutoScalingGroupLaunchTemplateLaunchTemplateSpecificationTypeDef
        ),
        "CapacityRebalance": bool,
    },
    total=False,
)

AwsAutoScalingAutoScalingGroupDetailsTypeDef = TypedDict(
    "AwsAutoScalingAutoScalingGroupDetailsTypeDef",
    {
        "LaunchConfigurationName": str,
        "LoadBalancerNames": Sequence[str],
        "HealthCheckType": str,
        "HealthCheckGracePeriod": int,
        "CreatedTime": str,
        "MixedInstancesPolicy": AwsAutoScalingAutoScalingGroupMixedInstancesPolicyDetailsTypeDef,
        "AvailabilityZones": Sequence[
            AwsAutoScalingAutoScalingGroupAvailabilityZonesListDetailsTypeDef
        ],
        "LaunchTemplate": (
            AwsAutoScalingAutoScalingGroupLaunchTemplateLaunchTemplateSpecificationTypeDef
        ),
        "CapacityRebalance": bool,
    },
    total=False,
)

AwsBackupBackupPlanBackupPlanDetailsPaginatorTypeDef = TypedDict(
    "AwsBackupBackupPlanBackupPlanDetailsPaginatorTypeDef",
    {
        "BackupPlanName": str,
        "AdvancedBackupSettings": List[
            AwsBackupBackupPlanAdvancedBackupSettingsDetailsPaginatorTypeDef
        ],
        "BackupPlanRule": List[AwsBackupBackupPlanRuleDetailsPaginatorTypeDef],
    },
    total=False,
)

AwsBackupBackupPlanBackupPlanDetailsTypeDef = TypedDict(
    "AwsBackupBackupPlanBackupPlanDetailsTypeDef",
    {
        "BackupPlanName": str,
        "AdvancedBackupSettings": Sequence[AwsBackupBackupPlanAdvancedBackupSettingsDetailsTypeDef],
        "BackupPlanRule": Sequence[AwsBackupBackupPlanRuleDetailsTypeDef],
    },
    total=False,
)

AwsCertificateManagerCertificateDetailsPaginatorTypeDef = TypedDict(
    "AwsCertificateManagerCertificateDetailsPaginatorTypeDef",
    {
        "CertificateAuthorityArn": str,
        "CreatedAt": str,
        "DomainName": str,
        "DomainValidationOptions": List[
            AwsCertificateManagerCertificateDomainValidationOptionPaginatorTypeDef
        ],
        "ExtendedKeyUsages": List[AwsCertificateManagerCertificateExtendedKeyUsageTypeDef],
        "FailureReason": str,
        "ImportedAt": str,
        "InUseBy": List[str],
        "IssuedAt": str,
        "Issuer": str,
        "KeyAlgorithm": str,
        "KeyUsages": List[AwsCertificateManagerCertificateKeyUsageTypeDef],
        "NotAfter": str,
        "NotBefore": str,
        "Options": AwsCertificateManagerCertificateOptionsTypeDef,
        "RenewalEligibility": str,
        "RenewalSummary": AwsCertificateManagerCertificateRenewalSummaryPaginatorTypeDef,
        "Serial": str,
        "SignatureAlgorithm": str,
        "Status": str,
        "Subject": str,
        "SubjectAlternativeNames": List[str],
        "Type": str,
    },
    total=False,
)

AwsCertificateManagerCertificateDetailsTypeDef = TypedDict(
    "AwsCertificateManagerCertificateDetailsTypeDef",
    {
        "CertificateAuthorityArn": str,
        "CreatedAt": str,
        "DomainName": str,
        "DomainValidationOptions": Sequence[
            AwsCertificateManagerCertificateDomainValidationOptionTypeDef
        ],
        "ExtendedKeyUsages": Sequence[AwsCertificateManagerCertificateExtendedKeyUsageTypeDef],
        "FailureReason": str,
        "ImportedAt": str,
        "InUseBy": Sequence[str],
        "IssuedAt": str,
        "Issuer": str,
        "KeyAlgorithm": str,
        "KeyUsages": Sequence[AwsCertificateManagerCertificateKeyUsageTypeDef],
        "NotAfter": str,
        "NotBefore": str,
        "Options": AwsCertificateManagerCertificateOptionsTypeDef,
        "RenewalEligibility": str,
        "RenewalSummary": AwsCertificateManagerCertificateRenewalSummaryTypeDef,
        "Serial": str,
        "SignatureAlgorithm": str,
        "Status": str,
        "Subject": str,
        "SubjectAlternativeNames": Sequence[str],
        "Type": str,
    },
    total=False,
)

AwsCloudFrontDistributionOriginsPaginatorTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginsPaginatorTypeDef",
    {
        "Items": List[AwsCloudFrontDistributionOriginItemPaginatorTypeDef],
    },
    total=False,
)

AwsCloudFrontDistributionOriginsTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginsTypeDef",
    {
        "Items": Sequence[AwsCloudFrontDistributionOriginItemTypeDef],
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupsPaginatorTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupsPaginatorTypeDef",
    {
        "Items": List[AwsCloudFrontDistributionOriginGroupPaginatorTypeDef],
    },
    total=False,
)

AwsCloudFrontDistributionOriginGroupsTypeDef = TypedDict(
    "AwsCloudFrontDistributionOriginGroupsTypeDef",
    {
        "Items": Sequence[AwsCloudFrontDistributionOriginGroupTypeDef],
    },
    total=False,
)

AwsDynamoDbTableDetailsPaginatorTypeDef = TypedDict(
    "AwsDynamoDbTableDetailsPaginatorTypeDef",
    {
        "AttributeDefinitions": List[AwsDynamoDbTableAttributeDefinitionTypeDef],
        "BillingModeSummary": AwsDynamoDbTableBillingModeSummaryTypeDef,
        "CreationDateTime": str,
        "GlobalSecondaryIndexes": List[AwsDynamoDbTableGlobalSecondaryIndexPaginatorTypeDef],
        "GlobalTableVersion": str,
        "ItemCount": int,
        "KeySchema": List[AwsDynamoDbTableKeySchemaTypeDef],
        "LatestStreamArn": str,
        "LatestStreamLabel": str,
        "LocalSecondaryIndexes": List[AwsDynamoDbTableLocalSecondaryIndexPaginatorTypeDef],
        "ProvisionedThroughput": AwsDynamoDbTableProvisionedThroughputTypeDef,
        "Replicas": List[AwsDynamoDbTableReplicaPaginatorTypeDef],
        "RestoreSummary": AwsDynamoDbTableRestoreSummaryTypeDef,
        "SseDescription": AwsDynamoDbTableSseDescriptionTypeDef,
        "StreamSpecification": AwsDynamoDbTableStreamSpecificationTypeDef,
        "TableId": str,
        "TableName": str,
        "TableSizeBytes": int,
        "TableStatus": str,
    },
    total=False,
)

AwsDynamoDbTableDetailsTypeDef = TypedDict(
    "AwsDynamoDbTableDetailsTypeDef",
    {
        "AttributeDefinitions": Sequence[AwsDynamoDbTableAttributeDefinitionTypeDef],
        "BillingModeSummary": AwsDynamoDbTableBillingModeSummaryTypeDef,
        "CreationDateTime": str,
        "GlobalSecondaryIndexes": Sequence[AwsDynamoDbTableGlobalSecondaryIndexTypeDef],
        "GlobalTableVersion": str,
        "ItemCount": int,
        "KeySchema": Sequence[AwsDynamoDbTableKeySchemaTypeDef],
        "LatestStreamArn": str,
        "LatestStreamLabel": str,
        "LocalSecondaryIndexes": Sequence[AwsDynamoDbTableLocalSecondaryIndexTypeDef],
        "ProvisionedThroughput": AwsDynamoDbTableProvisionedThroughputTypeDef,
        "Replicas": Sequence[AwsDynamoDbTableReplicaTypeDef],
        "RestoreSummary": AwsDynamoDbTableRestoreSummaryTypeDef,
        "SseDescription": AwsDynamoDbTableSseDescriptionTypeDef,
        "StreamSpecification": AwsDynamoDbTableStreamSpecificationTypeDef,
        "TableId": str,
        "TableName": str,
        "TableSizeBytes": int,
        "TableStatus": str,
    },
    total=False,
)

AwsEc2LaunchTemplateDetailsPaginatorTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDetailsPaginatorTypeDef",
    {
        "LaunchTemplateName": str,
        "Id": str,
        "LaunchTemplateData": AwsEc2LaunchTemplateDataDetailsPaginatorTypeDef,
        "DefaultVersionNumber": int,
        "LatestVersionNumber": int,
    },
    total=False,
)

AwsEc2LaunchTemplateDetailsTypeDef = TypedDict(
    "AwsEc2LaunchTemplateDetailsTypeDef",
    {
        "LaunchTemplateName": str,
        "Id": str,
        "LaunchTemplateData": AwsEc2LaunchTemplateDataDetailsTypeDef,
        "DefaultVersionNumber": int,
        "LatestVersionNumber": int,
    },
    total=False,
)

AwsEcsClusterDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsClusterDetailsPaginatorTypeDef",
    {
        "ClusterArn": str,
        "ActiveServicesCount": int,
        "CapacityProviders": List[str],
        "ClusterSettings": List[AwsEcsClusterClusterSettingsDetailsTypeDef],
        "Configuration": AwsEcsClusterConfigurationDetailsTypeDef,
        "DefaultCapacityProviderStrategy": List[
            AwsEcsClusterDefaultCapacityProviderStrategyDetailsTypeDef
        ],
        "ClusterName": str,
        "RegisteredContainerInstancesCount": int,
        "RunningTasksCount": int,
        "Status": str,
    },
    total=False,
)

AwsEcsClusterDetailsTypeDef = TypedDict(
    "AwsEcsClusterDetailsTypeDef",
    {
        "ClusterArn": str,
        "ActiveServicesCount": int,
        "CapacityProviders": Sequence[str],
        "ClusterSettings": Sequence[AwsEcsClusterClusterSettingsDetailsTypeDef],
        "Configuration": AwsEcsClusterConfigurationDetailsTypeDef,
        "DefaultCapacityProviderStrategy": Sequence[
            AwsEcsClusterDefaultCapacityProviderStrategyDetailsTypeDef
        ],
        "ClusterName": str,
        "RegisteredContainerInstancesCount": int,
        "RunningTasksCount": int,
        "Status": str,
    },
    total=False,
)

AwsEcsTaskDefinitionDetailsPaginatorTypeDef = TypedDict(
    "AwsEcsTaskDefinitionDetailsPaginatorTypeDef",
    {
        "ContainerDefinitions": List[
            AwsEcsTaskDefinitionContainerDefinitionsDetailsPaginatorTypeDef
        ],
        "Cpu": str,
        "ExecutionRoleArn": str,
        "Family": str,
        "InferenceAccelerators": List[AwsEcsTaskDefinitionInferenceAcceleratorsDetailsTypeDef],
        "IpcMode": str,
        "Memory": str,
        "NetworkMode": str,
        "PidMode": str,
        "PlacementConstraints": List[AwsEcsTaskDefinitionPlacementConstraintsDetailsTypeDef],
        "ProxyConfiguration": AwsEcsTaskDefinitionProxyConfigurationDetailsPaginatorTypeDef,
        "RequiresCompatibilities": List[str],
        "TaskRoleArn": str,
        "Volumes": List[AwsEcsTaskDefinitionVolumesDetailsPaginatorTypeDef],
    },
    total=False,
)

AwsEcsTaskDefinitionDetailsTypeDef = TypedDict(
    "AwsEcsTaskDefinitionDetailsTypeDef",
    {
        "ContainerDefinitions": Sequence[AwsEcsTaskDefinitionContainerDefinitionsDetailsTypeDef],
        "Cpu": str,
        "ExecutionRoleArn": str,
        "Family": str,
        "InferenceAccelerators": Sequence[AwsEcsTaskDefinitionInferenceAcceleratorsDetailsTypeDef],
        "IpcMode": str,
        "Memory": str,
        "NetworkMode": str,
        "PidMode": str,
        "PlacementConstraints": Sequence[AwsEcsTaskDefinitionPlacementConstraintsDetailsTypeDef],
        "ProxyConfiguration": AwsEcsTaskDefinitionProxyConfigurationDetailsTypeDef,
        "RequiresCompatibilities": Sequence[str],
        "TaskRoleArn": str,
        "Volumes": Sequence[AwsEcsTaskDefinitionVolumesDetailsTypeDef],
    },
    total=False,
)

AwsGuardDutyDetectorDataSourcesDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDataSourcesDetailsTypeDef",
    {
        "CloudTrail": AwsGuardDutyDetectorDataSourcesCloudTrailDetailsTypeDef,
        "DnsLogs": AwsGuardDutyDetectorDataSourcesDnsLogsDetailsTypeDef,
        "FlowLogs": AwsGuardDutyDetectorDataSourcesFlowLogsDetailsTypeDef,
        "Kubernetes": AwsGuardDutyDetectorDataSourcesKubernetesDetailsTypeDef,
        "MalwareProtection": AwsGuardDutyDetectorDataSourcesMalwareProtectionDetailsTypeDef,
        "S3Logs": AwsGuardDutyDetectorDataSourcesS3LogsDetailsTypeDef,
    },
    total=False,
)

AwsIamRoleDetailsTypeDef = TypedDict(
    "AwsIamRoleDetailsTypeDef",
    {
        "AssumeRolePolicyDocument": DictOrStrTypeDef,
        "AttachedManagedPolicies": Sequence[AwsIamAttachedManagedPolicyTypeDef],
        "CreateDate": str,
        "InstanceProfileList": Sequence[AwsIamInstanceProfileTypeDef],
        "PermissionsBoundary": AwsIamPermissionsBoundaryTypeDef,
        "RoleId": str,
        "RoleName": str,
        "RolePolicyList": Sequence[AwsIamRolePolicyTypeDef],
        "MaxSessionDuration": int,
        "Path": str,
    },
    total=False,
)

AwsRdsDbInstanceDetailsPaginatorTypeDef = TypedDict(
    "AwsRdsDbInstanceDetailsPaginatorTypeDef",
    {
        "AssociatedRoles": List[AwsRdsDbInstanceAssociatedRoleTypeDef],
        "CACertificateIdentifier": str,
        "DBClusterIdentifier": str,
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "DbInstancePort": int,
        "DbiResourceId": str,
        "DBName": str,
        "DeletionProtection": bool,
        "Endpoint": AwsRdsDbInstanceEndpointTypeDef,
        "Engine": str,
        "EngineVersion": str,
        "IAMDatabaseAuthenticationEnabled": bool,
        "InstanceCreateTime": str,
        "KmsKeyId": str,
        "PubliclyAccessible": bool,
        "StorageEncrypted": bool,
        "TdeCredentialArn": str,
        "VpcSecurityGroups": List[AwsRdsDbInstanceVpcSecurityGroupTypeDef],
        "MultiAz": bool,
        "EnhancedMonitoringResourceArn": str,
        "DbInstanceStatus": str,
        "MasterUsername": str,
        "AllocatedStorage": int,
        "PreferredBackupWindow": str,
        "BackupRetentionPeriod": int,
        "DbSecurityGroups": List[str],
        "DbParameterGroups": List[AwsRdsDbParameterGroupTypeDef],
        "AvailabilityZone": str,
        "DbSubnetGroup": AwsRdsDbSubnetGroupPaginatorTypeDef,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": AwsRdsDbPendingModifiedValuesPaginatorTypeDef,
        "LatestRestorableTime": str,
        "AutoMinorVersionUpgrade": bool,
        "ReadReplicaSourceDBInstanceIdentifier": str,
        "ReadReplicaDBInstanceIdentifiers": List[str],
        "ReadReplicaDBClusterIdentifiers": List[str],
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupMemberships": List[AwsRdsDbOptionGroupMembershipTypeDef],
        "CharacterSetName": str,
        "SecondaryAvailabilityZone": str,
        "StatusInfos": List[AwsRdsDbStatusInfoTypeDef],
        "StorageType": str,
        "DomainMemberships": List[AwsRdsDbDomainMembershipTypeDef],
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "MonitoringRoleArn": str,
        "PromotionTier": int,
        "Timezone": str,
        "PerformanceInsightsEnabled": bool,
        "PerformanceInsightsKmsKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "EnabledCloudWatchLogsExports": List[str],
        "ProcessorFeatures": List[AwsRdsDbProcessorFeatureTypeDef],
        "ListenerEndpoint": AwsRdsDbInstanceEndpointTypeDef,
        "MaxAllocatedStorage": int,
    },
    total=False,
)

AwsRdsDbInstanceDetailsTypeDef = TypedDict(
    "AwsRdsDbInstanceDetailsTypeDef",
    {
        "AssociatedRoles": Sequence[AwsRdsDbInstanceAssociatedRoleTypeDef],
        "CACertificateIdentifier": str,
        "DBClusterIdentifier": str,
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "DbInstancePort": int,
        "DbiResourceId": str,
        "DBName": str,
        "DeletionProtection": bool,
        "Endpoint": AwsRdsDbInstanceEndpointTypeDef,
        "Engine": str,
        "EngineVersion": str,
        "IAMDatabaseAuthenticationEnabled": bool,
        "InstanceCreateTime": str,
        "KmsKeyId": str,
        "PubliclyAccessible": bool,
        "StorageEncrypted": bool,
        "TdeCredentialArn": str,
        "VpcSecurityGroups": Sequence[AwsRdsDbInstanceVpcSecurityGroupTypeDef],
        "MultiAz": bool,
        "EnhancedMonitoringResourceArn": str,
        "DbInstanceStatus": str,
        "MasterUsername": str,
        "AllocatedStorage": int,
        "PreferredBackupWindow": str,
        "BackupRetentionPeriod": int,
        "DbSecurityGroups": Sequence[str],
        "DbParameterGroups": Sequence[AwsRdsDbParameterGroupTypeDef],
        "AvailabilityZone": str,
        "DbSubnetGroup": AwsRdsDbSubnetGroupTypeDef,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": AwsRdsDbPendingModifiedValuesTypeDef,
        "LatestRestorableTime": str,
        "AutoMinorVersionUpgrade": bool,
        "ReadReplicaSourceDBInstanceIdentifier": str,
        "ReadReplicaDBInstanceIdentifiers": Sequence[str],
        "ReadReplicaDBClusterIdentifiers": Sequence[str],
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupMemberships": Sequence[AwsRdsDbOptionGroupMembershipTypeDef],
        "CharacterSetName": str,
        "SecondaryAvailabilityZone": str,
        "StatusInfos": Sequence[AwsRdsDbStatusInfoTypeDef],
        "StorageType": str,
        "DomainMemberships": Sequence[AwsRdsDbDomainMembershipTypeDef],
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "MonitoringRoleArn": str,
        "PromotionTier": int,
        "Timezone": str,
        "PerformanceInsightsEnabled": bool,
        "PerformanceInsightsKmsKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "EnabledCloudWatchLogsExports": Sequence[str],
        "ProcessorFeatures": Sequence[AwsRdsDbProcessorFeatureTypeDef],
        "ListenerEndpoint": AwsRdsDbInstanceEndpointTypeDef,
        "MaxAllocatedStorage": int,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsPaginatorTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsPaginatorTypeDef",
    {
        "Predicate": (
            AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsPaginatorTypeDef
        ),
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsTypeDef",
    {
        "Predicate": AwsS3BucketBucketLifecycleConfigurationRulesFilterPredicateDetailsTypeDef,
    },
    total=False,
)

AwsS3BucketNotificationConfigurationDetailPaginatorTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationDetailPaginatorTypeDef",
    {
        "Events": List[str],
        "Filter": AwsS3BucketNotificationConfigurationFilterPaginatorTypeDef,
        "Destination": str,
        "Type": str,
    },
    total=False,
)

AwsS3BucketNotificationConfigurationDetailTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationDetailTypeDef",
    {
        "Events": Sequence[str],
        "Filter": AwsS3BucketNotificationConfigurationFilterTypeDef,
        "Destination": str,
        "Type": str,
    },
    total=False,
)

AwsStepFunctionStateMachineDetailsPaginatorTypeDef = TypedDict(
    "AwsStepFunctionStateMachineDetailsPaginatorTypeDef",
    {
        "Label": str,
        "LoggingConfiguration": (
            AwsStepFunctionStateMachineLoggingConfigurationDetailsPaginatorTypeDef
        ),
        "Name": str,
        "RoleArn": str,
        "StateMachineArn": str,
        "Status": str,
        "TracingConfiguration": AwsStepFunctionStateMachineTracingConfigurationDetailsTypeDef,
        "Type": str,
    },
    total=False,
)

AwsStepFunctionStateMachineDetailsTypeDef = TypedDict(
    "AwsStepFunctionStateMachineDetailsTypeDef",
    {
        "Label": str,
        "LoggingConfiguration": AwsStepFunctionStateMachineLoggingConfigurationDetailsTypeDef,
        "Name": str,
        "RoleArn": str,
        "StateMachineArn": str,
        "Status": str,
        "TracingConfiguration": AwsStepFunctionStateMachineTracingConfigurationDetailsTypeDef,
        "Type": str,
    },
    total=False,
)

AwsWafv2RulesActionDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2RulesActionDetailsPaginatorTypeDef",
    {
        "Allow": AwsWafv2ActionAllowDetailsPaginatorTypeDef,
        "Block": AwsWafv2ActionBlockDetailsPaginatorTypeDef,
        "Captcha": AwsWafv2RulesActionCaptchaDetailsPaginatorTypeDef,
        "Count": AwsWafv2RulesActionCountDetailsPaginatorTypeDef,
    },
    total=False,
)

AwsWafv2WebAclActionDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2WebAclActionDetailsPaginatorTypeDef",
    {
        "Allow": AwsWafv2ActionAllowDetailsPaginatorTypeDef,
        "Block": AwsWafv2ActionBlockDetailsPaginatorTypeDef,
    },
    total=False,
)

AwsWafv2RulesActionDetailsTypeDef = TypedDict(
    "AwsWafv2RulesActionDetailsTypeDef",
    {
        "Allow": AwsWafv2ActionAllowDetailsTypeDef,
        "Block": AwsWafv2ActionBlockDetailsTypeDef,
        "Captcha": AwsWafv2RulesActionCaptchaDetailsTypeDef,
        "Count": AwsWafv2RulesActionCountDetailsTypeDef,
    },
    total=False,
)

AwsWafv2WebAclActionDetailsTypeDef = TypedDict(
    "AwsWafv2WebAclActionDetailsTypeDef",
    {
        "Allow": AwsWafv2ActionAllowDetailsTypeDef,
        "Block": AwsWafv2ActionBlockDetailsTypeDef,
    },
    total=False,
)

AutomationRulesConfigTypeDef = TypedDict(
    "AutomationRulesConfigTypeDef",
    {
        "RuleArn": str,
        "RuleStatus": RuleStatusType,
        "RuleOrder": int,
        "RuleName": str,
        "Description": str,
        "IsTerminal": bool,
        "Criteria": AutomationRulesFindingFiltersTypeDef,
        "Actions": List[AutomationRulesActionTypeDef],
        "CreatedAt": datetime,
        "UpdatedAt": datetime,
        "CreatedBy": str,
    },
    total=False,
)

_RequiredCreateAutomationRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAutomationRuleRequestRequestTypeDef",
    {
        "RuleOrder": int,
        "RuleName": str,
        "Description": str,
        "Criteria": AutomationRulesFindingFiltersTypeDef,
        "Actions": Sequence[AutomationRulesActionTypeDef],
    },
)
_OptionalCreateAutomationRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAutomationRuleRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
        "RuleStatus": RuleStatusType,
        "IsTerminal": bool,
    },
    total=False,
)


class CreateAutomationRuleRequestRequestTypeDef(
    _RequiredCreateAutomationRuleRequestRequestTypeDef,
    _OptionalCreateAutomationRuleRequestRequestTypeDef,
):
    pass


_RequiredUpdateAutomationRulesRequestItemTypeDef = TypedDict(
    "_RequiredUpdateAutomationRulesRequestItemTypeDef",
    {
        "RuleArn": str,
    },
)
_OptionalUpdateAutomationRulesRequestItemTypeDef = TypedDict(
    "_OptionalUpdateAutomationRulesRequestItemTypeDef",
    {
        "RuleStatus": RuleStatusType,
        "RuleOrder": int,
        "Description": str,
        "RuleName": str,
        "IsTerminal": bool,
        "Criteria": AutomationRulesFindingFiltersTypeDef,
        "Actions": Sequence[AutomationRulesActionTypeDef],
    },
    total=False,
)


class UpdateAutomationRulesRequestItemTypeDef(
    _RequiredUpdateAutomationRulesRequestItemTypeDef,
    _OptionalUpdateAutomationRulesRequestItemTypeDef,
):
    pass


CreateInsightRequestRequestTypeDef = TypedDict(
    "CreateInsightRequestRequestTypeDef",
    {
        "Name": str,
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "GroupByAttribute": str,
    },
)

GetFindingsRequestGetFindingsPaginateTypeDef = TypedDict(
    "GetFindingsRequestGetFindingsPaginateTypeDef",
    {
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "SortCriteria": Sequence[SortCriterionTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

GetFindingsRequestRequestTypeDef = TypedDict(
    "GetFindingsRequestRequestTypeDef",
    {
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "SortCriteria": Sequence[SortCriterionTypeDef],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

InsightTypeDef = TypedDict(
    "InsightTypeDef",
    {
        "InsightArn": str,
        "Name": str,
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "GroupByAttribute": str,
    },
)

_RequiredUpdateFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFindingsRequestRequestTypeDef",
    {
        "Filters": AwsSecurityFindingFiltersTypeDef,
    },
)
_OptionalUpdateFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFindingsRequestRequestTypeDef",
    {
        "Note": NoteUpdateTypeDef,
        "RecordState": RecordStateType,
    },
    total=False,
)


class UpdateFindingsRequestRequestTypeDef(
    _RequiredUpdateFindingsRequestRequestTypeDef, _OptionalUpdateFindingsRequestRequestTypeDef
):
    pass


_RequiredUpdateInsightRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateInsightRequestRequestTypeDef",
    {
        "InsightArn": str,
    },
)
_OptionalUpdateInsightRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateInsightRequestRequestTypeDef",
    {
        "Name": str,
        "Filters": AwsSecurityFindingFiltersTypeDef,
        "GroupByAttribute": str,
    },
    total=False,
)


class UpdateInsightRequestRequestTypeDef(
    _RequiredUpdateInsightRequestRequestTypeDef, _OptionalUpdateInsightRequestRequestTypeDef
):
    pass


NetworkPathComponentPaginatorTypeDef = TypedDict(
    "NetworkPathComponentPaginatorTypeDef",
    {
        "ComponentId": str,
        "ComponentType": str,
        "Egress": NetworkHeaderPaginatorTypeDef,
        "Ingress": NetworkHeaderPaginatorTypeDef,
    },
    total=False,
)

NetworkPathComponentTypeDef = TypedDict(
    "NetworkPathComponentTypeDef",
    {
        "ComponentId": str,
        "ComponentType": str,
        "Egress": NetworkHeaderTypeDef,
        "Ingress": NetworkHeaderTypeDef,
    },
    total=False,
)

CustomDataIdentifiersDetectionsPaginatorTypeDef = TypedDict(
    "CustomDataIdentifiersDetectionsPaginatorTypeDef",
    {
        "Count": int,
        "Arn": str,
        "Name": str,
        "Occurrences": OccurrencesPaginatorTypeDef,
    },
    total=False,
)

SensitiveDataDetectionsPaginatorTypeDef = TypedDict(
    "SensitiveDataDetectionsPaginatorTypeDef",
    {
        "Count": int,
        "Type": str,
        "Occurrences": OccurrencesPaginatorTypeDef,
    },
    total=False,
)

CustomDataIdentifiersDetectionsTypeDef = TypedDict(
    "CustomDataIdentifiersDetectionsTypeDef",
    {
        "Count": int,
        "Arn": str,
        "Name": str,
        "Occurrences": OccurrencesTypeDef,
    },
    total=False,
)

SensitiveDataDetectionsTypeDef = TypedDict(
    "SensitiveDataDetectionsTypeDef",
    {
        "Count": int,
        "Type": str,
        "Occurrences": OccurrencesTypeDef,
    },
    total=False,
)

RuleGroupSourceStatelessRulesDetailsPaginatorTypeDef = TypedDict(
    "RuleGroupSourceStatelessRulesDetailsPaginatorTypeDef",
    {
        "Priority": int,
        "RuleDefinition": RuleGroupSourceStatelessRuleDefinitionPaginatorTypeDef,
    },
    total=False,
)

RuleGroupSourceStatelessRulesDetailsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRulesDetailsTypeDef",
    {
        "Priority": int,
        "RuleDefinition": RuleGroupSourceStatelessRuleDefinitionTypeDef,
    },
    total=False,
)

FirewallPolicyStatelessCustomActionsDetailsPaginatorTypeDef = TypedDict(
    "FirewallPolicyStatelessCustomActionsDetailsPaginatorTypeDef",
    {
        "ActionDefinition": StatelessCustomActionDefinitionPaginatorTypeDef,
        "ActionName": str,
    },
    total=False,
)

RuleGroupSourceCustomActionsDetailsPaginatorTypeDef = TypedDict(
    "RuleGroupSourceCustomActionsDetailsPaginatorTypeDef",
    {
        "ActionDefinition": StatelessCustomActionDefinitionPaginatorTypeDef,
        "ActionName": str,
    },
    total=False,
)

FirewallPolicyStatelessCustomActionsDetailsTypeDef = TypedDict(
    "FirewallPolicyStatelessCustomActionsDetailsTypeDef",
    {
        "ActionDefinition": StatelessCustomActionDefinitionTypeDef,
        "ActionName": str,
    },
    total=False,
)

RuleGroupSourceCustomActionsDetailsTypeDef = TypedDict(
    "RuleGroupSourceCustomActionsDetailsTypeDef",
    {
        "ActionDefinition": StatelessCustomActionDefinitionTypeDef,
        "ActionName": str,
    },
    total=False,
)

ActionPaginatorTypeDef = TypedDict(
    "ActionPaginatorTypeDef",
    {
        "ActionType": str,
        "NetworkConnectionAction": NetworkConnectionActionTypeDef,
        "AwsApiCallAction": AwsApiCallActionPaginatorTypeDef,
        "DnsRequestAction": DnsRequestActionTypeDef,
        "PortProbeAction": PortProbeActionPaginatorTypeDef,
    },
    total=False,
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "ActionType": str,
        "NetworkConnectionAction": NetworkConnectionActionTypeDef,
        "AwsApiCallAction": AwsApiCallActionTypeDef,
        "DnsRequestAction": DnsRequestActionTypeDef,
        "PortProbeAction": PortProbeActionTypeDef,
    },
    total=False,
)

AwsBackupBackupPlanDetailsPaginatorTypeDef = TypedDict(
    "AwsBackupBackupPlanDetailsPaginatorTypeDef",
    {
        "BackupPlan": AwsBackupBackupPlanBackupPlanDetailsPaginatorTypeDef,
        "BackupPlanArn": str,
        "BackupPlanId": str,
        "VersionId": str,
    },
    total=False,
)

AwsBackupBackupPlanDetailsTypeDef = TypedDict(
    "AwsBackupBackupPlanDetailsTypeDef",
    {
        "BackupPlan": AwsBackupBackupPlanBackupPlanDetailsTypeDef,
        "BackupPlanArn": str,
        "BackupPlanId": str,
        "VersionId": str,
    },
    total=False,
)

AwsCloudFrontDistributionDetailsPaginatorTypeDef = TypedDict(
    "AwsCloudFrontDistributionDetailsPaginatorTypeDef",
    {
        "CacheBehaviors": AwsCloudFrontDistributionCacheBehaviorsPaginatorTypeDef,
        "DefaultCacheBehavior": AwsCloudFrontDistributionDefaultCacheBehaviorTypeDef,
        "DefaultRootObject": str,
        "DomainName": str,
        "ETag": str,
        "LastModifiedTime": str,
        "Logging": AwsCloudFrontDistributionLoggingTypeDef,
        "Origins": AwsCloudFrontDistributionOriginsPaginatorTypeDef,
        "OriginGroups": AwsCloudFrontDistributionOriginGroupsPaginatorTypeDef,
        "ViewerCertificate": AwsCloudFrontDistributionViewerCertificateTypeDef,
        "Status": str,
        "WebAclId": str,
    },
    total=False,
)

AwsCloudFrontDistributionDetailsTypeDef = TypedDict(
    "AwsCloudFrontDistributionDetailsTypeDef",
    {
        "CacheBehaviors": AwsCloudFrontDistributionCacheBehaviorsTypeDef,
        "DefaultCacheBehavior": AwsCloudFrontDistributionDefaultCacheBehaviorTypeDef,
        "DefaultRootObject": str,
        "DomainName": str,
        "ETag": str,
        "LastModifiedTime": str,
        "Logging": AwsCloudFrontDistributionLoggingTypeDef,
        "Origins": AwsCloudFrontDistributionOriginsTypeDef,
        "OriginGroups": AwsCloudFrontDistributionOriginGroupsTypeDef,
        "ViewerCertificate": AwsCloudFrontDistributionViewerCertificateTypeDef,
        "Status": str,
        "WebAclId": str,
    },
    total=False,
)

AwsGuardDutyDetectorDetailsPaginatorTypeDef = TypedDict(
    "AwsGuardDutyDetectorDetailsPaginatorTypeDef",
    {
        "DataSources": AwsGuardDutyDetectorDataSourcesDetailsTypeDef,
        "Features": List[AwsGuardDutyDetectorFeaturesDetailsTypeDef],
        "FindingPublishingFrequency": str,
        "ServiceRole": str,
        "Status": str,
    },
    total=False,
)

AwsGuardDutyDetectorDetailsTypeDef = TypedDict(
    "AwsGuardDutyDetectorDetailsTypeDef",
    {
        "DataSources": AwsGuardDutyDetectorDataSourcesDetailsTypeDef,
        "Features": Sequence[AwsGuardDutyDetectorFeaturesDetailsTypeDef],
        "FindingPublishingFrequency": str,
        "ServiceRole": str,
        "Status": str,
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesDetailsPaginatorTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesDetailsPaginatorTypeDef",
    {
        "AbortIncompleteMultipartUpload": (
            AwsS3BucketBucketLifecycleConfigurationRulesAbortIncompleteMultipartUploadDetailsTypeDef
        ),
        "ExpirationDate": str,
        "ExpirationInDays": int,
        "ExpiredObjectDeleteMarker": bool,
        "Filter": AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsPaginatorTypeDef,
        "ID": str,
        "NoncurrentVersionExpirationInDays": int,
        "NoncurrentVersionTransitions": List[
            AwsS3BucketBucketLifecycleConfigurationRulesNoncurrentVersionTransitionsDetailsTypeDef
        ],
        "Prefix": str,
        "Status": str,
        "Transitions": List[AwsS3BucketBucketLifecycleConfigurationRulesTransitionsDetailsTypeDef],
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationRulesDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationRulesDetailsTypeDef",
    {
        "AbortIncompleteMultipartUpload": (
            AwsS3BucketBucketLifecycleConfigurationRulesAbortIncompleteMultipartUploadDetailsTypeDef
        ),
        "ExpirationDate": str,
        "ExpirationInDays": int,
        "ExpiredObjectDeleteMarker": bool,
        "Filter": AwsS3BucketBucketLifecycleConfigurationRulesFilterDetailsTypeDef,
        "ID": str,
        "NoncurrentVersionExpirationInDays": int,
        "NoncurrentVersionTransitions": Sequence[
            AwsS3BucketBucketLifecycleConfigurationRulesNoncurrentVersionTransitionsDetailsTypeDef
        ],
        "Prefix": str,
        "Status": str,
        "Transitions": Sequence[
            AwsS3BucketBucketLifecycleConfigurationRulesTransitionsDetailsTypeDef
        ],
    },
    total=False,
)

AwsS3BucketNotificationConfigurationPaginatorTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationPaginatorTypeDef",
    {
        "Configurations": List[AwsS3BucketNotificationConfigurationDetailPaginatorTypeDef],
    },
    total=False,
)

AwsS3BucketNotificationConfigurationTypeDef = TypedDict(
    "AwsS3BucketNotificationConfigurationTypeDef",
    {
        "Configurations": Sequence[AwsS3BucketNotificationConfigurationDetailTypeDef],
    },
    total=False,
)

AwsWafv2RulesDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2RulesDetailsPaginatorTypeDef",
    {
        "Action": AwsWafv2RulesActionDetailsPaginatorTypeDef,
        "Name": str,
        "OverrideAction": str,
        "Priority": int,
        "VisibilityConfig": AwsWafv2VisibilityConfigDetailsTypeDef,
    },
    total=False,
)

AwsWafv2RulesDetailsTypeDef = TypedDict(
    "AwsWafv2RulesDetailsTypeDef",
    {
        "Action": AwsWafv2RulesActionDetailsTypeDef,
        "Name": str,
        "OverrideAction": str,
        "Priority": int,
        "VisibilityConfig": AwsWafv2VisibilityConfigDetailsTypeDef,
    },
    total=False,
)

BatchGetAutomationRulesResponseTypeDef = TypedDict(
    "BatchGetAutomationRulesResponseTypeDef",
    {
        "Rules": List[AutomationRulesConfigTypeDef],
        "UnprocessedAutomationRules": List[UnprocessedAutomationRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateAutomationRulesRequestRequestTypeDef = TypedDict(
    "BatchUpdateAutomationRulesRequestRequestTypeDef",
    {
        "UpdateAutomationRulesRequestItems": Sequence[UpdateAutomationRulesRequestItemTypeDef],
    },
)

GetInsightsResponseTypeDef = TypedDict(
    "GetInsightsResponseTypeDef",
    {
        "Insights": List[InsightTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CustomDataIdentifiersResultPaginatorTypeDef = TypedDict(
    "CustomDataIdentifiersResultPaginatorTypeDef",
    {
        "Detections": List[CustomDataIdentifiersDetectionsPaginatorTypeDef],
        "TotalCount": int,
    },
    total=False,
)

SensitiveDataResultPaginatorTypeDef = TypedDict(
    "SensitiveDataResultPaginatorTypeDef",
    {
        "Category": str,
        "Detections": List[SensitiveDataDetectionsPaginatorTypeDef],
        "TotalCount": int,
    },
    total=False,
)

CustomDataIdentifiersResultTypeDef = TypedDict(
    "CustomDataIdentifiersResultTypeDef",
    {
        "Detections": Sequence[CustomDataIdentifiersDetectionsTypeDef],
        "TotalCount": int,
    },
    total=False,
)

SensitiveDataResultTypeDef = TypedDict(
    "SensitiveDataResultTypeDef",
    {
        "Category": str,
        "Detections": Sequence[SensitiveDataDetectionsTypeDef],
        "TotalCount": int,
    },
    total=False,
)

FirewallPolicyDetailsPaginatorTypeDef = TypedDict(
    "FirewallPolicyDetailsPaginatorTypeDef",
    {
        "StatefulRuleGroupReferences": List[
            FirewallPolicyStatefulRuleGroupReferencesDetailsTypeDef
        ],
        "StatelessCustomActions": List[FirewallPolicyStatelessCustomActionsDetailsPaginatorTypeDef],
        "StatelessDefaultActions": List[str],
        "StatelessFragmentDefaultActions": List[str],
        "StatelessRuleGroupReferences": List[
            FirewallPolicyStatelessRuleGroupReferencesDetailsTypeDef
        ],
    },
    total=False,
)

RuleGroupSourceStatelessRulesAndCustomActionsDetailsPaginatorTypeDef = TypedDict(
    "RuleGroupSourceStatelessRulesAndCustomActionsDetailsPaginatorTypeDef",
    {
        "CustomActions": List[RuleGroupSourceCustomActionsDetailsPaginatorTypeDef],
        "StatelessRules": List[RuleGroupSourceStatelessRulesDetailsPaginatorTypeDef],
    },
    total=False,
)

FirewallPolicyDetailsTypeDef = TypedDict(
    "FirewallPolicyDetailsTypeDef",
    {
        "StatefulRuleGroupReferences": Sequence[
            FirewallPolicyStatefulRuleGroupReferencesDetailsTypeDef
        ],
        "StatelessCustomActions": Sequence[FirewallPolicyStatelessCustomActionsDetailsTypeDef],
        "StatelessDefaultActions": Sequence[str],
        "StatelessFragmentDefaultActions": Sequence[str],
        "StatelessRuleGroupReferences": Sequence[
            FirewallPolicyStatelessRuleGroupReferencesDetailsTypeDef
        ],
    },
    total=False,
)

RuleGroupSourceStatelessRulesAndCustomActionsDetailsTypeDef = TypedDict(
    "RuleGroupSourceStatelessRulesAndCustomActionsDetailsTypeDef",
    {
        "CustomActions": Sequence[RuleGroupSourceCustomActionsDetailsTypeDef],
        "StatelessRules": Sequence[RuleGroupSourceStatelessRulesDetailsTypeDef],
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationDetailsPaginatorTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationDetailsPaginatorTypeDef",
    {
        "Rules": List[AwsS3BucketBucketLifecycleConfigurationRulesDetailsPaginatorTypeDef],
    },
    total=False,
)

AwsS3BucketBucketLifecycleConfigurationDetailsTypeDef = TypedDict(
    "AwsS3BucketBucketLifecycleConfigurationDetailsTypeDef",
    {
        "Rules": Sequence[AwsS3BucketBucketLifecycleConfigurationRulesDetailsTypeDef],
    },
    total=False,
)

AwsWafv2RuleGroupDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2RuleGroupDetailsPaginatorTypeDef",
    {
        "Capacity": int,
        "Description": str,
        "Id": str,
        "Name": str,
        "Arn": str,
        "Rules": List[AwsWafv2RulesDetailsPaginatorTypeDef],
        "Scope": str,
        "VisibilityConfig": AwsWafv2VisibilityConfigDetailsTypeDef,
    },
    total=False,
)

AwsWafv2WebAclDetailsPaginatorTypeDef = TypedDict(
    "AwsWafv2WebAclDetailsPaginatorTypeDef",
    {
        "Name": str,
        "Arn": str,
        "ManagedbyFirewallManager": bool,
        "Id": str,
        "Capacity": int,
        "CaptchaConfig": AwsWafv2WebAclCaptchaConfigDetailsTypeDef,
        "DefaultAction": AwsWafv2WebAclActionDetailsPaginatorTypeDef,
        "Description": str,
        "Rules": List[AwsWafv2RulesDetailsPaginatorTypeDef],
        "VisibilityConfig": AwsWafv2VisibilityConfigDetailsTypeDef,
    },
    total=False,
)

AwsWafv2RuleGroupDetailsTypeDef = TypedDict(
    "AwsWafv2RuleGroupDetailsTypeDef",
    {
        "Capacity": int,
        "Description": str,
        "Id": str,
        "Name": str,
        "Arn": str,
        "Rules": Sequence[AwsWafv2RulesDetailsTypeDef],
        "Scope": str,
        "VisibilityConfig": AwsWafv2VisibilityConfigDetailsTypeDef,
    },
    total=False,
)

AwsWafv2WebAclDetailsTypeDef = TypedDict(
    "AwsWafv2WebAclDetailsTypeDef",
    {
        "Name": str,
        "Arn": str,
        "ManagedbyFirewallManager": bool,
        "Id": str,
        "Capacity": int,
        "CaptchaConfig": AwsWafv2WebAclCaptchaConfigDetailsTypeDef,
        "DefaultAction": AwsWafv2WebAclActionDetailsTypeDef,
        "Description": str,
        "Rules": Sequence[AwsWafv2RulesDetailsTypeDef],
        "VisibilityConfig": AwsWafv2VisibilityConfigDetailsTypeDef,
    },
    total=False,
)

ClassificationResultPaginatorTypeDef = TypedDict(
    "ClassificationResultPaginatorTypeDef",
    {
        "MimeType": str,
        "SizeClassified": int,
        "AdditionalOccurrences": bool,
        "Status": ClassificationStatusTypeDef,
        "SensitiveData": List[SensitiveDataResultPaginatorTypeDef],
        "CustomDataIdentifiers": CustomDataIdentifiersResultPaginatorTypeDef,
    },
    total=False,
)

ClassificationResultTypeDef = TypedDict(
    "ClassificationResultTypeDef",
    {
        "MimeType": str,
        "SizeClassified": int,
        "AdditionalOccurrences": bool,
        "Status": ClassificationStatusTypeDef,
        "SensitiveData": Sequence[SensitiveDataResultTypeDef],
        "CustomDataIdentifiers": CustomDataIdentifiersResultTypeDef,
    },
    total=False,
)

AwsNetworkFirewallFirewallPolicyDetailsPaginatorTypeDef = TypedDict(
    "AwsNetworkFirewallFirewallPolicyDetailsPaginatorTypeDef",
    {
        "FirewallPolicy": FirewallPolicyDetailsPaginatorTypeDef,
        "FirewallPolicyArn": str,
        "FirewallPolicyId": str,
        "FirewallPolicyName": str,
        "Description": str,
    },
    total=False,
)

RuleGroupSourcePaginatorTypeDef = TypedDict(
    "RuleGroupSourcePaginatorTypeDef",
    {
        "RulesSourceList": RuleGroupSourceListDetailsPaginatorTypeDef,
        "RulesString": str,
        "StatefulRules": List[RuleGroupSourceStatefulRulesDetailsPaginatorTypeDef],
        "StatelessRulesAndCustomActions": (
            RuleGroupSourceStatelessRulesAndCustomActionsDetailsPaginatorTypeDef
        ),
    },
    total=False,
)

AwsNetworkFirewallFirewallPolicyDetailsTypeDef = TypedDict(
    "AwsNetworkFirewallFirewallPolicyDetailsTypeDef",
    {
        "FirewallPolicy": FirewallPolicyDetailsTypeDef,
        "FirewallPolicyArn": str,
        "FirewallPolicyId": str,
        "FirewallPolicyName": str,
        "Description": str,
    },
    total=False,
)

RuleGroupSourceTypeDef = TypedDict(
    "RuleGroupSourceTypeDef",
    {
        "RulesSourceList": RuleGroupSourceListDetailsTypeDef,
        "RulesString": str,
        "StatefulRules": Sequence[RuleGroupSourceStatefulRulesDetailsTypeDef],
        "StatelessRulesAndCustomActions": (
            RuleGroupSourceStatelessRulesAndCustomActionsDetailsTypeDef
        ),
    },
    total=False,
)

AwsS3BucketDetailsPaginatorTypeDef = TypedDict(
    "AwsS3BucketDetailsPaginatorTypeDef",
    {
        "OwnerId": str,
        "OwnerName": str,
        "OwnerAccountId": str,
        "CreatedAt": str,
        "ServerSideEncryptionConfiguration": (
            AwsS3BucketServerSideEncryptionConfigurationPaginatorTypeDef
        ),
        "BucketLifecycleConfiguration": (
            AwsS3BucketBucketLifecycleConfigurationDetailsPaginatorTypeDef
        ),
        "PublicAccessBlockConfiguration": AwsS3AccountPublicAccessBlockDetailsTypeDef,
        "AccessControlList": str,
        "BucketLoggingConfiguration": AwsS3BucketLoggingConfigurationTypeDef,
        "BucketWebsiteConfiguration": AwsS3BucketWebsiteConfigurationPaginatorTypeDef,
        "BucketNotificationConfiguration": AwsS3BucketNotificationConfigurationPaginatorTypeDef,
        "BucketVersioningConfiguration": AwsS3BucketBucketVersioningConfigurationTypeDef,
        "ObjectLockConfiguration": AwsS3BucketObjectLockConfigurationTypeDef,
    },
    total=False,
)

AwsS3BucketDetailsTypeDef = TypedDict(
    "AwsS3BucketDetailsTypeDef",
    {
        "OwnerId": str,
        "OwnerName": str,
        "OwnerAccountId": str,
        "CreatedAt": str,
        "ServerSideEncryptionConfiguration": AwsS3BucketServerSideEncryptionConfigurationTypeDef,
        "BucketLifecycleConfiguration": AwsS3BucketBucketLifecycleConfigurationDetailsTypeDef,
        "PublicAccessBlockConfiguration": AwsS3AccountPublicAccessBlockDetailsTypeDef,
        "AccessControlList": str,
        "BucketLoggingConfiguration": AwsS3BucketLoggingConfigurationTypeDef,
        "BucketWebsiteConfiguration": AwsS3BucketWebsiteConfigurationTypeDef,
        "BucketNotificationConfiguration": AwsS3BucketNotificationConfigurationTypeDef,
        "BucketVersioningConfiguration": AwsS3BucketBucketVersioningConfigurationTypeDef,
        "ObjectLockConfiguration": AwsS3BucketObjectLockConfigurationTypeDef,
    },
    total=False,
)

DataClassificationDetailsPaginatorTypeDef = TypedDict(
    "DataClassificationDetailsPaginatorTypeDef",
    {
        "DetailedResultsLocation": str,
        "Result": ClassificationResultPaginatorTypeDef,
    },
    total=False,
)

DataClassificationDetailsTypeDef = TypedDict(
    "DataClassificationDetailsTypeDef",
    {
        "DetailedResultsLocation": str,
        "Result": ClassificationResultTypeDef,
    },
    total=False,
)

RuleGroupDetailsPaginatorTypeDef = TypedDict(
    "RuleGroupDetailsPaginatorTypeDef",
    {
        "RuleVariables": RuleGroupVariablesPaginatorTypeDef,
        "RulesSource": RuleGroupSourcePaginatorTypeDef,
    },
    total=False,
)

RuleGroupDetailsTypeDef = TypedDict(
    "RuleGroupDetailsTypeDef",
    {
        "RuleVariables": RuleGroupVariablesTypeDef,
        "RulesSource": RuleGroupSourceTypeDef,
    },
    total=False,
)

AwsNetworkFirewallRuleGroupDetailsPaginatorTypeDef = TypedDict(
    "AwsNetworkFirewallRuleGroupDetailsPaginatorTypeDef",
    {
        "Capacity": int,
        "Description": str,
        "RuleGroup": RuleGroupDetailsPaginatorTypeDef,
        "RuleGroupArn": str,
        "RuleGroupId": str,
        "RuleGroupName": str,
        "Type": str,
    },
    total=False,
)

AwsNetworkFirewallRuleGroupDetailsTypeDef = TypedDict(
    "AwsNetworkFirewallRuleGroupDetailsTypeDef",
    {
        "Capacity": int,
        "Description": str,
        "RuleGroup": RuleGroupDetailsTypeDef,
        "RuleGroupArn": str,
        "RuleGroupId": str,
        "RuleGroupName": str,
        "Type": str,
    },
    total=False,
)

ResourceDetailsPaginatorTypeDef = TypedDict(
    "ResourceDetailsPaginatorTypeDef",
    {
        "AwsAutoScalingAutoScalingGroup": AwsAutoScalingAutoScalingGroupDetailsPaginatorTypeDef,
        "AwsCodeBuildProject": AwsCodeBuildProjectDetailsPaginatorTypeDef,
        "AwsCloudFrontDistribution": AwsCloudFrontDistributionDetailsPaginatorTypeDef,
        "AwsEc2Instance": AwsEc2InstanceDetailsPaginatorTypeDef,
        "AwsEc2NetworkInterface": AwsEc2NetworkInterfaceDetailsPaginatorTypeDef,
        "AwsEc2SecurityGroup": AwsEc2SecurityGroupDetailsPaginatorTypeDef,
        "AwsEc2Volume": AwsEc2VolumeDetailsPaginatorTypeDef,
        "AwsEc2Vpc": AwsEc2VpcDetailsPaginatorTypeDef,
        "AwsEc2Eip": AwsEc2EipDetailsTypeDef,
        "AwsEc2Subnet": AwsEc2SubnetDetailsPaginatorTypeDef,
        "AwsEc2NetworkAcl": AwsEc2NetworkAclDetailsPaginatorTypeDef,
        "AwsElbv2LoadBalancer": AwsElbv2LoadBalancerDetailsPaginatorTypeDef,
        "AwsElasticBeanstalkEnvironment": AwsElasticBeanstalkEnvironmentDetailsPaginatorTypeDef,
        "AwsElasticsearchDomain": AwsElasticsearchDomainDetailsPaginatorTypeDef,
        "AwsS3Bucket": AwsS3BucketDetailsPaginatorTypeDef,
        "AwsS3AccountPublicAccessBlock": AwsS3AccountPublicAccessBlockDetailsTypeDef,
        "AwsS3Object": AwsS3ObjectDetailsTypeDef,
        "AwsSecretsManagerSecret": AwsSecretsManagerSecretDetailsTypeDef,
        "AwsIamAccessKey": AwsIamAccessKeyDetailsTypeDef,
        "AwsIamUser": AwsIamUserDetailsPaginatorTypeDef,
        "AwsIamPolicy": AwsIamPolicyDetailsPaginatorTypeDef,
        "AwsApiGatewayV2Stage": AwsApiGatewayV2StageDetailsPaginatorTypeDef,
        "AwsApiGatewayV2Api": AwsApiGatewayV2ApiDetailsPaginatorTypeDef,
        "AwsDynamoDbTable": AwsDynamoDbTableDetailsPaginatorTypeDef,
        "AwsApiGatewayStage": AwsApiGatewayStageDetailsPaginatorTypeDef,
        "AwsApiGatewayRestApi": AwsApiGatewayRestApiDetailsPaginatorTypeDef,
        "AwsCloudTrailTrail": AwsCloudTrailTrailDetailsTypeDef,
        "AwsSsmPatchCompliance": AwsSsmPatchComplianceDetailsTypeDef,
        "AwsCertificateManagerCertificate": AwsCertificateManagerCertificateDetailsPaginatorTypeDef,
        "AwsRedshiftCluster": AwsRedshiftClusterDetailsPaginatorTypeDef,
        "AwsElbLoadBalancer": AwsElbLoadBalancerDetailsPaginatorTypeDef,
        "AwsIamGroup": AwsIamGroupDetailsPaginatorTypeDef,
        "AwsIamRole": AwsIamRoleDetailsPaginatorTypeDef,
        "AwsKmsKey": AwsKmsKeyDetailsTypeDef,
        "AwsLambdaFunction": AwsLambdaFunctionDetailsPaginatorTypeDef,
        "AwsLambdaLayerVersion": AwsLambdaLayerVersionDetailsPaginatorTypeDef,
        "AwsRdsDbInstance": AwsRdsDbInstanceDetailsPaginatorTypeDef,
        "AwsSnsTopic": AwsSnsTopicDetailsPaginatorTypeDef,
        "AwsSqsQueue": AwsSqsQueueDetailsTypeDef,
        "AwsWafWebAcl": AwsWafWebAclDetailsPaginatorTypeDef,
        "AwsRdsDbSnapshot": AwsRdsDbSnapshotDetailsPaginatorTypeDef,
        "AwsRdsDbClusterSnapshot": AwsRdsDbClusterSnapshotDetailsPaginatorTypeDef,
        "AwsRdsDbCluster": AwsRdsDbClusterDetailsPaginatorTypeDef,
        "AwsEcsCluster": AwsEcsClusterDetailsPaginatorTypeDef,
        "AwsEcsContainer": AwsEcsContainerDetailsPaginatorTypeDef,
        "AwsEcsTaskDefinition": AwsEcsTaskDefinitionDetailsPaginatorTypeDef,
        "Container": ContainerDetailsPaginatorTypeDef,
        "Other": Dict[str, str],
        "AwsRdsEventSubscription": AwsRdsEventSubscriptionDetailsPaginatorTypeDef,
        "AwsEcsService": AwsEcsServiceDetailsPaginatorTypeDef,
        "AwsAutoScalingLaunchConfiguration": (
            AwsAutoScalingLaunchConfigurationDetailsPaginatorTypeDef
        ),
        "AwsEc2VpnConnection": AwsEc2VpnConnectionDetailsPaginatorTypeDef,
        "AwsEcrContainerImage": AwsEcrContainerImageDetailsPaginatorTypeDef,
        "AwsOpenSearchServiceDomain": AwsOpenSearchServiceDomainDetailsPaginatorTypeDef,
        "AwsEc2VpcEndpointService": AwsEc2VpcEndpointServiceDetailsPaginatorTypeDef,
        "AwsXrayEncryptionConfig": AwsXrayEncryptionConfigDetailsTypeDef,
        "AwsWafRateBasedRule": AwsWafRateBasedRuleDetailsPaginatorTypeDef,
        "AwsWafRegionalRateBasedRule": AwsWafRegionalRateBasedRuleDetailsPaginatorTypeDef,
        "AwsEcrRepository": AwsEcrRepositoryDetailsTypeDef,
        "AwsEksCluster": AwsEksClusterDetailsPaginatorTypeDef,
        "AwsNetworkFirewallFirewallPolicy": AwsNetworkFirewallFirewallPolicyDetailsPaginatorTypeDef,
        "AwsNetworkFirewallFirewall": AwsNetworkFirewallFirewallDetailsPaginatorTypeDef,
        "AwsNetworkFirewallRuleGroup": AwsNetworkFirewallRuleGroupDetailsPaginatorTypeDef,
        "AwsRdsDbSecurityGroup": AwsRdsDbSecurityGroupDetailsPaginatorTypeDef,
        "AwsKinesisStream": AwsKinesisStreamDetailsTypeDef,
        "AwsEc2TransitGateway": AwsEc2TransitGatewayDetailsPaginatorTypeDef,
        "AwsEfsAccessPoint": AwsEfsAccessPointDetailsPaginatorTypeDef,
        "AwsCloudFormationStack": AwsCloudFormationStackDetailsPaginatorTypeDef,
        "AwsCloudWatchAlarm": AwsCloudWatchAlarmDetailsPaginatorTypeDef,
        "AwsEc2VpcPeeringConnection": AwsEc2VpcPeeringConnectionDetailsPaginatorTypeDef,
        "AwsWafRegionalRuleGroup": AwsWafRegionalRuleGroupDetailsPaginatorTypeDef,
        "AwsWafRegionalRule": AwsWafRegionalRuleDetailsPaginatorTypeDef,
        "AwsWafRegionalWebAcl": AwsWafRegionalWebAclDetailsPaginatorTypeDef,
        "AwsWafRule": AwsWafRuleDetailsPaginatorTypeDef,
        "AwsWafRuleGroup": AwsWafRuleGroupDetailsPaginatorTypeDef,
        "AwsEcsTask": AwsEcsTaskDetailsPaginatorTypeDef,
        "AwsBackupBackupVault": AwsBackupBackupVaultDetailsPaginatorTypeDef,
        "AwsBackupBackupPlan": AwsBackupBackupPlanDetailsPaginatorTypeDef,
        "AwsBackupRecoveryPoint": AwsBackupRecoveryPointDetailsTypeDef,
        "AwsEc2LaunchTemplate": AwsEc2LaunchTemplateDetailsPaginatorTypeDef,
        "AwsSageMakerNotebookInstance": AwsSageMakerNotebookInstanceDetailsPaginatorTypeDef,
        "AwsWafv2WebAcl": AwsWafv2WebAclDetailsPaginatorTypeDef,
        "AwsWafv2RuleGroup": AwsWafv2RuleGroupDetailsPaginatorTypeDef,
        "AwsEc2RouteTable": AwsEc2RouteTableDetailsPaginatorTypeDef,
        "AwsAmazonMqBroker": AwsAmazonMqBrokerDetailsPaginatorTypeDef,
        "AwsAppSyncGraphQlApi": AwsAppSyncGraphQlApiDetailsPaginatorTypeDef,
        "AwsEventSchemasRegistry": AwsEventSchemasRegistryDetailsTypeDef,
        "AwsGuardDutyDetector": AwsGuardDutyDetectorDetailsPaginatorTypeDef,
        "AwsStepFunctionStateMachine": AwsStepFunctionStateMachineDetailsPaginatorTypeDef,
        "AwsAthenaWorkGroup": AwsAthenaWorkGroupDetailsTypeDef,
    },
    total=False,
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "AwsAutoScalingAutoScalingGroup": AwsAutoScalingAutoScalingGroupDetailsTypeDef,
        "AwsCodeBuildProject": AwsCodeBuildProjectDetailsTypeDef,
        "AwsCloudFrontDistribution": AwsCloudFrontDistributionDetailsTypeDef,
        "AwsEc2Instance": AwsEc2InstanceDetailsTypeDef,
        "AwsEc2NetworkInterface": AwsEc2NetworkInterfaceDetailsTypeDef,
        "AwsEc2SecurityGroup": AwsEc2SecurityGroupDetailsTypeDef,
        "AwsEc2Volume": AwsEc2VolumeDetailsTypeDef,
        "AwsEc2Vpc": AwsEc2VpcDetailsTypeDef,
        "AwsEc2Eip": AwsEc2EipDetailsTypeDef,
        "AwsEc2Subnet": AwsEc2SubnetDetailsTypeDef,
        "AwsEc2NetworkAcl": AwsEc2NetworkAclDetailsTypeDef,
        "AwsElbv2LoadBalancer": AwsElbv2LoadBalancerDetailsTypeDef,
        "AwsElasticBeanstalkEnvironment": AwsElasticBeanstalkEnvironmentDetailsTypeDef,
        "AwsElasticsearchDomain": AwsElasticsearchDomainDetailsTypeDef,
        "AwsS3Bucket": AwsS3BucketDetailsTypeDef,
        "AwsS3AccountPublicAccessBlock": AwsS3AccountPublicAccessBlockDetailsTypeDef,
        "AwsS3Object": AwsS3ObjectDetailsTypeDef,
        "AwsSecretsManagerSecret": AwsSecretsManagerSecretDetailsTypeDef,
        "AwsIamAccessKey": AwsIamAccessKeyDetailsTypeDef,
        "AwsIamUser": AwsIamUserDetailsTypeDef,
        "AwsIamPolicy": AwsIamPolicyDetailsTypeDef,
        "AwsApiGatewayV2Stage": AwsApiGatewayV2StageDetailsTypeDef,
        "AwsApiGatewayV2Api": AwsApiGatewayV2ApiDetailsTypeDef,
        "AwsDynamoDbTable": AwsDynamoDbTableDetailsTypeDef,
        "AwsApiGatewayStage": AwsApiGatewayStageDetailsTypeDef,
        "AwsApiGatewayRestApi": AwsApiGatewayRestApiDetailsTypeDef,
        "AwsCloudTrailTrail": AwsCloudTrailTrailDetailsTypeDef,
        "AwsSsmPatchCompliance": AwsSsmPatchComplianceDetailsTypeDef,
        "AwsCertificateManagerCertificate": AwsCertificateManagerCertificateDetailsTypeDef,
        "AwsRedshiftCluster": AwsRedshiftClusterDetailsTypeDef,
        "AwsElbLoadBalancer": AwsElbLoadBalancerDetailsTypeDef,
        "AwsIamGroup": AwsIamGroupDetailsTypeDef,
        "AwsIamRole": AwsIamRoleDetailsTypeDef,
        "AwsKmsKey": AwsKmsKeyDetailsTypeDef,
        "AwsLambdaFunction": AwsLambdaFunctionDetailsTypeDef,
        "AwsLambdaLayerVersion": AwsLambdaLayerVersionDetailsTypeDef,
        "AwsRdsDbInstance": AwsRdsDbInstanceDetailsTypeDef,
        "AwsSnsTopic": AwsSnsTopicDetailsTypeDef,
        "AwsSqsQueue": AwsSqsQueueDetailsTypeDef,
        "AwsWafWebAcl": AwsWafWebAclDetailsTypeDef,
        "AwsRdsDbSnapshot": AwsRdsDbSnapshotDetailsTypeDef,
        "AwsRdsDbClusterSnapshot": AwsRdsDbClusterSnapshotDetailsTypeDef,
        "AwsRdsDbCluster": AwsRdsDbClusterDetailsTypeDef,
        "AwsEcsCluster": AwsEcsClusterDetailsTypeDef,
        "AwsEcsContainer": AwsEcsContainerDetailsTypeDef,
        "AwsEcsTaskDefinition": AwsEcsTaskDefinitionDetailsTypeDef,
        "Container": ContainerDetailsTypeDef,
        "Other": Mapping[str, str],
        "AwsRdsEventSubscription": AwsRdsEventSubscriptionDetailsTypeDef,
        "AwsEcsService": AwsEcsServiceDetailsTypeDef,
        "AwsAutoScalingLaunchConfiguration": AwsAutoScalingLaunchConfigurationDetailsTypeDef,
        "AwsEc2VpnConnection": AwsEc2VpnConnectionDetailsTypeDef,
        "AwsEcrContainerImage": AwsEcrContainerImageDetailsTypeDef,
        "AwsOpenSearchServiceDomain": AwsOpenSearchServiceDomainDetailsTypeDef,
        "AwsEc2VpcEndpointService": AwsEc2VpcEndpointServiceDetailsTypeDef,
        "AwsXrayEncryptionConfig": AwsXrayEncryptionConfigDetailsTypeDef,
        "AwsWafRateBasedRule": AwsWafRateBasedRuleDetailsTypeDef,
        "AwsWafRegionalRateBasedRule": AwsWafRegionalRateBasedRuleDetailsTypeDef,
        "AwsEcrRepository": AwsEcrRepositoryDetailsTypeDef,
        "AwsEksCluster": AwsEksClusterDetailsTypeDef,
        "AwsNetworkFirewallFirewallPolicy": AwsNetworkFirewallFirewallPolicyDetailsTypeDef,
        "AwsNetworkFirewallFirewall": AwsNetworkFirewallFirewallDetailsTypeDef,
        "AwsNetworkFirewallRuleGroup": AwsNetworkFirewallRuleGroupDetailsTypeDef,
        "AwsRdsDbSecurityGroup": AwsRdsDbSecurityGroupDetailsTypeDef,
        "AwsKinesisStream": AwsKinesisStreamDetailsTypeDef,
        "AwsEc2TransitGateway": AwsEc2TransitGatewayDetailsTypeDef,
        "AwsEfsAccessPoint": AwsEfsAccessPointDetailsTypeDef,
        "AwsCloudFormationStack": AwsCloudFormationStackDetailsTypeDef,
        "AwsCloudWatchAlarm": AwsCloudWatchAlarmDetailsTypeDef,
        "AwsEc2VpcPeeringConnection": AwsEc2VpcPeeringConnectionDetailsTypeDef,
        "AwsWafRegionalRuleGroup": AwsWafRegionalRuleGroupDetailsTypeDef,
        "AwsWafRegionalRule": AwsWafRegionalRuleDetailsTypeDef,
        "AwsWafRegionalWebAcl": AwsWafRegionalWebAclDetailsTypeDef,
        "AwsWafRule": AwsWafRuleDetailsTypeDef,
        "AwsWafRuleGroup": AwsWafRuleGroupDetailsTypeDef,
        "AwsEcsTask": AwsEcsTaskDetailsTypeDef,
        "AwsBackupBackupVault": AwsBackupBackupVaultDetailsTypeDef,
        "AwsBackupBackupPlan": AwsBackupBackupPlanDetailsTypeDef,
        "AwsBackupRecoveryPoint": AwsBackupRecoveryPointDetailsTypeDef,
        "AwsEc2LaunchTemplate": AwsEc2LaunchTemplateDetailsTypeDef,
        "AwsSageMakerNotebookInstance": AwsSageMakerNotebookInstanceDetailsTypeDef,
        "AwsWafv2WebAcl": AwsWafv2WebAclDetailsTypeDef,
        "AwsWafv2RuleGroup": AwsWafv2RuleGroupDetailsTypeDef,
        "AwsEc2RouteTable": AwsEc2RouteTableDetailsTypeDef,
        "AwsAmazonMqBroker": AwsAmazonMqBrokerDetailsTypeDef,
        "AwsAppSyncGraphQlApi": AwsAppSyncGraphQlApiDetailsTypeDef,
        "AwsEventSchemasRegistry": AwsEventSchemasRegistryDetailsTypeDef,
        "AwsGuardDutyDetector": AwsGuardDutyDetectorDetailsTypeDef,
        "AwsStepFunctionStateMachine": AwsStepFunctionStateMachineDetailsTypeDef,
        "AwsAthenaWorkGroup": AwsAthenaWorkGroupDetailsTypeDef,
    },
    total=False,
)

_RequiredResourcePaginatorTypeDef = TypedDict(
    "_RequiredResourcePaginatorTypeDef",
    {
        "Type": str,
        "Id": str,
    },
)
_OptionalResourcePaginatorTypeDef = TypedDict(
    "_OptionalResourcePaginatorTypeDef",
    {
        "Partition": PartitionType,
        "Region": str,
        "ResourceRole": str,
        "Tags": Dict[str, str],
        "DataClassification": DataClassificationDetailsPaginatorTypeDef,
        "Details": ResourceDetailsPaginatorTypeDef,
    },
    total=False,
)


class ResourcePaginatorTypeDef(
    _RequiredResourcePaginatorTypeDef, _OptionalResourcePaginatorTypeDef
):
    pass


_RequiredResourceTypeDef = TypedDict(
    "_RequiredResourceTypeDef",
    {
        "Type": str,
        "Id": str,
    },
)
_OptionalResourceTypeDef = TypedDict(
    "_OptionalResourceTypeDef",
    {
        "Partition": PartitionType,
        "Region": str,
        "ResourceRole": str,
        "Tags": Mapping[str, str],
        "DataClassification": DataClassificationDetailsTypeDef,
        "Details": ResourceDetailsTypeDef,
    },
    total=False,
)


class ResourceTypeDef(_RequiredResourceTypeDef, _OptionalResourceTypeDef):
    pass


_RequiredAwsSecurityFindingPaginatorTypeDef = TypedDict(
    "_RequiredAwsSecurityFindingPaginatorTypeDef",
    {
        "SchemaVersion": str,
        "Id": str,
        "ProductArn": str,
        "GeneratorId": str,
        "AwsAccountId": str,
        "CreatedAt": str,
        "UpdatedAt": str,
        "Title": str,
        "Description": str,
        "Resources": List[ResourcePaginatorTypeDef],
    },
)
_OptionalAwsSecurityFindingPaginatorTypeDef = TypedDict(
    "_OptionalAwsSecurityFindingPaginatorTypeDef",
    {
        "ProductName": str,
        "CompanyName": str,
        "Region": str,
        "Types": List[str],
        "FirstObservedAt": str,
        "LastObservedAt": str,
        "Severity": SeverityTypeDef,
        "Confidence": int,
        "Criticality": int,
        "Remediation": RemediationTypeDef,
        "SourceUrl": str,
        "ProductFields": Dict[str, str],
        "UserDefinedFields": Dict[str, str],
        "Malware": List[MalwareTypeDef],
        "Network": NetworkTypeDef,
        "NetworkPath": List[NetworkPathComponentPaginatorTypeDef],
        "Process": ProcessDetailsTypeDef,
        "Threats": List[ThreatPaginatorTypeDef],
        "ThreatIntelIndicators": List[ThreatIntelIndicatorTypeDef],
        "Compliance": CompliancePaginatorTypeDef,
        "VerificationState": VerificationStateType,
        "WorkflowState": WorkflowStateType,
        "Workflow": WorkflowTypeDef,
        "RecordState": RecordStateType,
        "RelatedFindings": List[RelatedFindingTypeDef],
        "Note": NoteTypeDef,
        "Vulnerabilities": List[VulnerabilityPaginatorTypeDef],
        "PatchSummary": PatchSummaryTypeDef,
        "Action": ActionPaginatorTypeDef,
        "FindingProviderFields": FindingProviderFieldsPaginatorTypeDef,
        "Sample": bool,
        "GeneratorDetails": GeneratorDetailsPaginatorTypeDef,
    },
    total=False,
)


class AwsSecurityFindingPaginatorTypeDef(
    _RequiredAwsSecurityFindingPaginatorTypeDef, _OptionalAwsSecurityFindingPaginatorTypeDef
):
    pass


_RequiredAwsSecurityFindingTypeDef = TypedDict(
    "_RequiredAwsSecurityFindingTypeDef",
    {
        "SchemaVersion": str,
        "Id": str,
        "ProductArn": str,
        "GeneratorId": str,
        "AwsAccountId": str,
        "CreatedAt": str,
        "UpdatedAt": str,
        "Title": str,
        "Description": str,
        "Resources": Sequence[ResourceTypeDef],
    },
)
_OptionalAwsSecurityFindingTypeDef = TypedDict(
    "_OptionalAwsSecurityFindingTypeDef",
    {
        "ProductName": str,
        "CompanyName": str,
        "Region": str,
        "Types": Sequence[str],
        "FirstObservedAt": str,
        "LastObservedAt": str,
        "Severity": SeverityTypeDef,
        "Confidence": int,
        "Criticality": int,
        "Remediation": RemediationTypeDef,
        "SourceUrl": str,
        "ProductFields": Mapping[str, str],
        "UserDefinedFields": Mapping[str, str],
        "Malware": Sequence[MalwareTypeDef],
        "Network": NetworkTypeDef,
        "NetworkPath": Sequence[NetworkPathComponentTypeDef],
        "Process": ProcessDetailsTypeDef,
        "Threats": Sequence[ThreatTypeDef],
        "ThreatIntelIndicators": Sequence[ThreatIntelIndicatorTypeDef],
        "Compliance": ComplianceTypeDef,
        "VerificationState": VerificationStateType,
        "WorkflowState": WorkflowStateType,
        "Workflow": WorkflowTypeDef,
        "RecordState": RecordStateType,
        "RelatedFindings": Sequence[RelatedFindingTypeDef],
        "Note": NoteTypeDef,
        "Vulnerabilities": Sequence[VulnerabilityTypeDef],
        "PatchSummary": PatchSummaryTypeDef,
        "Action": ActionTypeDef,
        "FindingProviderFields": FindingProviderFieldsTypeDef,
        "Sample": bool,
        "GeneratorDetails": GeneratorDetailsTypeDef,
    },
    total=False,
)


class AwsSecurityFindingTypeDef(
    _RequiredAwsSecurityFindingTypeDef, _OptionalAwsSecurityFindingTypeDef
):
    pass


GetFindingsResponsePaginatorTypeDef = TypedDict(
    "GetFindingsResponsePaginatorTypeDef",
    {
        "Findings": List[AwsSecurityFindingPaginatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchImportFindingsRequestRequestTypeDef = TypedDict(
    "BatchImportFindingsRequestRequestTypeDef",
    {
        "Findings": Sequence[AwsSecurityFindingTypeDef],
    },
)

GetFindingsResponseTypeDef = TypedDict(
    "GetFindingsResponseTypeDef",
    {
        "Findings": List[AwsSecurityFindingTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
