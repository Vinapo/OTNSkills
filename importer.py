#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import json
from adapters.aurora import *

import ConfigParser
import os

STAGE = 'development.ini'

settings_path = os.path.join('', STAGE)
settings = ConfigParser.ConfigParser()
settings.read(settings_path)

session = scoped_session(create_session(host=settings.get('app:main', 'aws.aurora')))


def load_makers():
    '''
    {
        "brand": "Audi",
        "name": "Audi AG",
        "native_name": "Audi",
        "found": 1909,
        "founder": [
          "August Horch"
        ],
        "revenue": "72,47 tỷ USD",
        "net_income": "5,33 tỷ USD",
        "sales": [
          {
            "year": 2017,
            "units": 1847613,
            "rank": 13,
            "year_over_year": "+1%"
          }
        ],
        "description": "AUDI AG là một công ty của Đức chuyên sản xuất ô tô hạng sang dưới nhãn hiệu Audi. Audi có trụ sở chính đặt tại Ingolstadt, Đức và là một công ty con của tập đoàn ô tô lớn nhất thế giới Volkswagen AG (sở hữu 99.55% cổ phần) từ năm 1964. Tập đoàn Volkswagen tái sử dụng cái tên Audi sau khi Audi trở thành một phần của tập đoàn.",
        "owner": [
          ["Volkswagen Group", 99.55]
        ],
         "divisions": [
          "Audi e-tron",
          "Audi India"
        ],
        "subsidiaries": 6,
        "website": "http://www.audi.com/en.html",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Audi-Logo_2016.svg/235px-Audi-Logo_2016.svg.png",
        "image": {
          "url": "https://upload.wikimedia.org/wikipedia/commons/2/20/Audi_Ingolstadt.jpg",
          "description": "Trụ sở chính của Audi tại thành phố Ingolstadt, Đức"
        }
    }
    '''

    with open('data/car_makers.json') as f:
        items = json.load(f)

        session()
        session.execute('''TRUNCATE TABLE maker''')
        session.execute('''TRUNCATE TABLE sales''')
        session.commit()

        i = 0
        for item in items:

            i += 1
            print(i)

            maker = Maker()
            maker.name = item.get('name')
            maker.brand = item.get('brand')
            maker.native_name = item.get('native_name')
            maker.found = item.get('found')
            maker.founder = json.dumps(item.get('founder'))
            maker.description = item.get('description')
            maker.website = item.get('website')
            maker.logo = item.get('logo')
            maker.image = item.get('image', {}).get('url')
            maker.image_description = item.get('image', {}).get('description')
            maker.subsidiaries = item.get('subsidiaries') or 0
            maker.shareholders = json.dumps(item.get('owner'))
            maker.divisions = json.dumps(item.get('divisions'))

            for field in ['revenue', 'net_income']:
                if u'tỷ USD' in item.get(field):
                    setattr(maker, field, float(
                        item.get(field).replace(',', '.').replace(u'tỷ USD', '').strip()) * 1000000000 if item.get(
                        field) else None)
                elif u'triệu USD' in item.get(field):
                    setattr(maker, field, float(
                        item.get(field).replace(',', '.').replace(u'triệu USD', '').strip()) * 1000000 if item.get(
                        field) else None)

            session.add(maker)

            for s in item.get('sales', []):
                sales = Sales()
                sales.name = maker.brand
                sales.units = s.get('units')
                sales.rank = int(s.get('rank') or 0)
                sales.date = '%s-01-01' % s.get('year')
                # sales.year_over_year = s.get('year_over_year')
                session.add(sales)

        session.commit()

        session.remove()


if __name__ == '__main__':
    load_makers()