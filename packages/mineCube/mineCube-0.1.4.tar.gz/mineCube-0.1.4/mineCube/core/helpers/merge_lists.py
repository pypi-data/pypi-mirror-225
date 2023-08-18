from collections import OrderedDict
def merge_lists(list1,list2):
    return list(OrderedDict.fromkeys(list1 + list2))