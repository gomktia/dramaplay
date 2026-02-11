import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import re

class AdvancedPageCloner:
    def __init__(self, url, output_dir):
        self.url = url
        self.output_dir = output_dir
        self.assets_dir = os.path.join(output_dir, 'assets')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Folder structure
        os.makedirs(os.path.join(self.assets_dir, 'css'), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, 'js'), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, 'img'), exist_ok=True)

    def download_asset(self, asset_url, subfolder):
        if not asset_url or asset_url.startswith('data:'):
            return asset_url
            
        try:
            clean_url = asset_url.split('?')[0].split('#')[0]
            filename = os.path.basename(urlparse(clean_url).path)
            if not filename or '.' not in filename:
                ext = '.asset'
                if subfolder == 'css': ext = '.css'
                elif subfolder == 'js': ext = '.js'
                elif subfolder == 'img': ext = '.jpg'
                filename = 'asset_' + re.sub(r'[^\w]', '_', asset_url[-10:]) + ext
            
            filename = re.sub(r'[^\w\.-]', '_', filename)
            local_path = os.path.join(self.assets_dir, subfolder, filename)
            
            if os.path.exists(local_path):
                return f'assets/{subfolder}/{filename}'

            print(f"Downloading {asset_url}...")
            response = self.session.get(asset_url, timeout=10)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                return f'assets/{subfolder}/{filename}'
        except Exception as e:
            print(f"Error downloading {asset_url}: {e}")
        return asset_url

    def clone(self):
        print(f"Fetching main page {self.url}...")
        response = self.session.get(self.url)
        if response.status_code != 200:
            print(f"Failed to fetch page: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Process CSS
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                link['href'] = self.download_asset(urljoin(self.url, href), 'css')

        # 2. Process JS
        for script in soup.find_all('script'):
            # Check all possible src attributes
            src_attrs = ['src', 'data-rocket-src', 'data-lazy-src', 'data-src']
            found_src = None
            for attr in src_attrs:
                if script.get(attr):
                    found_src = script[attr]
                    if attr != 'src':
                        del script[attr] # Remove the data- attribute
            
            if found_src:
                script['src'] = self.download_asset(urljoin(self.url, found_src), 'js')
                if script.get('type') == 'rocketlazyloadscript':
                    script['type'] = 'text/javascript'

        # 3. Process Images
        for img in soup.find_all('img'):
            src_attrs = ['src', 'data-lazy-src', 'data-rocket-src', 'data-src']
            found_src = None
            
            # Prioritize lazy sources
            for attr in src_attrs[1:]:
                if img.get(attr):
                    found_src = img[attr]
                    del img[attr]
            
            if not found_src and img.get('src'):
                # If it's a data URL or placeholder, we might have missed the real source
                if img['src'].startswith('data:'):
                    pass # Keep placeholder if no real source found? Better delete it or point to local.
                else:
                    found_src = img['src']

            if found_src:
                img['src'] = self.download_asset(urljoin(self.url, found_src), 'img')
            
            # Remove srcset to simplify
            for attr in ['srcset', 'data-lazy-srcset', 'data-srcset']:
                if img.get(attr):
                    del img[attr]

        # 4. Remove WP Rocket Artifacts
        for script in soup.find_all('script'):
            if script.string and any(x in script.string for x in ['RocketLazyLoadScripts', 'rocket-lazyload']):
                script.decompose()

        # Save HTML
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        
        print(f"Done! Cleaned page cloned to {self.output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Clone")
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    cloner = AdvancedPageCloner(args.url, args.output)
    cloner.clone()
