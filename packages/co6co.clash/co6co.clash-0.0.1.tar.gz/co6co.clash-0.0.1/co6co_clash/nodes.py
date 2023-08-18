
import random 
import yaml

import co6co.utils as utils 
from .nodeLink import * 
from .node import *
from co6co.utils import log
from typing import List
  
  
def _getName(name)->str:
    '''
    取出空白，为None 随机名字
    '''
    name=name.strip() if name else None
    if name ==None: f"未知_{random.randrange(1,100000)}"
    pattern="\s+"
    return re.sub(pattern,'',name)
"""
yaml 文件 解析
"""
def _parseYaml(yamlContent): # 解析yaml文本
    '''
    解析yaml 文本
    生成 Nodes节点
    '''
    try:
        yml = yaml.load(yamlContent, Loader=yaml.FullLoader) 
        tmp_list = []
        # clash新字段
        if yml.get('proxies'):tmp_list = yml.get('proxies')
        # clash旧字段
        elif yml.get('Proxy'):tmp_list = yml.get('Proxy')
        else:log.warn('clash节点提取失败,clash节点为空') 
        return _parseYamlNode(tmp_list) 
    except:
        raise
def _parseYamlNode(nodes:list):
    '''
    解析Yaml文件中的node 节点
    nodes: yaml.get('proxies') 或者 yaml.get('Proxy')
    return :nodes 基本上也是返回 参数，仅作整理过滤
    '''
    nodes_list = []
    for node in nodes:
        node['name'] = _getName( node['name'])
        node['server']=node['server'].strip()
        # 对clashR的支持
        if node.get('protocolparam'):
            node['protocol-param'] = node['protocolparam']
            del node['protocolparam']
        if node.get('obfsparam'):
            node['obfs-param'] = node['obfsparam']
            del node['obfsparam']
        node['udp'] = True
        node['port'] = int(node['port']) 

        if node.get('name')==None: continue
        nodes_list.append(node)
    return nodes_list

"""
text 文件 解析
"""
def _parseNodeText(text:str| bytes): # 解析 从 base64 解析出来的文本 
    '''
    text: b64decode 解析出来的文本
    解析节点
    '''
    text_list = text.splitlines()
    
    #if type(text) == str: text_list=[itm.encode("utf-8") for itm  in text_list]
    return parser(text_list)

def parser(nodeUrls: List[str] | List[bytes])->List[dict]|None: 
    nodes_list= []
    for node in nodeUrls: 
        if type(node) == str: node =node.encode("utf-8") 
        try:
            denode=None
            toClashNode=None
            if is_vmess_node(node): 
                denode=decode_v2ray_node
                toClashNode=v2ray_to_clash
            elif is_ss_node(node):
                denode = decode_ss_node 
                toClashNode=ss_to_clash  
            elif is_ssr_node(node):
                denode = decode_ssr_node 
                toClashNode=ssr_to_clash  

            elif is_trojan_node(node):
                denode= decode_trojan_node 
                toClashNode=trojan_to_clash 
            else:
                continue 
            tmp_node = denode(node) 
            clash_node = toClashNode(tmp_node)
            clash_node['name'] = _getName(clash_node['name'])
            nodes_list.append(clash_node)
        except Exception as e:
            log.err(f'节点转换出错："{node}",{e}') 
            continue   
    if len(nodes_list) > 0: return nodes_list
    else: return None
        
def __check(nodesContent:str)->list|dict|str:
    try:
        yamlData=yaml.full_load(nodesContent)
        return yamlData
    except:
        return nodesContent
    
def parser_content(nodesContent:str)->List[dict]:
    """
    解析文本为 clash节点s
    """
    nodes_list = [] 
    try: 
        #
        yamlData =__check(nodesContent) 
        if type (yamlData) == dict: #yaml 格式
            #log.succ(f"{type(yamlData)}’yaml dict‘<--{addr}")
            nodes_list=_parseYaml(nodesContent)
        elif type (yamlData) == list and type(yamlData[0]) == dict: #yaml 格式中的节点
            #log.succ(f"{type(yamlData)} ’yaml list dict‘<--{addr}")
            nodes_list=_parseYamlNode(yamlData)
        else: # base64加密 or node list
            # log.succ(f"{type(yamlData)} ’TEXT‘<--{addr}")
            # base64 需要解密后内容 
            rawTxt = base64.b64decode(nodesContent) if utils.isBase64(nodesContent)else nodesContent 
            #log.err(f"{type(rawTxt)},\n{rawTxt}") 
            nodes_list=_parseNodeText(rawTxt)
    except Exception as e: 
        log.err(f'[-]解析节点失败:"{e}"' )  
    return nodes_list


