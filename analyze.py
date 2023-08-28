import urllib.request
import json

base_url = 'https://api.boot.dev/v1/'
def get_leaders(type):
    if type == 'karma' or type == 'xp':
        return f'{base_url}leaderboard_{type}/alltime?limit=16'
    raise Exception('Wrong leaderboard type')

karma_leaders = None
with urllib.request.urlopen(get_leaders('karma')) as response:
    api_data_raw = response.read()
    karma_leaders = json.loads(api_data_raw)

xp_leaders = None
with urllib.request.urlopen(get_leaders('xp')) as response:
    api_data_raw = response.read()
    xp_leaders = json.loads(api_data_raw)

print('Waiting for API response. Press CTRL-C if it takes too long.')
while karma_leaders == None or xp_leaders == None:
    pass

unique_leaders = {}
for leader in karma_leaders:
    handle = leader['Handle']
    unique_leaders[handle] = leader

for leader in xp_leaders:
    handle = leader['Handle']
    if handle not in unique_leaders:
        unique_leaders[handle] = leader

print(f'Total number of unique boot.dev leaders: {len(unique_leaders)}')

with_github = []
for leader in unique_leaders:
    github = unique_leaders[leader]['GithubHandle']
    if github != None:
        with_github.append({'handle': leader, 'github': github, 'projects': 8})
print(f'Total number of unique boot.dev leaders with public github accounts: {len(with_github)}')

def wait_more():
    for i in range(len(with_github)):
        if with_github[i]['projects'] == 8:
            return True
    return False

def get_courses(user_handle):
    return f'{base_url}users/public/{user_handle}/courses'

for user in with_github:
    handle = user['handle']
    with urllib.request.urlopen(get_courses(handle)) as response:
        api_data_raw = response.read()
        courses = json.loads(api_data_raw)
        relevant_courses = 0
        for course in courses:
            if course['TypeDescription'] == 'Portfolio Project' and course['CompletedAt'] is not None:
                title = course['Title']
                if title.endswith('1'):
                    relevant_courses |= 1
                elif title.endswith('2'):
                    relevant_courses |= 2
                elif title.startswith('Capstone'):
                    relevant_courses |= 4
                else:
                    print('Wrong course title')
        user['projects'] = relevant_courses
        print(f'User {handle} checked')

print('Waiting for API response. Press CTRL-C if it takes too long.')
while wait_more():
    pass

