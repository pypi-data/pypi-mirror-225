from typing import Annotated, List, Optional

import typer

from api_compose import GlobalSettings
from api_compose.cli.utils import parse_context
from api_compose.core.logging import get_logger
from api_compose.manifests.deserialiser.deserialiser import deserialise_manifest_to_model
from api_compose.manifests.session_builder import build_session_from_model
from api_compose.root import run_session_model

app = typer.Typer(no_args_is_help=True)

logger = get_logger(__name__)


@app.command(help="Compile a template to a model")
def compile(
        manifest_path: str,
        ctx: Annotated[Optional[List[str]], typer.Option()] = None,
) -> None:
    """
    Render and Execute

    Usage:

    acp render --ctx key1=val1 --ctx key2=val2

    :return:
    """
    manifest_folder_path = GlobalSettings.get().MANIFESTS_FOLDER_PATH
    model = deserialise_manifest_to_model(
        manifest_path,
        manifests_folder_path=manifest_folder_path,
        context=parse_context(ctx),
    )

    logger.info(model.model_dump_json(indent=4))


@app.command(help="Compile a template to a model and run it as a session")
def run(
        manifest_path: str,
        ctx: Annotated[Optional[List[str]], typer.Option()] = None,
):
    """
    Render and Run

    acp run --ctx key1=val1 --ctx key2=val2

    :return:
    """
    manifest_folder_path = GlobalSettings.get().MANIFESTS_FOLDER_PATH
    model = deserialise_manifest_to_model(
        manifest_path,
        manifests_folder_path=manifest_folder_path,
        context=parse_context(ctx),
    )
    session_model = build_session_from_model(model)
    run_session_model(session_model)
