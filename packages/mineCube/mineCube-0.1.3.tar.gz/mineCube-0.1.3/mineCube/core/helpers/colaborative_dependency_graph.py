def collaborative_dependency_graph(activities, old_follow_counter, new_follow_counter, old_double_follow_counter, new_double_follow_counter , contribution_factor=0.5):
    dep_graph = [[0 for a in activities] for a in activities]
    short_loops = [[0 for a in activities] for a in activities]
    and_xor_observations = [[0 for a in activities] for a in activities]
    skipped_short_loops = [[0 for a in activities] for a in activities]

    for a1 in activities:
        a1_index = activities.index(a1)
        for a2 in activities:
            a2_index = activities.index(a2)
            # the collaborative dep graph
            dep_graph[a1_index][a2_index] = round(
                (contribution_factor*(old_follow_counter[a1_index][a2_index]-old_follow_counter[a2_index][a1_index]) +
                 (1-contribution_factor)*(new_follow_counter[a1_index][a2_index]-new_follow_counter[a2_index][a1_index])) /
                (contribution_factor*(old_follow_counter[a1_index][a2_index]+old_follow_counter[a2_index][a1_index]) +
                 (1-contribution_factor)*(new_follow_counter[a1_index][a2_index]+new_follow_counter[a2_index][a1_index]) + 1), 2)
            # handle Short loops
            # 1
            # TODO::: reimplement this calculation it's wrong
            if a1_index == a2_index:
                short_loops[a1_index][a2_index] = round(
                    (contribution_factor*old_follow_counter[a1_index][a1_index] + (1-contribution_factor)*new_follow_counter[a1_index][a1_index]) /
                    (contribution_factor*old_follow_counter[a1_index][a1_index] + (1-contribution_factor)*new_follow_counter[a1_index][a1_index] + 1), 2)
            # 2
            skipped_short_loops[a1_index][a2_index] = round(
                (contribution_factor*(old_double_follow_counter[a1_index][a2_index]+old_double_follow_counter[a2_index][a1_index]) +
                 (1-contribution_factor)*(new_double_follow_counter[a2_index][a1_index]+new_double_follow_counter[a1_index][a2_index])) /
                (contribution_factor*(old_double_follow_counter[a1_index][a2_index]+old_double_follow_counter[a2_index][a1_index]) +
                 (1-contribution_factor)*(new_double_follow_counter[a2_index][a1_index]+new_double_follow_counter[a1_index][a2_index]) + 1), 2)

            # and_xor_patterns
            for a3 in activities:
                a3_index = activities.index(a3)
                and_xor_observations[a2_index][a3_index] = round(
                    (contribution_factor*old_follow_counter[a2_index][a3_index] + (1-contribution_factor)*new_follow_counter[a3_index][a2_index]) /
                    (contribution_factor*old_follow_counter[a1_index][a3_index] + (1-contribution_factor)*new_follow_counter[a1_index][a2_index] + 1), 2)

    return short_loops, dep_graph, and_xor_observations
