import pydentic
from pydantic import BaseModel
from loguru import logger
import sys


logger.add(sys.stdout, colorize=True, level='DEBUG', format='<green>{time}</green><yellow>{name}</yellow><red>{message}</red>')




def main():
    class Cat(BaseModel):
        name: str = None
        age: int = None
        breed: str = None

    cat_data = Cat(name='Мурзик', age=12, breed='Сиамский')
    logger.info(f'Вот такую структуру данных мы создали {cat_data}')
    print('!!!', cat_data)
    my_cat = {'name': 'Киса', 'age': 22, 'breed': 'Дворовая кощька'}
    my_cat_model = Cat(**my_cat)
    print('!!!', my_cat_model)
    print(cat_data.model_dump())
    print(my_cat_model.model_dump_json())


    class Dog(BaseModel):
        name: str = None
        age: int = None

        @classmethod
        def rand_init(cls, name: str, age: int):
            return cls(name=name, age=age)


    my_dog = Dog.rand_init('Пыпень', 20)
    print('!!!', my_dog)

if __name__ == '__main__':
    main()
