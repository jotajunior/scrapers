import requests
import lxml.html

class Wow:
    base_url = 'http://us.battle.net/wow/en'
    # 0 => world, 1 => name
    character_url = '/character/{0}/{1}/simple'
    achievement_url = '/character/{0}/{1}/achievement'
    statistic_url = '/character/{0}/{1}/statistic'

    achievements = None
    statistics = None

    character_text = None

    def is_404(self, text):
        return text.find('<h3>Character Not Available</h3>') != -1

    def user_exists(self, name, world):
        if self.achievement_text or self.character_text:
            return True

        url = self.base_url
        url += self.character_url.format(world, name)
        text = requests.get(url).text

        if self.is_404(text):
            return False
        else:
            self.character_text = text
            return True

    def _parse_achievement_string(self, achv):
        achv = achv.replace('\t', '')\
                .replace('\n', '')\
                .replace('\xa0', '')\
                .replace(' ', '')

        achv = (achv.split('(')[0]).split('/')
        achv[0] = int(achv[0])
        achv[1] = int(achv[1])

        return achv

    def _get_total_achievement(self, page):
        query = '//div[@class="bar-contents"]/strong/text()'
        r = page.xpath(query)

        if r:
            return self._parse_achievement_string(r[0])
        
        return False
    
    def _get_strength_achievement(self, page):
        query = '//div[@class="profile-progress bar-contents border-4"]/text()'
        r = page.xpath(query)

        if r:
            return int(r[0])

        return False

    def _get_other_achievements(self, page):
        query = '//div[@class="bar-contents"]/text()'
        r = page.xpath(query)[2:]

        keys = ['general', 'quests', 'exploration', 'pvp', 'dungeons'\
                ,'professions', 'reputation', 'scenarios', 'events'\
                ,'pet_battles', 'collections','garrisons', 'legacy']

        result = {}
        i = 0

        for item in r:
            result[keys[i]] = self._parse_achievement_string(item)
            i += 1

        return result

    def _parse_achievements(self, text):
        page = lxml.html.fromstring(text)
        base = self._get_other_achievements(page)
        
        total = self._get_total_achievement(page)
        
        if total:
            base['total'] = total

        strength = self._get_strength_achievement(page)
        if strength:
            base['strength'] = strength

        self.achievements = base
        return base
    
    def _get_statistics_keys(self, page):
        query = '//li[@id="cat-summary"]/dl/dt/text()'
        r = page.xpath(query)

        return r

    def _get_statistics_values(self, page):
        query = '//li[@id="cat-summary" and @class="table"]/dl/dd/text()'
        r = page.xpath(query)

        return [int(i.replace('\t', '')\
                .replace('\n', '')\
                .replace(' ', '')\
                .replace(',', '')) for i in r]

    def _parse_statistics(self, text):
        page = lxml.html.fromstring(text)
        
        keys = self._get_statistics_keys(page)
        values = self._get_statistics_values(page)
        result = {}

        for i in range(len(keys)):
            result[keys[i]] = values[i]

        return result

    def get_user_achievements(self, name, world):
        if self.achievements:
            return self.achievements

        
        url = self.base_url
        url += self.achievement_url.format(world, name)
        text = requests.get(url).text
        # case user doesn't exist

        if self.is_404(text):
            return False
        else:
            self.achievement_text = text
            self.achievements = self._parse_achievements(text)

            return self.achievements

    def get_user_statistics(self, name, world):
        if self.statistics:
            return self.statistics

        url = self.base_url
        url += self.statistic_url.format(world, name)
        text = requests.get(url).text

        if self.is_404(text):
            return False
        else:
            self.statistic_text = text
            self.statistics = self._parse_statistics(text)

            return self.statistics
import time
start_time = time.time()

for i in range(10):
    a = Wow()
    print(a.get_user_statistics('xtreme', 'quelthalas'))
    print(a.get_user_achievements('xtreme', 'quelthalas'))
    print(a.user_exists('xtreme', 'quelthalas'))

print("--- %s seconds ---" % (time.time() - start_time))
