from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt

from application import SearchService
from domain import MunkresMatcher, Frame
from infrastructure import LocalRepository

plt.style.use('ggplot')

def draw_frame(frame: Frame):
    home_x, home_y = zip(*[
        (point.x, point.y) for point in frame.home_player_coordinates.values()
    ])
    away_x, away_y = zip(*[
        (point.x, point.y) for point in frame.away_player_coordinates.values()
    ])

    pitch = Pitch(figsize=(10, 8), pitch_type="uefa")
    fig, ax = pitch.draw()
    sc = pitch.scatter(home_x + away_x + (frame.ball_coordinates.x, ), home_y + away_y + (frame.ball_coordinates.y, ),
                       c=['blue'] * len(home_x) + ['red'] * len(away_x) + ['green'],
                       s=30, label='scatter', ax=ax)

    plt.show()



repository = LocalRepository("./")
    # repository.save(dataset)

search_service = SearchService(
    matcher_cls=MunkresMatcher,
    repository=repository
)

resultset = search_service.search_by_frame(
    "test", 201,
    min_score=80
)

frame = resultset.results[8].frame

draw_frame(frame)