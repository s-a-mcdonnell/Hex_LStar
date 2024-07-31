import solver
import sys

# To write to Excel
import xlwt 
from xlwt import Workbook 

if len(sys.argv) >= 2:
    file_name = sys.argv[1]
    print(f"Results from testing accuracy will be saved to {file_name}.xls")
    
    # Information on writing to Excel here: https://www.geeksforgeeks.org/writing-excel-sheet-using-python/#
    wb = Workbook()
else:
    file_name = False
    wb=None
    print("No accuracy checks will be completed.")


# Run solver several times with a different number of membership queries per equivalence query

# test_num serves to avoid attempting to create multiple pages with the same name
test_num = 0

# NOTE: You can set your own number of membership queries per equivalence query
# For example, to test one solve each with 20, 50, and 100, use: 
'''for mem_in_eq in [20, 50, 100]:'''
for mem_in_eq in [300]:
    print(f"\nRunning test with {mem_in_eq} membershup queries per equivalence query\n")
    
    try:
        solver.run_solver(mem_in_eq, show_graphs=False, accuracy_checks=file_name, wb=wb, test_id=test_num)
    except Exception as e:
        print(f"Error: {e}")
        if wb:
            wb.save(f'{file_name}.xls')
        exit(1)

    # Iterate test num
    test_num += 1

if wb:
    wb.save(f'{file_name}.xls')