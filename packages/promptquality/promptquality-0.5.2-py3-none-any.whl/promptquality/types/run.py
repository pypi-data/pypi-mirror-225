from io import BufferedReader
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import UUID4, BaseModel, Field, SecretStr, field_validator

from promptquality.constants.integrations import IntegrationName
from promptquality.constants.run import RunDefaults
from promptquality.types.settings import Settings
from promptquality.utils.dataset import DatasetType, dataset_to_path
from promptquality.utils.name import random_name


class RandomName(BaseModel):
    name: str = Field(default_factory=random_name)

    @field_validator("name", mode="before")
    def set_name(cls, value: Optional[str]) -> str:
        if value is None:
            return random_name()
        return value


class CreateProjectRequest(RandomName):
    type: str = RunDefaults.project_type


class CreateProjectResponse(CreateProjectRequest):
    id: UUID4


class BaseTemplateVersionRequest(BaseModel):
    template: str
    version: Optional[int] = None


class CreateTemplateRequest(RandomName, BaseTemplateVersionRequest):
    project_id: UUID4


class CreateTemplateVersionRequest(BaseTemplateVersionRequest):
    template_id: UUID4
    project_id: UUID4


class BaseTemplateVersionResponse(BaseTemplateVersionRequest):
    id: UUID4


class CreateTemplateVersionResponse(BaseTemplateVersionResponse):
    version: int


class BaseTemplateResponse(RandomName):
    id: UUID4
    template: str
    selected_version: CreateTemplateVersionResponse
    selected_version_id: UUID4
    all_versions: List[CreateTemplateVersionResponse] = Field(default_factory=list)


class BaseDatasetRequest(BaseModel):
    file_path: Path = Field(exclude=True)

    @field_validator("file_path", mode="before")
    def dataset_to_path(cls, value: DatasetType) -> Path:
        return dataset_to_path(value)

    @property
    def files(self) -> Dict[str, BufferedReader]:
        return dict(file=self.file_path.open("rb"))


class UploadDatasetRequest(BaseDatasetRequest):
    project_id: UUID4
    file_path: Path
    prompt_template_version_id: UUID4

    @property
    def data(self) -> Dict[str, str]:
        return dict(prompt_template_version_id=str(self.prompt_template_version_id))


class UploadDatasetResponse(BaseModel):
    id: UUID4 = Field(alias="dataset_id")


class EstimateCostRequest(BaseDatasetRequest, Settings):
    project_id: UUID4 = Field(exclude=True)
    template: str = Field(serialization_alias="prompt_template")

    @property
    def params(self) -> Dict[str, str]:
        return self.model_dump(
            mode="json", by_alias=True, exclude_unset=True, exclude_none=True
        )


class EstimatedCostResponse(BaseModel):
    total_cost: float
    query_cost: float
    log_probs_cost: float


class CreateRunRequest(RandomName):
    project_id: UUID4
    task_type: int = RunDefaults.task_type


class CreateRunResponse(CreateRunRequest):
    id: UUID4


class CreateJobRequest(BaseModel):
    project_id: UUID4
    run_id: UUID4
    prompt_dataset_id: UUID4
    prompt_template_version_id: UUID4
    prompt_settings: Optional[Settings] = None
    job_name: str = RunDefaults.job_name
    task_type: int = RunDefaults.task_type


class CreateJobResponse(CreateJobRequest):
    id: UUID4 = Field(alias="job_id")


class GetMetricsRequest(BaseModel):
    project_id: UUID4
    run_id: UUID4


class PromptMetrics(BaseModel):
    total_responses: Optional[int] = None
    average_hallucination: Optional[float] = None
    average_bleu: Optional[float] = None
    average_rouge: Optional[float] = None
    average_cost: Optional[float] = None
    total_cost: Optional[float] = None


class GetJobStatusResponse(BaseModel):
    id: UUID4
    project_id: UUID4
    run_id: UUID4
    status: str
    error_message: Optional[str]
    progress_message: Optional[str]
    steps_completed: int = 0
    steps_total: int = 0
    progress_percent: float = 0.0


class CreateIntegrationRequest(BaseModel):
    api_key: SecretStr
    name: IntegrationName = Field(default=IntegrationName.openai)
    organization_id: Optional[str] = None

    @property
    def body(self) -> Dict[str, Any]:
        extra = (
            dict(organization_id=self.organization_id)
            if self.organization_id
            else dict()
        )
        return dict(token=self.api_key.get_secret_value(), extra=extra)


class SelectTemplateVersionRequest(BaseModel):
    project_id: UUID4
    template_id: UUID4
    version: int
