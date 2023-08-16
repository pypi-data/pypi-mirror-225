from typing import List
from nornir.core.task import Result, Task
from nornir_junos.connections import CONNECTION_NAME
from .report import add_to_report
from lxml import etree
import logging
logger = logging.getLogger(__name__)

def node_values_list(xml_doc, xpath_expr):
    return [ x.text.strip() for x in xml_doc.xpath(xpath_expr) ]


def format_rpc(rpc_result):
    if isinstance(rpc_result,bool):
        return ''
    elif isinstance(rpc_result,str):
        return rpc_result
    else:
        return etree.tostring(rpc_result, encoding=str)

def junos_rpc(task: Task,rpc: str, to_str = 0, **kwargs):
    #result = task_host.get_connection("napalm", None).device.rpc['get_system_information']()
    try:
        dev = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
        result = dev.junos_rpc(rpc=rpc, to_str = to_str, **kwargs)
    except Exception as e:
        logger.error(str(e))
        result = str(e)
    report_list = [['RPC', rpc, format_rpc(result)]]
    add_to_report(task_host = task.host, report_list = report_list)
    return Result(host=task.host, result=result)