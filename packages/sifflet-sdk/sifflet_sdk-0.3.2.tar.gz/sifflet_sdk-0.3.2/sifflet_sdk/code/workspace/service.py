from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple
from uuid import UUID, uuid4

import yaml

from client.model.as_code_object_dto import AsCodeObjectDto
from client.model.workspace_apply_response_dto import WorkspaceApplyResponseDto
from sifflet_sdk.code.workspace.api import WorkspaceApi
from sifflet_sdk.configure.service import SiffletConfig
from sifflet_sdk.errors import exception_handler
from sifflet_sdk.logger import logger


class WorkspaceService:
    def __init__(self, sifflet_config: SiffletConfig):
        self.sifflet_config: SiffletConfig = sifflet_config
        self.api_instance = WorkspaceApi(sifflet_config)

    @exception_handler
    def initialize_workspace(self, file_name: Path, name: str) -> None:
        content = yaml.dump(
            {
                "kind": "Workspace",
                "version": 1,
                "id": str(uuid4()),
                "name": name,
                "include": ["*.yaml"],
                "exclude": [],
            },
            sort_keys=False,
        )

        logger.debug("Workspace content:")
        logger.debug(content)

        with open(file_name, "w") as file:
            file.write(content)

        logger.info(f"Workspace initialized at {file_name}.")

    @exception_handler
    def delete_workspace(self, id: UUID, dry_run: bool) -> WorkspaceApplyResponseDto:
        response: WorkspaceApplyResponseDto = self.api_instance.delete_workspace(id, dry_run)
        logger.info("Workspace deleted.")
        return response

    @exception_handler
    def apply_workspace(self, workspace_file_name: Path, dry_run: bool) -> WorkspaceApplyResponseDto:
        changes, workspace_id = self.get_changes_and_workspace_id(workspace_file_name)
        response: WorkspaceApplyResponseDto = self.api_instance.apply_workspace(workspace_id, changes, dry_run=dry_run)

        dry_run_mode = "DRY-RUN MODE - " if dry_run else ""
        if any(change.status == "Fatal" for change in response.changes):
            logger.error(f"{dry_run_mode}Workspace not deployed because of fatal errors.")
        elif any(change.status == "Error" for change in response.changes):
            logger.error(f"{dry_run_mode}Workspace deployed with errors (some objects may not have been deployed).")
        elif any(log.level == "Warning" for change in response.changes for log in change.logs):
            logger.warning(f"{dry_run_mode}Workspace deployed with warnings.")
        else:
            logger.info(f"{dry_run_mode}Workspace deployed.")
        return response

    @staticmethod
    def get_changes_and_workspace_id(workspace_file_name: Path) -> Tuple[List[AsCodeObjectDto], UUID]:
        def to_workspace(data):
            if data.get("kind") != "Workspace":
                raise InvalidWorkspaceFileError("The input YAML file must be of kind Workspace")
            if data.get("version") == 1:
                return AsCodeWorkspaceV1(**data)
            raise InvalidWorkspaceFileError(f"Unsupported Workspace version: {data.get('version')}")

        # Open and parse the workspace file
        folder = workspace_file_name.parent
        with open(workspace_file_name, "r") as file:
            data = yaml.safe_load(file)
        logger.debug("Workspace content:")
        logger.debug(data)
        workspace = to_workspace(data)

        # Select the files to be part of the deployment
        included_files: List[Path] = []
        for pattern in workspace.include:
            included_files.extend(folder.glob(pattern))
        excluded_files: List[Path] = []
        if workspace.exclude:
            for pattern in workspace.exclude:
                excluded_files.extend(folder.glob(pattern))
        filtered_files = [file for file in included_files if file not in excluded_files]
        logger.info(f"Included files: {[f.name for f in filtered_files]}")

        changes: List[AsCodeObjectDto] = []
        for object_file_name in filtered_files:
            with open(object_file_name, "r") as file:
                changes.append(yaml.safe_load(file))

        return changes, workspace.id


class InvalidWorkspaceFileError(Exception):
    pass


@dataclass(frozen=True)
class AsCodeWorkspaceV1:
    kind: str
    version: int
    id: UUID
    name: str
    include: List[str]
    description: Optional[str] = None
    exclude: Optional[List[str]] = None
