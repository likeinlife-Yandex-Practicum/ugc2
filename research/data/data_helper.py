import datetime
import random

from faker import Faker


class DataHelper:

    def __init__(self):
        self.faker = Faker()

    def get_guid(self) -> str:
        return self.faker.uuid4()

    @staticmethod
    def get_random_int(start: int = 0, end: int = 10) -> int:
        return random.randint(start, end)

    def get_random_datetime(self) -> datetime.datetime:
        return self.faker.date_time()

    def get_random_sentence(self, nb_words: int = 4) -> str:
        return self.faker.sentence(nb_words=nb_words)


data_helper = DataHelper()
