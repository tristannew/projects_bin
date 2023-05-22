import scrapy


class ProfilesSpider(scrapy.Spider):
    name = "profiles"
    start_urls = ['https://www.worldsurfleague.com/athletes/tour/mct?year=2010','https://www.worldsurfleague.com/athletes/tour/mct?year=2011','https://www.worldsurfleague.com/athletes/tour/mct?year=2012',
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
        for link in response.xpath('//table//a[contains(@class, "athlete-name")]/@href'): #css to href to their profile:
            yield response.follow(link.get(), callback=self.parse_profile)
            
    def parse_profile(self, response):
        # follow links to profile and collect data on surfer age, hometown, height, weight
        surfer_name = response.css('.avatar-text-primary > h1::text').extract_first().strip() #css to name
        surfer_country = response.css('.country-name::text').extract_first().strip()
        followers = response.css('.count::text').extract_first().strip()
        surfer_data = response.css('.value ::text').extract() # contains, height, wwight, avg heat score, first season, age, stance, hometwon, birth date
        profile_data = {"Name":surfer_name, "Nation":surfer_country, "Followers":followers, "Data":surfer_data}
        yield profile_data
