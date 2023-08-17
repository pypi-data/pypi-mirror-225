#!/usr/bin/env python3

import concurrent.futures
from glob import glob
import hashlib
import logging
import os
from pprint import pformat
from typing import List

import tator
from tator.util._upload_file import _upload_file
from tqdm import tqdm


logger = logging.getLogger(__name__)


def _calculate_md5(file_path):
    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def _import_video(
    host: str,
    token: str,
    path: str,
    project_id: int,
    media_type: int,
    file_ids: List[int],
    section_name: str,
) -> int:
    tator_api = tator.get_api(host=host, token=token)

    # Upload encrypted file to Tator
    filename = os.path.basename(path)
    logger.debug("Uploading %s", filename)

    response = None
    try:
        for progress, response in _upload_file(tator_api, project_id, path=path, filename=filename):
            logger.debug("Upload progress: %.1f%%", progress)
    except Exception as exc:
        raise RuntimeError(f"Raised exception while uploading '{filename}', skipping") from exc

    if response is None or not hasattr(response, "key") or response.key is None:
        raise RuntimeError(f"Did not upload '{filename}', skipping")

    logger.debug("Uploading %s successful!", filename)

    # Create a media object containing the key to the uploaded file
    media_spec = {
        "type": media_type,
        "section": section_name,
        "name": filename,
        "md5": _calculate_md5(path),
        "attributes": {
            "encrypted_path": response.key,
            "related_files": ",".join(str(file_id) for file_id in file_ids),
        },
    }

    logger.debug(
        "Creating media object in project %d with media_spec=%s", project_id, pformat(media_spec)
    )
    try:
        response = tator_api.create_media_list(project_id, [media_spec])
    except Exception as exc:
        raise RuntimeError(f"Could not create media with {project_id=} and {media_spec=}") from exc

    result = response.id[0] if response and hasattr(response, "id") and response.id else 0
    return result


def import_videos(
    *,
    host: str,
    token: str,
    directory: str,
    media_ext: str,
    project_id: int,
    media_type: int,
    section_name: str,
    file_ids: List[int],
    max_workers: int,
) -> List[int]:
    """
    Finds all encrypted video files in `directory`, uploads them to Tator, and creates a media
    object referencing the upload. A future algorithm will be responsible for decrypting and
    transcoding them. Disallows use of positional arguments.

    :param host: The hostname of the Tator deployment to upload to.
    :type host: str
    :param token: The Tator API token to use for authentication.
    :type token: str
    :param directory: The directory to search for encrypted video files.
    :type directory: str
    :param media_ext: The extension of the encrypted video files.
    :type media_ext: str
    :param project_id: The integer id of the project to upload the videos to.
    :type project_id: int
    :param media_type: The integer id of the media type to create.
    :type media_type: int
    :param section_name: The name of the section to import the media to.
    :type section_name: str
    :param file_ids: The list of file ids to associate imported media with.
    :type file_ids: List[int]
    :param max_workers: The maximum number of threads to use
    :type max_workers: int
    """
    file_list = glob(os.path.join(directory, f"*{media_ext}-[0-9]*"))
    logger.debug("Found the following files:\n* %s", "\n* ".join(file_list))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                _import_video, host, token, filename, project_id, media_type, file_ids, section_name
            ): filename
            for filename in file_list
        }

        results = []
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="Video Imports",
            ncols=80,
        ):
            filename = futures[future]
            try:
                media_id = future.result()
            except Exception:
                logger.error("Failed to import '%s'", os.path.basename(filename), exc_info=True)
            else:
                if media_id:
                    results.append(media_id)
    return results
