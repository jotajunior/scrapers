import requests

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
            return text

a = Wow()
print(a.get_user_achievements('xtreme', 'quelthalas'))
