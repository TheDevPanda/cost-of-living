from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "lebenshaltungskosten"

    def start_requests(self):
        urls = [
            "https://de.numbeo.com/lebenshaltungskosten/ranking-nach-land?title=2024",
            "https://de.numbeo.com/lebenshaltungskosten/ranking-nach-land?title=2023",
            "https://de.numbeo.com/lebenshaltungskosten/ranking-nach-land?title=2022",
            "https://de.numbeo.com/lebenshaltungskosten/ranking-nach-land?title=2021",
            "https://de.numbeo.com/lebenshaltungskosten/ranking-nach-land?title=2020",
            "https://de.numbeo.com/lebenshaltungskosten/ranking-nach-land?title=2019",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        year = int(response.url.split("=")[1])
        cols = [
            "Land",
            "Lebenshaltungskosten",
            "Miete",
            "LebenshaltungPlusMiete",
            "Lebensmittel",
            "Gaststaetten",
            "Kaufkraft",
        ]
        for row in response.xpath('//*[@id="t2"]//tbody/tr'):
            content = row.xpath("td//text()").extract()
            yield {"Jahr": year} | {
                x: y.replace(",", ".") for x, y in zip(cols, content)
            }
