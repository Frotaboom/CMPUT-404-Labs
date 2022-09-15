import requests

res = requests.get("https://raw.githubusercontent.com/Frotaboom/CMPUT-404-Labs/master/Lab1/request_version.py?token=GHSAT0AAAAAABYK5FCVJ7W44JA4NAY553N2YZCOHLQ")
print(res.text)