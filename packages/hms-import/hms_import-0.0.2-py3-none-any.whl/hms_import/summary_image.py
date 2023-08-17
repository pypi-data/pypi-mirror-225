from glob import iglob
import logging
import os
import re
from tempfile import NamedTemporaryFile
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
import tator


logger = logging.getLogger(__name__)
FONT = os.path.join(os.path.dirname(__file__), "Cascadia.ttf")
FONT_SIZE = 36


def create_summary_image(
    host: str,
    token: str,
    media_type: int,
    directory: str,
    sail_date: Optional[str] = None,
    land_date: Optional[str] = None,
    hdd_recv_date: Optional[str] = None,
    hdd_sn: Optional[str] = None,
) -> Tuple[int, str]:
    """Creates a summary image for a trip.

    :host: The Tator hostname
    :token: The Tator API token
    :media_type: The Tator media type to create
    :directory: The directory containing files to use to determine the vessel name
    :sail_date: The value for the Sail Date attribute
    :land_date: The value for the Land Date attribute
    :hdd_recv_date: The value for the HDD Date Received attribute
    :hdd_sn: The value for the HDD Serial Number attribute
    :returns: The id of the new image and the name of the newly created section

    """
    # Get the vessel name from the first filename found starting with `stream-`
    filename = os.path.basename(next(iglob(os.path.join(directory, f"stream-*"))))
    vessel_name = getattr(re.match(r"^stream-([^-]*)-.*$", filename), "groups", lambda: ("",))()[0]
    if not sail_date:
        sail_date = "N/A"
    if not land_date:
        land_date = "N/A"
    section_name = f"{vessel_name} - {sail_date}"
    summary_id = -1
    img_sz = 1024
    image_text = f"   Vessel: {vessel_name}\nSail Date: {sail_date}\nLand Date: {land_date}"
    font = ImageFont.truetype(font=FONT, size=FONT_SIZE)
    image = Image.new("RGB", (img_sz, img_sz), color="black")
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = draw.textbbox((0, 0), image_text, font=font)
    x_pos = (img_sz - (right - left)) // 2
    y_pos = (img_sz - (bottom - top)) // 2
    draw.text((x_pos, y_pos), image_text, fill="white", font=font)

    with NamedTemporaryFile(suffix=".png") as temp_file:
        image.save(temp_file.name)
        attrs = {
            "Vessel Name": vessel_name,
            "Sail Date": sail_date,
            "Land Date": land_date,
            "HDD Date Received": hdd_recv_date,
            "HDD Serial Number": hdd_sn,
        }

        import_media_args = {
            "api": tator.get_api(host=host, token=token),
            "type_id": media_type,
            "path": temp_file.name,
            "section": section_name,
            "fname": os.path.basename(temp_file.name),
            "attributes": {k: v for k, v in attrs.items() if v is not None},
        }

        response = None
        try:
            for progress, response in tator.util.upload_media(**import_media_args):
                logger.debug("Upload progress for %s: %d%%", temp_file.name, progress)
        except Exception:
            logger.error(
                "Could not create trip summary with args:\n%s", import_media_args, exc_info=True
            )

    if response and hasattr(response, "id") and response.id:
        summary_id = response.id
    return summary_id, section_name
