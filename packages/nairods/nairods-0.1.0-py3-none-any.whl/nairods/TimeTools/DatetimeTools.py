#! /usr/bin/env python
# -*-coding:utf-8-*-

# 简化时间类,方便查找
class TimeCurd(object):
    """
    时间的增删改查
    """

    def __init__(self):
        pass

    def current_time_ymd(self):
        """
        返回值为20230420
        主要用于创建文件夹
        :return: 20230420
        """
        from datetime import datetime
        current_date = datetime.now().strftime('%Y%m%d')
        return current_date

    def current_time_ymd_n(self, n):
        """
        当前时间往前推n天的日期
        :param n:  往前推的天数
        :return: 前推n天的年月日
        """
        import datetime

        # 获取当前日期
        today = datetime.datetime.now()
        # 计算前一天的日期
        n_day = datetime.timedelta(days=n)
        result = (today - n_day).strftime('%Y%m%d')
        # print(F'前{n}天的日期为:{result}')
        return result


# if __name__ == '__main__':
#     TC = TimeCurd()
#     TC.current_time_ymd()
#     TC.current_time_ymd_n(1)
