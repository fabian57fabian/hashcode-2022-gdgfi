import os

from read_data import read_all
from process_data import process as process_function_1
from process_data import process_mock as process_function_0
from write_output import write_submission


if __name__ == '__main__':
    #for fn in ['b_better_start_small.in.txt']:
    for fn in os.listdir("input_data"):
        data = read_all("input_data/" + fn)
        result = process_function_1(data)
        write_submission("out/"+fn, result)
        print("Job done.")

