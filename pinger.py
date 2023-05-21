#!/usr/bin/python3
from tabulate import tabulate
import concurrent.futures
import subprocess
import re
import sys

num = 0
ping_results = []

def ping(ip):
    ping = subprocess.Popen(["ping", "-c", ping_count, ip], stdout=subprocess.PIPE)
    ping.wait()
    output = ping.communicate()[0].decode()
    exit_code = ping.returncode
    loss_rate_pattern = r"(\d+)% packet loss"
    match = re.search(loss_rate_pattern, output)
    if match:
        loss_rate = float(match.group(1))
        if loss_rate < max_loss_rate:
            global num
            num = num + 1
            ping_results.append([num, ip, loss_rate])

if len(sys.argv) < 4:
    print("Usage: python my_script.py input_file ping_count max_loss_rate")
    sys.exit(1)

filename = sys.argv[1]
ping_count = sys.argv[2]
max_loss_rate = float(sys.argv[3])

with open(filename) as f:
    ips = [line.strip() for line in f.readlines()]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(ping, ip) for ip in ips]

table_headers = ["آدرس", "شماره IP", "ضریب از دست رفتگی"]
print(tabulate(ping_results,tablefmt="orgtbl", headers=table_headers))
