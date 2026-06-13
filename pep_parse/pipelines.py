import csv
import os
import datetime
from collections import defaultdict

from pep_parse.settings import BASE_DIR


FINAL_DIR = BASE_DIR / 'results'


class PepParsePipeline:

    def open_spider(self, spider):
        self.results = defaultdict(int)
        os.makedirs('results', exist_ok=True)

    def process_item(self, item, spider):
        status = item['status']
        self.results[status] += 1
        return item

    def close_spider(self, spider):
        self.results['Total'] = sum(self.results.values())
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{FINAL_DIR}/status_summary_{date}.csv'
        with open(filename, mode='w',
                  encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(('Статус', 'Количество'))
            writer.writerows(self.results.items())
        self.session.close()
