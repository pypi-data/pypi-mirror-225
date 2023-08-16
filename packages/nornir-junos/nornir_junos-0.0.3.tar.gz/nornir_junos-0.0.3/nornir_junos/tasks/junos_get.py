from typing import List
from nornir.core.task import Result, Task
from nornir_junos.connections import CONNECTION_NAME
from lxml import etree
from collections import OrderedDict
import re
import logging
from .report import add_to_report

invaild_cmd = re.compile('^(request|clear|start|restart).*')
get_config = re.compile('^show configuration .*')

logger = logging.getLogger(__name__)

def junos_get(task: Task, commands: List[str]) -> Result:
    """
    Run commands on remote devices using vicmiko
    Arguments:
      commands: commands to execute
    Returns:
      Result object with the following attributes set:
        * result (``dict``): result of the commands execution
    """
    try:
      dev = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
      result = dev.junos_get(commands)
    except Exception as e:
        logger.error(str(e))
        result = {'Failed': str(e)}
    report_list = []
    for k,v in result.items():
      report_list.append(['collect', k, v])
    add_to_report(task_host = task.host,report_list = report_list)
    
    return Result(host=task.host, result=result)