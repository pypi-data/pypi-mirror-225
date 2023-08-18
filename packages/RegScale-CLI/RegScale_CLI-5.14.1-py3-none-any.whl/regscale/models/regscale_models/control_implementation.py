#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Security Control Implementation """

# standard python imports
from pydantic import BaseModel
from typing import Any, Optional
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.models.regscale_models.control import Control


class ControlImplementation(BaseModel):
    """Control Implementation"""

    parentId: Optional[int]
    parentModule: Optional[str]
    controlOwnerId: str  # Required
    status: str  # Required
    controlID: int  # Required
    control: Optional[Control] = None
    id: Optional[int] = None
    createdById: Optional[str] = None
    uuid: Optional[str] = None
    policy: Optional[str] = None
    implementation: Optional[str] = None
    dateLastAssessed: Optional[str] = None
    lastAssessmentResult: Optional[str] = None
    practiceLevel: Optional[str] = None
    processLevel: Optional[str] = None
    cyberFunction: Optional[str] = None
    implementationType: Optional[str] = None
    implementationMethod: Optional[str] = None
    qdWellDesigned: Optional[str] = None
    qdProcedures: Optional[str] = None
    qdSegregation: Optional[str] = None
    qdFlowdown: Optional[str] = None
    qdAutomated: Optional[str] = None
    qdOverall: Optional[str] = None
    qiResources: Optional[str] = None
    qiMaturity: Optional[str] = None
    qiReporting: Optional[str] = None
    qiVendorCompliance: Optional[str] = None
    qiIssues: Optional[str] = None
    qiOverall: Optional[str] = None
    responsibility: Optional[str] = None
    inheritedControlId: Optional[int] = None
    inheritedRequirementId: Optional[int] = None
    inheritedSecurityPlanId: Optional[int] = None
    inheritedPolicyId: Optional[int] = None
    dateCreated: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    dateLastUpdated: Optional[str] = None
    weight: Optional[int] = None
    isPublic: bool = True
    inheritable: bool = False
    systemRoleId: Optional[int] = None

    @staticmethod
    def fetch_existing_implementations(
        app: Application, regscale_parent_id: int, regscale_module: str
    ):
        """_summary_

        :param app: Application instance
        :param regscale_parent_id: RegScale Parent ID
        :param regscale_module: RegScale Parent Module
        :return: _description_
        """
        api = Api(app)
        existing_implementations = []
        existing_implementations_response = api.get(
            url=app.config["domain"]
            + "/api/controlimplementation"
            + f"/getAllByParent/{regscale_parent_id}/{regscale_module}"
        )
        if existing_implementations_response.ok:
            existing_implementations = existing_implementations_response.json()
        return existing_implementations

    @staticmethod
    def from_dict(obj: Any) -> "ControlImplementation":
        """
        Create RegScale Port and Protocol from dictionary
        :param obj: dictionary
        :return: ControlImplementation class
        :rtype: ControlImplementation
        """
        if "id" in obj:
            del obj["id"]
        return ControlImplementation(**obj)

    def __hash__(self):
        return hash(
            (
                self.controlID,
                self.controlOwnerId,
                self.status,
            )
        )
