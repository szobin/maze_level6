from .conf import MOB_START_POS, MOB_START_DIRECTION
from .figure import Figure


class Mob(Figure):

    def __init__(self, canvas, board, control):
        super().__init__(canvas, board, control, 'mob', MOB_START_POS, MOB_START_DIRECTION)

