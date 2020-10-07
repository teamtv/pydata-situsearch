def match_that_frame(index_2_compare, Density_Results, search_scope):
    scaler = StandardScaler()

    Density_Results = Density_Results.reset_index(drop=True)
    Density_Results_columns = ["C" + str(f) for f in Density_Results.columns]

    scaler.fit(Density_Results[0:search_scope])
    scaled_df = scaler.transform(Density_Results.iloc[0:search_scope])
    scaled_df_test = scaler.transform(Density_Results.iloc[index_2_compare:index_2_compare + 1])

    scaled_df = pd.DataFrame(data=scaled_df,  # values
                             columns=Density_Results_columns)

    scaled_df_test = pd.DataFrame(data=scaled_df_test,  # values
                                  columns=Density_Results_columns)

    nbrs = NearestNeighbors(n_neighbors=len(scaled_df), algorithm='ball_tree').fit(scaled_df)
    distances, indices = nbrs.kneighbors(scaled_df_test)

    return (distances, indices)


def prepare_frame(frameID):
    frame = tdat[tdat['frameID'] == frameID].reset_index(drop=True)

    if frame['ball_owning_team'].iloc[0] == "H":
        team_in_possession = 1
        direction = frame[frame['team'] == team_in_possession].reset_index(drop=True).iloc[0].attacking_direction
    else:
        team_in_possession = 0
        direction = frame[frame['team'] == team_in_possession].reset_index(drop=True).iloc[0].attacking_direction

    if direction == 1:
        frame['x'] = [f * -1 for f in frame['x']]
        frame['y'] = [f * -1 for f in frame['y']]

    return (frame)


def calculateDD(frame_df):
    if frame_df['ball_owning_team'].iloc[0] == "H":
        team_in_possession = 1
    else:
        team_in_possession = 0

    frame_df = frame_df[frame_df['team'] != team_in_possession]

    x = frame_df['x']
    y = frame_df['y']

    deltaX = (max(x) - min(x)) / 200
    deltaY = (max(y) - min(y)) / 200

    xmin = -5500
    xmax = 5500
    ymin = -3400
    ymax = 3400

    # Create meshgrid
    xx, yy = np.mgrid[xmin:xmax:105j, ymin:ymax:68j]

    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x, y])
    kernel = st.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)
    f = f.flatten('C')
    return (f)


def calculateAD(frame_df):
    if frame_df['ball_owning_team'].iloc[0] == "H":
        team_in_possession = 1
    else:
        team_in_possession = 0

    frame_df = frame_df[frame_df['team'] == team_in_possession]

    x = frame_df['x']
    y = frame_df['y']
    deltaX = (max(x) - min(x)) / 200
    deltaY = (max(y) - min(y)) / 200

    xmin = -5500
    xmax = 5500
    ymin = -3400
    ymax = 3400

    # Create meshgrid
    xx, yy = np.mgrid[xmin:xmax:105j, ymin:ymax:68j]

    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x, y])
    kernel = st.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)
    f = f.flatten('C')
    return (f)


def plotAttackerDensity(frame_to_calculate, tracking_data):
    frame = tracking_data[tracking_data['frameID'] == frame_to_calculate]

    if frame['ball_owning_team'].iloc[0] == "H":
        team_in_possession = 1
        direction = frame[frame['team'] == team_in_possession].reset_index(drop=True).iloc[0].attacking_direction
    else:
        team_in_possession = 0
        direction = frame[frame['team'] == team_in_possession].reset_index(drop=True).iloc[0].attacking_direction

    frame = frame[frame['team'] == team_in_possession]

    x = frame['x']
    y = frame['y']

    deltaX = (max(x) - min(x)) / 200
    deltaY = (max(y) - min(y)) / 200

    xmin = -5500
    xmax = 5500
    ymin = -3400
    ymax = 3400

    # Create meshgrid
    xx, yy = np.mgrid[xmin:xmax:210j, ymin:ymax:136j]

    positions = np.vstack([xx.ravel(), yy.ravel()])
    values = np.vstack([x, y])
    kernel = st.gaussian_kde(values)
    f = np.reshape(kernel(positions).T, xx.shape)

    fig = plt.figure(figsize=(16, 10))

    ax = Axes3D(fig)  # <-- Note the difference from your original code...
    surf = ax.plot_surface(xx, yy, f, rstride=1, cstride=1, cmap='coolwarm', edgecolor='none')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(xmax, xmin)
    ax.set_ylim(ymax, ymin)
    ax.set_zlim(0, 4)
    ax.set_zlabel('DDV')
    fig.colorbar(surf, shrink=0.5, aspect=5)  # add color bar indicating the PDF
    # Hide grid lines
    ax.grid(False)

    # Hide axes ticks
    # ax.set_xticks([])
    # ax.set_yticks([])
    ax.set_zticks([])

    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_zaxis.line.set_lw(0.)
    ax.scatter(x, y, 1, color='black')

    return (ax.view_init(90, 90))


def plot_pitch_frame(frame_to_plot, team_to_plot):
    players_to_plot = tdat[(tdat['frameID'] == frame_to_plot) & (tdat['team'] == team_to_plot)]
    ball_to_plot = tdat[(tdat['frameID'] == frame_to_plot) & (tdat['team'] == 10)]

    plt.figure(figsize=(7.5, 5))
    plt.axis([-5600, 5600, -3600, 3600])
    # fig.grid(False)
    # Hide axes ticks
    # ax.set_xticks([])
    # ax.set_yticks([])
    # fig.set_zticks([])
    # ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    # ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    # ax.w_zaxis.line.set_lw(0.)
    plt.plot([-5250, -5250, 0, 0, -5250], [-3400, 3400, 3400, -3400, -3400], color='black', linewidth=1)
    plt.plot([5250, 5250, 0, 0, 5250], [-3400, 3400, 3400, -3400, -3400], color='black', linewidth=1)
    plt.plot([5250, 5250, 0, 0, 5250], [-3400, 3400, 3400, -3400, -3400], color='black', linewidth=1)

    plt.plot([-5250, -5250, -3600, -3600, -5250], [-2015, 2015, 2015, -2015, -2015], color='black', linewidth=1)
    plt.plot([5250, 5250, 3600, 3600, 5250], [-2015, 2015, 2015, -2015, -2015], color='black', linewidth=1)
    plt.plot([-5250, -5250], [-366, 366], color='black', linewidth=3)
    plt.plot([5250, 5250], [-366, 366], color='black', linewidth=3)

    plt.scatter(ball_to_plot['x'], ball_to_plot['y'], color='red')
    plt.scatter(players_to_plot['x'], players_to_plot['y'], color='black')

    return (plt)


def plot_pitch_frame_both(frame_to_plot, tracking_data=tdat):
    frame = tracking_data[tracking_data['frameID'] == frame_to_plot].reset_index(drop=True)

    if frame['ball_owning_team'].iloc[0] == "H":
        team_in_possession = 1
        direction = frame[frame['team'] == team_in_possession].reset_index(drop=True).iloc[0].attacking_direction
    else:
        team_in_possession = 0
        direction = frame[frame['team'] == team_in_possession].reset_index(drop=True).iloc[0].attacking_direction
    print(team_in_possession)
    print(direction)

    teamA = frame[frame['team'] == team_in_possession]
    teamD = frame[frame['team'] != team_in_possession]
    teamD = teamD[teamD['team'] != 10]
    ball_to_plot = frame[frame['team'] == 10]

    plt.figure(figsize=(7.5, 5))
    plt.axis([-5600, 5600, -3600, 3600])
    # fig.grid(False)
    # Hide axes ticks
    # ax.set_xticks([])
    # ax.set_yticks([])
    # fig.set_zticks([])
    # ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    # ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    # ax.w_zaxis.line.set_lw(0.)
    plt.plot([-5250, -5250, 0, 0, -5250], [-3400, 3400, 3400, -3400, -3400], color='black', linewidth=1)
    plt.plot([5250, 5250, 0, 0, 5250], [-3400, 3400, 3400, -3400, -3400], color='black', linewidth=1)
    plt.plot([5250, 5250, 0, 0, 5250], [-3400, 3400, 3400, -3400, -3400], color='black', linewidth=1)

    plt.plot([-5250, -5250, -3600, -3600, -5250], [-2015, 2015, 2015, -2015, -2015], color='black', linewidth=1)
    plt.plot([5250, 5250, 3600, 3600, 5250], [-2015, 2015, 2015, -2015, -2015], color='black', linewidth=1)
    plt.plot([-5250, -5250], [-366, 366], color='black', linewidth=3)
    plt.plot([5250, 5250], [-366, 366], color='black', linewidth=3)

    plt.scatter(teamA['x'], teamA['y'], color='red')
    plt.scatter(teamD['x'], teamD['y'], color='blue')
    plt.scatter(ball_to_plot['x'], ball_to_plot['y'], color='black')

    return (plt)


def get_frames_from_tracking(tdat):
    unique_frames = tdat[tdat['ball_status'] == "Alive"]['frameID'].unique()

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

    frames_to_assess = []

    for i in frame_list['breakID'].unique():
        subset = frame_list[frame_list['breakID'] == i]
        frames_ooo = subset.iloc[::12, :]['unique_frames']
        frames_to_assess.append(frames_ooo)

    frames_to_assess = [y for x in frames_to_assess for y in x]

    return (frames_to_assess)


def density_me_pockets(frames_to_assess_parsed):
    AttackerDensity_Results = pd.DataFrame()
    DefenderDensity_Results = pd.DataFrame()

    for i in tqdm(frames_to_assess_parsed):
        frame_dat = prepare_frame(i)

        AttackerDensity = pd.DataFrame(data=calculateAD(frame_dat)).T
        AttackerDensity_Results = pd.concat([AttackerDensity_Results, AttackerDensity])

        DefenderDensity = pd.DataFrame(data=calculateDD(frame_dat)).T
        DefenderDensity_Results = pd.concat([DefenderDensity_Results, DefenderDensity])

    return (AttackerDensity_Results, DefenderDensity_Results)


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
