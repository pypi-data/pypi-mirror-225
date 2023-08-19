"""
Type annotations for securityhub service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_securityhub.client import SecurityHubClient
    from mypy_boto3_securityhub.paginator import (
        DescribeActionTargetsPaginator,
        DescribeProductsPaginator,
        DescribeStandardsPaginator,
        DescribeStandardsControlsPaginator,
        GetEnabledStandardsPaginator,
        GetFindingHistoryPaginator,
        GetFindingsPaginator,
        GetInsightsPaginator,
        ListEnabledProductsForImportPaginator,
        ListFindingAggregatorsPaginator,
        ListInvitationsPaginator,
        ListMembersPaginator,
        ListOrganizationAdminAccountsPaginator,
        ListSecurityControlDefinitionsPaginator,
        ListStandardsControlAssociationsPaginator,
    )

    session = Session()
    client: SecurityHubClient = session.client("securityhub")

    describe_action_targets_paginator: DescribeActionTargetsPaginator = client.get_paginator("describe_action_targets")
    describe_products_paginator: DescribeProductsPaginator = client.get_paginator("describe_products")
    describe_standards_paginator: DescribeStandardsPaginator = client.get_paginator("describe_standards")
    describe_standards_controls_paginator: DescribeStandardsControlsPaginator = client.get_paginator("describe_standards_controls")
    get_enabled_standards_paginator: GetEnabledStandardsPaginator = client.get_paginator("get_enabled_standards")
    get_finding_history_paginator: GetFindingHistoryPaginator = client.get_paginator("get_finding_history")
    get_findings_paginator: GetFindingsPaginator = client.get_paginator("get_findings")
    get_insights_paginator: GetInsightsPaginator = client.get_paginator("get_insights")
    list_enabled_products_for_import_paginator: ListEnabledProductsForImportPaginator = client.get_paginator("list_enabled_products_for_import")
    list_finding_aggregators_paginator: ListFindingAggregatorsPaginator = client.get_paginator("list_finding_aggregators")
    list_invitations_paginator: ListInvitationsPaginator = client.get_paginator("list_invitations")
    list_members_paginator: ListMembersPaginator = client.get_paginator("list_members")
    list_organization_admin_accounts_paginator: ListOrganizationAdminAccountsPaginator = client.get_paginator("list_organization_admin_accounts")
    list_security_control_definitions_paginator: ListSecurityControlDefinitionsPaginator = client.get_paginator("list_security_control_definitions")
    list_standards_control_associations_paginator: ListStandardsControlAssociationsPaginator = client.get_paginator("list_standards_control_associations")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    AwsSecurityFindingFiltersTypeDef,
    AwsSecurityFindingIdentifierTypeDef,
    DescribeActionTargetsResponseTypeDef,
    DescribeProductsResponseTypeDef,
    DescribeStandardsControlsResponseTypeDef,
    DescribeStandardsResponseTypeDef,
    GetEnabledStandardsResponseTypeDef,
    GetFindingHistoryResponseTypeDef,
    GetFindingsResponsePaginatorTypeDef,
    GetInsightsResponseTypeDef,
    ListEnabledProductsForImportResponseTypeDef,
    ListFindingAggregatorsResponseTypeDef,
    ListInvitationsResponseTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListSecurityControlDefinitionsResponseTypeDef,
    ListStandardsControlAssociationsResponseTypeDef,
    PaginatorConfigTypeDef,
    SortCriterionTypeDef,
    TimestampTypeDef,
)

__all__ = (
    "DescribeActionTargetsPaginator",
    "DescribeProductsPaginator",
    "DescribeStandardsPaginator",
    "DescribeStandardsControlsPaginator",
    "GetEnabledStandardsPaginator",
    "GetFindingHistoryPaginator",
    "GetFindingsPaginator",
    "GetInsightsPaginator",
    "ListEnabledProductsForImportPaginator",
    "ListFindingAggregatorsPaginator",
    "ListInvitationsPaginator",
    "ListMembersPaginator",
    "ListOrganizationAdminAccountsPaginator",
    "ListSecurityControlDefinitionsPaginator",
    "ListStandardsControlAssociationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeActionTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.DescribeActionTargets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describeactiontargetspaginator)
    """

    def paginate(
        self,
        *,
        ActionTargetArns: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeActionTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.DescribeActionTargets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describeactiontargetspaginator)
        """

class DescribeProductsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.DescribeProducts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describeproductspaginator)
    """

    def paginate(
        self, *, ProductArn: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.DescribeProducts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describeproductspaginator)
        """

class DescribeStandardsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.DescribeStandards)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describestandardspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeStandardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.DescribeStandards.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describestandardspaginator)
        """

class DescribeStandardsControlsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.DescribeStandardsControls)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describestandardscontrolspaginator)
    """

    def paginate(
        self, *, StandardsSubscriptionArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeStandardsControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.DescribeStandardsControls.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#describestandardscontrolspaginator)
        """

class GetEnabledStandardsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.GetEnabledStandards)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getenabledstandardspaginator)
    """

    def paginate(
        self,
        *,
        StandardsSubscriptionArns: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetEnabledStandardsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.GetEnabledStandards.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getenabledstandardspaginator)
        """

class GetFindingHistoryPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.GetFindingHistory)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getfindinghistorypaginator)
    """

    def paginate(
        self,
        *,
        FindingIdentifier: AwsSecurityFindingIdentifierTypeDef,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetFindingHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.GetFindingHistory.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getfindinghistorypaginator)
        """

class GetFindingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.GetFindings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getfindingspaginator)
    """

    def paginate(
        self,
        *,
        Filters: AwsSecurityFindingFiltersTypeDef = ...,
        SortCriteria: Sequence[SortCriterionTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetFindingsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.GetFindings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getfindingspaginator)
        """

class GetInsightsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.GetInsights)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getinsightspaginator)
    """

    def paginate(
        self, *, InsightArns: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetInsightsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.GetInsights.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#getinsightspaginator)
        """

class ListEnabledProductsForImportPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListEnabledProductsForImport)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listenabledproductsforimportpaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListEnabledProductsForImportResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListEnabledProductsForImport.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listenabledproductsforimportpaginator)
        """

class ListFindingAggregatorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListFindingAggregators)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listfindingaggregatorspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListFindingAggregatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListFindingAggregators.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listfindingaggregatorspaginator)
        """

class ListInvitationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListInvitations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listinvitationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInvitationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListInvitations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listinvitationspaginator)
        """

class ListMembersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListMembers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listmemberspaginator)
    """

    def paginate(
        self, *, OnlyAssociated: bool = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListMembers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listmemberspaginator)
        """

class ListOrganizationAdminAccountsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListOrganizationAdminAccounts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listorganizationadminaccountspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListOrganizationAdminAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListOrganizationAdminAccounts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listorganizationadminaccountspaginator)
        """

class ListSecurityControlDefinitionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListSecurityControlDefinitions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listsecuritycontroldefinitionspaginator)
    """

    def paginate(
        self, *, StandardsArn: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSecurityControlDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListSecurityControlDefinitions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#listsecuritycontroldefinitionspaginator)
        """

class ListStandardsControlAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListStandardsControlAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#liststandardscontrolassociationspaginator)
    """

    def paginate(
        self, *, SecurityControlId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListStandardsControlAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityhub.html#SecurityHub.Paginator.ListStandardsControlAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityhub/paginators/#liststandardscontrolassociationspaginator)
        """
