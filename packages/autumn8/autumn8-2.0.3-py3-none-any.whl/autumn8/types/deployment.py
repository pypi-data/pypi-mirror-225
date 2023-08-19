import dataclasses
import enum
import json
from dataclasses import dataclass
from typing import Optional, Union

from pydantic import BaseModel


class DeploymentStatus(str, enum.Enum):
    STARTING = "STARTING"
    READY = "READY"
    INVALID = "INVALID"
    CRASHED = "CRASHED"
    SLEEPING = "SLEEPING"
    TERMINATING = "TERMINATING"
    TERMINATED = "TERMINATED"


class ServerType(str, enum.Enum):
    MULTIMODEL_SERVER = "MULTIMODEL_SERVER"
    CUSTOM_PYTORCH_INFERER = "PYTORCH"  # for CLI imported models
    TORCHSERVE = "TORCHSERVE"
    TENSORFLOW_SERVING = "TENSORFLOW"


class DeploymentView(BaseModel):
    initialization_progress: int = 100
    """Percents of progress, in range from 0 to 100"""
    initialization_status_details: str = (
        "Deployment set up and accepting requests"
    )

    deployment_id: str
    """Unique identifier of the deployment"""
    model_id: int
    """Unique identifier of the model that's hosted by the deployment"""
    instance_type: str

    status: DeploymentStatus = DeploymentStatus.STARTING
    created_at: Union[int, None] = None
    public_dns: Union[str, None] = None
    server_type: Union[ServerType, None] = None
    service_provider: str = "autumn8"


@dataclass
class A8FManifest:
    version: str
    """The version of the manifest"""

    uri: str
    """S3 Object key, or HTTP url, under which the model file is available"""

    memory: int
    model_name: str
    model_id: int
    """AutoDL ID of the model"""


    # Fast loading optimization info
    optimized: Optional[bool] = None
    chunk_count: Optional[int] = None
    optimized_model_bucket: Optional[str] = None
    optimized_path: Optional[str] = None


    deployment_id: Optional[
        str
    ] = None  # idk why, but for some time we passed this only for deployments with external s3 bucket models
    model_bucket: Optional[str] = None
    """An external public S3 bucket containing the model file"""

    @classmethod
    def load(cls, json_string: str) -> "A8FManifest":
        dict_content = json.loads(json_string)
        return cls(**dict_content)

    def dict(self):
        return dataclasses.asdict(self)
