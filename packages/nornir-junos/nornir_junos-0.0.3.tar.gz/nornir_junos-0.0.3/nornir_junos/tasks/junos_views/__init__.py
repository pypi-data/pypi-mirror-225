# -*- coding: utf-8 -*-
"""
Load tables/views
"""
import yaml
import re
from jnpr.junos.factory import FactoryLoader
from os import listdir
import pathlib

def load_junos_view(view_path):
    try:
        with open(view_path) as f:
            tmp_yaml = f.read()
        yaml_str = re.sub(r"unicode", "str", tmp_yaml)
        globals().update(FactoryLoader().load(yaml.safe_load(yaml_str)))
    except:
        pass

current_path = str(pathlib.Path(__file__).parent.absolute())
for view in listdir(current_path):
    if view.endswith('.yml'):
        load_junos_view('{}/{}'.format(current_path,view))