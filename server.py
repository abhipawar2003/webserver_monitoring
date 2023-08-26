import requests
import psutil
import time
import re
from datetime import datetime, timedelta

url = 'https://google.com'
max_response_time = 2 
check_interval = 60 
uptime_threshold = 0.99 
cpu_threshold = 80 
memory_threshold = 80 
error_threshold = 5 
traffic_threshold = 1000 
security_regex = r"<script>alert\('XSS'\);<\/script>"

def measure_response_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    return end_time - start_time, response.status_code, response.content.decode()

def measure_resource_utilization():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    return cpu_percent, memory_percent

def measure_traffic():
    traffic_start_time = datetime.now() - timedelta(minutes=1)
    traffic_count = 0
    with open('/var/log/nginx/access.log') as f:
        for line in f:
            fields = line.split()
            request_time = datetime.strptime(fields[3][1:], '%d/%b/%Y:%H:%M:%S')
            if request_time >= traffic_start_time:
                traffic_count += 1
    return traffic_count

start_time = time.time()
total_checks = 0
successful_checks = 0
error_count = 0
traffic_count = 0

while True:
    try:
        response_time, status_code, content = measure_response_time(url)
        total_checks += 1
        if response_time > max_response_time:
            print(f"ALERT: Response time ({response_time:.2f}s) exceeded threshold ({max_response_time}s)")
        else:
            successful_checks += 1
            print(f"Response time: {response_time:.2f}s, Status code: {status_code}")
        uptime = successful_checks / total_checks
        if uptime < uptime_threshold:
            print(f"ALERT: Uptime ({uptime:.2%}) fell below threshold ({uptime_threshold:.2%})")
        else:
            print(f"Uptime: {uptime:.2%}")
        cpu_percent, memory_percent = measure_resource_utilization()
        if cpu_percent > cpu_threshold:
            print(f"ALERT: CPU usage ({cpu_percent:.2f}%) exceeded threshold ({cpu_threshold}%)")
        else:
            print(f"CPU usage: {cpu_percent:.2f}%")
        if memory_percent > memory_threshold:
            print(f"ALERT: Memory usage ({memory_percent:.2f}%) exceeded threshold ({memory_threshold}%)")
        else:
            print(f"Memory usage: {memory_percent:.2f}%")
        if re.search(security_regex, content):
            print(f"ALERT: Security breach detected ({security_regex})")
        else:
            print("Security: OK")
        traffic_count = measure_traffic()
        if traffic_count > traffic_threshold:
            print(f"ALERT: Traffic count ({traffic_count}) exceeded threshold ({traffic_threshold})")
        else:
            print(f"Traffic count: {traffic_count}")
        error_count = 0
    except Exception as e:
        error_count += 1
        print(f"ALERT: Error occurred ({e}), count: {error_count}")
        if error_count >= error_threshold:
            print(f"ALERT: Maximum error threshold ({error_threshold}) exceeded, exiting...")