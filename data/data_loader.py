# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Insight Software Consortium
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
from os.path import join as pjoin


def save_summary(summary_filename, number_of_benchmark_files, modules_performance):

    itk_modules = []
    itk_distinct_versions = []
    number_of_modules = 0
    for module_name, module_dict in modules_performance.items():
        number_of_modules += 1
        module_itk_versions = list(module_dict.keys())
        itk_modules.append({module_name: module_itk_versions})
        itk_distinct_versions.append([versions for versions in module_dict.keys()
                                      if versions not in itk_distinct_versions])

    itk_distinct_versions = list(version for versions in itk_distinct_versions for version in versions)
    itk_distinct_versions = sorted(set(itk_distinct_versions))
    itk_distinct_versions.sort(key=lambda s: [int(u) for u in s.split('.')])
    number_itk_distinct_versions = len(itk_distinct_versions)

    data = {'number_of_benchmark_files': number_of_benchmark_files,
            'number_of_modules': number_of_modules,
            'number_itk_distinct_versions': number_itk_distinct_versions,
            'modules_versions': itk_modules}

    with open(summary_filename, 'w') as outfile:
        json.dump(data, outfile)


def load_benchmarking_modules_performance_data(data_dir, summary_filename):

    modules_performance = {}

    number_of_benchmark_files = 0

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

        number_of_benchmark_files += 1

    save_summary(summary_filename, number_of_benchmark_files, modules_performance)

    return modules_performance
