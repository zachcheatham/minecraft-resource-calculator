import itertools

def merge_lists(list1, list2):
    new_list = list1 + list2

    existing = set()

    for i in range(0, len(new_list)):
        if new_list[i] in existing:
            new_list[i] = ""
        else:
            existing.add(new_list[i])

    return list(itertools.filterfalse(lambda x: x == "", new_list))
