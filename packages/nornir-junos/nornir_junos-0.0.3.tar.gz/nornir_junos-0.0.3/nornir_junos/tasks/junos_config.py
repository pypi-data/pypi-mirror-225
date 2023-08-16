from nornir.core.task import Result, Task
from nornir_junos.connections import CONNECTION_NAME
import logging
from .report import add_to_report

logger = logging.getLogger(__name__)

def junos_config(task: Task,  config: str, mode: str, format: str='set', commit_comments: str = '',  comfirm: int = 1, load_action='merge') -> Result:
    
    task.host['config'] = config
    if 'password' in config and mode == 'commit':
        report_list = [[mode, 'config', 'hidden because include password']]
    else:
        report_list = [[mode, 'config', config]]


    try:
        dev = task.host.get_connection(CONNECTION_NAME, task.nornir.config) # get connection
    except Exception as e:
        logger.error(str(e))
        report_list.append([mode,'Error',str(e)])
        add_to_report(task_host=task.host,report_list = report_list)
        return Result(host=task.host, diff='') 
    
    if mode == 'commit' and commit_comments == '':
        report_list.append([mode,'Error','No commit comments'])
    else:
        try:
            if mode =='compare':
                result = dev.junos_compare(config = task.host.data['config'], format = format, load_action = load_action)
                if result['diff'] == None:
                    task.host['compare'] = 'NO DIFF'
                else:
                    task.host['compare'] = result['diff']
                report_list.append([mode, 'compare',task.host['compare']])

            elif mode == 'commit':
                logger.debug(task.host.name + ' :committing')
                result  = dev.junos_commit(mode = 'private', config = task.host.data['config'], commit_comments = commit_comments, format = format, comfirm = comfirm, load_action = load_action)
                if result['diff'] == None:
                    task.host['compare'] = 'NO DIFF'
                else:
                    task.host['compare'] = result['diff']

                if result['committed']:
                    task.host['commit'] = 'Successful'
                    logger.debug(task.host.name + ' :Commit: Successful')
                else:
                    task.host['commit'] = 'Failed'
                    logger.debug(task.host.name + ' :Commit: Failed')
                report_list.append([mode, 'compare',task.host['compare']])
                report_list.append([mode, 'commit',task.host['commit']])
            elif mode == 'config_only':
                pass
            else:
                report_list.append([mode,'Error','Wrong mode'])

        except Exception as e:
            logger.error(str(e))
            report_list.append([mode,'Error',str(e)])
    
    add_to_report(task_host=task.host,report_list = report_list)
    return Result(host=task.host, diff=task.host.get('compare','')) 