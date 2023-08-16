========
TDS2STAC
========

.. image:: https://codebase.helmholtz.cloud/cat4kit/tds2stac/-/raw/main/tds2stac-logo.png




=========

.. image:: https://img.shields.io/pypi/v/tds2stac.svg
        :target: https://pypi.python.org/pypi/tds2stac

.. image:: https://readthedocs.org/projects/tds2stac/badge/?version=latest
        :target: https://tds2stac.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



STAC specification is a method of exposing spatial and temporal data collections in a standardized manner. Specifically, the `SpatioTemporal Asset Catalog (STAC) <https://stacspec.org/en>`_ specification describes and catalogs spatiotemporal assets using a common structure. 
This package creates STAC metadata by harvesting dataset details from the `Thredds <https://www.unidata.ucar.edu/software/tds/>`_ data server. After creating STAC Catalogs, Collections, and Items, it imports them into `pgSTAC <https://stac-utils.github.io/pgstac/pgstac/>`_ and `STAC-FastAPI <https://stac-utils.github.io/stac-fastapi/>`_.

* Free software: EUPL-1.2
* Documentation: https://tds2stac.readthedocs.io.


Installation from PyPi
------------------------
.. code:: bash

   pip install tds2stac

Installation for development
--------------------------------
.. code:: bash

   git clone https://codebase.helmholtz.cloud/cat4kit/tds2stac.git
   cd tds2stac
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt


Installing using Docker
------------------------

For runnig by docker use `this <https://codebase.helmholtz.cloud/cat4kit/tds2stac-docker>`_ repository.


Usage
----------------
 
Use case:

You can use the following template for creating STAC catalog from the TDS web service for your project.

You can change configuration of PgSTAC in `config_pgstac <./tds2stac/config_pgstac.py>`_

.. code:: python

   from tds2stac.tds2stac import Converter

        from tds2stac import app

        app.Harvester("https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/climatology/catalog.html",
                stac = True,
                stac_id = "id",
                stac_description = "description",
                stac_dir = "/Users/hadizadeh-m/stac/",
                )

   output:

        INFO     2023-08-15 10:13:49,031         app.py @function __init__ line 123 - Start Scanning datasets
        Start Scanning datasets of https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/climatology/catalog.xml
        |__ https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/climatology/catalog.xml |  Number of branches:  2
        |_______ https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/climatology/0.05/catalog.xml |  Number of data:  1
        |_______ https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/climatology/0.1/catalog.xml |  Number of data:  1
        2 data are going to be set as items
        2 datasets are going to be set as collction
        INFO     2023-08-15 10:13:49,110         app.py @function __init__ line 196 - Harvesting datasets is started
        Start processing:  https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/climatology/0.05/catalog.xml
        2 / 2 STAC catalogs are created
        1 / 2 STAC items are connected to the related catalog
        100%|████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.82s/it]
        Start processing:  https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/climatology/0.1/catalog.xml
        2 / 2 STAC catalogs are created
        2 / 2 STAC items are connected to the related catalog
        100%|████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.40it/s]
        Start processing:  https://thredds.imk-ifu.kit.edu/thredds/catalog/regclim/raster/global/chirps/climatology/catalog.xml
        2 / 2 STAC catalogs are created
        2 / 2 STAC items are connected to the related catalog
        0it [00:00, ?it/s]
        INFO     2023-08-15 10:13:52,002         app.py @function __init__ line 247 - Harvesting datasets is finished

Copyright
---------
Copyright © 2023 Karlsruher Institut für Technologie

Licensed under the EUPL-1.2-or-later

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the EUPL-1.2 license for more details.

You should have received a copy of the EUPL-1.2 license along with this
program. If not, see https://www.eupl.eu/.
