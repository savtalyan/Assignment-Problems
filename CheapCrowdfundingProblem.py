

# this function will return the minimum pledge amount from the submitted list
def find_min_pledge(pledge_list):
    
    # changing the type to set to get only unique values
    pledge_set = set(pledge_list)

    # finding the smallest positive integer which is not in the list
    min_pledge = 1
    while min_pledge in pledge_set:
        min_pledge+=1
    
    return min_pledge