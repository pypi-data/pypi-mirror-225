import os
import re
import subprocess
import argparse

def get_pylint_score(filepath, score_threshold, rcfile):
    pylint_cmd = f"pylint --rcfile={rcfile} {filepath}"
    process = subprocess.Popen(pylint_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    pattern = r"rated at (\d+\.\d+)/10"
    def print_bad_output(output):
        print("\033[91m{}\033[0m".format(output))  # Output in red

    def print_good_output(output):
        print("\033[92m{}\033[0m".format(output))  # Output in green

    # Extracting the pylint score from the output, printing the score and the pylint output
    for line in stdout.decode("utf-8").splitlines():
        if line.startswith("Your code has been rated at"):
            match = re.search(pattern, line)
            if match:
                score = float(match.group(1))
                if score < score_threshold:
                    print_bad_output(f"{filepath}: Pylint Score - {score} - [BLOCKED]")
                    print(stdout.decode("utf-8"))
                else:
                    print_good_output(f"{filepath}: Pylint Score - {score} - [PASSED]")
                return score

def main():
    exit_code = 0  # By default, set exit code to 0

    parser = argparse.ArgumentParser(description='Run Pylint on files in a folder and print scores.')
    parser.add_argument('file_paths', nargs='+', help='Path to the file to be checked with Pylint.')
    parser.add_argument('--score_threshold', type=float, default=8.0, help='Score threshold for failing the check.')
    parser.add_argument('--rcfile', default='', help='Path to the custom .pylintrc')

    args = parser.parse_args()
    file_paths = args.file_paths
    score_threshold = args.score_threshold
    rcfile = args.rcfile

    for file_path in file_paths:
        if not os.path.isfile(file_path):
            print(f"The file '{file_path}' not found.")
            continue
        
        if not file_path.endswith('.py'):
            print(f"The file '{file_path}' is not a python file")
            continue

        # We pass the function through the files .py
        score = get_pylint_score(file_path, score_threshold, rcfile)
        if score is not None and score < score_threshold:
            exit_code = 1

    exit(exit_code)

if __name__ == "__main__":
    main()
