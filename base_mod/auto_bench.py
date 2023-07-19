import subprocess as sup
import re
import os
from collections import OrderedDict

def pgbench_runner(conf_dict):
    pgbench             = conf_dict['pgbench']
    connection_info     = conf_dict['connection_info']
    bench_info          = pgbench['bench_info']

    host                = str(connection_info['host'])
    user                = str(connection_info['user'])
    database            = str(connection_info['database'])
    client_num          = str(bench_info['client_num'])
    transaction_num     = str(bench_info['transaction_num'])

    with sup.Popen(['pgbench','-h',host,'-U',user,'-c',client_num,'-t',transaction_num,database], stdout=sup.PIPE) as bench_result:
        return bench_result.communicate()[0]

def pgbench_init(conf_dict):
    pgbench             = conf_dict['pgbench']
    connection_info     = conf_dict['connection_info']
    bench_init          = pgbench['bench_init']

    init_steps          = str(bench_init['init_steps'])
    partitions          = str(bench_init['partitions'])
    fillfactor          = str(bench_init['fillfactor'])
    database            = str(connection_info['database'])
    scale               = str(bench_init['scale'])

    with sup.Popen(['pgbench','--initialize',f'--init-steps={init_steps}',f'--partitions={partitions}','-F',fillfactor,'-s',scale,database], stdout=sup.PIPE) as bench_result:
        return_code = bench_result.returncode
        return [bench_result.communicate()[0],return_code]


def pgbench_to_dict(conf_dict):
    this_bench_result = pgbench_runner(conf_dict)
    print(this_bench_result)
    return_dic = OrderedDict()
    for i in this_bench_result.decode('utf-8').split('\n'):
        i = re.split(r"[:= ]",i)
        i = [value for value in i if value.strip()]
        if not i:
            continue
        if i[0] == 'pgbench':
            return_dic['pgbench version'] = re.sub(r"[()]","",i[1])
        elif i[0] == 'transaction':
            return_dic['transaction type'] = [i[3]]
        elif i[0] == 'scaling':
            return_dic['scaling factor'] = i[2]
        elif i[0] == 'partition':
            return_dic['partition method'] = i[2]
        elif i[0] == 'partitions':
            return_dic['partitions'] = i[1]
        elif i[0] == 'query':
            return_dic['query mode'] = i[2]
        elif i[0] == 'number' and i[2] == 'clients':
            return_dic['number of clients'] = i[3]
        elif i[0] == 'number' and i[2] == 'threads':
            return_dic['number of threads'] = i[3]
        elif i[0] == 'number' and i[2] == 'transactions':
            return_dic['number of transactions actually processed'] = i[5]
        elif i[0] == 'latency' and i[1] == 'average':
            return_dic['latency average'] = i[2]
        elif i[0] == 'initial' and i[1] == 'connection' and i[2] == 'time':
            return_dic['initial connection time'] = i[3]
        elif i[0] == 'tps':
            return_dic['tps'] = i[1]
    return return_dic

def dict_merger(dict1, dict2):
    result = OrderedDict()
    for key in set(dict1.keys()) | set(dict2.keys()):
        result[key] = []
        if key in dict1 and dict1[key]:
            result[key].extend(dict1[key] if isinstance(dict1[key], list) else [dict1[key]])
        if key in dict2 and dict2[key]:
            result[key].extend(dict2[key] if isinstance(dict2[key], list) else [dict2[key]])
    return result

def get_env():
    return os.environ
