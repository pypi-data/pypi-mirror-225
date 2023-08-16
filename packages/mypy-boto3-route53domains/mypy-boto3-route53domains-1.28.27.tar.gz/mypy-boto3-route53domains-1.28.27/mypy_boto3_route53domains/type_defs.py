"""
Type annotations for route53domains service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53domains/type_defs/)

Usage::

    ```python
    from mypy_boto3_route53domains.type_defs import AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef

    data: AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ContactTypeType,
    CountryCodeType,
    DomainAvailabilityType,
    ExtraParamNameType,
    ListDomainsAttributeNameType,
    OperationStatusType,
    OperationTypeType,
    OperatorType,
    ReachabilityStatusType,
    SortOrderType,
    StatusFlagType,
    TransferableType,
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
    "AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DnssecSigningAttributesTypeDef",
    "BillingRecordTypeDef",
    "CancelDomainTransferToAnotherAwsAccountRequestRequestTypeDef",
    "CheckDomainAvailabilityRequestRequestTypeDef",
    "CheckDomainTransferabilityRequestRequestTypeDef",
    "DomainTransferabilityTypeDef",
    "ConsentTypeDef",
    "ExtraParamTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DeleteTagsForDomainRequestRequestTypeDef",
    "DisableDomainAutoRenewRequestRequestTypeDef",
    "DisableDomainTransferLockRequestRequestTypeDef",
    "DisassociateDelegationSignerFromDomainRequestRequestTypeDef",
    "DnssecKeyTypeDef",
    "PriceWithCurrencyTypeDef",
    "DomainSuggestionTypeDef",
    "DomainSummaryTypeDef",
    "EnableDomainAutoRenewRequestRequestTypeDef",
    "EnableDomainTransferLockRequestRequestTypeDef",
    "FilterConditionTypeDef",
    "GetContactReachabilityStatusRequestRequestTypeDef",
    "GetDomainDetailRequestRequestTypeDef",
    "NameserverTypeDef",
    "GetDomainSuggestionsRequestRequestTypeDef",
    "GetOperationDetailRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "SortConditionTypeDef",
    "TimestampTypeDef",
    "OperationSummaryTypeDef",
    "ListPricesRequestRequestTypeDef",
    "ListTagsForDomainRequestRequestTypeDef",
    "TagTypeDef",
    "PushDomainRequestRequestTypeDef",
    "RejectDomainTransferFromAnotherAwsAccountRequestRequestTypeDef",
    "RenewDomainRequestRequestTypeDef",
    "ResendContactReachabilityEmailRequestRequestTypeDef",
    "ResendOperationAuthorizationRequestRequestTypeDef",
    "RetrieveDomainAuthCodeRequestRequestTypeDef",
    "TransferDomainToAnotherAwsAccountRequestRequestTypeDef",
    "UpdateDomainContactPrivacyRequestRequestTypeDef",
    "AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef",
    "AssociateDelegationSignerToDomainResponseTypeDef",
    "CancelDomainTransferToAnotherAwsAccountResponseTypeDef",
    "CheckDomainAvailabilityResponseTypeDef",
    "DeleteDomainResponseTypeDef",
    "DisableDomainTransferLockResponseTypeDef",
    "DisassociateDelegationSignerFromDomainResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableDomainTransferLockResponseTypeDef",
    "GetContactReachabilityStatusResponseTypeDef",
    "GetOperationDetailResponseTypeDef",
    "RegisterDomainResponseTypeDef",
    "RejectDomainTransferFromAnotherAwsAccountResponseTypeDef",
    "RenewDomainResponseTypeDef",
    "ResendContactReachabilityEmailResponseTypeDef",
    "RetrieveDomainAuthCodeResponseTypeDef",
    "TransferDomainResponseTypeDef",
    "TransferDomainToAnotherAwsAccountResponseTypeDef",
    "UpdateDomainContactPrivacyResponseTypeDef",
    "UpdateDomainContactResponseTypeDef",
    "UpdateDomainNameserversResponseTypeDef",
    "AssociateDelegationSignerToDomainRequestRequestTypeDef",
    "ViewBillingResponseTypeDef",
    "CheckDomainTransferabilityResponseTypeDef",
    "ContactDetailTypeDef",
    "DomainPriceTypeDef",
    "GetDomainSuggestionsResponseTypeDef",
    "ListDomainsResponseTypeDef",
    "UpdateDomainNameserversRequestRequestTypeDef",
    "ListPricesRequestListPricesPaginateTypeDef",
    "ListDomainsRequestListDomainsPaginateTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListOperationsRequestListOperationsPaginateTypeDef",
    "ListOperationsRequestRequestTypeDef",
    "ViewBillingRequestRequestTypeDef",
    "ViewBillingRequestViewBillingPaginateTypeDef",
    "ListOperationsResponseTypeDef",
    "ListTagsForDomainResponseTypeDef",
    "UpdateTagsForDomainRequestRequestTypeDef",
    "GetDomainDetailResponseTypeDef",
    "RegisterDomainRequestRequestTypeDef",
    "TransferDomainRequestRequestTypeDef",
    "UpdateDomainContactRequestRequestTypeDef",
    "ListPricesResponseTypeDef",
)

AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef = TypedDict(
    "AcceptDomainTransferFromAnotherAwsAccountRequestRequestTypeDef",
    {
        "DomainName": str,
        "Password": str,
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

DnssecSigningAttributesTypeDef = TypedDict(
    "DnssecSigningAttributesTypeDef",
    {
        "Algorithm": int,
        "Flags": int,
        "PublicKey": str,
    },
    total=False,
)

BillingRecordTypeDef = TypedDict(
    "BillingRecordTypeDef",
    {
        "DomainName": str,
        "Operation": OperationTypeType,
        "InvoiceId": str,
        "BillDate": datetime,
        "Price": float,
    },
    total=False,
)

CancelDomainTransferToAnotherAwsAccountRequestRequestTypeDef = TypedDict(
    "CancelDomainTransferToAnotherAwsAccountRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

_RequiredCheckDomainAvailabilityRequestRequestTypeDef = TypedDict(
    "_RequiredCheckDomainAvailabilityRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalCheckDomainAvailabilityRequestRequestTypeDef = TypedDict(
    "_OptionalCheckDomainAvailabilityRequestRequestTypeDef",
    {
        "IdnLangCode": str,
    },
    total=False,
)


class CheckDomainAvailabilityRequestRequestTypeDef(
    _RequiredCheckDomainAvailabilityRequestRequestTypeDef,
    _OptionalCheckDomainAvailabilityRequestRequestTypeDef,
):
    pass


_RequiredCheckDomainTransferabilityRequestRequestTypeDef = TypedDict(
    "_RequiredCheckDomainTransferabilityRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalCheckDomainTransferabilityRequestRequestTypeDef = TypedDict(
    "_OptionalCheckDomainTransferabilityRequestRequestTypeDef",
    {
        "AuthCode": str,
    },
    total=False,
)


class CheckDomainTransferabilityRequestRequestTypeDef(
    _RequiredCheckDomainTransferabilityRequestRequestTypeDef,
    _OptionalCheckDomainTransferabilityRequestRequestTypeDef,
):
    pass


DomainTransferabilityTypeDef = TypedDict(
    "DomainTransferabilityTypeDef",
    {
        "Transferable": TransferableType,
    },
    total=False,
)

ConsentTypeDef = TypedDict(
    "ConsentTypeDef",
    {
        "MaxPrice": float,
        "Currency": str,
    },
)

ExtraParamTypeDef = TypedDict(
    "ExtraParamTypeDef",
    {
        "Name": ExtraParamNameType,
        "Value": str,
    },
)

DeleteDomainRequestRequestTypeDef = TypedDict(
    "DeleteDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

DeleteTagsForDomainRequestRequestTypeDef = TypedDict(
    "DeleteTagsForDomainRequestRequestTypeDef",
    {
        "DomainName": str,
        "TagsToDelete": Sequence[str],
    },
)

DisableDomainAutoRenewRequestRequestTypeDef = TypedDict(
    "DisableDomainAutoRenewRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

DisableDomainTransferLockRequestRequestTypeDef = TypedDict(
    "DisableDomainTransferLockRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

DisassociateDelegationSignerFromDomainRequestRequestTypeDef = TypedDict(
    "DisassociateDelegationSignerFromDomainRequestRequestTypeDef",
    {
        "DomainName": str,
        "Id": str,
    },
)

DnssecKeyTypeDef = TypedDict(
    "DnssecKeyTypeDef",
    {
        "Algorithm": int,
        "Flags": int,
        "PublicKey": str,
        "DigestType": int,
        "Digest": str,
        "KeyTag": int,
        "Id": str,
    },
    total=False,
)

PriceWithCurrencyTypeDef = TypedDict(
    "PriceWithCurrencyTypeDef",
    {
        "Price": float,
        "Currency": str,
    },
)

DomainSuggestionTypeDef = TypedDict(
    "DomainSuggestionTypeDef",
    {
        "DomainName": str,
        "Availability": str,
    },
    total=False,
)

DomainSummaryTypeDef = TypedDict(
    "DomainSummaryTypeDef",
    {
        "DomainName": str,
        "AutoRenew": bool,
        "TransferLock": bool,
        "Expiry": datetime,
    },
    total=False,
)

EnableDomainAutoRenewRequestRequestTypeDef = TypedDict(
    "EnableDomainAutoRenewRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

EnableDomainTransferLockRequestRequestTypeDef = TypedDict(
    "EnableDomainTransferLockRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

FilterConditionTypeDef = TypedDict(
    "FilterConditionTypeDef",
    {
        "Name": ListDomainsAttributeNameType,
        "Operator": OperatorType,
        "Values": Sequence[str],
    },
)

GetContactReachabilityStatusRequestRequestTypeDef = TypedDict(
    "GetContactReachabilityStatusRequestRequestTypeDef",
    {
        "domainName": str,
    },
    total=False,
)

GetDomainDetailRequestRequestTypeDef = TypedDict(
    "GetDomainDetailRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

_RequiredNameserverTypeDef = TypedDict(
    "_RequiredNameserverTypeDef",
    {
        "Name": str,
    },
)
_OptionalNameserverTypeDef = TypedDict(
    "_OptionalNameserverTypeDef",
    {
        "GlueIps": List[str],
    },
    total=False,
)


class NameserverTypeDef(_RequiredNameserverTypeDef, _OptionalNameserverTypeDef):
    pass


GetDomainSuggestionsRequestRequestTypeDef = TypedDict(
    "GetDomainSuggestionsRequestRequestTypeDef",
    {
        "DomainName": str,
        "SuggestionCount": int,
        "OnlyAvailable": bool,
    },
)

GetOperationDetailRequestRequestTypeDef = TypedDict(
    "GetOperationDetailRequestRequestTypeDef",
    {
        "OperationId": str,
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

SortConditionTypeDef = TypedDict(
    "SortConditionTypeDef",
    {
        "Name": ListDomainsAttributeNameType,
        "SortOrder": SortOrderType,
    },
)

TimestampTypeDef = Union[datetime, str]
OperationSummaryTypeDef = TypedDict(
    "OperationSummaryTypeDef",
    {
        "OperationId": str,
        "Status": OperationStatusType,
        "Type": OperationTypeType,
        "SubmittedDate": datetime,
        "DomainName": str,
        "Message": str,
        "StatusFlag": StatusFlagType,
        "LastUpdatedDate": datetime,
    },
    total=False,
)

ListPricesRequestRequestTypeDef = TypedDict(
    "ListPricesRequestRequestTypeDef",
    {
        "Tld": str,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

ListTagsForDomainRequestRequestTypeDef = TypedDict(
    "ListTagsForDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

PushDomainRequestRequestTypeDef = TypedDict(
    "PushDomainRequestRequestTypeDef",
    {
        "DomainName": str,
        "Target": str,
    },
)

RejectDomainTransferFromAnotherAwsAccountRequestRequestTypeDef = TypedDict(
    "RejectDomainTransferFromAnotherAwsAccountRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

_RequiredRenewDomainRequestRequestTypeDef = TypedDict(
    "_RequiredRenewDomainRequestRequestTypeDef",
    {
        "DomainName": str,
        "CurrentExpiryYear": int,
    },
)
_OptionalRenewDomainRequestRequestTypeDef = TypedDict(
    "_OptionalRenewDomainRequestRequestTypeDef",
    {
        "DurationInYears": int,
    },
    total=False,
)


class RenewDomainRequestRequestTypeDef(
    _RequiredRenewDomainRequestRequestTypeDef, _OptionalRenewDomainRequestRequestTypeDef
):
    pass


ResendContactReachabilityEmailRequestRequestTypeDef = TypedDict(
    "ResendContactReachabilityEmailRequestRequestTypeDef",
    {
        "domainName": str,
    },
    total=False,
)

ResendOperationAuthorizationRequestRequestTypeDef = TypedDict(
    "ResendOperationAuthorizationRequestRequestTypeDef",
    {
        "OperationId": str,
    },
)

RetrieveDomainAuthCodeRequestRequestTypeDef = TypedDict(
    "RetrieveDomainAuthCodeRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)

TransferDomainToAnotherAwsAccountRequestRequestTypeDef = TypedDict(
    "TransferDomainToAnotherAwsAccountRequestRequestTypeDef",
    {
        "DomainName": str,
        "AccountId": str,
    },
)

_RequiredUpdateDomainContactPrivacyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDomainContactPrivacyRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalUpdateDomainContactPrivacyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDomainContactPrivacyRequestRequestTypeDef",
    {
        "AdminPrivacy": bool,
        "RegistrantPrivacy": bool,
        "TechPrivacy": bool,
    },
    total=False,
)


class UpdateDomainContactPrivacyRequestRequestTypeDef(
    _RequiredUpdateDomainContactPrivacyRequestRequestTypeDef,
    _OptionalUpdateDomainContactPrivacyRequestRequestTypeDef,
):
    pass


AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef = TypedDict(
    "AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateDelegationSignerToDomainResponseTypeDef = TypedDict(
    "AssociateDelegationSignerToDomainResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelDomainTransferToAnotherAwsAccountResponseTypeDef = TypedDict(
    "CancelDomainTransferToAnotherAwsAccountResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CheckDomainAvailabilityResponseTypeDef = TypedDict(
    "CheckDomainAvailabilityResponseTypeDef",
    {
        "Availability": DomainAvailabilityType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDomainResponseTypeDef = TypedDict(
    "DeleteDomainResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisableDomainTransferLockResponseTypeDef = TypedDict(
    "DisableDomainTransferLockResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateDelegationSignerFromDomainResponseTypeDef = TypedDict(
    "DisassociateDelegationSignerFromDomainResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableDomainTransferLockResponseTypeDef = TypedDict(
    "EnableDomainTransferLockResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetContactReachabilityStatusResponseTypeDef = TypedDict(
    "GetContactReachabilityStatusResponseTypeDef",
    {
        "domainName": str,
        "status": ReachabilityStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetOperationDetailResponseTypeDef = TypedDict(
    "GetOperationDetailResponseTypeDef",
    {
        "OperationId": str,
        "Status": OperationStatusType,
        "Message": str,
        "DomainName": str,
        "Type": OperationTypeType,
        "SubmittedDate": datetime,
        "LastUpdatedDate": datetime,
        "StatusFlag": StatusFlagType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterDomainResponseTypeDef = TypedDict(
    "RegisterDomainResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RejectDomainTransferFromAnotherAwsAccountResponseTypeDef = TypedDict(
    "RejectDomainTransferFromAnotherAwsAccountResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RenewDomainResponseTypeDef = TypedDict(
    "RenewDomainResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ResendContactReachabilityEmailResponseTypeDef = TypedDict(
    "ResendContactReachabilityEmailResponseTypeDef",
    {
        "domainName": str,
        "emailAddress": str,
        "isAlreadyVerified": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RetrieveDomainAuthCodeResponseTypeDef = TypedDict(
    "RetrieveDomainAuthCodeResponseTypeDef",
    {
        "AuthCode": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TransferDomainResponseTypeDef = TypedDict(
    "TransferDomainResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TransferDomainToAnotherAwsAccountResponseTypeDef = TypedDict(
    "TransferDomainToAnotherAwsAccountResponseTypeDef",
    {
        "OperationId": str,
        "Password": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDomainContactPrivacyResponseTypeDef = TypedDict(
    "UpdateDomainContactPrivacyResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDomainContactResponseTypeDef = TypedDict(
    "UpdateDomainContactResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDomainNameserversResponseTypeDef = TypedDict(
    "UpdateDomainNameserversResponseTypeDef",
    {
        "OperationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateDelegationSignerToDomainRequestRequestTypeDef = TypedDict(
    "AssociateDelegationSignerToDomainRequestRequestTypeDef",
    {
        "DomainName": str,
        "SigningAttributes": DnssecSigningAttributesTypeDef,
    },
)

ViewBillingResponseTypeDef = TypedDict(
    "ViewBillingResponseTypeDef",
    {
        "NextPageMarker": str,
        "BillingRecords": List[BillingRecordTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CheckDomainTransferabilityResponseTypeDef = TypedDict(
    "CheckDomainTransferabilityResponseTypeDef",
    {
        "Transferability": DomainTransferabilityTypeDef,
        "Message": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ContactDetailTypeDef = TypedDict(
    "ContactDetailTypeDef",
    {
        "FirstName": str,
        "LastName": str,
        "ContactType": ContactTypeType,
        "OrganizationName": str,
        "AddressLine1": str,
        "AddressLine2": str,
        "City": str,
        "State": str,
        "CountryCode": CountryCodeType,
        "ZipCode": str,
        "PhoneNumber": str,
        "Email": str,
        "Fax": str,
        "ExtraParams": List[ExtraParamTypeDef],
    },
    total=False,
)

DomainPriceTypeDef = TypedDict(
    "DomainPriceTypeDef",
    {
        "Name": str,
        "RegistrationPrice": PriceWithCurrencyTypeDef,
        "TransferPrice": PriceWithCurrencyTypeDef,
        "RenewalPrice": PriceWithCurrencyTypeDef,
        "ChangeOwnershipPrice": PriceWithCurrencyTypeDef,
        "RestorationPrice": PriceWithCurrencyTypeDef,
    },
    total=False,
)

GetDomainSuggestionsResponseTypeDef = TypedDict(
    "GetDomainSuggestionsResponseTypeDef",
    {
        "SuggestionsList": List[DomainSuggestionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDomainsResponseTypeDef = TypedDict(
    "ListDomainsResponseTypeDef",
    {
        "Domains": List[DomainSummaryTypeDef],
        "NextPageMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateDomainNameserversRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDomainNameserversRequestRequestTypeDef",
    {
        "DomainName": str,
        "Nameservers": Sequence[NameserverTypeDef],
    },
)
_OptionalUpdateDomainNameserversRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDomainNameserversRequestRequestTypeDef",
    {
        "FIAuthKey": str,
    },
    total=False,
)


class UpdateDomainNameserversRequestRequestTypeDef(
    _RequiredUpdateDomainNameserversRequestRequestTypeDef,
    _OptionalUpdateDomainNameserversRequestRequestTypeDef,
):
    pass


ListPricesRequestListPricesPaginateTypeDef = TypedDict(
    "ListPricesRequestListPricesPaginateTypeDef",
    {
        "Tld": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDomainsRequestListDomainsPaginateTypeDef = TypedDict(
    "ListDomainsRequestListDomainsPaginateTypeDef",
    {
        "FilterConditions": Sequence[FilterConditionTypeDef],
        "SortCondition": SortConditionTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDomainsRequestRequestTypeDef = TypedDict(
    "ListDomainsRequestRequestTypeDef",
    {
        "FilterConditions": Sequence[FilterConditionTypeDef],
        "SortCondition": SortConditionTypeDef,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

ListOperationsRequestListOperationsPaginateTypeDef = TypedDict(
    "ListOperationsRequestListOperationsPaginateTypeDef",
    {
        "SubmittedSince": TimestampTypeDef,
        "Status": Sequence[OperationStatusType],
        "Type": Sequence[OperationTypeType],
        "SortBy": Literal["SubmittedDate"],
        "SortOrder": SortOrderType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOperationsRequestRequestTypeDef = TypedDict(
    "ListOperationsRequestRequestTypeDef",
    {
        "SubmittedSince": TimestampTypeDef,
        "Marker": str,
        "MaxItems": int,
        "Status": Sequence[OperationStatusType],
        "Type": Sequence[OperationTypeType],
        "SortBy": Literal["SubmittedDate"],
        "SortOrder": SortOrderType,
    },
    total=False,
)

ViewBillingRequestRequestTypeDef = TypedDict(
    "ViewBillingRequestRequestTypeDef",
    {
        "Start": TimestampTypeDef,
        "End": TimestampTypeDef,
        "Marker": str,
        "MaxItems": int,
    },
    total=False,
)

ViewBillingRequestViewBillingPaginateTypeDef = TypedDict(
    "ViewBillingRequestViewBillingPaginateTypeDef",
    {
        "Start": TimestampTypeDef,
        "End": TimestampTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListOperationsResponseTypeDef = TypedDict(
    "ListOperationsResponseTypeDef",
    {
        "Operations": List[OperationSummaryTypeDef],
        "NextPageMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForDomainResponseTypeDef = TypedDict(
    "ListTagsForDomainResponseTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateTagsForDomainRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTagsForDomainRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalUpdateTagsForDomainRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTagsForDomainRequestRequestTypeDef",
    {
        "TagsToUpdate": Sequence[TagTypeDef],
    },
    total=False,
)


class UpdateTagsForDomainRequestRequestTypeDef(
    _RequiredUpdateTagsForDomainRequestRequestTypeDef,
    _OptionalUpdateTagsForDomainRequestRequestTypeDef,
):
    pass


GetDomainDetailResponseTypeDef = TypedDict(
    "GetDomainDetailResponseTypeDef",
    {
        "DomainName": str,
        "Nameservers": List[NameserverTypeDef],
        "AutoRenew": bool,
        "AdminContact": ContactDetailTypeDef,
        "RegistrantContact": ContactDetailTypeDef,
        "TechContact": ContactDetailTypeDef,
        "AdminPrivacy": bool,
        "RegistrantPrivacy": bool,
        "TechPrivacy": bool,
        "RegistrarName": str,
        "WhoIsServer": str,
        "RegistrarUrl": str,
        "AbuseContactEmail": str,
        "AbuseContactPhone": str,
        "RegistryDomainId": str,
        "CreationDate": datetime,
        "UpdatedDate": datetime,
        "ExpirationDate": datetime,
        "Reseller": str,
        "DnsSec": str,
        "StatusList": List[str],
        "DnssecKeys": List[DnssecKeyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRegisterDomainRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterDomainRequestRequestTypeDef",
    {
        "DomainName": str,
        "DurationInYears": int,
        "AdminContact": ContactDetailTypeDef,
        "RegistrantContact": ContactDetailTypeDef,
        "TechContact": ContactDetailTypeDef,
    },
)
_OptionalRegisterDomainRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterDomainRequestRequestTypeDef",
    {
        "IdnLangCode": str,
        "AutoRenew": bool,
        "PrivacyProtectAdminContact": bool,
        "PrivacyProtectRegistrantContact": bool,
        "PrivacyProtectTechContact": bool,
    },
    total=False,
)


class RegisterDomainRequestRequestTypeDef(
    _RequiredRegisterDomainRequestRequestTypeDef, _OptionalRegisterDomainRequestRequestTypeDef
):
    pass


_RequiredTransferDomainRequestRequestTypeDef = TypedDict(
    "_RequiredTransferDomainRequestRequestTypeDef",
    {
        "DomainName": str,
        "DurationInYears": int,
        "AdminContact": ContactDetailTypeDef,
        "RegistrantContact": ContactDetailTypeDef,
        "TechContact": ContactDetailTypeDef,
    },
)
_OptionalTransferDomainRequestRequestTypeDef = TypedDict(
    "_OptionalTransferDomainRequestRequestTypeDef",
    {
        "IdnLangCode": str,
        "Nameservers": Sequence[NameserverTypeDef],
        "AuthCode": str,
        "AutoRenew": bool,
        "PrivacyProtectAdminContact": bool,
        "PrivacyProtectRegistrantContact": bool,
        "PrivacyProtectTechContact": bool,
    },
    total=False,
)


class TransferDomainRequestRequestTypeDef(
    _RequiredTransferDomainRequestRequestTypeDef, _OptionalTransferDomainRequestRequestTypeDef
):
    pass


_RequiredUpdateDomainContactRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDomainContactRequestRequestTypeDef",
    {
        "DomainName": str,
    },
)
_OptionalUpdateDomainContactRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDomainContactRequestRequestTypeDef",
    {
        "AdminContact": ContactDetailTypeDef,
        "RegistrantContact": ContactDetailTypeDef,
        "TechContact": ContactDetailTypeDef,
        "Consent": ConsentTypeDef,
    },
    total=False,
)


class UpdateDomainContactRequestRequestTypeDef(
    _RequiredUpdateDomainContactRequestRequestTypeDef,
    _OptionalUpdateDomainContactRequestRequestTypeDef,
):
    pass


ListPricesResponseTypeDef = TypedDict(
    "ListPricesResponseTypeDef",
    {
        "Prices": List[DomainPriceTypeDef],
        "NextPageMarker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
