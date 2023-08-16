#!/usr/bin/env python

"""Tests for `tds2stac` package."""

import pytest

from click.testing import CliRunner

import sys
sys.path.append('../')
from tds2stac.app import Harvester
from tds2stac import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # return Harvester("https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/climate_catalog_ext.html?dataset=gleam_v3.5a_daily_aggregated",
    #                  stac=True, stac_dir="/app/stac/",
    #                  stac_id = "sample",
    #                  stac_description = "sample",
    #                  web_service = "iso",
    #                  datetime_filter=["2010-02-18T00:00:00.000Z","2040-02-22T00:00:00.000Z"],
    #                  catalog_ingestion = False,
    #                  api_posting = False,
    #                  aggregated_dataset = True,
    #                  aggregated_dataset_url = "https://thredds.imk-ifu.kit.edu/thredds/catalog/catalogues/climate_catalog_ext.html?dataset=gleam_v3.5a_daily_aggregated",)
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string



# def test_command_line_interface():
#     """Test the CLI."""
#     runner = CliRunner()
#     result = runner.invoke(cli.main)
#     print(result.exit_code)
#     assert result.exit_code == 0
#     assert "tds2stac.cli.main" in result.output
#     help_result = runner.invoke(cli.main, ["--help"])
#     assert help_result.exit_code == 0
#     assert "--help  Show this message and exit." in help_result.output
