from pydantic import BaseModel
from loguru import logger
import sys


l_format = '<green>{time}</green><yellow>{name}</yellow><red>{message}</red>'
logger.add(sys.stdout, colorize=True, level='DEBUG', format=l_format)


def main():
    class TrainTicket(BaseModel):
        train: str = None
        care: int = None
        seat: int = None

        @classmethod
        def init_c(cls, train: str, caret: int, seat: int):
            return cls(train=train, caret=caret, seat=seat)

    ticket_1 = TrainTicket.init_c('AC101', 4, 27)
    ticket_2 = TrainTicket.init_c(train='AS101', caret=1, seat=51)
    logger.info(f'!!! {ticket_1}')
    logger.info(f'!!! {ticket_2}')


if __name__ == '__main__':
    main()
