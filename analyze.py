import urllib.request
import json
from time import sleep

base_url = 'https://api.boot.dev/v1/'
def get_leaders_url(type):
    if type == 'karma' or type == 'xp':
        return f'{base_url}leaderboard_{type}/alltime?limit=16'
    raise Exception('Wrong leaderboard type')

karma_leaders = None
with urllib.request.urlopen(get_leaders_url('karma')) as response:
    api_data_raw = response.read()
    karma_leaders = json.loads(api_data_raw)

xp_leaders = None
with urllib.request.urlopen(get_leaders_url('xp')) as response:
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
    first_name = unique_leaders[leader]['FirstName'] 
    if first_name is None:
        first_name = ''
    last_name = unique_leaders[leader]['LastName'] 
    if last_name is None:
        last_name = ''
    full_name = first_name + last_name

    github = unique_leaders[leader]['GithubHandle']
    if github != None:
        with_github.append({'name': full_name, 'handle': leader, 'github': github, 'projects': -1})

print(f'Total number of unique boot.dev leaders with public github accounts: {len(with_github)}')

def wait_more():
    for i in range(len(with_github)):
        if with_github[i]['projects'] == -1:
            return True
    return False

def get_courses(user_handle):
    return f'{base_url}users/public/{user_handle}/courses'

for user in with_github:
    handle = user['handle']
    sleep(2)
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
        print(f'User checked: {handle}')

print('Waiting for API response. Press CTRL-C if it takes too long.')
while wait_more():
    pass

def create_filter(num_of_proj):
    def users_by_projects(user):
        return user['projects'] == num_of_proj
    return users_by_projects

def describe_progress(projects):
    match projects:
        case 7:
            return 'all 3 personal projects'
        case 6:
            return 'personal projects 2 and 3'
        case 5:
            return 'personal projects 1 and 3'
        case 4:
            return 'personal project 3'
        case 3:
            return 'personal projects 1 and 2'
        case 2:
            return 'personal project 2'
        case 1:
            return 'personal project 1'
        case other:
            raise Exception('Wrong number of projects')

for n in range(7, 0, -1):
    filter_func = create_filter(n)
    filtered_users = []
    for user in with_github:
        if filter_func(user):
            filtered_users.append(user)
    if len(filtered_users) > 0:
        print(f'There are {len(filtered_users)} users, who have completed {describe_progress(n)}')
        for user in filtered_users:
            name = user['name']
            github = 'https://github.com/' + user['github']
            print(f'User: {name}    GitHub: {github}')

    

