#!/usr/bin/env python3
"""
Proxy Manager
Proxy loading and management
"""

import random
import requests
import time

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.last_update = 0
        
    def load_proxies(self, force=False):
        """Load proxies from various sources"""
        # Only reload if older than 1 hour or forced
        if not force and time.time() - self.last_update < 3600 and self.proxies:
            return self.proxies
        
        print("[*] Loading proxies...")
        all_proxies = []
        
        # Static proxy list (always available)
        static_proxies = [
            '45.77.56.114:8080',
            '138.197.157.32:8080',
            '165.227.36.191:8080',
            '167.71.41.76:8080',
            '45.76.44.175:8080',
            '45.32.140.23:8080',
            '209.97.150.167:8080',
            '51.158.68.26:8811',
            '51.158.68.133:8811',
            '188.166.83.17:3128',
            '159.203.61.169:8080',
            '167.99.123.158:8080',
            '64.225.8.82:9991',
            '64.225.8.82:9992',
            '64.225.8.82:9993',
            '64.225.8.82:9994',
            '64.225.8.82:9995',
            '104.238.156.12:8080',
            '104.238.156.12:8081',
            '104.238.156.12:8082',
            '104.238.156.12:8083',
            '104.238.156.12:8084',
            '45.77.245.244:3128',
            '45.77.245.244:8080',
            '45.77.245.244:8888',
            '45.77.245.244:9999',
            '45.77.245.244:10000',
            '161.97.126.96:3128',
            '161.97.126.96:8080',
            '161.97.126.96:8888',
            '161.97.126.96:9999',
            '161.97.126.96:10000',
            '198.199.86.11:8080',
            '198.199.86.11:3128',
            '198.199.86.11:8888',
            '198.199.86.11:9999',
            '198.199.86.11:10000',
            '167.71.5.83:8080',
            '167.71.5.83:3128',
            '167.71.5.83:8888',
            '167.71.5.83:9999',
            '167.71.5.83:10000',
            '68.183.45.189:8080',
            '68.183.45.189:3128',
            '68.183.45.189:8888',
            '68.183.45.189:9999',
            '68.183.45.189:10000',
            '157.245.27.9:3128',
            '157.245.27.9:8080',
            '157.245.27.9:8888',
            '157.245.27.9:9999',
            '157.245.27.9:10000'
        ]
        all_proxies.extend(static_proxies)
        
        # Online sources
        sources = [
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
            'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
            'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt'
        ]
        
        for source in sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    lines = response.text.strip().split('\n')
                    valid_proxies = []
                    for line in lines:
                        line = line.strip()
                        if ':' in line and len(line.split(':')) == 2:
                            valid_proxies.append(line)
                    
                    all_proxies.extend(valid_proxies)
                    print(f"[+] Loaded {len(valid_proxies)} proxies from {source.split('/')[-1]}")
                    
            except Exception as e:
                continue
        
        # Remove duplicates
        self.proxies = list(set(all_proxies))
        self.last_update = time.time()
        
        # Save to file
        try:
            with open('data/proxies.txt', 'w') as f:
                for proxy in self.proxies:
                    f.write(f"{proxy}\n")
        except:
            pass
        
        print(f"[✓] Total proxies: {len(self.proxies)}")
        return self.proxies
    
    def get_proxies(self, count=50):
        """Get specified number of random proxies"""
        if not self.proxies:
            self.load_proxies()
        
        if len(self.proxies) < count:
            return self.proxies
        
        return random.sample(self.proxies, count)
    
    def get_random_proxy(self):
        """Get a single random proxy"""
        if not self.proxies:
            self.load_proxies()
        
        if self.proxies:
            return random.choice(self.proxies)
        return None
    
    def test_proxy(self, proxy):
        """Test if proxy is working"""
        try:
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=5
            )
            
            return response.status_code == 200
        except:
            return False
    
    def get_working_proxies(self, max_tests=20):
        """Get working proxies by testing them"""
        if not self.proxies:
            self.load_proxies()
        
        working = []
        test_proxies = random.sample(self.proxies, min(max_tests, len(self.proxies)))
        
        print("[*] Testing proxies...")
        for proxy in test_proxies:
            if self.test_proxy(proxy):
                working.append(proxy)
        
        print(f"[✓] Found {len(working)} working proxies")
        return working
