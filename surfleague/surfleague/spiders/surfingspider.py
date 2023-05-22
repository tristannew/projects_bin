import scrapy


class SurfingspiderSpider(scrapy.Spider):
    name = "surfingspider"
    start_urls = ['https://www.worldsurfleague.com/athletes/tour/mct?year=2010',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2011',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2012',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2013',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2014',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2015',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2016',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2017',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2018',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2019',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2020',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2021',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2022',
                'https://www.worldsurfleague.com/athletes/tour/mct?year=2023']
    
    def start_requests(self):
        return super().start_requests()

    def parse(self, response):
        
        # navigate to surfer name, nation and scores for each year
        surfer_names = response.css('.athlete-name::text').extract() #css to their names
        surfer_nation = response.css('.athlete-country-name::text').extract() #css to their nation
        surfer_scores = response.xpath('//td[contains(@class, "athlete-event-place")]//text()').extract() #css to scores for each event
        surfer_total_score = response.css('.tour-points::text').extract() #css to total score for year
        rankings_data = {"Names":surfer_names, "Nations":surfer_nation, "Scores":surfer_scores, "Total Scores":surfer_total_score}
        yield rankings_data
