from scrapy.item import Item, Field

class Item(Item):
    name = Field()
    url = Field()
    title = Field()
    link = Field()
    page_title = Field()
    desc_link = Field()
    body = Field()
    news_headline = Field()
