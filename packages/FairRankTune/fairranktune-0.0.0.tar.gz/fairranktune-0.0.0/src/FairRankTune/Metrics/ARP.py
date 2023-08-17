from FairRankTune.Metrics.ComboUtil import *
import pandas as pd

# Script to calculate ARP metric, using Cachel et al implementation
# Code References:  https://github.com/KCachel/MANI-Rank/blob/main/multi_fair/metrics.py
# References: Cachel, K., Rundensteiner, E., & Harrison, L. (2022, May). Mani-rank: Multiple attribute and intersectional group fairness for consensus ranking.
# In 2022 IEEE 38th International Conference on Data Engineering (ICDE) (pp. 1124-1137). IEEE.


def FPR(ranking_df, item_group_dict):
    """Compute the Favored Pair Representation of each group.
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :return fpr: python list of fpr score for each group (indexed by group id)"""

    unique_grps, grp_count_items = np.unique(
        list(item_group_dict.values()), return_counts=True
    )
    num_unique_rankings = len(ranking_df.columns)
    fpr = np.zeros_like(unique_grps, dtype=np.float64)

    for r in range(0, num_unique_rankings):
        single_ranking = ranking_df[ranking_df.columns[r]]  # isolate ranking
        single_ranking = np.array(
            single_ranking[~pd.isnull(single_ranking)]
        )  # drop any NaNs
        pair_cnt = pair_count_at_position_array(len(single_ranking))
        (
            groups_of_candidates,
            groups_of_single_ranking,
        ) = create_candidates_by_group_dict(single_ranking, item_group_dict)
        for i in np.unique(groups_of_single_ranking):
            cands = groups_of_candidates[i]
            grp_sz = len(cands)
            total_favored = int(0)
            for x in cands:
                indx_in_r = np.argwhere(single_ranking == x).flatten()[0]
                favored_pairs_at_pos = pair_cnt[indx_in_r]
                total_favored += int(favored_pairs_at_pos)

            favored_over_other_grp = total_favored - pair_count(grp_sz)  # numerator
            total_mixed_with_group = grp_sz * (
                len(single_ranking) - grp_sz
            )  # denominator
            fpr[i] += favored_over_other_grp / total_mixed_with_group

    return fpr, unique_grps


def ARP(ranking_df, item_group_dict, combo):
    """
    Calculate Attribute Rank Parity ARP (Cachel et al.).
    :param ranking_df: Pandas dataframe of ranking(s).
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :param combo: String for the aggregation metric used in calculating the meta metric.
    :return: ARP value, Dictionary of group FPR scores (groups are keys).
    """
    vals, unique_grps = np.asarray(FPR(ranking_df, item_group_dict))
    if combo == "MinMaxRatio":
        return MinMaxRatio(vals), dict(zip(unique_grps, vals))
    if combo == "MaxMinRatio":
        return MaxMinRatio(vals), dict(zip(unique_grps, vals))
    if combo == "MaxMinDiff":
        return MaxMinDiff(vals), dict(zip(unique_grps, vals))
    if combo == "MaxAbsDiff":
        return MaxAbsDiff(vals), dict(zip(unique_grps, vals))
    if combo == "MeanAbsDev":
        return MeanAbsDev(vals), dict(zip(unique_grps, vals))
    if combo == "LTwo":
        return LTwo(vals), dict(zip(unique_grps, vals))
    if combo == "Variance":
        return Variance(vals), dict(zip(unique_grps, vals))


def pair_count(num_candidates):
    """
    Calculate how many pairs are in a given ranking.
    :param num_candidates: Int, count of items being ranked.
    :return: Int, count of pairs.
    """
    return (num_candidates * (num_candidates - 1)) / 2


def create_candidates_by_group_dict(candidates, item_group_dict):
    """
    Function to create dictionary where keys are the group id and values are item id  ints instead of strings.
    :param candidates: Numpy array of candidates.
    :param item_group_dict: Dictionary of items (keys) and their group membership (values).
    :return: group_id_dict, candidate_grp
    """
    group_id_dict = {}
    candidate_grps = [item_group_dict[c] for c in candidates]

    for var in np.unique(candidate_grps):
        idx = np.where(candidate_grps == var)
        group_id_dict[(var)] = [
            item for item in candidates[idx].tolist()
        ]  # make it a list of ints
    return group_id_dict, candidate_grps


def pair_count_at_position_array(num_candidates):
    """
    Create a list with the count of pairs associated with each position.
    :param num_candidates: Int, number of items to be ranked.
    :return: List of pairs
    """
    return list(np.arange(num_candidates - 1, -1, -1))
