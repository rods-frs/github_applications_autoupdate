#packages
from github import Github
import subprocess
from pathlib import Path

#pre-run config
g = Github()
downloads = Path.home() / "Downloads"
golden_list = ["rpm", "64"]

#global variables
repo_list = []
repo_list_name = "repo_list.txt"

#functions
def read_repo_list():
    try:
        with open(repo_list_name, "r") as f:
            for line in f:
                repo_list.append(line.strip())

    except Exception as e:
        print(f"Failed to open the repositories list .txt: {e}")    

def add_repo():

    usr_input = str(input("What repo you want to add?\n>> "))

    try:
        repo = g.get_repo(usr_input)
        release = repo.get_latest_release()

        if usr_input not in repo_list:
            print("The repo has being found! Adding to the repo list .txt...")
            with open(repo_list_name, "a") as f:
                f.write(f"{usr_input}\n")
            print("Repo added!")  
          
        else: print(f"The repo {usr_input} is already in the repo list!")

    except Exception as e:
        print(f"Failed to add the {usr_input} repo: {e}")

def install_packages():
    for repo_name in repo_list:

        try:
            repo = g.get_repo(repo_name)

            release = repo.get_latest_release()

            for asset in release.get_assets():
                objects_detected = 0
                objects_to_be_detected = len(golden_list)
                for object in golden_list:
                    if object in asset.name:
                        objects_detected += 1
                if objects_detected == objects_to_be_detected:
                    print(f"The object to be installed is: {asset.name}")
                    package = asset.name

            subprocess.run(["/usr/bin/gh", "release", "download", release.tag_name, "--repo", repo_name, "--pattern", package, "--dir", downloads, "--skip-existing"])
            subprocess.run(["sudo", "dnf", "install", f"{downloads}/{package}"])

        except Exception as e:
            print(f"Error while installing the program from the repo {repo_name}: {e}")
            continue

#main loop
while True:
    try:
        read_repo_list()
        print("="*10)
        print(f"Current repo list: ")
        for repo in repo_list:
            print(repo)
        
        usr_command = int(input("What`s your command?\n1- Update repo list\n2- Install packages\n>> "))

        if usr_command == 1:
            add_repo()

        elif usr_command == 2:
            install_packages()

        else: print(f"{usr_command} is not a valid command.")
    
    except Exception as e:
        print(f"Failed to execute the main loop: {e}")

        