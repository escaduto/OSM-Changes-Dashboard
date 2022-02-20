import datetime
from datetime import date, datetime, timedelta

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

def generateDSList(time_interval, start_yr, start_mth, start_dt, end_yr, end_mth, end_dt):
    dts = [dt.strftime('%Y-%m-%dT%H:%M:%SZ') for dt in 
        datetime_range(datetime(start_yr, start_mth, start_dt, 0), datetime(end_yr, end_mth, end_dt, 0), 
        timedelta(hours=time_interval))]
    return dts

def retrieve_DS_List(interval, start_yr, start_mnth, start_dt, end_yr, end_mnth, end_dt):
    '''
    Create a list of start and end dates by interval
    '''
    dts = generateDSList(interval, start_yr, start_mnth, start_dt, end_yr, end_mnth, end_dt)
    start_dt_list = [] 
    end_dt_list = []

    for i in range(0, len(dts) - 1): 
        start_dt_list.append(dts[i])
        end_dt_list.append(dts[i+1])

    start_end_ds = list(zip(start_dt_list, end_dt_list))
    return start_end_ds 
