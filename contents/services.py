import ipaddress
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class LinkPreviewService:
    TIMEOUT = 5
    MAX_RESPONSE_SIZE = 2 * 1024 * 1024  # 2MB
    YOUTUBE_OEMBED_URL = 'https://www.youtube.com/oembed?url={url}&format=json'

    def fetch_preview(self, url: str) -> dict:
        """Fetch Open Graph metadata from a URL.

        Returns dict with preview_image_url, og_title, og_description.
        All values default to None on any failure.

        Falls back to YouTube oEmbed when OG scraping returns nothing,
        since YouTube blocks OG tags for datacenter IPs.
        """
        empty = {'preview_image_url': None, 'og_title': None, 'og_description': None}

        if not url:
            return empty

        if not self._is_safe_url(url):
            return empty

        result = self._fetch_og(url)

        if not any(result.values()) and self._is_youtube_url(url):
            result = self._fetch_youtube_oembed(url)

        return result

    def _fetch_og(self, url: str) -> dict:
        empty = {'preview_image_url': None, 'og_title': None, 'og_description': None}
        try:
            headers = {'User-Agent': 'StudyHub/1.0 (link preview fetcher)'}
            response = requests.get(
                url, timeout=self.TIMEOUT, headers=headers, stream=True
            )
            response.raise_for_status()

            content = b''
            for chunk in response.iter_content(chunk_size=8192):
                content += chunk
                if len(content) > self.MAX_RESPONSE_SIZE:
                    break

            soup = BeautifulSoup(content, 'html.parser')

            def get_og(prop):
                tag = soup.find('meta', property=prop) or soup.find(
                    'meta', attrs={'name': prop}
                )
                return tag.get('content', '').strip() if tag else None

            return {
                'preview_image_url': get_og('og:image') or None,
                'og_title': get_og('og:title') or None,
                'og_description': get_og('og:description') or None,
            }

        except Exception:
            return empty

    def _is_youtube_url(self, url: str) -> bool:
        try:
            hostname = urlparse(url).hostname or ''
            return hostname in ('www.youtube.com', 'youtube.com', 'youtu.be')
        except Exception:
            return False

    def _fetch_youtube_oembed(self, url: str) -> dict:
        empty = {'preview_image_url': None, 'og_title': None, 'og_description': None}
        try:
            oembed_url = self.YOUTUBE_OEMBED_URL.format(url=requests.utils.quote(url, safe=''))
            response = requests.get(oembed_url, timeout=self.TIMEOUT)
            response.raise_for_status()
            data = response.json()
            return {
                'preview_image_url': data.get('thumbnail_url') or None,
                'og_title': data.get('title') or None,
                'og_description': data.get('author_name') or None,
            }
        except Exception:
            return empty

    def _is_safe_url(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            if parsed.scheme not in ('http', 'https'):
                return False
            hostname = parsed.hostname
            if not hostname:
                return False
            try:
                addr = ipaddress.ip_address(hostname)
                return not (
                    addr.is_private or addr.is_loopback or addr.is_link_local
                )
            except ValueError:
                # It's a hostname, not an IP — allow it
                return True
        except Exception:
            return False
