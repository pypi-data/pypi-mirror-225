from typing import Optional

from fiddler.schema.base import BaseDataSchema


class Baseline(BaseDataSchema):
    id: Optional[int] = None
    name: str
    project_id: Optional[str]
    organization_id: Optional[str]
    type: Optional[str]
    model_id: Optional[str]

    dataset_id: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    offset: Optional[int] = None
    window_size: Optional[int] = None

    run_async: bool = True
