import time

start_time = time.time()

# Call the function you want to time here
import run_once.table_import_consolidated  # noqa

end_time = time.time()
# 3.74s for table import
# 32s for table consolidated
execution_time = end_time - start_time

print(f"The execution time of the script is {execution_time} seconds.")