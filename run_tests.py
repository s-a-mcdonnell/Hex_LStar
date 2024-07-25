import solver
import sys

# To write to Excel
import xlwt 
from xlwt import Workbook 
  


# Parse command-line arguments
args = []
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        args.append(sys.argv[i].lower())

print(f"args: {args}")

# Use values from passed arguments
if "graphs" in args:
    show_graphs = True
else:
    show_graphs = False

if "accuracy" in args:
    accuracy_checks = True
    # Information on writing to Excel here: https://www.geeksforgeeks.org/writing-excel-sheet-using-python/#
    wb = Workbook()
else:
    accuracy_checks = False
    wb = None



# TODO: Run solver several times with a different number of membership queries per equivalence query
solver.run_solver(100, show_graphs, accuracy_checks, wb)

