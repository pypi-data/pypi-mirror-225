import sys
import co6co.utils.log as log
import json, base64, re
import urllib.parse
from typing import List, Dict


def _safe_decode(s: str) -> str:
    # print("saft_decode:",s)
    num = len(s) % 4
    if num:
        s += '=' * (4 - num)
    # print(f"s:{s},num:{num}")
    return base64.urlsafe_b64decode(s).decode('utf-8')

def str_to_bytes(s: str) -> bytes:
    return s.encode("utf-8")

def bytes_to_str(data: bytes) -> str:
    return data.decode('utf-8')

def is_v2ray_node(node_link: bytes) -> bool:
    return is_vmess_node(node_link)

def is_vmess_node(node_link: bytes) -> bool: 
    return node_link.startswith(b'vmess://') 
def is_ss_node(node_link: bytes) -> bool:
    return node_link.startswith(b'ss://')

def is_ssr_node(node_link: bytes) -> bool:
    return node_link.startswith(b'ssr://') 
def is_trojan_node(node_link: bytes) -> bool:
    return node_link.startswith(b'trojan://')

def decode_vmess_node(node_link: bytes) -> Dict | None:
    return decode_v2ray_node(node_link)
 
def decode_v2ray_node(node_link: bytes) -> Dict | None:
    """
    解析v2ray节点
    """ 
    if not is_v2ray_node(node_link):
        log.warn(f"不是v2ray节点:{node_link}")
        return None
    decode_proxy = node_link.decode('utf-8')[8:]
    if not decode_proxy or decode_proxy.isspace():
        return None
    proxy_str = base64.b64decode(decode_proxy).decode('utf-8')
    result = json.loads(proxy_str)
    return result

def decode_ss_node(node_link: bytes) -> Dict | None:
    """
    解析ss节点
    """
    if not is_ss_node(node_link):
        log.warn(f"不是ss节点:{node_link}")
        return None

    decode_proxy = node_link.decode('utf-8')[5:]
    if not decode_proxy or decode_proxy.isspace():
        log.info('ss节点信息为空')
        return None
    result = dict()
    param = decode_proxy
    if param.find('#') > -1:
        remark = urllib.parse.unquote(param[param.find('#') + 1:])
        result['name'] = remark
        param = param[:param.find('#')]
    if param.find('/?') > -1:
        plugin = urllib.parse.unquote(param[param.find('/?') + 2:])
        param = param[:param.find('/?')]
        for p in plugin.split(';'):
            key_value = p.split('=')
            result[key_value[0]] = key_value[1]
    if param.find('@') > -1:
        matcher = re.match(r'(.*?)@(.*):(.*)', param)
        if matcher:
            param = matcher.group(1)
            result['server'] = matcher.group(2).strip()
            result['port'] = matcher.group(3)
        else:
            return None
        matcher = re.match(
            r'(.*?):(.*)', _safe_decode(param))
        if matcher:
            result['method'] = matcher.group(1)
            result['password'] = matcher.group(2)
        else:
            return None
    else:
        matcher = re.match(r'(.*?):(.*)@(.*):(.*)',
                           _safe_decode(param))
        if matcher:
            result['method'] = matcher.group(1)
            result['password'] = matcher.group(2)
            result['server'] = matcher.group(3).strip()
            result['port'] = matcher.group(4)
        else:
            return None
    return result


def decode_ssr_node(node_link: bytes) -> Dict:
    """
    解析ssr节点
    """
    if not is_ssr_node(node_link):
        log.warn(f"不是ssr节点:{node_link}")
        return None

    decode_proxy = node_link.decode('utf-8')[6:] 
    if not decode_proxy or decode_proxy.isspace():
        log.warn('ssr节点信息为空，跳过该节点')
        return None
    proxy_str = _safe_decode(decode_proxy)
     
    parts = proxy_str.split(':') 
    if len(parts) != 6:
        log.info('该ssr节点解析失败，链接:{}'.format(node_link))
        return None
    result = {
        'server': parts[0].strip(),
        'port': parts[1],
        'protocol': parts[2],
        'method': parts[3],
        'obfs': parts[4]
    }
    password_params = parts[5].split('/?') 
    result['password'] = _safe_decode(password_params[0]) 
    params = password_params[1].split('&')
    for p in params:
        key_value = p.split('=') 
        if key_value[1] !=  None and key_value[1] !="":
            result[key_value[0]] = _safe_decode(key_value[1]) 
    return result


def decode_trojan_node(node_link: bytes) -> Dict | None:
    """
    解析Trojan节点
    """
    if not is_trojan_node(node_link):
        log.warn(f"不是trojan节点:{node_link}")
        return None
    result = dict()
    try:
        node_link = urllib.parse.unquote(bytes_to_str(node_link))
        parsed_url = node_link.replace('trojan://', '')
        part_list = re.split('#', parsed_url, maxsplit=1)
        result.setdefault('name', part_list[1])
        server_part = part_list[0].replace('trojan://', '')
        server_part_list = re.split(':|@|\?|&', server_part)
        result.setdefault('server', server_part_list[1].strip())
        result.setdefault('port', int(server_part_list[2]))
        result.setdefault('type', 'trojan')
        result.setdefault('password', server_part_list[0])
        server_part_list = server_part_list[3:]
        for config in server_part_list:
            if 'sni=' in config:
                result.setdefault('sni', config[4:])
            elif 'allowInsecure=' in config or 'tls=' in config:
                if config[-1] == 0:
                    result.setdefault('tls', False)
            elif 'type=' in config:
                if config[5:] != 'tcp':
                    result.setdefault('network', config[5:])
            elif 'path=' in config:
                result.setdefault('ws-path', config[5:])
            elif 'security=' in config:
                if config[9:] != 'tls':
                    result.setdefault('tls', False)
        result.setdefault('skip-cert-verify', True)
    except Exception as e:
        log.err(f"解析trojan出错{e}")
        return None

    return result
