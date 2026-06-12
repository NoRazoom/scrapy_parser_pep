import csv
import os
import datetime

"""from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base"""

from pep_parse.settings import BASE_DIR


FINAL_DIR = BASE_DIR / 'results'
"""Base = declarative_base()"""


"""class Pep(Base):
    __tablename__ = 'pep'
    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    status = Column(String(20))
    number = Column(Integer)"""


class PepParsePipeline:

    def open_spider(self, spider):
        """engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session(engine)"""
        self.results = {}
        os.makedirs('results', exist_ok=True)

    """def process_item(self, item, spider):
        pep = Pep(
            number=int(item['number']),
            name=item['name'],
            status=item['status']
        )
        self.session.add(pep)
        self.session.commit()
        return item"""

    def process_item(self, item, spider):
        status = item['status']
        if self.results.get(status):
            self.results[status] += 1
        else:
            self.results[status] = 1
        return item

    def close_spider(self, spider):
        statuses_for_pep = [('Статус', 'Количество')]

        """statuses = self.session.query(Pep.status).all()
        counts = defaultdict(int)
        for (status_value,) in statuses:
            if status_value == 'Draft':
                key = ''
            elif status_value:
                key = status_value[0]

            status = EXPECTED_STATUS.get(key, (status_value,))
            counts[status] += 1
        statuses_for_pep = [('Статус', 'Количество')]
        for status, count in counts.items():
            statuses_for_pep.append((status, count))

        statuses_for_pep.append(('Total', len(statuses)))"""

        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{FINAL_DIR}/status_summary_{date}.csv'
        with open(filename, mode='w',
                  encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(statuses_for_pep)
            for key, value in self.results.items():
                writer.writerow([key, value])
            writer.writerow(['Total', sum(self.results.values())])
        self.session.close()
