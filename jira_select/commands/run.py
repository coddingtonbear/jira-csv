import argparse
import subprocess
import tempfile
import sys
from typing import IO

from rich.progress import track
from yaml import safe_load

from ..plugin import BaseCommand, get_installed_formatters
from ..query import Query
from ..types import QueryDefinition


class Command(BaseCommand):
    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        formatters = get_installed_formatters()

        parser.add_argument("query_file", help="Query definition file to run")
        parser.add_argument("--format", "-f", choices=formatters.keys(), default="csv")
        parser.add_argument("--output", "-o")
        parser.add_argument("--view", "-v", default=False, action="store_true")

    @classmethod
    def get_help(cls) -> str:
        return "Interactively generates a query definition (in yaml format)."

    def handle(self) -> None:
        query_definition: QueryDefinition = {}
        with open(self.options.query_file, "r") as inf:
            query_definition = safe_load(inf)

        output: IO[str] = sys.stdout
        output_file = self.options.output
        if self.options.output:
            output = open(self.options.output, "w")
        elif self.options.view:
            output = tempfile.NamedTemporaryFile("w", suffix=".csv")
            output_file = output.name

        formatter_cls = get_installed_formatters()[self.options.format]

        query = Query(self.jira, query_definition)
        with formatter_cls(query, output) as formatter:
            if output == sys.stdout:
                for row in query:
                    formatter.writerow(row)
            else:
                count = query.count()
                for row in track(query, description="Running query...", total=count):
                    formatter.writerow(row)
        output.flush()

        if self.options.view:
            viewer = self.config.get("viewers", {}).get("csv", "vd")

            proc = subprocess.Popen([viewer, output_file])
            proc.wait()

        if output is not sys.stdout:
            output.close()
