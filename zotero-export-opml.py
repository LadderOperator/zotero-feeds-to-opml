import os, sqlite3

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree

from xml.dom import minidom

ZotFilePath = input("Please enter your Zotero Database file path:")
if os.path.exists(ZotFilePath):
    try:
        #Read Zotero Database
        zotdb = sqlite3.connect(ZotFilePath, timeout=3)
        p = zotdb.cursor()
        p.execute("select * from feeds")
        feeds = p.fetchall()
        p.execute("select * from settings where key='username'")
        username = p.fetchone()[2]
        p.close()

        # Generate OPML
        root = Element('opml')
        head = SubElement(root, 'head')
        title = SubElement(head, 'title')
        title.text = "Export from Zotero"
        name = SubElement(head, 'ownerName')
        name.text = username
        body = SubElement(root, 'body')
        for feed in feeds:
            item = SubElement(body, 'outline')
            item.set("text", feed[1])
            item.set("title", feed[1])
            item.set("xmlUrl", feed[2])
            item.set("type", "rss")

        tree = ElementTree(root)
        tree.write('zotero_feeds.opml', encoding = 'utf-8')
        print("Export successfully!")



    except (sqlite3.OperationalError):
        print("Database is locked, make sure Zotero is closed.")
else:
    print("Cannot find zotero.sqlite!")