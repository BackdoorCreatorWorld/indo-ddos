#!/usr/bin/env python3
"""
Cloudflare Bypass Handler
Bypass Cloudflare protection
"""

import requests
import random
import time
import re

class CloudflareBypass:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        })
        
    def detect_cloudflare(self, url):
        """Detect if site uses Cloudflare"""
        try:
            response = self.session.get(url, timeout=5, allow_redirects=True)
            
            # Check headers
            headers = str(response.headers).lower()
            if 'cloudflare' in headers or 'cf-ray' in headers:
                return True
            
            # Check page content
            content = response.text.lower()
            cf_indicators = [
                'cloudflare',
                'cf-challenge',
                'jschl_vc',
                'jschl_answer',
                'ray id',
                'cf-browser-verification'
            ]
            
            for indicator in cf_indicators:
                if indicator in content:
                    return True
            
            return False
            
        except Exception as e:
            print(f"[!] Cloudflare detection failed: {str(e)}")
            return False
    
    def bypass_v2_5(self, url):
        """Attempt Cloudflare bypass v2.5"""
        print("[*] Attempting Cloudflare bypass v2.5...")
        
        methods = [
            self._bypass_header_rotation,
            self._bypass_cookie_injection,
            self._bypass_js_challenge,
            self._bypass_referer_spoof
        ]
        
        for method in methods:
            try:
                print(f"[*] Trying {method.__name__}...")
                success = method(url)
                if success:
                    print("[✓] Bypass successful")
                    return True
            except Exception as e:
                continue
        
        print("[!] All bypass methods failed")
        return False
    
    def _bypass_header_rotation(self, url):
        """Bypass method 1: Header rotation"""
        headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            },
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'DNT': '1'
            },
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-gb',
                'X-Requested-With': 'XMLHttpRequest'
            }
        ]
        
        for headers in headers_list:
            try:
                response = self.session.get(url, headers=headers, timeout=10)
                if response.status_code == 200 and 'cf-browser-verification' not in response.text:
                    return True
            except:
                continue
        
        return False
    
    def _bypass_cookie_injection(self, url):
        """Bypass method 2: Cookie injection"""
        # Common Cloudflare cookie patterns
        cookie_templates = [
            '__cfduid={rand32}; cf_clearance={rand40}',
            '__cf_bm={rand60}; __cfduid={rand32}',
            'cf_clearance={rand40}; __cflb={rand20}'
        ]
        
        for template in cookie_templates:
            try:
                # Generate fake cookies
                rand32 = ''.join(random.choices('0123456789abcdef', k=32))
                rand40 = ''.join(random.choices('0123456789abcdef', k=40))
                rand60 = ''.join(random.choices('0123456789abcdef', k=60))
                rand20 = ''.join(random.choices('0123456789abcdef', k=20))
                
                cookies = template.format(
                    rand32=rand32,
                    rand40=rand40,
                    rand60=rand60,
                    rand20=rand20
                )
                
                headers = {'Cookie': cookies}
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    # Update session cookies
                    if 'set-cookie' in response.headers:
                        self.session.headers.update({'Cookie': response.headers['set-cookie']})
                    return True
                    
            except:
                continue
        
        return False
    
    def _bypass_js_challenge(self, url):
        """Bypass method 3: JavaScript challenge solver (simulated)"""
        print("[*] Simulating JS challenge solving...")
        time.sleep(2)  # Simulate solving time
        
        try:
            # Extract challenge if present (simplified)
            response = self.session.get(url, timeout=10)
            
            if 'jschl_vc' in response.text and 'jschl_answer' in response.text:
                # Simulate solving the challenge
                time.sleep(1)
                
                # Make another request with "solved" challenge
                headers = self.session.headers.copy()
                headers['Cookie'] = 'cf_clearance=simulated_' + ''.join(random.choices('0123456789abcdef', k=32))
                
                response2 = self.session.get(url, headers=headers, timeout=10)
                return response2.status_code == 200
            
            return response.status_code == 200
            
        except:
            return False
    
    def _bypass_referer_spoof(self, url):
        """Bypass method 4: Referer spoofing"""
        referers = [
            'https://www.google.com/',
            'https://www.facebook.com/',
            'https://twitter.com/',
            'https://www.reddit.com/',
            'https://www.bing.com/',
            'https://duckduckgo.com/',
            'https://www.youtube.com/',
            'https://www.amazon.com/'
        ]
        
        for referer in referers:
            try:
                headers = {'Referer': referer}
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    return True
            except:
                continue
        
        return False
    
    def generate_stealth_headers(self):
        """Generate stealth headers for requests"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36'
        ]
        
        accept_languages = [
            'en-US,en;q=0.9',
            'en-GB,en;q=0.8',
            'en;q=0.7',
            'en-US,en;q=0.5'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': '*/*',
            'Accept-Language': random.choice(accept_languages),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'DNT': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Add random referer 30% of the time
        if random.random() > 0.7:
            referers = ['https://google.com', 'https://facebook.com', 'https://twitter.com']
            headers['Referer'] = random.choice(referers)
        
        return headers
