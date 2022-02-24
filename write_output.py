import os

def write_submission(fn:str, output:dict):
    if not os.path.exists('out'): os.makedirs('out')
    with open(fn, 'w') as file:
        file.write("{}\n".format(len(output.keys())))
        for project in output.keys():
            file.write(project + "\n")
            file.write(" ".join(output[project]) + "\n")