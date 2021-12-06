import traceback

import click
from flask import Blueprint

from src.patents.application.fetch_patents_use_case import FetchPatentsUseCase
from src.patents.infrastructure.adapter.http_patent_acl_adapter import (
    HttpPatentAclAdapter,
)
from src.patents.infrastructure.sqlalchemy_patent_repository import (
    SqlalchemyPatentRepository,
)

patents_command_controller = Blueprint("patents", __name__)


@patents_command_controller.cli.command("patents")
@click.argument("from_date")
@click.argument("to_date")
def fetch_patents(from_date, to_date):
    try:
        service = FetchPatentsUseCase(
            patent_acl_adapter=HttpPatentAclAdapter(),
            patent_repository=SqlalchemyPatentRepository(),
        )
        service.execute(from_date=from_date, to_date=to_date)
    except:
        traceback.print_exc()
