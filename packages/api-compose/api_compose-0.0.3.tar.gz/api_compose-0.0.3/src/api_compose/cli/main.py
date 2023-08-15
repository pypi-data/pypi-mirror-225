from typing import Annotated, List, Optional

import typer

from api_compose.cli.commands import config, manifest
from api_compose.cli.utils import parse_context
from api_compose.core.utils.settings import GlobalSettings
from api_compose.manifests.session_builder import build_session_from_tags
from api_compose.root import run_session_model
from api_compose.version import __version__

DOCUMENTATION_URL = "https://python-database-version-control.readthedocs.io/en/latest/"
EPILOG_TXT = f"Doc: {DOCUMENTATION_URL}"
HELP_TXT = "Declaratively Compose and Test your API Calls"

app = typer.Typer(
    help=HELP_TXT,
    short_help=HELP_TXT,
    epilog=EPILOG_TXT,
    no_args_is_help=True
)

app.add_typer(config.app, name='cfg', help="Configuration")
app.add_typer(manifest.app, name='manifest', help="Manifests")


@app.command(help="Scaffold Project Structure")
def version() -> None:
    typer.echo(__version__)


@app.command(help="Scaffold Project Structure")
def scaffold(project_name: str) -> None:
    pass


@app.command(help="Run everything according to configurations")
def run(ctx: Annotated[Optional[List[str]], typer.Option()] = None, ):
    """
    Render and Run

    acp run --ctx key1=val1 --ctx key2=val2

    :return:
    """
    session_model = build_session_from_tags(
        manifests_folder_path=GlobalSettings.get().MANIFESTS_FOLDER_PATH,
        target_tags=GlobalSettings.get().TAGS,
        **parse_context(ctx),
    )
    run_session_model(session_model)


if __name__ == "__main__":
    app()
