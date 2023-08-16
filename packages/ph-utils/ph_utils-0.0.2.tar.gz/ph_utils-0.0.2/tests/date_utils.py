import ph_utils.date_utils as date_utils

def date_parse():
    print(date_utils.parse())
    print(date_utils.parse('2023-08-14 15:23:23'))
    print(date_utils.parse('20230814 152323'))
    print(date_utils.parse('2023/08/14 15:23:23', '%Y/%m/%d %H:%M:%S'))
    print(date_utils.parse(1691997308))
    print(date_utils.parse(date_utils.parse()))

def date_set():
    date_utils.set(None, '20230815')

def date_diff():
    print(date_utils.diff(date_utils.subtract(delta={'days':1}), date_utils.parse()))

if __name__ == "__main__":
    print(date_utils.set(values='20230814121212'))
