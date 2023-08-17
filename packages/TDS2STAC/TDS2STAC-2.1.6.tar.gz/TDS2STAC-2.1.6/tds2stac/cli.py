"""Console script for tds2stac."""
import argparse
import sys

import click

# from tds2stac.app import Harvester


@click.command()
def main():
    """Console script for tds2stac."""

    # parser = argparse.ArgumentParser(description='This package creates STAC metadata by harvesting dataset details from the Thredds data server. After creating STAC Catalogs, Collections, and Items, it imports them into pgSTAC and STAC-FastAPI.')
    # parser.add_argument('--url', '-u', dest='main_catalog_url', required=True, help='TDS Catalog url to start harvesting')
    # parser.add_argument('--stac', '-s', dest='stac', required=True, help='Permitting creation of STAC catalogs (True or False')
    # parser.add_argument('--stac_dir', '-sd', dest='stac_dir', required=True, help='Directory of saving created STAC catalogs ("/app/stac/")')
    # parser.add_argument('--stac_id', '-si', dest='stac_id', required=False, help='STAC catalog ID')
    # parser.add_argument('--stac_desc', '-sdsc', dest='stac_description', required=False, help='STAC catalog description')
    # parser.add_argument('--webservice', '-ws', dest='web_service', required=False, help='TDS XML-based webservives to start crawling("iso","ncml", and "wms")')
    # parser.add_argument('--dtfilter', '-dtf', dest='datetime_filter', required=False, help='Datetime-based filtering e.g ["2010-02-18T00:00:00.000Z","2040-02-22T00:00:00.000Z"]')
    # parser.add_argument('--ingestion', '-ci', dest='catalog_ingestion', required=False, help='Ingesting static catalog in STAC-API (True or False)')
    # parser.add_argument('--api', '-api', dest='api_posting', required=False, help='Posting STAC catalog in STAC-API (True) or ingesting directly into pgSTAC (False) (True or False)')
    # parser.add_argument('--agg', '-a', dest='aggregated_dataset', required=False, help='An option for harvesting aggregated datasets in TDS (True or False)')
    # parser.add_argument('--agg_url', '-au', dest='main_catalog_url', required=False, help='Aggregating datasets url address in TDS (URL address)')
    # parser.set_defaults(defaultSkips=True)
    # args = parser.parse_args()
    # Harvester(catalog_url=args.catalog_url, out_dir=args.out_dir, log_file=args.log_file, select=args.select, skip=args.skip, clean=args.clean)
    # """Console script for tds2stac."""
    click.echo(
        "Replace this message by putting your code into " "tds2stac.cli.main"
    )
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


# if __name__ == "__main__":
#     sys.exit(main())  # pragma: no cover
