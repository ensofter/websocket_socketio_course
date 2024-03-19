from loguru import logger
from pydantic import BaseModel
from faker import Faker
import sys


fake = Faker()


loguru_format = "<green>{time}</green> <level>{message}</level>"
logger.add(sys.stdout, colorize=True, level="INFO", format=loguru_format)


def main():
    class CompanyShare(BaseModel):
        name: str = None
        ticket: str = None
        value: float = None

        @classmethod
        def rand_init(cls, name: str = None, ticket: str = None, value: float = None):
            name = name or fake.word()
            ticket = ticket or fake.word()
            value = value or fake.pyfloat(left_digits=2, right_digits=4, positive=True)
            return cls(name=name, ticket=ticket, value=value)

    tsla_company = CompanyShare.rand_init('Tesla', 'TSLA', 234.0)
    apple_stock = CompanyShare.rand_init(name='Apple')
    amazon_stock = CompanyShare.rand_init()

    logger.info(f'{tsla_company}')
    logger.info(f'{apple_stock}')
    logger.info(f'{amazon_stock}')

    print('!!!', tsla_company)
    print('!!!', apple_stock)
    print('!!!', amazon_stock)

if __name__ == '__main__':
    main()
