import logging
import uuid
from dataclasses import dataclass

from _qwak_proto.qwak.user_application.common.v0.resources_pb2 import (
    ClientPodComputeResources,
    PodComputeResourceTemplateSpec,
)
from _qwak_proto.qwak.workspace.workspace_pb2 import Workspace, WorkspaceImage
from _qwak_proto.qwak.workspace.workspace_service_pb2 import (
    CreateWorkspaceResponse,
    DeleteWorkspaceResponse,
    GetWorkspaceByIdResponse,
    ListWorkspaceImagesResponse,
    ListWorkspacesResponse,
    UpdateWorkspaceResponse,
)
from _qwak_proto.qwak.workspace.workspace_service_pb2_grpc import (
    WorkspaceManagementServiceServicer,
)

logger = logging.getLogger(__name__)


@dataclass
class WorkspaceData:
    workspace_name: str
    image_id: str
    template_id: str
    status: str


class WorkspaceManagerServiceMock(WorkspaceManagementServiceServicer):
    def __init__(self):
        super(WorkspaceManagerServiceMock, self).__init__()
        self.workspaces = dict()
        self.image_ids_to_names = {
            "1": "cpu_3.7",
            "2": "cpu_3.8",
            "3": "gpu_3.7",
            "4": "gpu_3.8",
        }

    def CreateWorkspace(self, request, context):
        logger.info(f"Creating workspace {request}")
        workspace_id = self._get_workspace_id()
        self.workspaces[workspace_id] = WorkspaceData(
            workspace_name=request.workspace_spec.workspace_name,
            image_id=request.workspace_spec.image_id,
            template_id=request.workspace_spec.client_pod_compute_resources.template_spec.template_id,
            status="CREATED",
        )
        return CreateWorkspaceResponse(workspace_id=workspace_id)

    def UpdateWorkspace(self, request, context):
        logger.info(f"Updating workspace {request}")
        self.workspaces[request.workspace_id] = WorkspaceData(
            workspace_name=request.workspace_spec.workspace_name,
            image_id=request.workspace_spec.image_id,
            template_id=request.workspace_spec.client_pod_compute_resources.template_spec.template_id,
            status="CREATED",
        )
        return UpdateWorkspaceResponse()

    def DeleteWorkspace(self, request, context):
        logger.info(f"delete workspace request: {request}")
        del self.workspaces[request.workspace_id]
        return DeleteWorkspaceResponse()

    def GetWorkspaceById(self, request, context):
        logger.info(f"get workspace by id request: {request}")
        return GetWorkspaceByIdResponse(
            workspace=Workspace(
                workspace_name=self.workspaces[request.workspace_id].workspace_name,
                image_id=self.workspaces[request.workspace_id].image_id,
                client_pod_compute_resources=ClientPodComputeResources(
                    template_spec=PodComputeResourceTemplateSpec(
                        template_id=self.workspaces[request.workspace_id].template_id
                    )
                ),
            )
        )

    def ListWorkspaces(self, request, context):
        logger.info(f"list workspaces: {request}")
        return ListWorkspacesResponse(
            workspaces=[
                Workspace(
                    workspace_name=workspace.workspace_name,
                )
                for workspace_id, workspace in self.workspaces.items()
            ]
        )

    def DeployWorkspace(self, request, context):
        logger.info(f"Deploying workspace {request}")
        current_workspace = self.workspaces[request.workspace_id]
        self.workspaces[request.workspace_id] = WorkspaceData(
            workspace_name=current_workspace.workspace_name,
            image_id=current_workspace.image_id,
            template_id=current_workspace.template_id,
            status="DEPLOYING",
        )
        return UpdateWorkspaceResponse()

    def UndeployWorkspace(self, request, context):
        logger.info(f"Undeploying workspace {request}")
        current_workspace = self.workspaces[request.workspace_id]

        self.workspaces[request.workspace_id] = WorkspaceData(
            workspace_name=current_workspace.workspace_name,
            image_id=current_workspace.image_id,
            template_id=current_workspace.template_id,
            status="UNDEPLOYING",
        )
        return UpdateWorkspaceResponse()

    def ListWorkspaceImages(self, request, context):
        logger.info("List workspace images")
        workspace_images = []
        for k, v in self.image_ids_to_names.items():
            workspace_images.append(WorkspaceImage(name=v, id=k))
        return ListWorkspaceImagesResponse(workspace_images=workspace_images)

    @staticmethod
    def _get_workspace_id():
        return str(uuid.uuid4())
