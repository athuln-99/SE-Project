from scrapy.spiders import CrawlSpider



class SpiderCrawler(CrawlSpider):
    name = "mycrawler"
    start_urls = ['https://slack.com/help/articles/115004071768-What-is-Slack-#:~:text=Slack%20is%20a%20messaging%20app,transforms%20the%20way%20organizations%20communicate.']
    def parse(self, response):
        # Extract links containing the topics
        for link in response.css('a::attr(href)').getall():
            for topic in self.settings.get('TOPICS'):
                if topic in link:
                    yield {
                        'link': link,
                        'topic': topic
                    }

        # Follow other links
        for next_page in response.css('a::attr(href)').getall():
            yield response.follow(next_page, callback=self.parse)

