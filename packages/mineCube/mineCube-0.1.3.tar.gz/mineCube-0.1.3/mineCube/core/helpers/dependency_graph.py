def dependency_graph(activities,follow_counter,double_follow_counter):
    dep_graph = [[0 for a in activities] for a in activities]
    short_loops = [[0 for a in activities] for a in activities]
    and_xor_observations = [[0 for a in activities] for a in activities]
    skipped_short_loops = [[0 for a in activities] for a in activities]

    for a1 in activities:
        for a2 in activities:
            a1_index = activities.index(a1)
            a2_index = activities.index(a2)
            dep_graph[a1_index][a2_index] = round(
                (follow_counter[a1_index][a2_index] - follow_counter[a2_index][a1_index]) / (
                            follow_counter[a1_index][a2_index] + follow_counter[a2_index][a1_index] + 1), 2)
            # handle Short loops
            # 1
            if a1_index == a2_index:
                short_loops[a1_index][a2_index] = round(
                    (follow_counter[a1_index][a1_index]) / (follow_counter[a1_index][a1_index] + 1), 2)

            # 2
            skipped_short_loops[a1_index][a2_index] = round(
                (double_follow_counter[a1_index][a2_index] + double_follow_counter[a2_index][a1_index]) / (
                            double_follow_counter[a1_index][a2_index] + double_follow_counter[a2_index][a1_index] + 1),
                2)

            # and_xor_patterns
            for a3 in activities:
                a3_index = activities.index(a3)
                and_xor_observations[a2_index][a3_index] = round(
                    (follow_counter[a2_index][a3_index] + follow_counter[a3_index][a2_index]) / (
                                follow_counter[a1_index][a3_index] + follow_counter[a1_index][a2_index] + 1), 2)

    return short_loops,dep_graph,and_xor_observations