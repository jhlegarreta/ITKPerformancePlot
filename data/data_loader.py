# !/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from os.path import join as pjoin


def load_benchmarking_modules_performance_data(data_dir):

    modules_performance = {}

    # ToDo
    # Identify the modules affected by a commit so that the (slight?) variations
    # in performance detected against the previous commit in other modules can be
    # filtered when reporting performance diffs across commits.

    # ToDo
    # Deal with earlier day JSONs where keys may not be the same.

    # ToDo
    # Some features (e.g. the version) are present in two different dictionaries
    # (e.g. ['ITKBuildInformation']['VERSION'] vs.
    # ['SystemInformation']['ITKVersion']). Set the criterion to take one or the
    # other.

    for filename in os.listdir(data_dir):
        filename = pjoin(data_dir, filename)
        with open(filename) as data_file:
            data_string = data_file.read()
            try:
                df = json.loads(data_string)
                module_name = df['Probes'][0]['Name']

                if module_name not in modules_performance:
                    modules_performance[module_name] = {}

                probes_mean_time = df['Probes'][0]['Mean']
                config_date = df['ITK_MANUAL_BUILD_INFORMATION']['GIT_CONFIG_DATE']
                commit_hash = df['ITK_MANUAL_BUILD_INFORMATION']['GIT_CONFIG_SHA1']
                probes = commit_hash, config_date, probes_mean_time

                itk_version = df['SystemInformation']['ITKVersion']

                if itk_version in modules_performance[module_name]:
                    modules_performance[module_name][itk_version].append(probes)
                else:
                    modules_performance[module_name][itk_version] = []
                    modules_performance[module_name][itk_version].append(probes)

            except ValueError:
                print(repr(data_string))

    return modules_performance
