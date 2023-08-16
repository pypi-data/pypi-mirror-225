#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from urllib.parse import urljoin


class LeveragedAuthorizations(BaseModel):
    """LeveragedAuthorizations model."""

    id: Optional[int] = None
    isPublic: bool = True
    uuid: Optional[str] = None
    title: str
    fedrampId: Optional[str] = None
    ownerId: str
    securityPlanId: int
    dateAuthorized: str
    description: Optional[str] = None
    servicesUsed: Optional[str] = None
    securityPlanLink: Optional[str] = None
    crmLink: Optional[str] = None
    responsibilityAndInheritanceLink: Optional[str] = None
    createdById: str
    dateCreated: Optional[str] = None
    lastUpdatedById: str
    dateLastUpdated: Optional[str] = None
    tenantsId: Optional[int] = None

    @staticmethod
    def insert_leveraged_authorizations(
        app: Application, leveraged_auth: "LeveragedAuthorizations"
    ):
        """Insert a leveraged authorization into the database.
        :param app (Application): The application instance.
        :param leveraged_auth (LeveragedAuthorizations): The leveraged authorization to insert.
        :Returns: LeveragedAuthorizations dictionary.
        :rtype dict: The response from the API.
        """
        api = Api(app)

        # Construct the URL by joining the domain and endpoint
        url = urljoin(app.config.get("domain"), "/api/leveraged-authorization")
        # Convert the Pydantic model to a dictionary
        data = leveraged_auth.dict()

        # Make the POST request to insert the data
        response = api.post(url, json=data)

        # Check for success and handle the response as needed
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()
