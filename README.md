# shl2endpoints
extract endpoint info from a static host list and output to an endpoints xml file that can be imported into ClearPass

## Installation
Only standard libraries are used for this script so no pip install is required. It is written using python 3.10

## Usage
Run it as a python script:
`python shl2endpoints.py`
Note that depending on your platform, you might need to use python3 instead of python.
There are a few optional flags that can be included:
1. -v or --version. This defines the version of CPPM to create the endpoints.xml for. Defaults to 6.11
2. -f or --file. This is a path to the static host lists xml file. Defaults to ./StaticHostList.xml
3. -o or --output. This is the output file name where you want the endpoints XML to be written to.
4. -d or --directory. If provided, this will process all static host list XMLs within a given directory and output their results in the currrent directory.

example with flags:
`python shl2endpoints.py -v 6.10 -f ../mystatichosts.xml -o ./myendpoints.xml`

### Processing multiple static host files
If there is a need to process more than one static host file XML, place the files into a directory and provide the script with the -d or --directory flag.
The output files will be named the same as the static host files but with a _Endpoints appended to the name.

example:
`python shl2endpoints.py -d mydirectory`

If the contents of mydirectory is: shl1.xml, shl2.xml then the resulting endpoints files will be shl1_Endpoints.xml and shl2_Endpoints.xml.

The directory can be a relative or absolute path.
