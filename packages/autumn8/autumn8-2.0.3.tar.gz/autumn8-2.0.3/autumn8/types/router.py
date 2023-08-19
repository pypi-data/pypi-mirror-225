from typing import Optional

from pydantic import BaseModel

from autumn8.common.config import settings


class NewModelInfo(BaseModel):
    name: str
    s3_file_url: Optional[str] = None  # initialized later
    s3_input_file_url: Optional[str] = None
    framework: settings.Framework
    quantization: settings.Quantization
    model_file_type: Optional[str] = None
    domain: Optional[str] = None
    task: Optional[str] = None
    inputs: Optional[str] = None
    group_id: Optional[str] = None
