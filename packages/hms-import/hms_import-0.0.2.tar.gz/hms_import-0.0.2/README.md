# HMS Import

Import utility for encrypted video and metadata files.

# Installation

## From Wheel

This assumes you have [Python 3.9+](https://www.python.org/downloads/) installed and `pip3` is on
your path. With the `hms-import.whl` file in your current directory, run:

```bash
~$ pip3 install ./hms-import.whl
...
~$ hms-import -h
usage: hms-import [-h] config_file

Script for uploading raw, encrypted video files.

positional arguments:
  config_file  The configuration .ini file used to initialize hms_import.

  options:
    -h, --help   show this help message and exit
```

## From Source

This assumes you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Python
3.9+](https://www.python.org/downloads/), and
[poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) installed
already.

```bash
~$ git clone git@github.com:cvisionai/hms.git
...
~$ cd hms/scripts/hms-import
hms-import$ poetry install
...
hms-import$ poetry run hms-import -h
```

# Usage

The first step is to set up your `config.ini` file. Start by copying the contents of
[sample_hms-config.ini](./sample_hms-config.ini) included below for reference, and replace the
default values:

```ini
[Local]
# The directory containing the video files for import
Directory=dir1
# The extension of the encrypted video files
MediaExtension=.video
# The extension of the encrypted metadata files
MetadataExtension=.log
# The maximum number of parallel processes to run, set to 1 to process serially
MaxWorkers=4

[Tator]
# The url to the tator deployment
Host=https://hms.tator.io
# The API token for tator
Token=6485c83cf040deadbeef07b7aea13706
# The integer id of the project to upload the videos to
ProjectId=-1
# The integer id of the media type to create, required if the project has more than one video media type
MediaType=-1
# The integer id of the file type to create for the uploaded encrypted sensor data file
FileType=-1
# The integer id of the image type to create for the trip summary image
SummaryType=-1
# The name of the algorithm to launch upon upload of each trup
AlgorithmName=Decrypt Trip

[Trip]
# The ISO-formatted, timezone aware (if applicable) sail date
SailDate=2023-07-15T19:46:16.671406+00:00
# The ISO-formatted, timezone aware (if applicable) land date
LandDate=2023-07-18T19:46:16.671406+00:00
# The ISO-formatted, timezone aware (if applicable) HDD receipt date
HddDateReceived=2023-07-19T19:46:16.671406+00:00
# The serial number of the hard drive
HddSerialNumber=123ABC
```

Once configured, you can run the import utility:

```bash
$ poetry run hms-import -h
usage: hms-import [-h] config_file

Script for uploading raw, encrypted video files.

positional arguments:
  config_file  The configuration .ini file used to initialize hms_import.

  options:
    -h, --help   show this help message and exit
```

## Troubleshooting

If an import fails, the logs have more detail than the console, they can be found in the same folder
the command was run from, with the filename `hms_import.log`. These are rotating logs that cycle
daily (if the log file is not current, it will have an `.MM-DD-YY` extension appended to the
filename) and are kept for up to 7 days, so as to not consume disk space without limit.
