# shl2endpoints
extract endpoint info from a static host list and output to an endpoints xml file that can be imported into ClearPass

## Installation
Only standard libraries are used for this script so no pip install is required. It is written using python 3.10

## Usage
Run it as a python script:
`python shl2endpoints.py`
Note that depending on your platform, you might need to use python3 instead of python.
There are two optional flags that can be included:
1. -v or --version. This defines the version of CPPM to create the endpoints.xml for. Defaults to 6.11
2. -f or --file. This is a path to the static host lists xml file. Defaults to ./StaticHostList.xml

example with flags:
`python shl2endpoints.py -v 6.10 -f ../mystatichosts.xml`
