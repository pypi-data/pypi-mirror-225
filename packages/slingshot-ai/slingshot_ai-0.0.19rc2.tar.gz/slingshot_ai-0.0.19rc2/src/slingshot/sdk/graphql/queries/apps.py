from __future__ import annotations

from pydantic import BaseModel, Field

from slingshot import schemas

from ..base_graphql import BaseGraphQLQuery
from ..fragments import AppInstance, AppSpec


class AppSpecsForProjectResponse(BaseModel):
    app_specs: list[AppSpec] = Field(..., alias="appSpecs")


class AppSpecsForProjectQuery(BaseGraphQLQuery[AppSpecsForProjectResponse]):
    _query = """
        query AppSpecsForProject($projectId: String!) {
            appSpecs(where: {
                project: { projectId: {_eq: $projectId} },
                isArchived: {_eq: false}
            }) {
                ...SlingshotAppSpec
            }
        } """

    _depends_on = [AppSpec]

    def __init__(self, project_id: str):
        super().__init__(variables={"projectId": project_id}, response_model=AppSpecsForProjectResponse)


class AppInstancesResponse(BaseModel):
    app_instances: list[AppInstance] = Field(..., alias="appInstances")


class AppInstancesByAppTypeQuery(BaseGraphQLQuery[AppInstancesResponse]):
    _query = """
        query AppInstancesByAppType($appType: AppTypeEnumEnum!, $projectId: String!) {
            appInstances(where: {_and: {appType: {_eq: $appType}, appSpec: {projectId: {_eq: $projectId}}}}) {
                ...AppInstance
            }
        }
    """

    _depends_on = [AppInstance]

    def __init__(self, app_type: str, project_id: str):
        super().__init__(variables={"appType": app_type, "projectId": project_id}, response_model=AppInstancesResponse)


class LatestAppInstanceForAppSpecQuery(BaseGraphQLQuery[AppInstancesResponse]):
    _query = """
        query LatestAppInstanceForAppSpec($appSpecId: String!) {
            appInstances(where: {appSpecId: {_eq: $appSpecId}}, orderBy: {createdAt: DESC}, limit: 1) {
                ...AppInstance
            }
        } """

    _depends_on = [AppInstance]

    def __init__(self, app_spec_id: str):
        super().__init__(variables={"appSpecId": app_spec_id}, response_model=AppInstancesResponse)


class AppInstanceQuery(BaseGraphQLQuery[AppInstancesResponse]):
    _query = """
        query AppInstance($appInstanceId: String!, $projectId: String!) {
            appInstances(where: {_and: {appInstanceId: {_eq: $appInstanceId}, appSpec: {projectId: {_eq: $projectId}}}}) {
                ...AppInstance
           }
        }
    """

    _depends_on = [AppInstance]

    def __init__(self, app_instance_id: str, project_id: str):
        super().__init__(
            variables={"appInstanceId": app_instance_id, "projectId": project_id}, response_model=AppInstancesResponse
        )


class AppSpecsResponse(BaseModel):
    app_specs: list[AppSpec] = Field(..., alias="appSpecs")


class AppSpecByIdQuery(BaseGraphQLQuery[AppSpecsResponse]):
    _query = """
        query AppSpecQueryByIdQuery($appSpecId: String!, $projectId: String!) {
            appSpecs(where: {_and: {appSpecId: {_eq: $appSpecId}, projectId: {_eq: $projectId}}}) {
                ...SlingshotAppSpec
           }
        }
    """

    _depends_on = [AppSpec]

    def __init__(self, app_spec_id: str, project_id: str):
        super().__init__(variables={"appSpecId": app_spec_id, "projectId": project_id}, response_model=AppSpecsResponse)


class AppSpecByNameQuery(BaseGraphQLQuery[AppSpecsResponse]):
    _query = """
        query AppSpecByName($appSpecName: String!, $projectId: String!) {
            appSpecs(where: {_and: {appSpecName: {_eq: $appSpecName}, projectId: {_eq: $projectId}}}) {
                ...SlingshotAppSpec
           }
        }
    """

    _depends_on = [AppSpec]

    def __init__(self, app_spec_name: str, project_id: str):
        super().__init__(
            variables={"appSpecName": app_spec_name, "projectId": project_id}, response_model=AppSpecsResponse
        )


class DeploymentSpecByNameQuery(BaseGraphQLQuery[AppSpecsResponse]):
    _query = """
        query DeploymentSpecByName($appSpecName: String!, $projectId: String!) {
            appSpecs(where: {_and: {
                appSpecName: {_eq: $appSpecName},
                projectId: {_eq: $projectId},
                appType: {_eq: DEPLOYMENT}
            }}) {
                ...SlingshotAppSpec
           }
        }
    """

    _depends_on = [AppSpec]

    def __init__(self, app_spec_name: str, project_id: str):
        super().__init__(
            variables={"appSpecName": app_spec_name, "projectId": project_id}, response_model=AppSpecsResponse
        )


class AppInstanceWithStatus(BaseModel):
    app_instance_status: schemas.AppInstanceStatus = Field(..., alias="appInstanceStatus")


class AppInstancesWithStatusResponse(BaseModel):
    app_instances: list[AppInstanceWithStatus] = Field(..., alias="appInstances")


class AppSpecStatusSubscription(BaseGraphQLQuery[AppInstancesWithStatusResponse]):
    _query = """
        subscription AppSpecStatusSubscription($appSpecId: String!) {
          appInstances(where: {appSpec: {appSpecId: {_eq: $appSpecId}}}, orderBy: {createdAt: DESC}, limit: 1) {
            appInstanceStatus
          }
        }
    """
    _depends_on = []

    def __init__(self, app_spec_id: str):
        super().__init__(variables={"appSpecId": app_spec_id}, response_model=AppInstancesWithStatusResponse)
