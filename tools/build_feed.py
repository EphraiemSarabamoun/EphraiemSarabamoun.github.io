#!/usr/bin/env python3
"""Build an RSS 2.0 feed (feed.xml) of every post in posts/blog*.html.

Why it exists: the site is hand-written HTML with no generator, so it had no
feed, and Substack's post importer only takes a URL or an RSS feed. This
script reads each post, pulls out the title, date, header image and body, and
writes one <item> per post with the full HTML in <content:encoded>.

Usage: python3 build_feed.py <site-repo-dir>   (writes <site-repo-dir>/feed.xml)

Assumptions, all true of the posts as of 2026-10-30:
  - each post has h1.blog-title, p.blog-meta (a <time datetime> or a
    "Month D, YYYY" date), an optional img.blog-image, and div.blog-content
    running to the end of the file;
  - relative links point at ../images/, ../writings.html or a sibling post.
YouTube iframes become plain watch links, because importers drop iframes and
Substack turns a bare YouTube link into an embed.
"""
import html
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

SITE = "https://www.scipolitic.com"
AUTHOR = "Ephraiem Sarabamoun"


def first(pattern, text, default=""):
    """Return group 1 of the first match of pattern in text, or default."""
    m = re.search(pattern, text, re.S)
    return m.group(1) if m else default


def post_date(meta):
    """Read the publication date from the blog-meta paragraph."""
    iso = first(r'<time datetime="(\d{4}-\d{2}-\d{2})"', meta)
    if iso:
        d = datetime.strptime(iso, "%Y-%m-%d")
    else:
        plain = re.sub(r"<[^>]+>|\s+", " ", meta)
        d = datetime.strptime(first(r"([A-Z][a-z]+ \d{1,2}, \d{4})", plain), "%B %d, %Y")
    # Noon UTC keeps the calendar date stable in any reader's time zone.
    return d.replace(hour=12, tzinfo=timezone.utc)


def body_html(src):
    """Extract the post body: header image plus blog-content, with absolute URLs."""
    content = first(r'<div class="blog-content"[^>]*>(.*)', src)
    # Trim the closing wrapper, back link and page tail after the body.
    content = re.split(r'<a href="\.\./writings\.html"', content)[0]
    content = re.sub(r"(\s*</div>)+\s*$", "", content.strip())
    # Only an image ABOVE the body counts as the header; blog20 has none and
    # its first blog-image sits inside the body, which would show it twice.
    above = src.split('<div class="blog-content"')[0]
    header = first(r'(<img [^>]*class="blog-image"[^>]*>)', above)
    out = (header + "\n" if header else "") + content

    def youtube(m):
        vid = m.group(1)
        title = first(r'title="([^"]*)"', m.group(0), "Video")
        url = f"https://www.youtube.com/watch?v={vid}"
        return f'<p><a href="{url}">{title}</a></p>\n<p>{url}</p>'

    out = re.sub(r'<iframe[^>]*youtube[^>]*/embed/([\w-]+)[^>]*>\s*</iframe>', youtube, out)
    out = out.replace('src="../images/', f'src="{SITE}/images/')
    out = out.replace('href="../', f'href="{SITE}/')
    out = re.sub(r'href="(blog\d+\.html)"', rf'href="{SITE}/posts/\1"', out)
    return out


def item(path):
    """Build one RSS <item> for a post file; returns (date, xml)."""
    src = path.read_text(encoding="utf-8")
    title = html.unescape(re.sub(r"\s+", " ", first(r'class="blog-title"[^>]*>(.*?)</h1>', src)).strip())
    date = post_date(first(r'class="blog-meta"[^>]*>(.*?)</p>', src))
    summary = html.unescape(first(r'<meta property="og:description" content="([^"]*)"', src))
    link = f"{SITE}/posts/{path.name}"
    body = body_html(src).replace("]]>", "]]]]><![CDATA[>")
    xml = f"""    <item>
      <title>{html.escape(title)}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{format_datetime(date)}</pubDate>
      <dc:creator>{AUTHOR}</dc:creator>
      <description>{html.escape(summary)}</description>
      <content:encoded><![CDATA[{body}]]></content:encoded>
    </item>"""
    return date, xml


def main(repo):
    posts = sorted(Path(repo, "posts").glob("blog*.html"))
    items = sorted((item(p) for p in posts), key=lambda x: x[0], reverse=True)
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{AUTHOR}: Writings</title>
    <link>{SITE}/writings.html</link>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Essays by {AUTHOR}.</description>
    <language>en-us</language>
    <lastBuildDate>{format_datetime(items[0][0])}</lastBuildDate>
{chr(10).join(x for _, x in items)}
  </channel>
</rss>
"""
    Path(repo, "feed.xml").write_text(feed, encoding="utf-8")
    print(f"wrote {len(items)} items to {Path(repo, 'feed.xml')}")


if __name__ == "__main__":
    main(sys.argv[1])
