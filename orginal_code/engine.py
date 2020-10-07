
## set some variables
FRAME_TO_MATCH = 200
search_scope = 2500
matching_weight = 0.5 # defenders 0.0 - 1.0 attackers (0.5 - no weighting)
clear_window = 30 # minimum seconds between matched frames

## read data
tdat = pd.read_hdf(glob.glob("Datasets/2018_19/parsed_tracab/*.h5")[1])
game_id = glob.glob("Datasets/2018_19/parsed_tracab/*.h5")[1].split("/")[3].split("_")[0]

## get list of frames to include in the match
frames_to_assess = get_frames_from_tracking(tdat)


## calculate the densities for each frame
AttackerDensity_Results, DefenderDensity_Results = density_me_pockets(frames_to_assess[0:search_scope])

## get the distances for the frame selected to mattch
distance_summary = keep_your_distance(FRAME_TO_MATCH, AttackerDensity_Results, DefenderDensity_Results, search_scope)

## match and filter
frames_to_present = [int(distance_summary.frameIndex.iloc[0])]
for i in distance_summary.frameIndex:
    selected_frame = int(distance_summary.frameIndex.iloc[0])
    include = 0

    for j in frames_to_present:

        if i in frames_to_present or ( j -clear_window) <= i <= ( j +clear_window):
            include = include + 1

    if include == 0:
        frames_to_present.append(i)

## drop frames that aren't to be included
distance_summary = distance_summary[distance_summary['frameIndex'].isin(frames_to_present)].reset_index(drop=True)

## apply the matching weights # 0 all defence - 1 all attack
distance_summary = weight_those_buggers(distance_summary, matching_weight)


## add frameID to distance summary
list_of_frameIDs = []
for i in distance_summary['frameIndex']:
    list_of_frameIDs.append(frames_to_assess[i])
distance_summary['frameID'] = list_of_frameIDs

## add distance to the ball

ball_only = tdat[tdat['team'] == 10][['frameID', 'x', 'y']]
ball_only = ball_only[ball_only['frameID'].isin(frames_to_assess)].reset_index(drop=True)

distance_summary = distance_summary.merge(ball_only, on = "frameID")
distance_summary['ball_x'] = distance_summary.iloc[0]['x']
distance_summary['ball_y'] = distance_summary.iloc[0]['y']

distance_summary['ball_location_difference'] = distance_summary[['x', 'y']].sub \
    (np.array([distance_summary.iloc[0]['x'] , distance_summary.iloc[0]['y']])).pow(2).sum(1).pow(0.5)

## plot the frame and the best 3 matches
plot_pitch_frame_both(distance_summary['frameID'].iloc[0])
plot_pitch_frame_both(distance_summary['frameID'].iloc[1])
plot_pitch_frame_both(distance_summary['frameID'].iloc[2])
plot_pitch_frame_both(distance_summary['frameID'].iloc[3])


