from typing import Callable

from pydantic import BaseModel as _BaseModel, Field


class BaseAssertionConfigModel(_BaseModel):
    pass


class JinjaAssertionConfigModel(BaseAssertionConfigModel):
    template: str = Field('', description='Renderable core template content')
    template_file_path: str = Field('', description='path to core template')


class PythonAssertionConfigModel(BaseAssertionConfigModel):
    funcname: str

    @property
    def func(self) -> Callable[...,bool]:
        return lambda x: True


