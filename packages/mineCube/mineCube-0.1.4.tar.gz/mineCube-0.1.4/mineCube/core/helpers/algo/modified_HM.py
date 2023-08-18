def ModifiedHM(activities,old_follow_counter,new_follow_counter,short_loops,dep_graph,and_xor_observations,threshold=0.05,positive_observations=3,dependency_threshold=0.9,and_threshold=0.1,xor_threshold=0.1):
    # creating model based on previews
    # need thresholds for each one of those
    model = "graph LR\n"
    for a1 in activities:
        a1_index = activities.index(a1)
        for a2 in activities:
            a2_index = activities.index(a2)
            # check number of observations
            if old_follow_counter[a1_index][a2_index] >= positive_observations or new_follow_counter[a1_index][a2_index] >= positive_observations:
                if a1 == a2:
                    # check if there is any short loop
                    if short_loops[a1_index][a2_index] >= dependency_threshold:
                        model += f"{a1.replace(' ','_')}-->|{new_follow_counter[a1_index][a2_index]}|{a2.replace(' ','_')}\n"
                else:
                    # check if they are above dependecy treshold
                    if dep_graph[a1_index][a2_index] >= dependency_threshold:
                        model += f"{a1.replace(' ','_')}-->|{new_follow_counter[a1_index][a2_index]}|{a2.replace(' ','_')}\n"
        temp_model = []
        for e in model.split("\n"):
            if e not in temp_model:
                temp_model.append(e)

    model = "\n".join(temp_model)

    return model