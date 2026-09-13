def calculate_fairness(group_a_scores, group_b_scores):
    """
    Calculate the difference in average matching scores
    between two groups.
    """

    if len(group_a_scores) == 0 or len(group_b_scores) == 0:
        return 0

    average_a = sum(group_a_scores) / len(group_a_scores)
    average_b = sum(group_b_scores) / len(group_b_scores)

    difference = abs(average_a - average_b)

    return round(difference, 2)