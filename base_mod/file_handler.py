import yaml
import pandas as pd
import logging

# log 파일 쓰기
def log_writer(log_path, log_level, log_message):
    logging.basicConfig(filename=log_path, level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s] : %(message)s')
    logger = logging.getLogger()
    if log_level == 'DEBUG':
        logger.debug(log_message)
    elif log_level == 'INFO':
        logger.info(log_message)
    elif log_level == 'WARNING':
        logger.warning(log_message)
    elif log_level == 'ERROR':
        logger.error(log_message)
    elif log_level == 'CRITICAL':
        logger.critical(log_message)

# YAML 파일 읽기
def config_loader(config_path):
    this_config_path = config_path
    with open(this_config_path, 'r', newline='') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

# CSV 파일 쓰기
def dict_to_csv(data, file_path):
    this_data = data
    this_file_path = file_path
    columns = ['pgbench version',
                'transaction type',
                'scaling factor',
                'partition method',
                'partitions',
                'query mode',
                'number of clients',
                'number of threads',
                'number of transactions actually processed',
                'latency average',
                'initial connection time',
                'tps'
    ]
    df = pd.DataFrame(this_data, columns=columns)
    df.to_csv(this_file_path, mode='a', header=False, index=False)
