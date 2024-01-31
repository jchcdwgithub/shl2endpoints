import xml.etree.ElementTree as ET
import argparse

def main():

    parser = argparse.ArgumentParser(prog='shl2endpoint', description='reads from a static host list xml file and extracts the endpoints and prints them to and endpoints xml')
    parser.add_argument('-v', '--version', default="6.11", help="version of CPPM. Defaults to 6.11")
    parser.add_argument('-f', '--file', default='./StaticHostList.xml', help="the path to the static host list xml file. Defaults to StaticHostList.xml in current folder.")
    args = parser.parse_args()

    try:
        tree = ET.parse(args.file)
    except:
        print(f'Could not open or read from {args.file}. Check the filename and path.')
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
                        mac_addresses.append(cm_attribs['address'].replace('-','').lower())

    custom_root = ET.Element('TipsContents', {'xmlns' : 'http://www.avendasys.com/tipsapiDefs/1.0'})
    ET.SubElement(custom_root, 'TipsHeader', {'version' : args.version})
    endpoints = ET.SubElement(custom_root, 'Endpoints')
    for mac in mac_addresses:
        endpoint_attrib = {'macAddress': mac, 'status': 'Unknown'}
        ET.SubElement(endpoints, 'Endpoint', endpoint_attrib)
    with open('generated_endpoints.xml', mode='w', encoding='utf-8') as f:
        f.write(ET.tostring(custom_root).decode())

if __name__ == "__main__":
    main()