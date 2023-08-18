##
#     Project: WatchPage
# Description: Watch webpages for changes
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2022-2023 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import json
import re
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


class Target(object):
    def __init__(self,
                 name: str,
                 url: str,
                 parser: str,
                 type: str,
                 use_absolute_urls: bool,
                 filters: list,
                 headers: dict[str, str]):
        self.name = name
        self.initial_url = url
        if url.startswith('github:'):
            # Handle special url with github: prefix
            url = f'https://github.com/{url[7:]}'
            if type.casefold() in ('github-tags',
                                   'github-tags-tgz',
                                   'github-tags-zip'):
                url = f'{url}/tags'
        self.url = url
        self.parser = parser
        self.type = type
        self.use_absolute_urls = use_absolute_urls
        self.filters = filters
        self.headers = headers

    def open_url(self) -> bytes:
        """
        Get the raw URL content

        :return: downloaded content from the URL
        """
        request = urllib.request.Request(url=self.url)
        for header, value in self.headers.items():
            request.add_header(key=header, val=value)
        with urllib.request.urlopen(url=request) as response:
            return response.read()

    def parse_url(self) -> BeautifulSoup:
        """
        Parser the associated URL

        :return: parsed page
        """
        soup = BeautifulSoup(markup=self.open_url(),
                             features=self.parser)
        return soup

    def get_github_tags(self) -> list[str]:
        """
        Get all the GitHub tags in the page

        :return: list of URLs
        """
        results = []
        for url in self.get_links():
            # Find only tags urls
            filter_url = f'/{self.initial_url[7:]}/archive/refs/tags/'
            if self.use_absolute_urls:
                filter_url = f'https://github.com{filter_url}'
            matching_url = False
            if url.startswith(filter_url):
                matching_url = True
                if (self.type.casefold() == 'github-tags-zip' and
                        not url.endswith('.zip')):
                    # Exclude urls not in zip format
                    matching_url = False
                elif (self.type.casefold() == 'github-tags-tgz' and
                      not url.endswith('.tar.gz')):
                    # Exclude urls not in tar.gz format
                    matching_url = False
            # Include only matching URLs
            if matching_url:
                results.append(url)
        return results

    def get_links(self) -> list[str]:
        """
        Get all the links in the page

        :return: list of URLs
        """
        parser = self.parse_url()
        results = []
        for anchor in parser.find_all('a'):
            # Find only anchors with href
            if 'href' in anchor.attrs:
                if self.use_absolute_urls:
                    # Make URL absolute
                    url = urllib.parse.urljoin(base=self.url,
                                               url=anchor['href'])
                else:
                    # Leave the URL as is
                    url = anchor['href']
                if url:
                    results.append(url)
        return results

    def get_rss_links(self) -> list[str]:
        """
        Get all the links from a RSS page

        :return: list of URLs
        """
        parser = self.parse_url()
        results = []
        for anchor in parser.find_all('item'):
            # Find only anchors with href
            if anchor.link:
                if self.use_absolute_urls:
                    # Make URL absolute
                    url = urllib.parse.urljoin(base=self.url,
                                               url=anchor.link.text)
                else:
                    # Leave the URL as is
                    url = anchor.link.text
                results.append(url)
        return results

    def get_results(self) -> list[str]:
        """
        Get the results from the downloaded page from the URL

        :return: results list
        """
        # Get results
        if self.type.casefold() == 'links':
            # Get only links from the page
            items = self.get_links()
        elif self.type.casefold() == 'text':
            # Filter empty lines and remove leading spaces
            items = filter(len,
                           map(str.strip,
                               self.open_url()
                               .decode('utf-8')
                               .replace('\r', '')
                               .split('\n')))
        elif self.type.casefold() == 'rss':
            # Get only links from a RSS feed
            items = self.get_rss_links()
        elif self.type.casefold() in ('github-tags',
                                      'github-tags-tgz',
                                      'github-tags-zip'):
            # Get only GitHub tags links
            items = self.get_github_tags()
        else:
            # Unexpected response type
            items = []
        # Filter results
        results = []
        for item in items:
            valid = True
            # Filter results
            for filter_type in self.filters:
                # Skip further checks if the result is not valid
                if not valid:
                    break
                if 'STARTS' in filter_type:
                    # Link starts with the pattern
                    filter_value = filter_type['STARTS']
                    valid = item.startswith(filter_value)
                elif 'NOT STARTS' in filter_type:
                    # Link doesn't start with the pattern
                    filter_value = filter_type['NOT STARTS']
                    valid = not item.startswith(filter_value)
                elif 'ENDS' in filter_type:
                    # Link ends with the pattern
                    filter_value = filter_type['ENDS']
                    valid = item.endswith(filter_value)
                elif 'NOT ENDS' in filter_type:
                    # Link doesn't end with the pattern
                    filter_value = filter_type['NOT ENDS']
                    valid = not item.endswith(filter_value)
                elif 'CONTAINS' in filter_type:
                    # Link contains the pattern
                    filter_value = filter_type['CONTAINS']
                    valid = filter_value in item
                elif 'NOT CONTAINS' in filter_type:
                    # Link doesn't contain the pattern
                    filter_value = filter_type['NOT CONTAINS']
                    valid = filter_value not in item
                elif 'REGEX' in filter_type:
                    # Link matches the pattern
                    filter_value = filter_type['REGEX']
                    valid = bool(re.search(pattern=filter_value,
                                           string=item))
                elif 'NOT REGEX' in filter_type:
                    # Link doesn't match the pattern
                    filter_value = filter_type['NOT REGEX']
                    valid = not bool(re.search(pattern=filter_value,
                                               string=item))
                elif 'TRIM' in filter_type:
                    # Trim characters on the left and right side
                    filter_value = filter_type['TRIM']
                    item = item.strip(filter_value)
                elif 'LTRIM' in filter_type:
                    # Trim characters on the left side
                    filter_value = filter_type['LTRIM']
                    item = item.lstrip(filter_value)
                elif 'RTRIM' in filter_type:
                    # Trim characters on the right side
                    filter_value = filter_type['RTRIM']
                    item = item.rstrip(filter_value)
                elif 'PREPEND' in filter_type:
                    # Prepend text
                    filter_value = filter_type['PREPEND']
                    item = f'{filter_value}{item}'
                elif 'APPEND' in filter_type:
                    # Append text
                    filter_value = filter_type['APPEND']
                    item = f'{item}{filter_value}'
                elif 'REMOVE' in filter_type:
                    # Remove matching
                    filter_value = filter_type['REMOVE']
                    item = item.replace(filter_value, '')
                elif 'REVERSE' in filter_type:
                    # Reverse the text
                    item = item[::-1]
                elif 'UPPER' in filter_type:
                    # Make the text uppercase
                    item = item.upper()
                elif 'LOWER' in filter_type:
                    # Make the text lowercase
                    item = item.lower()
                elif 'LEFT' in filter_type:
                    # Leftmost characters
                    filter_value = filter_type['LEFT']
                    item = item[:filter_value]
                elif 'RIGHT' in filter_type:
                    # Rightmost characters
                    filter_value = filter_type['RIGHT']
                    item = item[-filter_value:]
                elif 'REPLACE' in filter_type:
                    # Replace pattern
                    filter_value = filter_type['REPLACE']
                    filter_value_2 = filter_type['WITH']
                    item = item.replace(filter_value, filter_value_2)
                elif 'REGEX REPLACE' in filter_type:
                    # Replace a regular expression pattern
                    filter_value = filter_type['REGEX REPLACE']
                    filter_value_2 = filter_type['WITH']
                    item = re.sub(pattern=filter_value,
                                  repl=filter_value_2,
                                  string=item)
                elif 'REGEX SEARCH' in filter_type:
                    # Return the first regular expression match
                    filter_value = filter_type['REGEX SEARCH']
                    item = re.search(pattern=filter_value,
                                     string=item)[0]
                elif 'JSON DICT' in filter_type:
                    # Get a value from a JSON dictionary
                    filter_value = filter_type['JSON DICT']
                    item = json.dumps(json.loads(item)[filter_value])
                elif 'JSON LIST' in filter_type:
                    # Get a value from a JSON list
                    filter_value = filter_type['JSON LIST']
                    item = json.dumps(json.loads(item)[filter_value])
                else:
                    # Invalid filter
                    valid = False
            if valid:
                # Add a valid link
                results.append(item)
        return results
