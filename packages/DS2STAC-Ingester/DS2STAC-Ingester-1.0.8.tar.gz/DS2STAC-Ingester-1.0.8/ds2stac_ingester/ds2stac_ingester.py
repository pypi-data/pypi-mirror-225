"""Main module."""


import json
import logging
import os
import sys

from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods

from . import config_pgstac


class Ingester(object):
    def __init__(
        self,
        collection_id=None,  # STAC directory (*)
        stac_dir=None,  # STAC directory (*)
        logger_handler=None,  # Logger handler (*)
        logger_name=None,  # Logger name (*)
        logger_id=None,  # Logger id (*)
        logger_handler_host=None,  # Logger host (*)
        logger_handler_url=None,  # Logger url (*)
        API_posting=False,
    ):
        self.collection_id = collection_id
        self.logger_handler = logger_handler
        self.logger_name = logger_name
        self.logger_id = logger_id
        self.logger_handler_host = logger_handler_host
        self.logger_handler_url = logger_handler_url

        # using 'xml_processing' we get the catalog URL with
        # XML extension and catalog id and XML content of catalog.

        if self.logger_handler is None:
            self.logger = logging.getLogger("stream_handler")
            self.logger.setLevel(level=logging.DEBUG)
            # self.logger.setLevel(level=logging.WARNING)

            logStreamFormatter = logging.Formatter(
                fmt=f"%(levelname)-8s %(asctime)s \t %(filename)s @function %(funcName)s line %(lineno)s - %(message)s",
            )
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(logStreamFormatter)
            streamHandler.setLevel(logging.DEBUG)
            self.logger.addHandler(streamHandler)
        elif self.logger_handler == "HTTPHandler":
            self.logger = logging.getLogger(
                str(self.logger_name) + "_" + str(self.logger_id)
            )
            self.logger.setLevel(level=logging.DEBUG)
            # self.logger.setLevel(level=logging.WARNING)

            logHttpFormatter = logging.Formatter(
                fmt=f"%(levelname)-8s %(asctime)s \t %(filename)s @function %(funcName)s line %(lineno)s - %(message)s",
            )
            httpHandler = logging.handlers.HTTPHandler(
                host=self.logger_handler_host,
                url=self.logger_handler_url,
                method="POST",
            )
            httpHandler.setFormatter(logHttpFormatter)
            httpHandler.setLevel(logging.DEBUG)

            self.logger.addHandler(httpHandler)

        self.logger.info("Ingesting catalogs is started")
        if API_posting is False:
            """With enabling 'stac_catalog_dynamic' STAC catalogs
            , collections and items ingest into the 'pgSTAC'"""

            config_pgstac.run_all()  # This enables the confiduration of pgSTAC
            # First of all catalog should be opened
            f = open(os.path.join(stac_dir, "stac/catalog.json"))
            catalog_json = json.load(f)
            # pgSTAC database will be loaded here
            loader = Loader(db=PgstacDB(dsn=""))
            # Each collection and item that are linked to the catalog through 'links' is extracted.
            if self.collection_id is None:
                for dc in catalog_json["links"]:
                    # if dc["rel"] == "item":
                    #     try:
                    #         loader.load_items(
                    #             str(
                    #                 os.path.join(
                    #                     stac_dir,
                    #                     "stac/" + dc["href"].replace("./", ""),
                    #                 )
                    #             ),
                    #             Methods.insert,
                    #         )
                    #     except:
                    #         continue
                    #     print("|____", dc["href"])

                    # 'child' means Collection in Catalog json file
                    if dc["rel"] == "child":
                        self.ingest(
                            loader,
                            dc["href"],
                            stac_dir,
                            "stac/" + dc["href"].replace("./", ""),
                        )
            else:
                self.ingest(
                    loader,
                    self.collection_id,
                    stac_dir,
                    "stac/" + self.collection_id + "/collection.json",
                )
        self.logger.info("Ingesting catalogs is finished")
        self.logger.info("Job finished successfully! STAC catalog is created")

    def ingest(self, loaderx, param, stac_dirx, address_coll):
        """This is a function for ingesting collections
        into pgSTAC specifically for nested datasets"""

        f = open(os.path.join(stac_dirx, address_coll))
        collection_json_path = os.path.join(stac_dirx, address_coll)
        collection_json_data = json.load(f)

        item_collection_list = [
            ci["rel"] for ci in collection_json_data["links"]
        ]

        if (
            "child" in item_collection_list
        ):  # To ensure collection exists in 'links'
            item_collection_list = []  # Considered empty to prevent recursion

            for ci in collection_json_data["links"]:
                if ci["rel"] == "child":
                    try:
                        self.ingest(
                            loaderx,
                            ci["href"],
                            stac_dirx,
                            collection_json_path.replace(
                                "collection.json", "/"
                            )
                            + ci["href"].replace("./", ""),
                        )
                    except Exception:
                        (
                            ex_type,
                            ex_value,
                            ex_traceback,
                        ) = sys.exc_info()

                        self.logger.error(
                            "%s : %s" % (ex_type.__name__, ex_value)
                        )
                        continue
        else:
            item_collection_list = []  # Considered empty to prevent recursion
            loaderx.load_collections(
                str(os.path.join(stac_dirx, collection_json_path)),
                Methods.upsert,
            )

            print(collection_json_path.replace("collection.json", ""))
            for ci in collection_json_data["links"]:
                if ci["rel"] == "item":
                    try:
                        loaderx.load_items(
                            str(
                                os.path.join(
                                    stac_dirx,
                                    collection_json_path.replace(
                                        "collection.json", "/"
                                    )
                                    + ci["href"].replace("./", ""),
                                )
                            ),
                            Methods.upsert,
                        )
                        print("|____", ci["href"])
                    except Exception:
                        (
                            ex_type,
                            ex_value,
                            ex_traceback,
                        ) = sys.exc_info()

                        self.logger.error(
                            "%s : %s" % (ex_type.__name__, ex_value)
                        )
                        continue


class Deleter(object):
    def __init__(
        self,
        collection_id=None,
        stac_dir=None,  # STAC directory (*)
        logger_handler=None,  # Logger handler
        logger_name=None,  # Logger name
        logger_id=None,  # Logger id
        logger_handler_host=None,  # Logger host
        logger_handler_url=None,  # Logger url
        API_posting=False,
    ):
        self.collection_id = collection_id
        self.logger_handler = logger_handler
        self.logger_name = logger_name
        self.logger_id = logger_id
        self.logger_handler_host = logger_handler_host
        self.logger_handler_url = logger_handler_url

        # using 'xml_processing' we get the catalog URL with
        # XML extension and catalog id and XML content of catalog.

        if self.logger_handler is None:
            self.logger = logging.getLogger("stream_handler")
            self.logger.setLevel(level=logging.DEBUG)
            # self.logger.setLevel(level=logging.WARNING)

            logStreamFormatter = logging.Formatter(
                fmt=f"%(levelname)-8s %(asctime)s \t %(filename)s @function %(funcName)s line %(lineno)s - %(message)s",
            )
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(logStreamFormatter)
            streamHandler.setLevel(logging.DEBUG)
            self.logger.addHandler(streamHandler)
        elif self.logger_handler == "HTTPHandler":
            self.logger = logging.getLogger(
                str(self.logger_name) + "_" + str(self.logger_id)
            )
            self.logger.setLevel(level=logging.DEBUG)
            # self.logger.setLevel(level=logging.WARNING)

            logHttpFormatter = logging.Formatter(
                fmt=f"%(levelname)-8s %(asctime)s \t %(filename)s @function %(funcName)s line %(lineno)s - %(message)s",
            )
            httpHandler = logging.handlers.HTTPHandler(
                host=self.logger_handler_host,
                url=self.logger_handler_url,
                method="POST",
            )
            httpHandler.setFormatter(logHttpFormatter)
            httpHandler.setLevel(logging.DEBUG)

            self.logger.addHandler(httpHandler)

        self.logger.info("Deleting catalogs is started")
        if API_posting is False:
            """With enabling 'stac_catalog_dynamic' STAC catalogs
            , collections and items ingest into the 'pgSTAC'"""
            self.db = PgstacDB()

            # config_pgstac.run_all()  # This enables the confiduration of pgSTAC
            # First of all catalog should be opened
            f = open(os.path.join(stac_dir, "stac/catalog.json"))
            catalog_json = json.load(f)
            # pgSTAC database will be loaded here
            loader = Loader(db=PgstacDB(dsn=""))
            # Each collection and item that are linked to the catalog through 'links' is extracted.
            if self.collection_id is None:
                for dc in catalog_json["links"]:
                    if dc["rel"] == "child":
                        self.delete(
                            loader,
                            dc["href"],
                            stac_dir,
                            "stac/" + dc["href"].replace("./", ""),
                        )

            else:
                self.delete(
                    loader,
                    self.collection_id,
                    stac_dir,
                    "stac/" + self.collection_id + "/collection.json",
                )

        self.logger.info("Deleting catalogs is finished")

    def delete(self, loaderx, param, stac_dirx, address_coll):
        """This is a function for ingesting collections
        into pgSTAC specifically for nested datasets"""

        f = open(os.path.join(stac_dirx, address_coll))
        collection_json_path = os.path.join(stac_dirx, address_coll)
        collection_json_data = json.load(f)

        item_collection_list = [
            ci["rel"] for ci in collection_json_data["links"]
        ]

        if (
            "child" in item_collection_list
        ):  # To ensure collection exists in 'links'
            item_collection_list = []  # Considered empty to prevent recursion

            for ci in collection_json_data["links"]:
                if ci["rel"] == "child":
                    try:
                        self.delete(
                            loaderx,
                            ci["href"],
                            stac_dirx,
                            collection_json_path.replace(
                                "collection.json", "/"
                            )
                            + ci["href"].replace("./", ""),
                        )
                    except Exception:
                        (
                            ex_type,
                            ex_value,
                            ex_traceback,
                        ) = sys.exc_info()

                        self.logger.error(
                            "%s : %s" % (ex_type.__name__, ex_value)
                        )
                        continue
        else:
            item_collection_list = []  # Considered empty to prevent recursion

            print(param)
            for ci in collection_json_data["links"]:
                if ci["rel"] == "item":
                    try:
                        loaderx.load_items(
                            str(
                                os.path.join(
                                    stac_dirx,
                                    collection_json_path.replace(
                                        "collection.json", "/"
                                    )
                                    + ci["href"].replace("./", ""),
                                )
                            ),
                            Methods.delsert,
                        )
                        print("|____", ci["href"])
                    except Exception:
                        (
                            ex_type,
                            ex_value,
                            ex_traceback,
                        ) = sys.exc_info()

                        self.logger.error(
                            "%s : %s" % (ex_type.__name__, ex_value)
                        )
                        continue
        print(
            "collection_json_path.replace(collection.json, )",
            param.replace("/collection.json", "").replace("./", ""),
        )
        try:
            gen_collections = self.db.func(
                "delete_collection",
                param.replace("/collection.json", "").replace("./", ""),
            )
            for e in gen_collections:
                print("e", e)
        except:
            pass
