
# In the all subdirectories of Papers, run the command "java -cp cermine-impl-1.13-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path {subdirectory}"

import os
import time
import subprocess
from tqdm import tqdm

def main():
    processes = []
    subdirectories = [os.path.join("Papers", subdirectory) for subdirectory in os.listdir("Papers") if os.path.isdir(os.path.join("Papers", subdirectory))]
    # Run 10 processes at a time
    for subdirectory in tqdm(subdirectories):
        processes.append(subprocess.Popen(["java", "-cp", "cermine-impl-1.13-jar-with-dependencies.jar", "pl.edu.icm.cermine.ContentExtractor", "-path", subdirectory]))
        while len(processes) == 10:
            for process in processes:
                if process.poll() is not None:
                    processes.remove(process)
            time.sleep(5)

if __name__ == "__main__":
    main()