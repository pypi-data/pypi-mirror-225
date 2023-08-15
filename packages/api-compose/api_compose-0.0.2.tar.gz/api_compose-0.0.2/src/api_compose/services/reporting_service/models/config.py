from pydantic import BaseModel as _BaseModel, Field


class BaseReportRendererConfigModel(_BaseModel):
    report_folder: str = Field(
        'reports',
        description='Location of rendered report',

    )

class HtmlReportRendererConfigModel(BaseReportRendererConfigModel):
    pass
