import time
import os

initial_time = time.time()
print(initial_time)
os.system("python run.py")
end_time = time.time()
print(end_time - initial_time)