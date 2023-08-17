from typing import Optional, Union, List

from phi.docker.app.base import DockerApp, WorkspaceVolumeType, ContainerContext  # noqa: F401


class Streamlit(DockerApp):
    # -*- App Name
    name: str = "streamlit"

    # -*- Image Configuration
    image_name: str = "phidata/streamlit"
    image_tag: str = "1.23"
    command: Optional[Union[str, List[str]]] = "streamlit hello"

    # -*- App Ports
    # Open a container port if open_container_port=True
    open_container_port: bool = True
    # Port number on the container
    container_port: int = 8501
    # Host port to map to the container port
    host_port: int = 8501

    # -*- Workspace Volume
    # Mount the workspace directory from host machine to the container
    mount_workspace: bool = False
    # Path to mount the workspace volume inside the container
    workspace_volume_container_path: str = "/usr/local/app"
