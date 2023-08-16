"""Console script for ds2stac_ingester."""
import sys

import click


@click.command()
def main(args=None):
    """Console script for ds2stac_ingester."""
    click.echo(
        "Replace this message by putting your code into "
        "ds2stac_ingester.cli.main"
    )
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
