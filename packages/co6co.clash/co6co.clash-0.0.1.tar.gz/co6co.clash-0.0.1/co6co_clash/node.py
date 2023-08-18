# -*- coding: utf-8 -*-

from co6co.utils  import log 
from typing import List, Dict

def v2ray_to_clash(v2ray_node: dict)-> dict | None:
    """
    v2ray 转 clash
    """
    if v2ray_node==None or v2ray_node =={}:return None
    if v2ray_node.get('ps') is None and v2ray_node.get('add') is None and v2ray_node.get('port') is None \
       and v2ray_node.get('id') is None and v2ray_node.get('aid') is None:
        return None
    obj = {
        'name': v2ray_node.get('ps').strip() if v2ray_node.get('ps') else None, 
        'type': 'vmess',
        'server': v2ray_node.get('add').strip(),
        'port': int(v2ray_node.get('port')),
        'uuid': v2ray_node.get('id'),
        'alterId': int(v2ray_node.get('aid')),
        'cipher': 'auto',
        'udp': True,
        # 'network': item['net'] if item['net'] and item['net'] != 'tcp' else None,
        'network': v2ray_node.get('net'),
        'tls': True if v2ray_node.get('tls') == 'tls' else None,
        'ws-path': v2ray_node.get('path'),
        'ws-headers': {'Host': v2ray_node.get('host')} if v2ray_node.get('host') else None
    }
    # 删除为 None 的属性
    for key in list(obj.keys()):
        if obj.get(key) is None:
            del obj[key]
    # 增加 alterid 不为 空 的节点
    if obj.get('alterId') is not None:
        return  obj
            
    return None
 
def ss_to_clash(ss_node:dict)-> dict | None:
    """
    ss 节点转 clash
    """
    if ss_node==None or ss_node =={} : return None 
    node = {
        'name': ss_node.get('name').strip() if ss_node.get('name') else None,
        'type': 'ss',
        'server': ss_node.get('server').strip(),
        'port': int(ss_node.get('port')),
        'cipher': ss_node.get('method'),
        'password': ss_node.get('password'),
        'plugin': 'obfs' if ss_node.get('plugin') and ss_node.get('plugin').startswith('obfs') else None,
        'plugin-opts': {} if ss_node.get('plugin') else None
    }
    if ss_node.get('obfs'):
        node['plugin-opts']['mode'] = ss_node.get('obfs')
    if ss_node.get('obfs-host'):
        node['plugin-opts']['host'] = ss_node.get('obfs-host')
    for key in list(node.keys()):
        if node.get(key) is None:
            del node[key]
            
    return node
 
def ssr_to_clash(ssr_node:dict)->dict:
    """
    ssr 节点转换 
    """
    if ssr_node==None or ssr_node =={} : return None 
    cipher_tuple = ("aes-128-gcm", "aes-192-gcm", "aes-256-gcm", "aes-128-cfb", "aes-192-cfb", "aes-256-cfb", "aes-128-ctr", "aes-192-ctr", "aes-256-ctr",
            "rc4-md5","rc4",
            "chacha20","chacha20-ietf","xchacha20","chacha20-ietf-poly1305","plain" ,"http_simple","auth_sha1_v4","auth_aes128_md5",
            "auth_aes128_sha1","auth_chain_a","auth_chain_b")
    obj = {
        'name': ssr_node.get('remarks').strip() if ssr_node.get('remarks') else None,
        'type': 'ssr',
        'server': ssr_node.get('server').strip(),
        'port': int(ssr_node.get('port')),
        'cipher': ssr_node.get('method'),
        'password': ssr_node.get('password'),
        'obfs': ssr_node.get('obfs'),
        'protocol': ssr_node.get('protocol'),
        'obfs-param': ssr_node.get('obfsparam'),
        'protocol-param': ssr_node.get('protoparam'),
        'udp': True
    }
    try:
        for key in list(obj.keys()):
            if obj.get(key) is None:
                del obj[key] 
        if obj.get('name'): # 存在Name属性
            if obj['cipher'] in cipher_tuple:
                return obj
            else:log. warn(f"不支持的ssr 算法{ obj['cipher']}")
    except Exception as e:
        log.err(f'ssr 转换出错{e}')
    return None
 
def trojan_to_clash(trojan_node: dict)-> dict|None:
    """
    trojan 节点转 clash
    """
    return trojan_node
    