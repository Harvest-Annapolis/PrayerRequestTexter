#!/usr/bin/env python3
import re
import feedparser

def get_message():
    data = feedparser.parse("https://www.harvestannapolis.org/daily-church-prayer?format=rss")
    message = re.sub("<[^>]+>", "\n", data.entries[0].content[0].value).strip().replace("\n\n", "\n")
    return message

