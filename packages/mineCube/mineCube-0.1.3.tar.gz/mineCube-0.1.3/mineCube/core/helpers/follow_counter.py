def follow_count(transactions, activities):
    follow_counter = [[0 for a in activities] for a in activities]
    double_follow_counter = [[0 for a in activities] for a in activities]
    for trace in transactions:
        for i, e in enumerate(trace):
            curr_index = activities.index(e)
            if i + 1 < len(trace):
                next_index = activities.index(trace[i + 1])
                follow_counter[curr_index][next_index] += 1
            # double follow  counter
            if i + 2 < len(trace):
                next_index = activities.index(trace[i + 2])
                double_follow_counter[curr_index][next_index] += 1
    return follow_counter, double_follow_counter
