def split_date_range(start_date, end_date, num=30):
    '''
    用于分割日期范围，每个子范围最多30天
    split_date_range("2023-01-04", "2023-05-20", num=30)
    [('2023-01-04', '2023-02-02'), ('2023-02-03', '2023-03-04'), ('2023-03-05', '2023-04-03'), ('2023-04-04', '2023-05-03'), ('2023-05-04', '2023-05-20')]

    :param num:
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 返回一个列表，每个元素是一个元组，元组的第一个元素是开始日期，第二个元素是结束日期
    使用场景:
    用于查询广告报表时，如果查询的日期范围超过30天，需要分割成多个子范围
    或是其他需要分割日期范围的场景,比如查询订单,因为日期限制等等
    '''
    date_format = "%Y-%m-%d"
    from datetime import datetime, timedelta
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    delta = end - start

    if delta.days > num:
        split_dates = []
        current_start = start
        while current_start + timedelta(days=num) < end:
            current_end = current_start + timedelta(days=num) - timedelta(days=1)
            split_dates.append((current_start.strftime(date_format), current_end.strftime(date_format)))
            current_start = current_end + timedelta(days=1)
        split_dates.append((current_start.strftime(date_format), end.strftime(date_format)))
        return split_dates
    else:
        return [(start_date, end_date)]


def get_date_str(days=0):
    import datetime
    current_date = datetime.datetime.now()
    return (current_date - datetime.timedelta(days=days)).strftime("%Y-%m-%d")

# 更新了阿里云的操作
# 获取当前的时间节点
def get_now_str():
    import datetime
    current_time = datetime.datetime.now().time()
    time_string = current_time.strftime("%H:%M:%S")
    return time_string


if __name__ == '__main__':
    # print(split_date_range("2023-01-04", "2023-05-20", num=30))
    print(get_date_str(1))
    print(get_now_str())
