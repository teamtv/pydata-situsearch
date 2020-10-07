from contextlib import contextmanager
from itertools import groupby
import pandas as pd
import numpy as np

import time

import scipy.stats as st

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


# from numba import jit


def match_that_frame(index_2_compare, Density_Results, search_scope):
    scaler = StandardScaler()

    Density_Results = Density_Results.reset_index(drop=True)
    Density_Results_columns = ["C" + str(f) for f in Density_Results.columns]

    with timeit("scale"):
        scaler.fit(Density_Results[0:search_scope])
        with timeit("transform 1"):
            scaled_df = scaler.transform(Density_Results.iloc[0:search_scope])

        with timeit("transform 2"):
            scaled_df_test = scaler.transform(Density_Results.iloc[index_2_compare:index_2_compare + 1])

    scaled_df = pd.DataFrame(data=scaled_df,  # values
                             columns=Density_Results_columns)

    scaled_df_test = pd.DataFrame(data=scaled_df_test,  # values
                                  columns=Density_Results_columns)

    with timeit("nn"):
        nbrs = NearestNeighbors(n_neighbors=len(scaled_df), algorithm='ball_tree').fit(scaled_df)
        distances, indices = nbrs.kneighbors(scaled_df_test)

    return distances, indices


def get_frames_from_tracking(tracking_data):
    unique_frames = tracking_data[tracking_data['ball_status'] == "Alive"]['frameID'].unique()

    offset = np.diff(unique_frames)

    breakID = [1]
    break_count = 1

    for i in range(len(unique_frames) - 1):

        if offset[i] < 24:
            breakID.append(break_count)
        else:
            break_count = break_count + 1
            breakID.append(break_count)

    frame_list = pd.DataFrame(
        {'unique_frames': unique_frames,
         'breakID': breakID,
         })

    # print(breakID)
    frames_to_assess = []

    for i in frame_list['breakID'].unique():
        subset = frame_list[frame_list['breakID'] == i]
        frames_ooo = subset.iloc[::12, :]['unique_frames']
        frames_to_assess.append(frames_ooo)

    # exit()

    frames_to_assess = [y for x in frames_to_assess for y in x]

    return frames_to_assess


@contextmanager
def timeit(desc):
    start = time.time()
    try:
        yield
    finally:
        took = time.time() - start
        print("Took", desc, took)


# @jit(nopython=False)
# def gaussian_kde(values, positions):


from multiprocessing import Pool

xmin = -5500
xmax = 5500
ymin = -3400
ymax = 3400

# Create meshgrid
lin_x = np.linspace(xmin, xmax, 105)
lin_y = np.linspace(ymin, ymax, 68)
xx, yy = np.meshgrid(lin_x, lin_y)
# xx, yy = np.mgrid[xmin:xmax:105j, ymin:ymax:68j]

positions = np.vstack([xx.ravel(), yy.ravel()])


# @jit(nopython=False)
def guassian_kde(args):
    index, team1, team2 = args
    # if  True:
    # if len(team1) == 0:
    # print(team1)
    values = np.array(team1)
    kernel = st.gaussian_kde(values)
    f1 = np.reshape(
        kernel(positions).T,
        xx.shape)

    values = np.array(team2)
    kernel = st.gaussian_kde(values)
    f2 = np.reshape(
        kernel(positions).T,
        xx.shape)

    return (index, f1.flatten('C'), f2.flatten('C'))


def density_me_pockets(data_frame, frames_to_assess_parsed):
    with timeit("density_me_pockets"):
        with timeit("preparing"):
            rowsAD = np.zeros(
                [len(frames_to_assess_parsed), 7140],
                dtype=np.float64
            )

            rowsDD = np.zeros(
                [len(frames_to_assess_parsed), 7140],
                dtype=np.float64
            )

            frames_to_assess_parsed = set(frames_to_assess_parsed)

        with timeit("calculating"):
            pool = Pool(5)

            def iter():
                index = 0
                # frameID=1541327.0, ball_owning_team='H', team=1.0, ball_status='Alive', x=-31.0, y=1844.0, attacking_direction=1
                for frame_id, rows in groupby(data_frame.itertuples(index=False, name=None), key=lambda row: row[0]):
                    if frame_id not in frames_to_assess_parsed:
                        continue

                    rows = list(rows)
                    if rows[0][1] == 'H':
                        attacking_players = [player for player in rows if player[2] == 0]
                        defending_players = [player for player in rows if player[2] == 1]
                    else:
                        attacking_players = [player for player in rows if player[2] == 1]
                        defending_players = [player for player in rows if player[2] == 0]

                    # attacking direction
                    if attacking_players[0][6] == 1:
                        direction_correction_mult = -1
                    else:
                        direction_correction_mult = 1

                    attacking_team = list(zip(*[
                        (
                            # x
                            player[4] * direction_correction_mult,
                            # y
                            player[5] * direction_correction_mult
                        )
                        for player in attacking_players
                    ]))
                    defending_team = list(zip(*[
                        (
                            # x
                            player[4] * direction_correction_mult,
                            # y
                            player[5] * direction_correction_mult
                        )
                        for player in defending_players
                    ]))

                    yield (index, attacking_team, defending_team)

                    index += 1

                # result = pool.apply_async(guassian_kde, (index, attacking_team, defending_team), callback=update_me)
                # res.append(result)
                # index += 1

            for index, attacker_density, defender_density in pool.imap_unordered(guassian_kde, iter()):
                rowsAD[index, :] = attacker_density
                rowsDD[index, :] = defender_density

            pool.close()
            pool.join()

        with timeit("finalizing"):
            attacker_density_results = pd.DataFrame(data=rowsAD)

            defender_density_results = pd.DataFrame(data=rowsDD)

    return attacker_density_results, defender_density_results


def keep_your_distance(FRAME_TO_MATCH_, AttackerDensity_Results, DefenderDensity_Results, search_scope):
    distances, indices = match_that_frame(FRAME_TO_MATCH_, AttackerDensity_Results, search_scope)

    attack_summary = pd.DataFrame(
        {'frameIndex': indices[0],
         'attack_distances': distances[0]})

    distances, indices = match_that_frame(FRAME_TO_MATCH_, DefenderDensity_Results, search_scope)

    defence_summary = pd.DataFrame(
        {'frameIndex': indices[0],
         'defence_distances': distances[0]})

    distance_summary = attack_summary.merge(defence_summary, on='frameIndex')

    distance_summary['total_distance'] = distance_summary['defence_distances'] + distance_summary['attack_distances']

    distance_summary = distance_summary.sort_values(by=['total_distance'])

    return (distance_summary)


def weight_those_buggers(distance_summary2, weighting):
    distance_summary2['attack_distances_adj'] = distance_summary2['attack_distances'] * weighting
    distance_summary2['defence_distances_adj'] = distance_summary2['defence_distances'] * (1 - weighting)
    distance_summary2['total_adj'] = distance_summary2['defence_distances_adj'] + distance_summary2[
        'attack_distances_adj']

    distance_summary2 = distance_summary2.sort_values(by=['total_adj']).reset_index(drop=True)
    return (distance_summary2)