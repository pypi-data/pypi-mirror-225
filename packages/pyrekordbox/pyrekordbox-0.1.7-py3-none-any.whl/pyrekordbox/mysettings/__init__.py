# -*- coding: utf-8 -*-
# Author: Dylan Jones
# Date:   2023-02-01

import os
import re
from . import structs
from .file import (
    FILES,
    SettingsFile,
    MySettingFile,
    MySetting2File,
    DjmMySettingFile,
    DevSettingFile,
)

RE_MYSETTING = re.compile(".*SETTING[0-9]?.DAT$")


def get_mysetting_paths(root, deep=False):
    files = list()
    for root, _, names in os.walk(root):
        for fname in names:
            if RE_MYSETTING.match(fname):
                files.append(os.path.join(root, fname))
        if not deep:
            break
    return files


def read_mysetting_file(path) -> SettingsFile:
    obj = FILES[os.path.split(path)[1]]
    return obj.parse_file(path)
