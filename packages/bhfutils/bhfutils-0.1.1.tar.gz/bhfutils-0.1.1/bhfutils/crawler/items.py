# -*- coding: utf-8 -*-

# Define here the models for your scraped items

from scrapy import Item, Field


class RawResponseItem(Item):
    appid = Field()
    crawlid = Field()
    url = Field()
    responseUrl = Field()
    statusCode = Field()
    success = Field()
    exception = Field()
    encoding = Field()
    attrs = Field()


class MenuResponseItem(RawResponseItem):
    playgroundId = Field()
    groupCategoryName = Field()
    groupName = Field()
    groupUrl = Field()


class ProductResponseItem(RawResponseItem):
    playgroundId = Field()
    productUrl = Field()
    groupId = Field()
    price = Field()


class ProductDetailsResponseItem(RawResponseItem):
    playgroundId = Field()
    productUrl = Field()
    groupId = Field()
    imageUrl = Field()
    name = Field()
    description = Field()
    details = Field()


class ReviewResponseItem(RawResponseItem):
    technoBlogId = Field()
    reviewUrl = Field()
    createDate = Field()
    name = Field()
    category = Field()
    imageUrl = Field()


class ReviewDetailsResponseItem(RawResponseItem):
    technoBlogId = Field()
    reviewUrl = Field()
    createDate = Field()
    author = Field()
    name = Field()
    category = Field()
    keywords = Field()
    description = Field()
    imageUrl = Field()
    pros = Field()
    cons = Field()
    productName = Field()
    productParameters = Field()
    verdict = Field()
    baseParameters = Field()


class BrandProductResponseItem(RawResponseItem):
    brandId = Field()
    groupId = Field()
    productUrl = Field()
    imageUrl = Field()


class BrandProductDetailsResponseItem(RawResponseItem):
    brandId = Field()
    groupId = Field()
    productUrl = Field()
    code = Field()
    name = Field()
    description = Field()
    imageUrls = Field()
    variations = Field()
    productParameters = Field()
    minPrice = Field()
