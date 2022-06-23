from client import create_client_post_to_post, process_alpha, create_client_post_alpha
from distributor import *

import schedule, time, log




logger = log.get_logger(__name__)


if __name__ == "__main__":
    
    logger.info("Программа стартует")
    config = get_config() 
   

    client_5min = config['rate_5_min']['cl_table']
    client_hour = config['rate_1_hour']['cl_table']
    client_day = config['rate_1_day']['cl_table']
    
    # настройка по расписанию postgres -> opc -> postgres
    schedule.every(5).minutes.at(":00").do(create_client_post_to_post, client_5min)
    schedule.every().hour.at(f"{config['rate_1_hour']['cl_rate']}").do(create_client_post_to_post, client_hour)
    schedule.every().day.at(f"{config['rate_1_day']['cl_rate']}").do(create_client_post_to_post, client_day)

    #настройка по расписанию postgres -> opc
    schedule.every(int(config['ather_setting']['rate_data_to_alpha'])).seconds.do(create_client_post_alpha)

    while True:
        schedule.run_pending()
        time.sleep(1)
