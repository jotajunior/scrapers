import requests

class BFHL:
    platform = None
    
    platforms = ['pc', 'xbox', 'ps3', 'xone', 'ps4']
    outputs = ['json', 'jsonp', 'js', 'lines']
    base_url = 'http://api.bfhstats.com/api'

    def set_platform(self, platform):
        self.platform = platform.replace(' ', '').lower()

    def check_platform(self, platform):
        if not platform or platform not in self.platforms:
            raise Exception('BFHL: Invalid platform.')

    def check_output(self, output):
        if not output or output not in self.outputs:
            raise Exception('BFHL: Invalid output.')

    def __init__(self, platform='pc'):
        self.set_platform(platform)
        self.check_platform(self.platform)

    def get_basic_parameters(self, platform=None, output=None):
        platform = platform if platform else self.platform
        output = output if output else 'json'

        return {'plat': platform, 'output': output}

    def get_player_by_name(self, name, output=None, platform=None):
        if not output:
            output = self.output

        if not platform:
            platform = self.platform

        self.check_platform(platform)
        self.check_output(output)

        data = self.get_basic_parameters(platform, output)
        data['name'] = name
        url = self.base_url + '/playerInfo'

        return requests.get(url, params = data).text

    def user_exists(self, name, platform=None):
        if not platform:
            platform = self.platform

        result = self.get_player_by_name(name, 'json', platform)
        return result != '{"error":"notFound"}'
