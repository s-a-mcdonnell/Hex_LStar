import solver

# To write to Excel
import xlwt 
from xlwt import Workbook 

# Information on writing to Excel here: https://www.geeksforgeeks.org/writing-excel-sheet-using-python/#
wb = Workbook()


# Run solver several times with a different number of membership queries per equivalence query
# NOTE: You can set your own number of membership queries per equivalence query
'''for mem_in_eq in [20, 50, 100, 150, 200]:'''
for mem_in_eq in [5, 20]:
    solver.run_solver(mem_in_eq, show_graphs=False, accuracy_checks=True, wb=wb)

if wb:
    wb.save('Acc__states_w__mem_per_eq.xls')


