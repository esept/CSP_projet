from pycsp3 import *
import TankSolver
import os
import shutil

def verifier_solution(solver, file, solution):

    file_name = file.split('/')[-1]
    print(file_name)
    solver.get_new_file(file) # load new data file
    solver.read_file() # read data
    solver.define_vars() # define variables
    solver.def_sat() # define constraints
    solver.veferication(thesolution=solution)


if __name__ == '__main__':
    path = './data/dataTankAllocation'
    all_files = os.listdir(path)
    all_files = [os.path.join(path, af) for af in all_files]

    all_files = ["./data/dataTankAllocation/0000.json","./data/dataTankAllocation/chemical.json"] 

    tk = TankSolver.TankSolver()
    res_0000 = [14, 10, 5, 12, 12, 0, 1, 11, 0, 1, 1, 12, 13, 13, 5, 7, 14, 2, 5, 8, 14, 9, 14, 13, 0]

    # verifier_solution(tk, all_files[0], res_0000)

    for file in all_files[:10]:
        file_name = file.split('/')[-1]
        print(file_name)
        tk.get_new_file(file) # load new data file
        tk.read_file() # read data
        tk.define_vars() # define variables

        tk.def_sat() # define constraints

        # tk.veferication(thesolution=res_0000)
        # break
        tk.solve() # solve the problem 

        shutil.move("tank_allocation.xml",f"./docs/xmls/{file_name}.xml") # Rename xml file as original data file name and move to ./docs/xmls/

        logfile = [i for i in os.listdir("./") if i.endswith('log')][0]
        shutil.move(logfile,f"./docs/logs/{logfile}") # Move log file to ./docs/logs/ 
