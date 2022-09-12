from ciscoconfparse import CiscoConfParse
import ipaddress, os, yaml

def parse (file):
    parse = CiscoConfParse(file, syntax='ios')

    vlans=[]
    device_spl = file.split(".", 1)
    device = device_spl[0].split('/')[-1]

    for intf_obj in parse.find_objects('^interface\sVlan'):

        int_name = intf_obj.re_match_typed('^interface\s+Vlan(\d+)$')

        int_ip = intf_obj.re_match_iter_typed(
            r'ip\saddress\s(\d+\.\d+\.\d+\.\d+)\s\S+$', result_type=str,
            group=1, default='')

        int_mask = intf_obj.re_match_iter_typed(
            r'ip\saddress\s(\d+\.\d+\.\d+\.\d+)\s(\d+\.\d+\.\d+\.\d+)', result_type=str,
            group=2, default='')

        int_ip2 = intf_obj.re_match_iter_typed(
            r'ip\saddress\s(\d+\.\d+\.\d+\.\d+)\s\S+\ssecondary$', result_type=str,
            group=1, default='')

        int_mask2 = intf_obj.re_match_iter_typed(
            r'ip\saddress\s(\d+\.\d+\.\d+\.\d+)\s(\d+\.\d+\.\d+\.\d+)\ssecondary$', result_type=str,
            group=2, default='')

        int_shut =  intf_obj.re_match_iter_typed(
            r'shutdown', result_type=str,
            group=0, default='')

        int_desc = intf_obj.re_match_iter_typed(
            r'description\s(\S+)', result_type=str,
            group=1, default='')

        int_acl_in = intf_obj.re_match_iter_typed(
            r'access-group\s(\S+)\sin', result_type=str,
            group=1, default='')

        int_acl_out = intf_obj.re_match_iter_typed(
            r'access-group\s(\S+)\sout', result_type=str,
            group=1, default='')

        if int_desc == '':
            int_desc = int_name

        if int_shut != 'shutdown' :
            if int_ip != '':
                vlan = {'vlan':int_name, 'ip': int_ip, 'mask': int_mask, 'ip2': int_ip2, 'mask2': int_mask2, 'desc': int_desc, 'acl_in': int_acl_in, 'acl_out': int_acl_out, 'sw':device}
                vlans.append(vlan)
    return vlans

def acls_dict(ip_add_src, ip_add_dst):

    conf_path  = '/usr/local/Cisco/confs/'
    files = ['dcm4500x','dcx4500x','spb4500e','msk4500e','vnukovo3750x','gorelovo3750x']

    summary = []


    for f in files:
        vlan_acl = parse(conf_path+f)
        summary = summary + vlan_acl


    naumen = {'acl_in':'','acl_out':''}

    for something in summary:
        src_ip = ipaddress.IPv4Interface(ip_add_src)
        dst_ip = ipaddress.IPv4Interface(ip_add_dst)
        mask = ipaddress.IPv4Network('0.0.0.0/'+something['mask']).prefixlen
        intrfc = ipaddress.IPv4Interface(something['ip']+'/'+str(mask))

        if dst_ip in intrfc.network :
            naumen['acl_out'] = something['acl_out']
            continue

        if src_ip in intrfc.network :
            naumen['acl_in'] = something['acl_in']
            continue
    print(naumen)
    return naumen

def acls(acs: list): 

    with open('/tftp/tftpboot/ACL_SECURITY/acl_devs.yaml') as f:
        acl_devs = yaml.safe_load(f)

    list_of_acl = {}

    for ac in acs:
        ac_dict = acls_dict(ac['source']['host'], ac['destination']['host'])
        if list_of_acl[ac_dict['acl_in']]:
            list_of_acl[ac_dict['acl_in']].append(ac)
        else:
            list_of_acl[ac_dict['acl_in']] = []
        if list_of_acl[ac_dict['acl_out']]:
            list_of_acl[ac_dict['acl_out']].append(ac)
        else:
            list_of_acl[ac_dict['acl_out']]=[]
    
    print(list_of_acl)

    for acl in list_of_acl.keys():
        dev = acl_devs[acl]

    

