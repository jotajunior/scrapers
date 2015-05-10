import requests
import lxml.html

class Wow:
    base_url = 'http://us.battle.net/wow/en'
    # 0 => world, 1 => name
    character_url = '/character/{0}/{1}/simple'
    achievement_url = '/character/{0}/{1}/achievement'

    achievement_text = None
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

        achv = achv.split('(')
        achv = achv[0]
        achv = achv.split('/')
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
        print('total', total)
        if total:
            base['total'] = total

        strength = self._get_strength_achievement(page)
        if strength:
            base['strength'] = strength

        self.achievements = base
        return base

    def get_user_achievements(self, name, world):
        if self.achievement_text:
            return self.achievement_text

        
        url = self.base_url
        url += self.achievement_url.format(world, name)
        text = requests.get(url).text
        # case user doesn't exist

        if self.is_404(text):
            return False
        else:
            self.achievement_text = text
            return self._parse_achievements(text)

a = Wow()
text = a.get_user_achievements('xtreme', 'quelthalas')
