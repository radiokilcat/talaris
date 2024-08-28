import re
import webbrowser
import os
import sys

def open_urls_in_firefox(file_path):
    # Regex to find URLs in the format [text](http://example.com) or just http://example.com
    url_pattern = re.compile(r'\[.*?\]\((http[s]?://.*?)\)|\b(http[s]?://\S+)\b')

    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Find all matches in the content
        matches = url_pattern.findall(content)
        urls = [match[0] if match[0] else match[1] for match in matches]

        if not urls:
            print("No URLs found in the note.")
            return

        print(f"Found {len(urls)} URLs. Opening in Firefox...")

        # Open each URL in Firefox
        for url in urls:
            webbrowser.get('firefox').open(url)
            print(f"Opened: {url}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(r'C:\Program Files\Mozilla Firefox\firefox.exe'))
    if len(sys.argv) != 2:
        print("Usage: python open_urls.py <path_to_obsidian_note>")
        sys.exit(1)

    file_path = sys.argv[1]
    open_urls_in_firefox(file_path)
