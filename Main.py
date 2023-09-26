import subprocess
import time

start_time = time.time()  # Record the start time

print('Starting The Cyypto News....')
print ('\n') 

# List of script paths to run sequentially
scripts_to_run = [
    '/Volumes/@2TB/Programs/Programs  python/webscraper/CryptyoNewsCryptoScraper.py',
    '/Volumes/@2TB/Programs/Programs  python/webscraper/ArticalScraper2.py',
    '/Volumes/@2TB/Programs/Programs  python/webscraper/Sumerize2.py',
]

for script in scripts_to_run:
    # Run the script and wait for it to complete
    try:
        subprocess.run(['/usr/local/bin/python3', script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")
    

end_time = time.time()  # Record the end time
elapsed_time = end_time - start_time