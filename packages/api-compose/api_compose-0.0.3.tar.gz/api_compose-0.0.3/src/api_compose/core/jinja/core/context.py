"""
Standardize Jinja Contexts used for different purposes
"""
from __future__ import annotations

__all__ = ['BaseJinjaContext']

from types import SimpleNamespace
from typing import Dict

from pydantic import BaseModel as _BaseModel, Field

from api_compose.core.utils.settings import GlobalSettings


class BaseJinjaContext(_BaseModel, extra='allow'):
    """
    Standardise what core context is passed to render stuff
    """

    # Static - Session Scoped
    env: Dict = Field(
        SimpleNamespace(**GlobalSettings.get().env_vars),
        description='environment variables from .env file'
    )

    def dict(self):
        # do not recursively render. Only get the first layer
        return dict(self)
