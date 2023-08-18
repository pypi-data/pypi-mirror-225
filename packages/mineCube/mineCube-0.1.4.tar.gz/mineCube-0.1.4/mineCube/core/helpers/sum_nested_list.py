def add_nested_lists(offline, online,contribution_factor):
    # Check if both lists have the same dimensions
    if len(offline) != len(online) or any(len(inner) != len(online[0]) for inner in offline):
        raise ValueError("Both nested lists must have the same dimensions.")

    result = []
    for i in range(len(offline)):
        inner_result = []
        for j in range(len(offline[i])):
            inner_result.append(contribution_factor*offline[i][j] + (1-contribution_factor)*online[i][j])
        result.append(inner_result)

    return result