from datetime import datetime,timedelta
from lib import read_config
logger= read_config.logger()
d=datetime.now()
print(str(d))
# time_after_2Years=d-timedelta(month=1)
# time_after_3Years=d+timedelta(days=1095)
# print("time after 2 years",str(time_after_2Years))
# print("time after 3 years",str(time_after_3Years))
# time_before_2Years=d-timedelta(days=730)
# time_before_3Years=d-timedelta(days=1095)
# print("time before 2 years",str(time_after_2Years))
# print("time before 3 years",str(time_after_3Years))
logger.info('hello')