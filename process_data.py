# mock = {
#     'projects': {
#         'proj1': {
#             'days_to_complete': 9,
#             'score': 10,
#             'best_before': 12,
#             'roles': {
#                 'C++': 3,
#                 'Python': 2,
#             },
#         },
#         'proj2': {
#             'days_to_complete': 7,
#             'score': 20,
#             'best_before': 10,
#             'roles': {
#                 'HTML': 1,
#                 'CSS': 4,
#             },
#         },
#     },
#     'contributors':{
#         'contrib1': {
#             'C++': 3,
#             'CSS': 5,
#         },
#         'contrib2': {
#             'HTML': 1, 
#             'C++': 2,
#         },
#         'contrib3': {
#             'HTML': 3,
#             'CSS': 1,
#             'Python': 2,
#         },
#     },
# }

mock_output = {
    'Logging': ['Anna'],
    'WebServer': [ 'Anna', 'Bob' ],
    'WebChat': [ 'Maria' ],
}

def process_mock(data):
    return mock_output


from read_data import read_all

fn = "input_data/b_better_start_small.in.txt"
data = read_all(fn)


def get_contributors_by_skill(contributors, requested_skill, requested_level, mentorship=False):
    valid_contributors = []
    all_contributors = {}
    for contributor_name in contributors:
        skills = contributors[contributor_name]
        for skill_name in skills:
            skill_level = contributors[contributor_name][skill_name]
            if skill_name == requested_skill and skill_level >= (requested_level - 1 if mentorship else requested_level):
                valid_contributors.append((contributor_name, skill_level))
                all_contributors[contributor_name] = contributors[contributor_name]
    valid_contributors.sort(key=lambda x: x[1])
    return valid_contributors, all_contributors

def get_skills_of_contributor(contr_name):
    #todo: finish
    return {}

def contributors_expanded(data):

    # Sort by project score to time ratio
    projects_tuples = sorted(data['projects'].items(), key=lambda x: x[1]['score'] / x[1]['days_to_complete'], reverse=True)
    projects = []
    for p in projects_tuples:
        p[1]['name'] = p[0]
        projects.append(p[1])
    # [{'name': 'proj2', 'score': 20, 'days_to_complete': 7, 'best_before': 10, 'roles': {'HTML': 1, 'CSS': 4}}, ...]
    return projects


def process_v1(data):
    projects = contributors_expanded(data)
    output = {}
    contributors = data['contributors']
    for project in projects:
        currentContributors = []
        for requestedSkill, level in project['roles'].items():
            contr_possible, _ = get_contributors_by_skill(contributors, requestedSkill, level)
            if len(contr_possible) > 0:
                currentContributor = contr_possible[0][0]
                currentContributors.append(currentContributor)
                del contributors[currentContributor]
            else:
                # cannot find contributor for projecct
                pass
        found_c = len(currentContributors)
        needed_c = len(project['roles'])
        if found_c > 0:
            if found_c == needed_c:
                output[project['name']] = currentContributors
    return output


def process_v2(data):
    projects = contributors_expanded(data)
    output = {}
    contributors = data['contributors']

    possibleMentors = {}

    for project in projects:
        currentContributors = []
        for requestedSkill, level in project['roles'].items():
            #TODO: improve this logic
            contr_possible, contr_possible_from_data = get_contributors_by_skill(contributors, requestedSkill, level)
            if len(contr_possible) > 0:
                currentContributor = contr_possible[0][0]
                currentContributors.append(currentContributor)
                #TODO increase current contributor's level
                possibleMentors[currentContributor] = contr_possible_from_data[currentContributor]
                del contributors[currentContributor]
            else:
                if True:
                    coordinated_contr_possible, all_coo = get_contributors_by_skill(contributors, requestedSkill, level-1)
                    mentors_possible, all_men = get_contributors_by_skill(possibleMentors, requestedSkill, level)
                    if len(mentors_possible) > 0 and len(coordinated_contr_possible) > 0:
                        currentContributor = coordinated_contr_possible[0][0]
                        currentMentor = mentors_possible[0][0]
                        currentContributors.append(currentContributor)
                        currentContributors.append(currentMentor)

                        del contributors[currentContributor]
                        del possibleMentors[currentMentor]

                    # cannot find contributor for projecct
                    pass
        found_c = len(currentContributors)
        needed_c = len(project['roles'])
        if project['name'] == 'WearOSMaxv2':
            debug_here = 3
        if found_c > 0:
            if found_c == needed_c:
                output[project['name']] = currentContributors
    
    return output
