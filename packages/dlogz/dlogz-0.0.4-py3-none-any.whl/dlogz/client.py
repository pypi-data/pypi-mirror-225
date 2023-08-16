import requests
import re
import subprocess
from datetime import datetime
# import zipfile
# import os

# class Dlogz:
#     def __init__(self, api_url):
#         self.api_url = api_url

#     def compress_files(self, files, compressed_filename):
#         with zipfile.ZipFile(compressed_filename, 'w') as zipf:
#             for file_path in files:
#                 zipf.write(file_path, os.path.basename(file_path))

#     def send_compressed_files(self, files):
#         try:
#             compressed_filename = 'compressed_files.zip'
#             self.compress_files(files, compressed_filename)

#             with open(compressed_filename, 'rb') as compressed_file:
#                 response = requests.post(self.api_url, files={'compressed_file': compressed_file})
#                 if response.status_code == 200:
#                     print('Compressed files sent successfully!')
#                 else:
#                     print('Failed to send compressed files. Status code:', response.status_code)

#             os.remove(compressed_filename)
#         except Exception as e:
#             print('Error:', e)


class Dlogz:
    def __init__(self, file, api_url):
        self.file = file
        self.api_url = api_url
    
    def get_commit_details(self):
        commit_details = []
        git_log_command = ["git", "log", "--follow", "--date=iso", "--format=%ad %H", self.file]
        result = subprocess.run(git_log_command, capture_output=True, text=True)
        if result.returncode == 0:
            commit_details_str = result.stdout
            commit_lines = commit_details_str.strip().split('\n')
            commit_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \+\d{4}) ([a-f0-9]+)"

            for line in commit_lines:
                match = re.match(commit_pattern, line)
                if match:
                    timestamp_str, commit_hash = match.groups()
                    date = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S %z").strftime("%Y-%m-%d")
                    commit_details.append((date, commit_hash, self.file))
            return commit_details
        else:
            return []
    
    def send_file_details(self):
        commit_details = self.get_commit_details()
        payload = {'filename': self.file, 'details': {}, 'user': 'abhijeet@kredily.com'}
        for date, commit_hash, filename in commit_details:
            year = int(date[:4])
            if 2022 <= year <= 2023:
                git_checkout_command = ["git", "checkout", commit_hash, "--", filename]
                try:
                    subprocess.run(git_checkout_command, check=True)
                    result = subprocess.run(["radon", "cc", filename], capture_output=True, text=True)
                    output = result.stdout.strip()
                    year_month = date[:7]
                    payload['details'].update({year_month: output})
                except subprocess.CalledProcessError as e:
                    print("An error occurred:", e)
                finally:
                    # Reset repository back to the latest commit
                    git_reset_command = ["git", "reset", "--hard", "HEAD"]
                    subprocess.run(git_reset_command, check=True)
        self.populate_file_commits_by_month(payload=payload)

    
    def populate_file_commits_by_month(self, payload):
        try:
            print(f'payload: {payload}')
            response = requests.post(self.api_url, data=payload)
            if response.status_code == 200:
                print('Compressed files sent successfully!')
            else:
                print('Failed to send compressed files. Status code:', response.status_code)
        except Exception as err:
            print(err)