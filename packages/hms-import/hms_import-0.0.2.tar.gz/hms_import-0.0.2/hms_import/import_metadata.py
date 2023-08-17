import concurrent.futures
from glob import glob
import logging
import os
from pprint import pformat

import tator
from tator.util._upload_file import _upload_file
from tqdm import tqdm

logger = logging.getLogger(__name__)


def _import_metadata(host: str, token: str, filename: str, project_id: int, file_type: int) -> int:
    tator_api = tator.get_api(host=host, token=token)

    # Upload encrypted file to Tator
    base_filename = os.path.basename(filename)

    # TODO replace vvv with use of `tator.util.upload_generic_file` when it is released
    file_spec = {
        "description": "Encrypted sensor data",
        "name": base_filename,
        "type": file_type,
        "attributes": {},  # Attributes is (erroneously) a required field
    }

    # Create the file object
    logger.debug("Creating File (file_type=%d) with file_spec=%s", file_type, pformat(file_spec))
    try:
        response = tator_api.create_file(project=project_id, file_spec=file_spec)
    except Exception as exc:
        raise RuntimeError(f"Raised exception while creating '{base_filename}', skipping") from exc

    # Upload the file to the created object
    file_id = response.id
    logger.debug("Uploading file %s with ID %d", base_filename, file_id)
    try:
        for progress, upload_info in _upload_file(
            api=tator_api, project=project_id, path=filename, file_id=file_id
        ):
            logger.debug("Upload progress: %.1f%%", progress)
    except Exception as exc:
        raise RuntimeError(f"Raised exception while uploading '{base_filename}', skipping") from exc

    # Update the file object's path value
    try:
        tator_api.update_file(id=response.id, file_update={"path": upload_info.key})
    except Exception as exc:
        raise RuntimeError(f"Raised exception while updating '{base_filename}', skipping") from exc
    # TODO replace ^^^ with use of `tator.util.upload_generic_file` when it is released
    # try:
    #     for progress, response in tator.util.upload_generic_file(tator_api, file_type, filename, "Encrypted sensor data", name=base_filename):
    #         logger.debug("Upload progress: %.1f%%", progress)
    # except Exception as exc:
    #     raise RuntimeError(f"Raised exception while uploading '{base_filename}', skipping") from exc
    # file_id = response.id

    return file_id


def import_metadata(
    *,
    host: str,
    token: str,
    directory: str,
    meta_ext: str,
    project_id: int,
    file_type: int,
    max_workers: int,
):
    """Finds all encrypted metadata files in `directory`, uploads them to Tator, and runs a workflow
    to decrypt and turn them into States. Disallows use of positional arguments.

    :param host: The hostname of the Tator deployment to upload to.
    :type host: str
    :param token: The Tator API token to use for authentication.
    :type token: str
    :param directory: The directory to search for encrypted metadata files.
    :type directory: str
    :param meta_ext: The extension of the encrypted metadata files.
    :type meta_ext: str
    :param project_id: The integer id of the project to upload the sensor data to.
    :type project_id: int
    :param max_workers: The maximum number of threads to use
    :type max_workers: int
    """
    file_list = glob(os.path.join(directory, f"*{meta_ext}-[0-9]*"))
    logger.debug("Found the following files:\n* %s", "\n* ".join(file_list))

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                _import_metadata, host, token, filename, project_id, file_type
            ): filename
            for filename in file_list
        }

        results = []
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="GPS Imports",
            ncols=80,
        ):
            filename = futures[future]
            try:
                file_id = future.result()
            except Exception:
                logger.error("Failed to import '%s'", os.path.basename(filename), exc_info=True)
            else:
                if file_id:
                    results.append(file_id)

    return results
