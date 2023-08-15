#!/usr/bin/env python3

import os
import metadata_magic.file_tools as mm_file_tools
import gallery_dvk.extractor.extractor as gd_extractor
from gallery_dvk.extractor.extractor import Extractor
from os.path import abspath, basename, exists, join

def test_get_filename_from_page():
    """
    Tests the get_filename_from_page function.
    """
    # Test the getting default filenames
    temp_dir = mm_file_tools.get_temp_dir()
    assert gd_extractor.get_filename_from_page({"title":"Name?!"}, temp_dir) == "Name-!"
    assert gd_extractor.get_filename_from_page({}, temp_dir) == "{title}"  
    # Test getting more complicated filenames
    page = {"title":"New", "id":"1234", "date":"2012-12-21", "artist":"Person"}
    assert gd_extractor.get_filename_from_page(page, temp_dir, "[{id}] {title}") == "[1234] New"
    assert gd_extractor.get_filename_from_page(page, temp_dir, "website-{title}") == "website-New" 
    assert gd_extractor.get_filename_from_page(page, temp_dir, "{date}_{id}_{artist}") == "2012-12-21_1234_Person" 
    # Test if there is an existing media file with the same name and different extension
    mm_file_tools.write_text_file(abspath(join(temp_dir, "duplicate.jpg")), "TEST")
    page = {"title":"duplicate", "image_url":"blah/thing.png"}
    assert gd_extractor.get_filename_from_page(page, temp_dir) == "duplicate"
    page = {"title":"duplicate", "url":"blah/thing.txt"}
    assert gd_extractor.get_filename_from_page(page, temp_dir) == "duplicate"
    # Test if there is an existing media file with the same name and extension
    page = {"title":"duplicate", "image_url":"blah/thing.jpg"}
    assert gd_extractor.get_filename_from_page(page, temp_dir) == "duplicate-2"
    page = {"title":"duplicate", "url":"blah/thing.jpg"}
    assert gd_extractor.get_filename_from_page(page, temp_dir) == "duplicate-2"
    # Test if there is an existing json file with the same name
    mm_file_tools.write_json_file(abspath(join(temp_dir, "new.json")), {"key":"value"})
    mm_file_tools.write_json_file(abspath(join(temp_dir, "new-2.json")), {"key":"value"})
    page = {"title":"new", "image_url":"blah/thing.txt"}
    assert gd_extractor.get_filename_from_page(page, temp_dir) == "new-3"
    page = {"title":"new", "url":"blah/thing.png"}
    assert gd_extractor.get_filename_from_page(page, temp_dir) == "new-3"

def test_get_date():
    """
    Tests the get_date function.
    """
    # Test getting date with full month
    assert gd_extractor.get_date("5 January, 2015") == "2015-01-05"
    assert gd_extractor.get_date("08 february,2012") == "2012-02-08"
    assert gd_extractor.get_date("25 March, 2015") == "2015-03-25"
    assert gd_extractor.get_date("14 April, 2023") == "2023-04-14"
    assert gd_extractor.get_date("  14  May,  2023 ") == "2023-05-14"
    assert gd_extractor.get_date("12 June 2014") == "2014-06-12"
    assert gd_extractor.get_date("12:30 July 15 2023") == "2023-07-15"
    assert gd_extractor.get_date("August 24, 2023") == "2023-08-24"
    assert gd_extractor.get_date("Thing 2015 September 4") == "2015-09-04"
    assert gd_extractor.get_date("October  18 , 1997 other crap") == "1997-10-18"
    assert gd_extractor.get_date("14 November, 2022") == "2022-11-14"
    assert gd_extractor.get_date("14, December 2023  12:14") == "2023-12-14"
    # Test getting date with abriviated month
    assert gd_extractor.get_date("Udf, 10 Jan 2010 12:05:55 GMT") == "2010-01-10"
    assert gd_extractor.get_date("14 Feb 2034") == "2034-02-14"
    assert gd_extractor.get_date("Mar 13, 1997  ") == "1997-03-13"
    assert gd_extractor.get_date("Apr 25, 2034 20:12") == "2034-04-25"
    assert gd_extractor.get_date(" 3 may 2014") == "2014-05-03"
    assert gd_extractor.get_date("Time jun 28 2040 Thing") == "2040-06-28"
    assert gd_extractor.get_date("10 JUL 2042") == "2042-07-10"
    assert gd_extractor.get_date("AUG 2042 10") == "2042-08-10"
    assert gd_extractor.get_date("10 sep 2042") == "2042-09-10"
    assert gd_extractor.get_date("10 oct 2042") == "2042-10-10"
    assert gd_extractor.get_date("10 nov 2042") == "2042-11-10"
    assert gd_extractor.get_date("10 dec 2042") == "2042-12-10"
    # Test getting date in various number formats
    assert gd_extractor.get_date("10/1/2020", date_order="dmy") == "2020-01-10"
    assert gd_extractor.get_date(" 9/02/2020 ", date_order="dmy") == "2020-02-09"
    assert gd_extractor.get_date("12 14-03-2021 thing", date_order="dmy") == "2021-03-14"
    assert gd_extractor.get_date("thing 14-04-2021 10", date_order="dmy") == "2021-04-14"
    assert gd_extractor.get_date("5/1/2020", date_order="mdy") == "2020-05-01"
    assert gd_extractor.get_date(" 6/02/2020 ", date_order="mdy") == "2020-06-02"
    assert gd_extractor.get_date("12 07-03-2021 thing", date_order="mdy") == "2021-07-03"
    assert gd_extractor.get_date("thing 08-04-2021 10", date_order="mdy") == "2021-08-04"
    assert gd_extractor.get_date("2024/9/13", date_order="ymd") == "2024-09-13"
    assert gd_extractor.get_date(" 2020/10/15 ", date_order="ymd") == "2020-10-15"
    assert gd_extractor.get_date("12 2021-11-07 thing", date_order="ymd") == "2021-11-07"
    assert gd_extractor.get_date("thing 2021-12-06 10", date_order="ymd") == "2021-12-06"

def test_get_id():
    """
    Tests the get_id method.
    """
    with Extractor("thing", []) as extractor:
        assert extractor.get_id("thing") == "thing"

def test_match_url():
    """
    Tests the match_url function.
    """
    with Extractor("thing", []) as extractor:
        # Test matching page URL
        match = extractor.match_url("thing.txt/view/blah")
        assert match["section"] == "blah"
        assert match["type"] == "submission"
        match = extractor.match_url("http://www.thing.txt/view/next/")
        assert match["section"] == "next"
        assert match["type"] == "submission"
        match = extractor.match_url("https://thing.txt/view/final/")
        assert match["section"] == "final"
        assert match["type"] == "submission"
        # Test matching gallery URL
        match = extractor.match_url("thing.txt/user/blah")
        assert match["section"] == "blah"
        assert match["type"] == "gallery"
        match = extractor.match_url("http://www.thing.txt/user/next/")
        assert match["section"] == "next"
        assert match["type"] == "gallery"
        match = extractor.match_url("https://thing.txt/user/final/")
        assert match["section"] == "final"
        assert match["type"] == "gallery"
        # Test matching invalid URL
        assert extractor.match_url("thing.txt/other/thing") is None
        assert extractor.match_url("thing.txt/user/thing/new") is None
        assert extractor.match_url("thing.com/view/thing") is None
        assert extractor.match_url("google.com/whatever") is None

def test_download_from_url():
    """
    Tests the download_from_url function.
    """
    with Extractor("thing", []) as extractor:
        # Test trying to download invalid URLs
        assert not extractor.download_from_url("thing.com/view/thing", "doesn't")
        assert not extractor.download_from_url("thing.txt/other/thing", "matter")
        assert not extractor.download_from_url("google.com/thing", "file")
        # Test tyring to download from valid URLs
        assert extractor.download_from_url("http://www.thing.txt/view/next/", "thing")
        assert extractor.download_from_url("http://www.thing.txt/user/next/", "other")
        assert extractor.download_from_url("thing.txt/view/blah", "final")
        assert extractor.attempted_login

def test_get_info_from_config():
    """
    Tests the get_info_from_config method.
    """
    # Test if there is no config file to get info from
    with Extractor("thing", []) as extractor:
        assert extractor.archive_file is None
        assert extractor.archive_connection is None
        assert not extractor.write_metadata
        assert extractor.include == []
        assert extractor.username is None
        assert extractor.password is None
        assert not extractor.attempted_login
        assert extractor.filename_format == "{title}"
    # Test getting the archive_file from the config file
    temp_dir = mm_file_tools.get_temp_dir()
    config_file = abspath(join(temp_dir, "config.json"))
    config = {"thing":{"archive":"/file/path/"}, "other":{"archive":"thing"}}
    mm_file_tools.write_json_file(config_file, config)
    assert exists(config_file)
    with Extractor("thing", [config_file]) as extractor:
        assert extractor.archive_file == "/file/path/"
        assert extractor.archive_connection is None
        assert not extractor.write_metadata
    # Test getting the write_metadata variable
    config = {"thing":{"metadata":True}, "other":{"metadata":False}}
    mm_file_tools.write_json_file(config_file, config)
    with Extractor("thing", [config_file]) as extractor:
        assert extractor.write_metadata
    # Test getting the included variable
    config = {"thing":{"include":["gallery", "scraps"]}}
    mm_file_tools.write_json_file(config_file, config)
    with Extractor("thing", [config_file]) as extractor:
        assert extractor.include == ["gallery", "scraps"]
    # Test getting the username and password variables
    config = {"thing":{"username":"Person", "password":"other"}}
    mm_file_tools.write_json_file(config_file, config)
    with Extractor("thing", [config_file]) as extractor:
        assert extractor.username == "Person"
        assert extractor.password == "other"
    # Test getting the filename_format
    config = {"thing":{"filename_format":"[{date}] {title}"}}
    mm_file_tools.write_json_file(config_file, config)
    with Extractor("thing", [config_file]) as extractor:
        assert extractor.filename_format == "[{date}] {title}"
    # Test if the category is invalid
    with Extractor("different", [config_file]) as extractor:
        assert extractor.archive_file is None
        assert extractor.archive_connection is None
        assert not extractor.write_metadata
        assert extractor.include == []
        assert extractor.username is None
        assert extractor.password is None
        assert not extractor.attempted_login
        assert extractor.filename_format == "{title}"

def test_open_archive():
    """
    Tests the open_archive method.
    """
    # Test attempting to open archive if there is no archive file
    with Extractor("thing", []) as extractor:
        extractor.open_archive()
        assert extractor.archive_file is None
        assert extractor.archive_connection is None
    # Test attempting to open archive if the archive directory is invalid
    with Extractor("thing", ["/non/existant/directory/"]) as extractor:
        extractor.open_archive()
        assert extractor.archive_file is None
        assert extractor.archive_connection is None
    # Test properly opening an archive file
    temp_dir = mm_file_tools.get_temp_dir()
    config_file = abspath(join(temp_dir, "config.json"))
    database_file = abspath(join(temp_dir, "data.sqlite3"))
    config = {"thing":{"archive":database_file}}
    mm_file_tools.write_json_file(config_file, config)
    assert exists(config_file)
    assert not exists(database_file)
    with Extractor("thing", [config_file]) as extractor:
        extractor.open_archive()
        assert extractor.archive_file == database_file
        assert extractor.archive_connection is not None
    assert exists(database_file)
    assert sorted(os.listdir(temp_dir)) == ["config.json", "data.sqlite3"]

def test_add_to_archive():
    """
    Tests the add_to_archive method.
    """
    # Test attempting to add to archive if the archive file does not exist
    with Extractor("thing", []) as extractor:
        extractor.open_archive()
        assert extractor.archive_file is None
        assert extractor.archive_connection is None
        extractor.add_to_archive("whatever")
    # Test checking archive contents
    temp_dir = mm_file_tools.get_temp_dir()
    config_file = abspath(join(temp_dir, "config.json"))
    database_file = abspath(join(temp_dir, "data.sqlite3"))
    config = {"thing":{"archive":database_file}}
    mm_file_tools.write_json_file(config_file, config)
    assert exists(config_file)
    assert not exists(database_file)
    with Extractor("thing", [config_file]) as extractor:
        extractor.open_archive()
        extractor.add_to_archive("new")
        extractor.add_to_archive("thing")
    with Extractor("thing", [config_file]) as extractor:
        extractor.open_archive()
        assert extractor.archive_contains("new")
        assert extractor.archive_contains("thing")
        assert not extractor.archive_contains("archive")
        assert not extractor.archive_contains("blah")

def test_archive_contains():
    """
    Tests the archive_contains method.
    """
    # Test attempting to read archive if the archive file does not exist
    with Extractor("thing", []) as extractor:
        extractor.open_archive()
        assert extractor.archive_file is None
        assert extractor.archive_connection is None
        assert not extractor.archive_contains("whatever")
    # Test checking archive contents
    temp_dir = mm_file_tools.get_temp_dir()
    config_file = abspath(join(temp_dir, "config.json"))
    database_file = abspath(join(temp_dir, "data.sqlite3"))
    config = {"thing":{"archive":database_file}}
    mm_file_tools.write_json_file(config_file, config)
    assert exists(config_file)
    assert not exists(database_file)
    with Extractor("thing", [config_file]) as extractor:
        extractor.open_archive()
        extractor.add_to_archive("item")
        extractor.add_to_archive("other")
    with Extractor("thing", [config_file]) as extractor:
        extractor.open_archive()
        assert extractor.archive_contains("item")
        assert extractor.archive_contains("other")
        assert not extractor.archive_contains("thing")
        assert not extractor.archive_contains("blah")

def test_dict_to_header():
    """
    Tests the dict_to_header method.
    """
    with Extractor("thing", []) as extractor:
        # Test adding a key
        extractor.initialize()
        extractor.dict_to_header({"a":"thing", "b":"other"}, "key")
        assert extractor.requests_session.headers["key"] == "a=thing;b=other"
        # Test if there is only one entry
        extractor.dict_to_header({"Thing":"New"}, "new")
        assert extractor.requests_session.headers["new"] == "Thing=New"
        # Test if the dictionary is empty
        extractor.dict_to_header({}, "Blah")
        try:
            assert extractor.requests_session.headers["Blah"] == "Thing"
        except KeyError: pass
        # Test overwriting a header entry
        extractor.dict_to_header({"yet":"another"}, "key")
        assert extractor.requests_session.headers["key"] == "yet=another"

def test_web_get():
    """
    Tests the web_get method.
    """
    # Test getting webpage
    with Extractor("thing", []) as extractor:
        bs = extractor.web_get("https://pythonscraping.com/exercises/exercise1.html")
        element = bs.find("h1").get_text()
        assert element == "An Interesting Title"
        element = bs.find("div").get_text()
        assert "Lorem ipsum dolor" in element
        assert "sed do eiusmod tempor" in element
        assert "id est laborum." in element

def test_download():
    """
    Tests the download function.
    """
    with Extractor("thing", []) as extractor:
        # Test downloading a given file
        test_dir = mm_file_tools.get_temp_dir()
        file = abspath(join(test_dir, "image.jpg"))
        url = "https://www.pythonscraping.com/img/gifts/img6.jpg"
        extractor.download(url, file)
        assert exists(file)
        assert os.stat(file).st_size == 39785
        # Test downloading with invalid parameters
        file = join(test_dir, "invalid.jpg")
        extractor.download(None, None)
        assert not exists(file)
        extractor.download(None, file)
        assert not exists(file)
        extractor.download("asdfasdf", file)
        assert not exists(file)
        extractor.download(url, None)
        assert not exists(file)


    
def test_download_page():
    """
    Tests the download_page method.
    """
    temp_dir = mm_file_tools.get_temp_dir()
    database_file = abspath(join(temp_dir, "data.db"))
    page = {"title":"Thing!", "url": "https://www.pythonscraping.com/img/gifts/img6.jpg"}
    config_file = abspath(join(temp_dir, "config.json"))
    archive_file = abspath(join(temp_dir, "test.sqlite3"))
    config = {"thing":{"archive":archive_file, "metadata":True}}
    mm_file_tools.write_json_file(config_file, config)
    # Test downloading to same directory, adding date
    with Extractor("thing", [config_file]) as extractor:
        media_file = extractor.download_page(page, temp_dir)
        assert basename(media_file) == "Thing!.jpg"
        assert exists(media_file)
        assert extractor.archive_contains("https://www.pythonscraping.com/img/gifts/img6.jpg")
    json_file = abspath(join(temp_dir, "Thing!.json"))
    assert exists(json_file)
    assert os.stat(media_file).st_size == 39785
    meta = mm_file_tools.read_json_file(json_file)
    assert meta["title"] == "Thing!"
    assert meta["url"] == "https://www.pythonscraping.com/img/gifts/img6.jpg"
    assert meta["date"] == "2014-08-04"
    # Test downloading to subdirectory, retaining date
    page["title"] = "Title: Revelations"
    page["url"] = "blah"
    page["image_url"] = "https://www.pythonscraping.com/img/gifts/img4.jpg"
    page["date"] = "2017-10-31"
    with Extractor("thing", [config_file]) as extractor:
        extractor.filename_format = "[{date}] {title}"
        media_file = extractor.download_page(page, temp_dir, ["sub", "dirs"])
        assert basename(media_file) == "[2017-10-31] Title - Revelations.jpg"
        assert exists(media_file)
        assert extractor.archive_contains("blah")
    sub = abspath(join(temp_dir, "sub"))
    sub = abspath(join(sub, "dirs"))
    assert exists(sub)
    json_file = abspath(join(sub, "[2017-10-31] Title - Revelations.json"))
    assert exists(json_file)
    assert os.stat(media_file).st_size == 85007
    meta = mm_file_tools.read_json_file(json_file)
    assert meta["title"] == "Title: Revelations"
    assert meta["url"] == "blah"
    assert meta["image_url"] == "https://www.pythonscraping.com/img/gifts/img4.jpg"
    assert meta["date"] == "2017-10-31"
    # Test that ids were added to database
    with Extractor("thing", [config_file]) as extractor:
        extractor.initialize()
        assert extractor.archive_contains("blah")
        assert extractor.archive_contains("https://www.pythonscraping.com/img/gifts/img6.jpg")
        assert not extractor.archive_contains("Something Else")
    # Test if file is already downloaded
    with Extractor("thing", [config_file]) as extractor:
        media_file = extractor.download_page(page, temp_dir, ["new"])
        assert media_file is None
        assert not exists(abspath(join(temp_dir, "new")))
        extractor.add_to_archive("totally new")
        media_file = extractor.download_page({"url":"totally new"}, temp_dir, ["other"])
        assert media_file is None
        assert not exists(abspath(join(temp_dir, "other")))
    # Test if there is an existing media file with the same name
    duplicate_media = abspath(join(temp_dir, "duplicate.jpg"))
    mm_file_tools.write_text_file(duplicate_media, "Contents")
    page = {"title":"duplicate", "url": "https://www.pythonscraping.com/img/gifts/img3.jpg", "description":"other"}
    with Extractor("thing", [config_file]) as extractor:
        media_file = extractor.download_page(page, temp_dir)
        assert basename(media_file) == "duplicate-2.jpg"
        assert exists(media_file)
    json_file = abspath(join(temp_dir, "duplicate-2.json"))
    assert exists(duplicate_media)
    assert exists(json_file)
    meta = mm_file_tools.read_json_file(json_file)
    assert meta["title"] == "duplicate"
    assert meta["url"] == "https://www.pythonscraping.com/img/gifts/img3.jpg"
    assert meta["description"] == "other"
    assert os.stat(media_file).st_size == 71638
    assert mm_file_tools.read_text_file(duplicate_media) == "Contents"
    # Test if there is an existing JSON wile with the same name
    duplicate_json = abspath(join(temp_dir, "unique.json"))
    mm_file_tools.write_json_file(duplicate_json, {"some":"key"})
    page = {"title":"unique", "url": "https://www.pythonscraping.com/img/gifts/img1.jpg", "description":"New"}
    with Extractor("thing", [config_file]) as extractor:
        media_file = extractor.download_page(page, temp_dir)
        assert basename(media_file) == "unique-2.jpg"
        assert exists(media_file)
    json_file = abspath(join(temp_dir, "unique-2.json"))
    assert exists(duplicate_json)
    assert exists(json_file)
    meta = mm_file_tools.read_json_file(json_file)
    assert meta["title"] == "unique"
    assert meta["url"] == "https://www.pythonscraping.com/img/gifts/img1.jpg"
    assert meta["description"] == "New"
    assert os.stat(media_file).st_size == 84202
    assert mm_file_tools.read_json_file(duplicate_json) == {"some":"key"}
    # Test if the extractor is set to not use metadata
    config = {"thing":{"archive":archive_file, "metadata":False}}
    mm_file_tools.write_json_file(config_file, config)
    page = {"title":"No Meta", "url": "https://www.pythonscraping.com/img/gifts/img2.jpg"}
    with Extractor("thing", [config_file]) as extractor:
        media_file = extractor.download_page(page, temp_dir)
        assert basename(media_file) == "No Meta.jpg"
        assert exists(media_file)
    json_file = abspath(join(sub, "No Meta.json"))
    assert not exists(json_file)
    assert os.stat(media_file).st_size == 58424
