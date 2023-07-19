import sys
from base_mod import file_handler as fh
from base_mod import platform_info as pi
from base_mod import auto_bench as ab
from base_mod import print_help as ph
import os
from datetime import datetime

## version info
version = 'v0.1'

## var
run_dir = os.getcwd()
now_date_detail = str(datetime.now())
now_date = str(datetime.now().strftime("%Y%m%d"))
config_file = str(f'{run_dir}/pg_autobench_conf.yaml')
config_data = None
pgbench_bin = str(os.environ['PGHOME'])+'/bin/pgbench'
round = 1
log_path = f'{run_dir}/pg_autobench_{now_date}.log'
log_level = 'INFO'
init_yn = False

# platform_info
platform_data = pi.get_platform_info()
os_name= platform_data['os']
os_detail = platform_data['os_detail']
cpu_brand = platform_data['cpu_brand']
cpu_arc = platform_data['cpu_arc']
physical_cores = platform_data['physical_cores']
logical_cores = platform_data['logical_cores']
memory_mega_bytes = platform_data['memory_mega_bytes']

## Main func
def parse_args(args):
    parsed_args = {}
    current_key = None
    for arg in args:
        if arg.startswith('--'):
            current_key = arg[2:]
            parsed_args[current_key] = []
        elif arg.startswith('-'):
            current_key = arg[1:]
            parsed_args[current_key] = []
        else:
            if current_key is not None:
                parsed_args[current_key].append(arg)
    return parsed_args


### get args
if __name__ == '__main__':
    args = sys.argv[1:]
    parsed_args = parse_args(args)
    parsed_keys = list(parsed_args.keys())

if 'f' in parsed_keys:
    config_file = parsed_args['f'][0]

if 'round' in parsed_keys:
    round = int(parsed_args['round'][0])

if 'i' in parsed_keys:
    init_yn = True

if 'h' or '?' or 'help' in parsed_keys:
    ph.print_help(version)

### exec area
if os.path.exists(pgbench_bin):
    if os.path.exists(config_file):
        config_data = fh.config_loader(config_file)
        if init_yn :
            ab.pgbench_init(config_data)
        else:
            origin = {}
            for i in range(round):
                new = ab.pgbench_to_dict(config_data)
                temp = dict.fromkeys(new.keys())
                if i == 0:
                    origin = ab.dict_merger(temp,new)
                else :
                    origin = ab.dict_merger(origin,new)
            fh.dict_to_csv(origin,f'{config_data["general_info"]["csv_output_path"]}/pg_autobench_{now_date}.csv')
            fh.log_writer(config_data['general_info']['log_path'],log_level,'pg_autobench run.')
    else:
        print(f'The config file could not be found in the default[{run_dir}] location.')
        print("Please use the -f option to specify the correct location of the config file.")
else:
    print('Can not find pgbench in $PGHOME/bin direcroty.')
    print('Please check pgbench is installed.')