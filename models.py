#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import graphene


class Source(graphene.ObjectType):
    url = graphene.String()
    description = graphene.String()
    label = graphene.String()


class Organization(graphene.ObjectType):
    name = graphene.String()
    share = graphene.String()


class Sales(graphene.ObjectType):
    units = graphene.Int()
    year = graphene.Int()
    rank = graphene.Int()
    year_over_year = graphene.Int()


class Maker(graphene.ObjectType):
    '''
    {
        "brand": "Toyota",
        "name": "Toyota Motor Corporation",
        "native_name": "トヨタ自動車株式会社",
        "found": 1937,
        "founder": [
          "Kiichiro Toyoda"
        ],
        "revenue": "202,86 tỷ USD",
        "net_income": "13,93 tỷ USD",
        "description": "Toyota Motor Corporation (トヨタ自動車株式会社 Toyota Jidosha Kabushiki-gaisha?) là một công ty đa quốc gia có trụ sở tại Nhật Bản, và là nhà sản xuất ô tô lớn nhất thế giới vào năm 2015[3]. Về mặt công nhận quốc tế, hãng Toyota là nhà sản xuất xe hơi duy nhất có mặt trong nhóm top 10 xếp hạng công nhận tên BrandZ.",
        "owner": [
          ["Japan Trustee Services Bank", 9.7],
          ["Tyota Industries", 6.73],
          ["The Master Trust Bank of Japan", 5.32],
          ["Denso", 2.59]
        ],
        "divisions": [
          "Lexus",
          "Scion (defunct)",
          "TRD"
        ],
        "subsidiaries": 545,
        "website": "http://www.toyota-global.com/",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Toyota_carlogo.svg/500px-Toyota_carlogo.svg.png",
        "image": {
          "url": "https://vignette.wikia.nocookie.net/tractors/images/5/58/Toyota_Headquarter_Toyota_City.jpg/revision/latest?cb=20110412155137",
          "description": "Trụ sở chính của Toyota tại thành phố Toyota, Nhật Bản"
        }
      },
      '''

    brand = graphene.String()
    name = graphene.String()
    nativeName = graphene.String()
    found = graphene.Int()
    founder = graphene.List(lambda : graphene.String)
    revenue = graphene.String()
    netIncome = graphene.String()
    description = graphene.String()
    shareholders = graphene.List(lambda : Organization)
    divisions = graphene.List(lambda : graphene.String)
    subsidiaries = graphene.Int()
    website = graphene.String()
    logo = graphene.Field(lambda : Source)
    image = graphene.Field(lambda : Source)
    sales = graphene.List(lambda : Sales)


class Series(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    maker = graphene.Field(lambda : Maker)


class Model(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    trim = graphene.String()
    series = graphene.Field(lambda : Series)
    avatar = graphene.Field(lambda : Source)
    images = graphene.List(lambda : Source)


class Transmission(graphene.ObjectType):
    drivetrain = graphene.String()
    type = graphene.String()


class CarPricing(graphene.ObjectType):
    trim = graphene.String()
    series = graphene.Field(lambda : Series)
    price = graphene.Float()
    rollingPrice = graphene.Float()
    transmission = graphene.Field(lambda : Transmission)


class Definitions(graphene.ObjectType):
    '''
    {
    "name": "suv",
    "title": "SUV",
    "content": "Bản chất SUV là Sport Utility Vehicle, xe thể thao đa dụng, với đặc trưng gầm cao, hệ dẫn động 4 bánh toàn thời gian hoặc bán thời gian. Kích thước dòng xe này thường từ cỡ trung đến lớn, với trang bị thiên về khả năng chạy đường dài, off-road nhiều hơn là di chuyển phố. Cũng vì thế, SUV thường có thiết kế vuông vức, đường nét đơn giản, nam tính. "
    "source": {
      "name": "VnExpress",
      "url": "http://vnexpress.net/tin-tuc/oto-xe-may/phan-biet-cac-dong-oto-tai-viet-nam-3263772.html"
    },
    "image": {
      "url": "https://i-vnexpress.vnecdn.net/2015/08/14/Honda-CR-V-3-8746-1422334185-6379-1439542960.jpg",
      "description": "Honda CR-V xếp vào nhóm crossover."
    }
  }
    '''
    name = graphene.String()
    title = graphene.String()
    content = graphene.String()
    source = graphene.Field(lambda : Source)
    image = graphene.Field(lambda: Source)