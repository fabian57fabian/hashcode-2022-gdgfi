
def read_all(fn:str):
    data = {
        "projects":{},
        "contributors":{},
    }
    contributors, projects = 0,0
    with open(fn, 'r') as file:
        parsed_contr = 0
        parsed_projs = 0
        on_people = True
        skills_count = 0
        proj_skill_count = 0
        last_person = ""
        last_projname = ""
        s = file.readline().rstrip().split(' ')
        contributors, projects = int(s[0]), int(s[1])
        line_num = 0
        for line in file.readlines():
            if on_people:
                if len(line.rstrip().split()) > 2 and skills_count == 0:
                    print('now on projects')
                    on_people = False
            if on_people:
                if skills_count == 0:
                    # parse contributor
                    s = line.rstrip().split(' ')
                    person, skills = s[0], int(s[1])
                    if person not in data["contributors"]:
                        data["contributors"][person] = {}
                    skills_count = skills
                    last_person = person
                    parsed_contr += 1
                else:
                    # parse skill contributor
                    s = line.rstrip().split(' ')
                    skill, count = s[0], int(s[1])
                    data["contributors"][last_person][skill] = count
                    skills_count -= 1
            if not on_people:
                if proj_skill_count == 0:
                    # parse project
                    s = line.rstrip().split(' ')
                    projname = s[0]
                    data["projects"][projname] = {'days_to_complete': int(s[1]),
                        'score': int(s[2]),
                        'best_before': int(s[3]),
                        'roles': {}
                        }
                    proj_skill_count = int(s[4])
                    last_projname = projname
                    parsed_projs += 1
                else:
                    # parse project's skill
                    s = line.rstrip().split(' ')
                    skill, count = s[0], int(s[1])
                    data["projects"][last_projname]["roles"][skill] = count
                    proj_skill_count -= 1
            line_num += 1
    print("contributors: {}, parsed {}".format(contributors, len(data['contributors'])))
    print("projects    : {}, parsed {}".format(projects, len(data['projects'])))
    return data