# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from future import standard_library

import re

from . import Crypter, Package

standard_library.install_aliases()


class XfilesharingProFolder(Crypter):
    __name__ = "XfilesharingProFolder"
    __type__ = "crypter"
    __pattern__ = r'http://(?:www\.)?((easybytez|turboupload|uploadville|file4safe|fileband|filebeep|grupload|247upload)\.com|(muchshare|annonhost).net|bzlink.us)/users/.*'
    __version__ = "0.01"
    __description__ = """Generic XfilesharingPro Folder Plugin"""
    __author_name__ = ("zoidberg")
    __author_mail__ = ("zoidberg@mujmail.cz")

    LINK_PATTERN = r'<div class="link"><a href="([^"]+)" target="_blank">[^<]*</a></div>'
    SUBFOLDER_PATTERN = r'<TD width="1%"><img src="[^"]*/images/folder2.gif"></TD><TD><a href="([^"]+)"><b>(?!\. \.<)([^<]+)</b></a></TD>'

    def decrypt_url(self, url):
        return self.decrypt_file(self.load(url, decode=True))

    def decrypt_file(self, html):
        new_links = []

        new_links.extend(re.findall(self.LINK_PATTERN, html))

        subfolders = re.findall(self.SUBFOLDER_PATTERN, html)
        # self.log_debug(subfolders)
        for (url, name) in subfolders:
            if self.package:
                name = "{0}/{1}".format(self.package.name, name)
            new_links.append(Package(name, [url]))

        if not new_links:
            self.fail(_('Could not extract any links'))

        return new_links
