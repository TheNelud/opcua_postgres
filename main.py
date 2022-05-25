from distributor import *
from client import create_client
import schedule, time, log

logger = log.get_logger(__name__)


if __name__ == "__main__":
    
    logger.info("Программа стартует")
    config = get_config()

    client_5min = config['rate_5_min']['cl_table']
    client_hour = config['rate_1_hour']['cl_table']
    client_day = config['rate_1_day']['cl_table']

    schedule.every(int(config['rate_5_min']['cl_rate'])).seconds.do(create_client,client_5min)
    schedule.every(int(config['rate_1_hour']['cl_rate'])).minutes.do(create_client,client_hour)
    schedule.every(int(config['rate_1_day']['cl_rate'])).hours.do(create_client,client_day)

    while True:
        schedule.run_pending()
        time.sleep(1)





