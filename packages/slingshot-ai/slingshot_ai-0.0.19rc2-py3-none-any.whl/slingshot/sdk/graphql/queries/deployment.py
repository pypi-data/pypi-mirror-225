from __future__ import annotations

from pydantic import BaseModel, Field

from slingshot import schemas

from ..base_graphql import BaseGraphQLQuery


class DeploymentInstanceWithStatus(BaseModel):
    deployment_instance_status: schemas.AppInstanceStatus = Field(..., alias="deploymentStatus")


class DeploymentInstancesWithStatusResponse(BaseModel):
    deployment_instances: list[DeploymentInstanceWithStatus] = Field(..., alias="deployments")


class DeploymentStatusSubscription(BaseGraphQLQuery[DeploymentInstancesWithStatusResponse]):
    _query = """
        subscription DeploymentStatusSubscription($appSpecId: String!) {
          deployments(where: {appSpec: {appSpecId: {_eq: $appSpecId}}}, orderBy: {createdAt: DESC}, limit: 1) {
            deploymentStatus
          }
        }
    """
    _depends_on = []

    def __init__(self, app_spec_id: str):
        super().__init__(variables={"appSpecId": app_spec_id}, response_model=DeploymentInstancesWithStatusResponse)
