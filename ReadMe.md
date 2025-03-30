.
├── ReadMe.md 
├── data : data files 
│   ├── OPL.json : data for OPL problem 
│   └── dataTankAllocation : data for Tank allocation problem
│
├── docs : logs and xmls
│   ├── logs : log files 
│   ├── xmls : xml files
│   └── rpts : reports in chinese 
│
├── run.sh : use java ace run code ("./run.sh ./docs/xmls/0000.xml(xmlpath)")
└── src : python codes
    ├── csp_opl.ipynb : jupyter notebook for OPL
    ├── csp_tankallocation.ipynb : jupyter notebook for Tank allocation 
    ├── TankSolver.py : class for Tank allocation problem
    ├── opl.py : code for OPL problem
    └── tank_allocation.py : code for Tank allocation problem