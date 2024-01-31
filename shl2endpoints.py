import xml.etree.ElementTree as ET
import argparse
import os

def remove_delimiters_from_mac(mac_address:str) -> str:
    legal_mac_chars = 'abcdefABCDEF0123456789'
    non_delimiter_mac = ''
    for ch in mac_address:
        if ch in legal_mac_chars:
            non_delimiter_mac += ch
    return non_delimiter_mac.lower()

def extract_endpoints_from_static_host_list(filename:str) -> list[str]:
    '''
    Extract endpoints from the given static host list xml and return a list of macs with no delimiter and lowercased characters.
    '''
    try:
        tree = ET.parse(filename)
    except:
        print(f'Could not open or read from {filename}. Check the filename and path.')
    root = tree.getroot()

    tips_ns = "{http://www.avendasys.com/tipsapiDefs/1.0}"
    shls = f'{tips_ns}StaticHostLists'
    shl = f'{tips_ns}StaticHostList'
    mac_addresses = []
    for tab in root.findall(shls):
        for host_list in tab.findall(shl):
            host_attribs = host_list.attrib
            if host_attribs['memberType'] == 'MACAddress' and host_attribs['memberFormat'] == 'list':
                for member in host_list.findall(f'{tips_ns}Members'):
                    for child_member in member:
                        cm_attribs = child_member.attrib
                        non_delimiter_mac = remove_delimiters_from_mac(cm_attribs['address'])
                        mac_addresses.append(non_delimiter_mac)
    return mac_addresses

def write_endpoints_xml(filename:str, endpoints_macs:list[str], version:str):
    '''
    Create the Endpoints XML file with the filename and MACs from the endpoints_macs list.
    '''
    custom_root = ET.Element('TipsContents', {'xmlns' : 'http://www.avendasys.com/tipsapiDefs/1.0'})
    ET.SubElement(custom_root, 'TipsHeader', {'version' : version})
    endpoints = ET.SubElement(custom_root, 'Endpoints')
    for mac in endpoints_macs:
        endpoint_attrib = {'macAddress': mac, 'status': 'Unknown'}
        ET.SubElement(endpoints, 'Endpoint', endpoint_attrib)
    with open(filename, mode='w', encoding='utf-8') as f:
        f.write(ET.tostring(custom_root).decode())


def main():

    parser = argparse.ArgumentParser(prog='shl2endpoint', description='reads from a static host list xml file and extracts the endpoints and prints them to and endpoints xml')
    parser.add_argument('-v', '--version', default="6.11", help="version of CPPM. Defaults to 6.11")
    parser.add_argument('-f', '--file', default='./StaticHostList.xml', help="the path to the static host list xml file. Defaults to StaticHostList.xml in current folder.")
    parser.add_argument('-o', '--output', default="generated_endpoints.xml", help="the name of the xml file to save the endpoints output to.")
    parser.add_argument('-d', '--directory', help="The filepath to a directory of files. Each file in the directory should be a static host list and their endpoints will be extracted into a separate file.")
    args = parser.parse_args()

    if not args.directory:
        macs = extract_endpoints_from_static_host_list(args.file)
        write_endpoints_xml(args.output, macs, args.version)
    else:
        if not os.path.exists(args.directory):
            print('The directory provided does not exist. Check the path.')
        else:
            for shl_file in os.listdir(args.directory):
                shl_file_path = os.path.join(args.directory, shl_file)
                splitted_filename = shl_file.split('.')
                if len(splitted_filename) >= 2 and 'xml' == splitted_filename[-1]:
                    output_name = ''.join(splitted_filename[:-1]) + '_Endpoints.xml'
                    print(f'extracting endpoints from {shl_file_path}')
                    macs = extract_endpoints_from_static_host_list(shl_file_path)
                    print(f'writing endpoints to {output_name}')
                    write_endpoints_xml(output_name, macs, args.version)

if __name__ == "__main__":
    main()