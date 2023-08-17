#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2023 The OpenRL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""""""

from pathlib import Path

from openplugin.plugin.webapp_plugin import WebAppPlugin
from openplugin.run.local_run import run_local_plugin
from openplugin.utils.util import get_plugin_list


def run_plugin(plugin_name, host: str, port: int):
    if plugin_name == "./":
        run_local_plugin(host, port)
        return

    plugin_list = get_plugin_list()
    if plugin_name not in plugin_list:
        print(f"Plugin {plugin_name} not installed!")
        return

    plugin_path = f"{str(Path.home())}/.openplugin/plugins/{plugin_name}"

    plugin = WebAppPlugin(plugin_name, plugin_path)
    plugin.run(host, port)
