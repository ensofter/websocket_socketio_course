from loguru import logger


def main():
    logger.debug('Это текст debug уровня')
    logger.info('Это текст info уровня')
    logger.warning('Это текс warning уровня')
    logger.error('Это текст error уровня')
    logger.critical('Это текст critical уровня')


if __name__ == '__main__':
    main()
