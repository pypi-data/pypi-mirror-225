import json
from typing import List
from uuid import UUID

from client.api import workspace_api
from client.exceptions import ApiException
from client.model.as_code_object_dto import AsCodeObjectDto
from client.model.workspace_apply_request_dto import WorkspaceApplyRequestDto
from client.model.workspace_apply_response_dto import WorkspaceApplyResponseDto
from sifflet_sdk.apis.base import BaseApi
from sifflet_sdk.logger import logger


class WorkspaceApi(BaseApi):
    def __init__(self, sifflet_config):
        super().__init__(sifflet_config)
        self.api_instance = workspace_api.WorkspaceApi(self.api)

    def delete_workspace(self, id: UUID, dry_run: bool) -> WorkspaceApplyResponseDto:
        logger.debug(f"Request: id={id}, dry_run={dry_run}")
        response = self.api_instance.delete_workspace(str(id), dry_run=dry_run)
        logger.debug(f"Response: {response}")
        return response

    def apply_workspace(self, id: UUID, changes: List[AsCodeObjectDto], dry_run: bool) -> WorkspaceApplyResponseDto:
        # We do not check the type to allow the use of new monitor parameters DTO
        # Without updating the CLI
        request = WorkspaceApplyRequestDto(_check_type=False)
        request.changes = changes
        logger.debug(f"Request: id={id}, dry_run={dry_run}, body=")
        logger.debug(request)
        try:
            response = self.api_instance.deploy_workspace(str(id), request, dry_run=dry_run)
            logger.debug("Response: body=")
            logger.debug(response)
        except ApiException as err:
            logger.debug(err)
            if err.body:
                error_body = json.loads(err.body)
                if error_body.get("type") == "sifflet:errors:workspace:apply":
                    response = error_body["properties"]["response"]
                    return WorkspaceApplyResponseDto(**response)
            raise err
        return response
