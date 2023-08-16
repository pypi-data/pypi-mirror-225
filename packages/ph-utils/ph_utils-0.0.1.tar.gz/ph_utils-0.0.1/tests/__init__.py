import ph_utils.date_utils as date_utils

def date_test():
    print(date_utils.parse())
    print(date_utils.parse('2023-08-14 15:23:23'))
    print(date_utils.parse('20230814 152323'))
    print(date_utils.parse('2023/08/14 15:23:23', '%Y/%m/%d %H:%M:%S'))
    print(date_utils.parse(1691997308))
    print(date_utils.parse(date_utils.parse()))
