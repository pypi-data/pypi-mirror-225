#!/usr/bin/env python3

import io
import os
import re
import bs4
import time
import shutil
import urllib
import getpass
import sqlite3
import requests
import gallery_dvk.config
import html_string_tools
import python_print_tools.printer
import metadata_magic.file_tools as mm_file_tools
import metadata_magic.rename.rename_tools as mm_rename_tools
from os.path import abspath, exists, join
from typing import List

def get_filename_from_page(page:dict, directory:str, filename_format:str="{title}") -> str:
    """
    Creates a filename based on contents of a given page, formatted to a given format.
    Will append filename with a number if the given filename already exists in the given directory.
    The file will follow the structure of filename_format.
    Keys in curly brackets will be replaced with that key's value in the page
    
    :param page: Page to extract values from if necessary
    :type page: dict, required
    :param directory: Directory the file is destined for, used to check if filename already exists
    :type directory: str, required
    :param filename_format: How to format the filename
    :type filename_format: str, required
    :return: Filename for the page
    :rtype: str
    """
    # Replace stand-in keys in the filename
    filename = filename_format
    keys = re.findall(r"(?<={)[^}]+(?=})", filename)
    for key in keys:
        try:
            filename = filename.replace(f"{{{key}}}", page[key])
        except KeyError: pass
    filename = mm_rename_tools.create_filename(filename)
    # Get the extension for the media type
    try: extension = html_string_tools.html.get_extension(page["image_url"])
    except KeyError:
        try: extension = html_string_tools.html.get_extension(page["url"])
        except KeyError: extension = ""
    if extension == "":
        extension = ".jpg"
    # Append the with numbers if necessary
    num = 2
    base_filename = filename
    while (exists(abspath(join(directory, f"{filename}{extension}")))
                or exists(abspath(join(directory, f"{filename}.json")))):
        filename = f"{base_filename}-{num}"
        num += 1
    # Return the filename
    return filename

def get_date(date_string:str, date_order:str=None) -> str:
    """
    Attempts to format a given date string into YYYY-MM-DD format.
    If date_order is None, attempts to find month as a string, determining day and year from context.
    If date_order is not None, attempts to get date with day month and string all represented as numbers.
    date_order should have "y" "m" and "d" in the order that date_string is formatted.
    For example, if date_string is YYYY/MM/DD, date_order should be "ymd"
    If date_string is MM/DD/YYYY, date_order should be "mdy"
    
    :param date_string: String containing date information
    :type date_string: str, required
    :param date_order: Day(d), Month(m), and Year(d) in the order date_string is formatted, defaults to None
    :type date_order: str, optional
    :return: Date in YYYY-MM-DD format
    :rtype: str
    """
    # Try getting date if a given date string format is given
    if date_order is not None:
        string = re.findall(r"\b[0-9]+\/[0-9]+\/[0-9]+\b|\b[0-9]+-[0-9]+-[0-9]+\b", date_string)[0]
        regex = {"y":"[0-9]{4}", "m":"[0-1]?[0-9]", "d":"[0-3]?[0-9]"}
        regex[date_order[0]] = "^" + regex[date_order[0]] + r"(?=[\/-])"
        regex[date_order[1]] = r"(?<=[\/-])" + regex[date_order[1]] + r"(?=[\/-])"
        regex[date_order[2]] = r"(?<=[\/-])" + regex[date_order[2]] + "$"
        year = re.findall(regex["y"], string)[0].zfill(4)
        month = re.findall(regex["m"], string)[0].zfill(2)
        day = re.findall(regex["d"], string)[0].zfill(2)
        return f"{year}-{month}-{day}"
    # Get the string month
    month_dict = {"jan":"01", "feb":"02", "mar":"03", "apr":"04", "may":"05", "jun":"06",
                    "jul":"07", "aug":"08", "sep":"09", "oct":"10", "nov":"11", "dec":"12",
                    "january":"01", "february":"02", "march":"03", "april":"04", "may":"05", "june":"06",
                    "july":"07", "august":"08", "september":"09", "october":"10", "november":"11", "december":"12"}
    strings = re.findall(r"\b[a-z]+\b", date_string.lower())
    month = None
    for string in strings:
        try:
            month = month_dict[string]
            break
        except KeyError: month = None
    assert int(month) < 13
    # Get the day
    day = re.findall(r"(?<=[^:])\b[0-3]?[0-9]\b(?=[^:])", f" {date_string} ")[0].zfill(2)
    # Get the year
    year = re.findall(r"(?<=[^:])\b[0-9]{4}\b(?=[^:])", f" {date_string} ")[0]
    # Return a string for the year
    return f"{year}-{month}-{day}"

class Extractor:
    def __init__(self, category:str, config_paths:List[str]=gallery_dvk.config.get_default_config_paths()):
        """
        Creates the Extractor object and loads configuration files.
        
        :param category: Category of the extractor based on what site is being downloaded from
        :type category: str, required
        :param config_paths: Paths to attempt to read as a configuration file, defaults to default config paths
        :type config_paths: list[str]
        """
        # Set the URL matchers
        self.url_matchers = []
        page_match = r"(?:https?:\/\/)?(?:www\.)?thing\.txt\/view\/[^\/]+\/?$"
        page_section = r"(?<=thing\.txt\/view\/)[^\/]+(?=\/?$)"
        self.url_matchers.append({"match":page_match, "section":page_section, "type":"submission"})
        gallery_match = r"(?:https?:\/\/)?(?:www\.)?thing\.txt\/user\/[^\/]+\/?$"
        gallery_section = r"(?<=thing\.txt\/user\/)[^\/]+(?=\/?$)"
        self.url_matchers.append({"match":gallery_match, "section":gallery_section, "type":"gallery"})
        # Set session and archive files to be empty
        self.requests_session = None
        self.archive_file = None
        self.archive_connection = None
        # Load the config file
        config = gallery_dvk.config.get_config(config_paths)
        self.get_info_from_config(config, category)
        # Set the extractor so that login has not been attempted
        self.attempted_login = False
    
    def __enter__(self):
        """
        Setup for when the extractor is opened.
        """
        return self
    
    def __exit__(self, *args):
        """
        Cleanup for the extractor once it is closed.
        """
        # Close the sqlite archive connection
        try:
            self.archive_connection.close()
        except AttributeError: pass
        # Close the requests session
        try:
            self.requests_session.close()
        except AttributeError: pass
    
    def get_id(self, url:str) -> str:
        """
        Returns the ID for a given URL.
        Intended as stand-in to get overwritten by inherited classes.

        :param url: URL to use to generate ID
        :type url: str, required
        :return: ID based on the URL
        :rtype: str
        """
        return url
    
    def match_url(self, url:str) -> dict:
        """
        Matches a given URL to a particular function based on the regex matches in the self.url_matchers list.
        If the URL matches none of the patterns in self.url_matchers, None is returned.
        If a URL matches a pattern, a section is extracted based on the "section" key in self.url_matchers.
        A dictionary with the URL section and type indicating the function to use will be returned.
        
        :param url: URL to attempt to match to the patterns in the self.url_matchers list.
        :type url: str, required
        :return: Dictionary containing URL section and the type of method to use for downloading.
        :rtype: dict
        """
        for matcher in self.url_matchers:
            if re.fullmatch(matcher["match"], url.lower()):
                section = re.findall(matcher["section"], url.lower())[0]
                return {"section":section, "type":matcher["type"]}
        return None
    
    def download_from_url(self, url:str, directory:str) -> bool:
        """
        Attempts to download from a given URL, basing method to use off of the match_url method.
        If the URL matches none of the patterns in self.url_matchers, the method returns False.
        
        :param url: URL to attempt download from.
        :type url: str, required
        :param directory: Directory in which to save files
        :type directory: str, required.
        :return: Whether or not the download completed successfully.
        :rtype: bool
        """
        match = self.match_url(url)
        if match is None:
            return False
        self.user_login()
        return getattr(self, "download_" + match["type"])(match["section"], abspath(directory))
    
    def download_submission(self, section:str, directory:str) -> bool:
        """
        Stand-In method to be overwritten.
        """
        return True
    
    def download_gallery(self, section:str, directory:str) -> bool:
        """
        Stand-In method to be overwritten.
        """
        return True
    
    def get_info_from_config(self, config:dict, category:str):
        """
        Sets variables in the Extractor object based on values in a given config dictionary.
        
        :param config: Dictionary containing gallery-dvk config info
        :type config: dict, required
        :param category: Category of extractor to search config file for
        :type category: str, required
        """
        # Get the archive file
        try:
            self.archive_file = str(config[category]["archive"])
        except KeyError: self.archive_file = None
        # Get whether to include metadata
        try:
            self.write_metadata = bool(config[category]["metadata"])
        except KeyError: self.write_metadata = False
        # Get the galleries to include
        try:
            self.include = config[category]["include"]
        except KeyError: self.include = []
        # Get the site username
        try:
            self.username = str(config[category]["username"])
        except KeyError: self.username = None
        # Get the site password
        try:
            self.password = str(config[category]["password"])
        except KeyError: self.password = None
        # Get the filename format for the site
        try:
            self.filename_format = str(config[category]["filename_format"])
        except KeyError: self.filename_format = "{title}"
            
    
    def open_archive(self):
        """
        Attempts to open a sqlite database based on the archive file given in the config file.
        """
        try:
            # Open Connection
            assert self.archive_connection is None
            self.archive_connection = sqlite3.connect(self.archive_file)
            # Check if table exists
            cursor = self.archive_connection.cursor()
            try:
                result = cursor.execute("SELECT idtitle FROM identifiers")
            except sqlite3.OperationalError:
                result = cursor.execute("CREATE TABLE identifiers(idtitle)")
            # Commit
            self.archive_connection.commit()
        except TypeError:
            self.archive_connection = None
    
    def add_to_archive(self, identifier:str):
        """
        Attempts to add a given identifying string as an entry to the archive database.
        
        :param identifier: Identifying string to add as an entry
        :type identifier: str, required
        """
        try:
            # Add identifier to the database table
            cursor = self.archive_connection.cursor()
            result = cursor.execute(f"INSERT INTO identifiers VALUES ('{identifier}')")
            self.archive_connection.commit()
        except AttributeError: pass
    
    def archive_contains(self, identifier:str) -> bool:
        """
        Returns whether the archive database contains a given identifying string.
        Returns false if there is no archive file.
        
        :param identifier: Identifying string to search the database for.
        :type identifier: str, required
        :return: Whether the database contains an entry for the given identifier
        :rtype: bool
        """
        try:
            # Search for identifier with the given name
            cursor = self.archive_connection.cursor()
            result = cursor.execute(f"SELECT idtitle FROM identifiers WHERE idtitle='{identifier}'")
            return result.fetchone() is not None
        except AttributeError:
            return False
    
    def initialize(self):
        """
        Initializes the requests session and sqlite archive database.
        Does nothing if objects are already created.
        """
        # Set the Session object
        if self.requests_session is None:
            headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
                        "Accept-Language":"en-US,en;q=0.5"}
            self.requests_session = requests.Session()
            self.requests_session.headers.update(headers)
        # Open database
        if self.archive_connection is None:
            self.open_archive()
            
    def dict_to_header(self, dictionary:dict, key:str):
        """
        Adds a given dictionary and key to the requests header of the sessions object.

        :param dictionary: Dictionary to turn into form-data
        :type dictionary: dict, required
        :param key: Header key
        :type key: str, required
        """
        # Add items to the text
        dict_text = ""
        for item in dictionary.items():
            dict_text = f"{dict_text};{item[0]}={item[1]}"
        # Remove semicolon
        while dict_text.startswith(";"):
            dict_text = dict_text[1:]
        # Add to the header list
        if not dict_text == "" and not key == "":
            self.requests_session.headers.update({key:dict_text})

    def cookies_to_header(self):
        """
        Add session cookies to the requests header.
        """
        self.dict_to_header(self.requests_session.cookies.get_dict(), "Cookie")
        
    def web_get(self, url:str, sleep:float=1.0) -> bs4.BeautifulSoup:
        """
        Returns a BeautifulSoup object for the response of a GET request on a given URL.
        
        :param url: URL to get with a GET request
        :type url: str, required
        :param sleep: Amount of time to sleep after the request, defaults to 1.0
        :type sleep: float, optional
        :return: BeautifulSoup object from the response
        :rtype: BeautifulSoup
        """
        # Get URL
        self.initialize()
        response = self.requests_session.get(url)
        # Get BeautifulSoup object from the URL
        time.sleep(sleep)
        response.encoding = "utf-8"
        bs = bs4.BeautifulSoup(response.text, features="lxml")
        return bs
        
    def download(self, url:str=None, file_path:str=None, sleep:float=1.0) -> dict:
        """
        Downloads a file from given URL to given file.
        
        :param url: Given URL, defaults to None
        :type url: str, optional
        :param file_path: Given file path, defaults to None
        :type file_path: str, optional
        :param sleep: Amount of time to sleep after the request, defaults to 1.0
        :type sleep: float, optional
        :return: Headers retrieved from the given media URL
        :rtype: dict
        """
        try:
            self.initialize()
            file = abspath(file_path)
            response = self.requests_session.get(url)
            byte_obj = io.BytesIO(response.content)
            byte_obj.seek(0)
            with open(file, "wb") as f:
                shutil.copyfileobj(byte_obj, f)
            return response.headers
        except (AttributeError,
                    urllib.error.HTTPError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.MissingSchema,
                    ConnectionResetError,
                    TypeError):
            if url is not None:
                python_print_tools.printer.color_print(f"Failed to download: {url}", "r")
        time.sleep(sleep)
        return dict()
    
    def download_page(self, page:dict, directory:str, subs:List[str]=[]) -> str:
        """
        Downloads a URL from info gathered from a page dict.
        Creates a JSON metadata file from the page if self.write_metadata in Extractor is True.
        Adds date from last-modified response if no date present in page dict.

        :param page: Dictionary containing page data, uses "title" and "url"/"image_url"
        :type page: dict, required
        :param directory: Directory to save files into
        :type directory: str, required
        :param subs: Optional subdirectories to create to save files into, defaults to []
        :type subs: list[str]
        :return: Path of the media file created, if applicable
        :rtype: str
        """
        # Check if the page is already downloaded
        self.initialize()
        identifier = self.get_id(page["url"])
        if self.archive_contains(identifier):
            print(page["url"])
            return None
        # Create subfolders if necessary
        full_directory = abspath(directory)
        for sub in subs:
            full_directory = abspath(join(full_directory, mm_rename_tools.create_filename(sub)))
            if not exists(full_directory):
                os.mkdir(full_directory)
        # Get filename
        filename = get_filename_from_page(page, directory, self.filename_format)
        # Get media URL
        try:
            media_url = page["image_url"]
        except KeyError:
            media_url = page["url"]
        # Download media
        extension = html_string_tools.html.get_extension(media_url)
        if extension == "":
            extension = ".jpg"
        media_file = abspath(join(full_directory, f"{filename}{extension}"))
        response = self.download(media_url, media_file)
        assert exists(media_file)
        python_print_tools.printer.color_print(page["url"], "g")
        # Add date if required
        updated_page = page
        try: date = updated_page["date"]
        except KeyError:
            updated_page["date"] = get_date(response["Last-Modified"])
        # Write JSON file
        if self.write_metadata:
            json_file = abspath(join(full_directory, f"{filename}.json"))
            mm_file_tools.write_json_file(json_file, updated_page)
        # Add identifier to the database
        self.add_to_archive(identifier)
        return media_file
    
    def login(self, username:str, password:str) -> bool:
        """
        Attempts to login the requests_session object to a website.
        Stand-in method to be overwritten

        :param username: Username
        :type username: str, required
        :param password: Password
        :type password: str, required
        :return: Whether login was successful
        :rtype: bool
        """
        self.attempted_login = True
        return True
    
    def user_login(self, site:str=None) -> bool:
        """
        Asks user for login information before attempting login.
        
        :param site: Site that is being logged in to, defaults to None
        :type site: str, optional
        :return: Whether the login was successful
        :rtype: bool
        """
        if site is not None and not self.attempted_login:
            self.attempted_login = True
            # Get the username and password from the config file
            username = self.username
            password = self.password
            # Get the username and password from the user if not already configured
            if username is None:
                username = input(f"{site} Username: ")
            if password is None:
                password = getpass.getpass(f"{site} Password: ")
            # Attempt login
            logged_in = self.login(username, password)
            username = None
            password = None
            return logged_in
        self.attempted_login = True
        return False
