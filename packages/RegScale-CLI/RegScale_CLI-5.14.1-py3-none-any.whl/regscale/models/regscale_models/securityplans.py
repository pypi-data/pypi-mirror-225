#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional


class SecurityPlan(BaseModel):
    """Security Plan Model"""

    systemName: str
    planInformationSystemSecurityOfficerId: str
    planAuthorizingOfficialId: str
    systemOwnerId: Optional[str] = ""
    otherIdentifier: Optional[str] = ""
    confidentiality: Optional[str] = ""
    integrity: Optional[str] = ""
    availability: Optional[str] = ""
    status: Optional[str] = ""
    description: Optional[str] = ""
    dateSubmitted: Optional[str] = ""
    approvalDate: Optional[str] = ""
    expirationDate: Optional[str] = ""
    systemType: Optional[str] = ""
    purpose: Optional[str] = ""
    conditionsOfApproval: Optional[str] = ""
    environment: Optional[str] = ""
    lawsAndRegulations: Optional[str] = ""
    authorizationBoundary: Optional[str] = ""
    networkArchitecture: Optional[str] = ""
    dataFlow: Optional[str] = ""
    overallCategorization: Optional[str] = ""
    maturityTier: Optional[str] = ""
    wizProjectId: Optional[str] = ""
    serviceNowAssignmentGroup: Optional[str] = ""
    jiraProject: Optional[str] = ""
    tenableGroup: Optional[str] = ""
    facilityId: Optional[int] = None
    orgId: Optional[int] = None
    parentId: Optional[int] = 0
    parentModule: Optional[str] = ""
    createdById: Optional[str] = ""
    dateCreated: Optional[str] = ""
    lastUpdatedById: Optional[str] = ""
    dateLastUpdated: Optional[str] = ""
    users: Optional[int] = 0
    privilegedUsers: Optional[int] = 0
    usersMFA: Optional[int] = 0
    privilegedUsersMFA: Optional[int] = 0
    hva: Optional[bool] = False
    practiceLevel: Optional[str] = ""
    processLevel: Optional[str] = ""
    cmmcLevel: Optional[str] = ""
    cmmcStatus: Optional[str] = ""
    isPublic: Optional[bool] = True
    executiveSummary: Optional[str] = ""
    recommendations: Optional[str] = ""
    id: Optional[int] = None
    uuid: Optional[str] = ""
    bDeployGov: Optional[bool] = None
    bDeployHybrid: Optional[bool] = None
    bDeployPrivate: Optional[bool] = None
    bDeployPublic: Optional[bool] = None
    bModelIaaS: Optional[bool] = None
    bModelOther: Optional[bool] = None
    bModelPaaS: Optional[bool] = None
    bModelSaaS: Optional[bool] = None

    @staticmethod
    def from_dict(data: dict) -> "SecurityPlan":
        """
        Create a SecurityPlan object from a dictionary.
        :param data: The dictionary to create the object from.
        :return: A SecurityPlan object.
        """
        return SecurityPlan(**data)
