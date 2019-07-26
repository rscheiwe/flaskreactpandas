# Quick mapping function for low-yield modes

def custom_style(row):
    color = 'white'
    if row.values[-1] < 60:
        color = 'lightyellow'
    return ['background-color: %s' % color]*len(row.values)

# These first two should return the same results. Used to check accuracy of results.

# list1 should be `modes_without_abp_subset`
# list2 should be `loader_modes`
def safety_list(list1,list2):
    new_list = []
    for elem in list2: 
        if elem in list1 and elem not in new_list:
            new_list.append(elem)
    return new_list

# list1 should be `unique_modes_without_abp_subset`
# list2 should be `loader_modes`
def unique_list(list1,list2):
    new_list = []
    for elem in list2: 
        if elem in list1:
            new_list.append(elem)
    return new_list

# Used to find the discrepancies between `unique_modes_without_abp_subset` and the following `final_list`

# list1 should be `final_list`
# list2 should be `unique_modes_without_abp_subset`
def outlier_list(list1,list2):
    new_list = []
    for elem in list2: 
        if elem not in list1:
            new_list.append(elem)
    return new_list