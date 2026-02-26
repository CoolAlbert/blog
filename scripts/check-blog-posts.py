#!/usr/bin/env python3
"""
Check Albert's blog for new posts and notify Lisa.

Checks RSS/Atom feed for new entries and sends notifications via Telegram.
Uses only standard library to avoid external dependencies.
"""

import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import json
import os
from datetime import datetime, timezone
import subprocess
import html
import re

# Configuration
BLOG_RSS_URL = "https://coolalbert.github.io/blog/feed.xml"
LIZA_TELEGRAM_ID = "333273004"
STATE_FILE = "/home/user/.openclaw/workspace/scripts/blog-notifications-state.json"


def load_state():
    """Load the state file with known posts."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"notified_posts": {}, "last_check": None}


def save_state(state):
    """Save the state file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def send_to_lisa(message):
    """Send message to Lisa via Telegram using openclaw."""
    cmd = [
        'openclaw', 'message', 'send',
        '--channel', 'telegram',
        '--target', LIZA_TELEGRAM_ID,
        '--message', message
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def strip_html(text):
    """Simple HTML tag removal."""
    if not text:
        return ''
    text = re.sub(r'<[^>]+>', '', text)
    return html.unescape(text).strip()


def get_text_content(elem):
    """Get text content from element, handling CDATA and nested elements."""
    if elem is None:
        return ''

    # Try direct text first
    if elem.text:
        return elem.text

    # Try to get text from all children
    text_parts = []
    if elem.text:
        text_parts.append(elem.text)
    for child in elem:
        if child.text:
            text_parts.append(child.text)
        if child.tail:
            text_parts.append(child.tail)

    return ''.join(text_parts)


def check_blog():
    """Check blog RSS feed for new posts."""
    print(f"[{datetime.now().isoformat()}] Checking blog...")

    state = load_state()
    notified_posts = set(state.get("notified_posts", {}).keys())

    # Fetch RSS feed
    try:
        with urllib.request.urlopen(BLOG_RSS_URL, timeout=30) as response:
            rss_content = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error fetching feed: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    # Parse XML with CDATA handling
    try:
        root = ET.fromstring(rss_content)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return

    # Try to detect format and get entries
    entries = []

    # Check for Atom format
    atom_entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
    if atom_entries:
        # Atom format
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in atom_entries:
            # Get title - try direct text, then handle type="html"
            title_elem = entry.find('atom:title', ns)
            title = ''
            if title_elem is not None:
                title = get_text_content(title_elem)

            # Get link
            link = ''
            link_elem = entry.find('atom:link[@rel="alternate"]', ns)
            if link_elem is not None:
                link = link_elem.get('href', '')
            else:
                # Try other link formats
                link_elem2 = entry.find('atom:link', ns)
                if link_elem2 is not None:
                    link = link_elem2.get('href', '')

            # Get published date
            published = ''
            pub_elem = entry.find('atom:published', ns)
            if pub_elem is not None and pub_elem.text:
                published = pub_elem.text
            else:
                updated_elem = entry.find('atom:updated', ns)
                if updated_elem is not None and updated_elem.text:
                    published = updated_elem.text

            # Get ID
            post_id = ''
            id_elem = entry.find('atom:id', ns)
            if id_elem is not None and id_elem.text:
                post_id = id_elem.text
            elif link:
                post_id = link

            # Get summary/description
            description = ''
            summary_elem = entry.find('atom:summary', ns)
            if summary_elem is not None:
                description = get_text_content(summary_elem)
            if not description:
                content_elem = entry.find('atom:content', ns)
                if content_elem is not None:
                    desc = get_text_content(content_elem)
                    description = desc[:200] + '...' if len(desc) > 200 else desc

            # Clean title
            if title:
                title = strip_html(title)

            # Clean description
            if description:
                description = strip_html(description)
                if len(description) > 200:
                    description = description[:200] + '...'

            if post_id:
                entries.append({
                    'id': post_id,
                    'title': title or 'Без названия',
                    'link': link,
                    'published': published or 'Без даты',
                    'description': description
                })
    else:
        # Try RSS 2.0 format
        rss_entries = root.findall('.//item')
        for entry in rss_entries:
            title_elem = entry.find('title')
            link_elem = entry.find('link')
            pub_elem = entry.find('pubDate')
            desc_elem = entry.find('description')

            title = title_elem.text if title_elem is not None and title_elem.text else 'Без названия'
            link = link_elem.text if link_elem is not None and link_elem.text else ''
            published = pub_elem.text if pub_elem is not None and pub_elem.text else 'Без даты'

            description = ''
            if desc_elem is not None and desc_elem.text:
                desc = strip_html(desc_elem.text)
                description = desc[:200] + '...' if len(desc) > 200 else desc

            post_id = link

            if post_id:
                entries.append({
                    'id': post_id,
                    'title': title,
                    'link': link,
                    'published': published,
                    'description': description
                })

    # Filter out already notified posts
    new_posts = [p for p in entries if p['id'] not in notified_posts]

    # Notify about new posts
    if new_posts:
        print(f"Found {len(new_posts)} new post(s)")

        for post in new_posts:
            message = f"""📝 **Новый пост в блоге Альберта!**

**{post['title']}**

📅 {post['published']}

{post['description']}

🔗 {post['link']}
"""

            if send_to_lisa(message):
                print(f"  ✓ Notified about: {post['title'][:50]}")
                state['notified_posts'][post['id']] = {
                    'title': post['title'],
                    'link': post['link'],
                    'notified_at': datetime.now(timezone.utc).isoformat()
                }
            else:
                print(f"  ✗ Failed to notify about: {post['title'][:50]}")
    else:
        print("No new posts")

    # Update state
    state['last_check'] = datetime.now(timezone.utc).isoformat()
    save_state(state)

    print(f"[{datetime.now().isoformat()}] Check complete")


if __name__ == '__main__':
    check_blog()
