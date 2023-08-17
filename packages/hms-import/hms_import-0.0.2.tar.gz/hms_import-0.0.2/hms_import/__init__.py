from argparse import ArgumentParser
from configparser import ConfigParser
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pprint import pformat

import tator

from .import_videos import import_videos
from .import_metadata import import_metadata
from .summary_image import create_summary_image

# Log info and up to console, everything to file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
file_handler = TimedRotatingFileHandler(
    os.path.join(os.getcwd(), f"{__name__.split('.')[0]}.log"), when="midnight", backupCount=7
)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s - %(levelname)s - %(name)s]: %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_parser():
    parser = ArgumentParser(description="Script for uploading raw, encrypted video files.")
    parser.add_argument(
        "config_file",
        type=str,
        help=f"The configuration .ini file used to initialize {__name__}.",
    )
    return parser


def validate_type_from_config(api, config, config_field, project_id, tator_type, list_filters=None):
    if tator_type not in ["media_type", "file_type"]:
        raise ValueError(f"Cannot validate {config_field=} for {tator_type=}")

    type_id = config["Tator"].getint(config_field, -1)
    if type_id > 0:
        try:
            getattr(api, f"get_{tator_type}")(type_id)
        except Exception as exc:
            raise ValueError(f"Could not find {config_field} with id {type_id}") from exc
    else:
        try:
            types = getattr(api, f"get_{tator_type}_list")(project_id)
        except Exception as exc:
            raise RuntimeError(f"Could not list {config_field}s from project {project_id}") from exc
        if list_filters:
            for attr, value in list_filters:
                types = [
                    _type
                    for _type in types
                    if hasattr(_type, attr) and getattr(_type, attr) == value
                ]
        if len(types) > 1:
            raise ValueError(
                f"Project {project_id} has more than one {config_field}, specify one of the "
                f"following in the config: {types}"
            )
        type_id = types[0].id
    return type_id


def main():
    # Parse arguments
    parser = get_parser()
    args = parser.parse_args()

    # Read and parse the config file
    logger.debug("Parsing config file %s", args.config_file)
    config = ConfigParser()
    config.read(args.config_file)

    # Validate config values
    host = config["Tator"]["Host"]
    token = config["Tator"]["Token"]
    project_id = config["Tator"].getint("ProjectId", -1)

    tator_api = tator.get_api(host=host, token=token)
    if project_id < 0:
        raise ValueError(f"Missing ProjectId value in the Tator section of the config file")
    try:
        tator_api.get_project(project_id)
    except Exception as exc:
        raise ValueError(f"Could not get project {project_id}") from exc

    file_type = validate_type_from_config(tator_api, config, "FileType", project_id, "file_type")
    media_type = validate_type_from_config(
        tator_api, config, "MediaType", project_id, "media_type", list_filters=[("dtype", "video")]
    )
    summary_type = validate_type_from_config(
        tator_api,
        config,
        "SummaryType",
        project_id,
        "media_type",
        list_filters=[("dtype", "image")],
    )
    directory = config["Local"]["Directory"]

    # Create trip summary image
    create_summary_kwargs = {
        "host": host,
        "media_type": summary_type,
        "directory": directory,
        "sail_date": config["Trip"].get("SailDate", None),
        "land_date": config["Trip"].get("LandDate", None),
        "hdd_recv_date": config["Trip"].get("HddDateReceived", None),
        "hdd_sn": config["Trip"].get("HddSerialNumber", None),
    }
    logger.debug("Creating trip summary with configuration %s", pformat(create_summary_kwargs))
    summary_id, section_name = create_summary_image(token=token, **create_summary_kwargs)
    logger.debug("Created trip summary (id %d; section %s)", summary_id, section_name)

    # Construct metadata argument dictionary for logging (do not log token for security)
    import_metadata_kwargs = {
        "host": host,
        "directory": directory,
        "max_workers": config["Local"].getint("MaxWorkers"),
        "project_id": project_id,
        "meta_ext": config["Local"]["MetadataExtension"],
        "file_type": file_type,
    }
    logger.debug("Starting metadata import with configuration %s", pformat(import_metadata_kwargs))
    file_ids = import_metadata(token=token, **import_metadata_kwargs)
    logger.debug("Metadata import complete!")

    # Construct video argument dictionary for logging (do not log token for security)
    import_video_kwargs = {
        "host": host,
        "directory": directory,
        "max_workers": config["Local"].getint("MaxWorkers"),
        "project_id": project_id,
        "file_ids": file_ids,
        "media_ext": config["Local"]["MediaExtension"],
        "media_type": media_type,
        "section_name": section_name,
    }
    logger.debug("Starting video import with configuration %s", pformat(import_video_kwargs))
    media_ids = import_videos(token=token, **import_video_kwargs)
    logger.debug("Video import complete!")
    logger.info("Created the following media: %s", pformat(media_ids))

    logger.info(
        "Launching decryption workflow for %d media objects and %d metadata files",
        len(media_ids),
        len(file_ids),
    )

    # Launch one workflow for all media ids
    algorithm_name = config["Tator"]["AlgorithmName"]
    job_spec = {"algorithm_name": algorithm_name, "media_ids": media_ids}
    try:
        response = tator_api.create_job_list(project=project_id, job_spec=job_spec)
    except Exception:
        logger.error(
            "Could not launch job with job_spec=%s in project %d",
            pformat(job_spec),
            project_id,
            exc_info=True,
        )
    else:
        logger.info(
            "Launched workflow %s on media %s (received response %s)",
            algorithm_name,
            pformat(media_ids),
            pformat(response),
        )
