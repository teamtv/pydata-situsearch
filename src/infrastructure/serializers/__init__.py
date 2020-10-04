import ujson

from domain import TrackingDataset, Frame


class DataSetToJson(object):
    @classmethod
    def serialize(cls, dataset: TrackingDataset) -> str:
        def frame_to_dict(frame: Frame):
            return dict(
                frame_id=frame.frame_id,
                timestamp=frame.timestamp,
                ball_position={'x': frame.ball_coordinates.x, 'y': frame.ball_coordinates.y},
                home=[{'x': player.x, 'y': player.y} for player in frame.home_player_coordinates.values()],
                away=[{'x': player.x, 'y': player.y} for player in frame.away_player_coordinates.values()]
            )

        return ujson.dumps(
            dict(
                frames=[frame_to_dict(frame) for frame in dataset.frames]
            )
        )
