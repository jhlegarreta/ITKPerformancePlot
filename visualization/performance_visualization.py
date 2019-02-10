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

import functools
import itertools
import operator

import matplotlib.pyplot as plt
import numpy as np

from collections import OrderedDict
from visualization.heatmap_utils import heatmap, annotate_heatmap


# ToDo
# Refactor the existing methods to be able to easily switch across
# visualization types (the data preparation part could be shared for some
# visualization types if done properly).


def plot_module_performance_version_scatter(modules_performance):
    # ToDo
    # Plot the mean probes time of a given module for all ITK versions
    # across different commits as a scatter plot. All data points
    # ('Probes':'values') in each JSON file would be considered as a separate
    # data point. The abscissa would be the dates along with the short commit
    # hash, and points would be colored according to the ITK version (shown as
    # a legend).

    print('ToDo')


def plot_module_performance_os_scatter(modules_performance):
    # ToDo
    # Plot the mean probes time of a given module for all ITK versions
    # across different commits as a scatter plot. All data points
    # ('Probes':'values') in each JSON file would be considered as a separate
    # data point. The abscissa would be the ITK version, and points would be
    # colored according to the OS (shown as a legend).

    colormap = {'Linux': 'red', 'macOS': 'green', 'Windows': 'blue'}

    module_scatter_data = {}

    # Prepare data

    for module_name, module_dict in modules_performance.items():
        if module_name not in module_scatter_data:
            module_scatter_data[module_name] = []

        # Each probed version may have a different number of data points, so a
        # list of dictionaries needs to be kept
        for itk_version, os_probes in module_dict.items():
            for os, probes in os_probes.items():
                # os, commit_hash, config_date, probes_mean_time = zip(*probes)
                commit_hash = []
                config_date = []
                probes_mean_time = []
                probes_time_values = []
                for point in probes:
                    commit_hash.append(point[0])
                    config_date.append(point[1])
                    probes_mean_time.append(point[2])
                    probes_time_values.append(point[3])

                probes_time_values = functools.reduce(operator.concat, probes_time_values)

                module_version_os_data = {itk_version: {os: probes_time_values}}
                module_scatter_data[module_name].append(module_version_os_data)

    # Visualize

    # ToDo
    # Sort the values so that the ITK versions and their corresponding
    # data points are always in ascending order. Regardless of the
    # order in which the files where processed. It may well happen
    # that the filename convention changes or old ITK versions are
    # re-tested.
    # Also, for ordering purposes, '4.13.0' is considered to come
    # before '4.9.0', so more processing than simple sorting will be
    # required. See the data_loader.save_summary() method.
    # May be the sorting will need to be done in a utils.version_sort
    # method to avoid duplicating code.

    for module_name, module_dict in module_scatter_data.items():

        fig, ax = plt.subplots()
        fig.canvas.set_window_title("Performance stats")  # or benchmarking
        for elem in module_scatter_data[module_name]:
            # item = list(elem.items())[0]
            itk_vers = list(elem.keys())[0]  # or item[0]
            os_and_vals = list(elem.values())[0]  # or item[1]
            os = list(os_and_vals.keys())[0]
            probes = list(os_and_vals.values())[0]
            itk_version = [itk_vers for _ in range(len(probes))]
            # ToDo
            # Slightly perturb the version list using a delta and a sign
            # depending on the OS, so that the data points are displayed as
            # three different clusters OS-wise around the ITK version. If the
            # delta is fixed, each cluster will be a column; if it is a random
            # number within some limits, they could be scattered around the
            # ITK version. Adding a random perturbation may be nice
            # visualization/distribution-wise, but does not really add any
            # real/useful information.
            # In order to do that, the ITK version should be cast into a
            # a real number, and taking care of the MAJOR, MINOR and PATCH
            # VERSION splitting periods.
            # delta = 0.01
            # sign = {'Linux': -1, 'macOS': 0, 'Win': 1}
            # itk_versions = [version_to_num(itk_v) * delta * sign[os] for itk_v in itk_version]

            ax.scatter(itk_version, probes, c=colormap[os], label=os)

        plt.title('ITK Module: {}'.format(module_name))
        plt.xlabel('ITK version')
        plt.ylabel('Mean Probes Time (s)')
        # Filter duplicate labels
        # ToDo
        # Filtering duplicate labels would not be necessary if the
        # visualization was done in a OS-wise (i.e. looping over the colormap
        # dictionary keys) instead of in module-wise fashion. If the former
        # turns out to be more straightforward or efficient, it would be
        # worthwhile implementing it.
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())

        plt.show()


def plot_commit_module_performance_errorbar(modules_performance):
    # ToDo
    # Plot the variation of the mean probes time of a given module for the
    # same ITK version but across different commits (i.e. the abscissa would
    # be the short commit hash along with the date).

    print('ToDo')


def plot_version_module_performance_errorbar(modules_performance):

    # ToDo
    # May be a boxplot instead of/in addition to an errobar could be more meaningful:
    # https://discourse.itk.org/t/itk-5-0-alpha-2-performance/959
    # See for example:
    # https://github.com/rasbt/matplotlib-gallery/blob/master/ipynb/boxplots.ipynb

    for module_name, module_dict in modules_performance.items():
        module_errbar_data = []

        # Each probed version may have a different number of data points, so a
        # list of dictionaries needs to be kept

        # ToDo
        # Deal with different OS platforms and versions (?)
        # ToDo
        # For the moment, pick just the Linux probes.
        for itk_version, probes in module_dict.items():
            # commit_hash, config_date, probes_mean_time = zip(*probes)
            commit_hash = []
            config_date = []
            probes_mean_time = []
            if 'Linux' in probes:
                for point in probes['Linux']:
                    commit_hash.append(point[0])
                    config_date.append(point[1])
                    probes_mean_time.append(point[2])

            module_version_wise_data = dict(itk_version=itk_version, probes_mean_time=probes_mean_time)
            module_errbar_data.append(module_version_wise_data)

        # ToDo
        # Sort the values so that the ITK versions and their corresponding
        # data points are always in ascending order. Regardless of the
        # order in which the files where processed. It may well happen
        # that the filename convention changes or old ITK versions are
        # re-tested.
        # Also, for ordering purposes, '4.13.0' is considered to come
        # before '4.9.0', so more processing than simple sorting will be
        # required. See the data_loader.save_summary() method.
        # May be the sorting will need to be done in a utils.version_sort
        # method to avoid duplicating code.
        x = [elem['itk_version'] for elem in module_errbar_data]
        # ToDo
        # Compute the mean for every version and use that as y
        y = [elem['probes_mean_time'][0] for elem in module_errbar_data]
        # ToDo
        # Once the mean computed, get all data points, and split them into
        # two groups, those above the mean and those below the mean to
        # properly build the yerr.
        # Each JSON file contains mean/min/max values for a number of
        # iterations performed on each module for a given commit. We are
        # interested in the mean/min/max values over the means across
        # different JSON files, though.
        # Another option is to compose the error bar using the fastest and
        # slowest times across the three platforms (macOS, Linux, Windows).
        #
        # https://matplotlib.org/gallery/statistics/errorbar_features.html
        # yerr = [elem['probes_mean_time'] for elem in module_errbar_data]

        fig = plt.figure("Performance stats")  # or benchmarking
        # plt.scatter(x=x, y=y)
        plt.errorbar(x=x, y=y)
        plt.title('ITK Module: {}'.format(module_name))
        plt.xlabel('ITK version')
        plt.ylabel('Mean Probes Time (s)')
        plt.show()

    # ToDo
    # Investigate whether the plot.scatter or plt.errorbar can return
    # objects that we can save in a list to later plot all the modules' plots
    # at the same time with different colors and a legend.
    # In that case, care may need to be taken if modules have missing values
    # (i.e. version in which they were not present/tested).
    #
    # Additionally, plot them separately as subplots.


def plot_historical_performance_heatmap(modules_performance):

    # ToDo
    # Deal with missing values (i.e. modules present in one version but not in
    # another) (check if it is necessary?)

    # ToDo
    # Deal with renamed values (i.e. modules that have changed their name from one
    # version to another).

    # ToDo
    # Assume all modules were benchmarked on the same versions with no missing
    # values and that they contain only a data point per version.

    # ToDo
    # Sort the values so that the ITK versions and their corresponding data
    # points are always in ascending order. Regardless of the order in which
    # the files where processed. It may well happen that are the filename
    # convention changes or old ITK versions are re-tested.
    # Also, for ordering purposes, '4.13.0' is considered to come
    # before '4.9.0', so more processing than simple sorting will be required.
    # See the data_loader.save_summary() method.
    # May be the sorting will need to be done in a utils.version_sort
    # method to avoid duplicating code.

    number_modules = len(modules_performance)
    number_versions_per_module = {key: len(value) for key, value in modules_performance.items()}
    number_versions = list(number_versions_per_module.values())
    # Alternatively
    # number_versions = [len(v) for v in modules_performance.values()]
    # ToDo
    # Taking the first element, if the list's elements are not all equal, it
    # means that modules were benchmarked on a varying number of versions.
    # If that happens, missing values for the affected modules will need to be
    # assigned with some default value (either zero or the mean of the rest, but
    # be marked with some different color in the heatmap).
    number_versions = number_versions[0]
    # ToDo
    # Check number of probes per module and version: if there are multiple probes,
    # compute the average

    itk_historical_benchmarks = np.zeros((number_versions, number_modules))

    modules_versions = [list(value.keys()) for key, value in modules_performance.items()]
    itk_versions = list(set(list(itertools.chain.from_iterable(modules_versions))))

    itk_modules = [key for key, value in modules_performance.items()]

    for module_name, module_dict in modules_performance.items():
        for itk_version, probes in module_dict.items():
            # commit_hash, config_date, probes_mean_time = zip(*probes)
            commit_hash = []
            config_date = []
            probes_mean_time = []

            # ToDo
            # Deal with different OS platforms and versions (?)
            # ToDo
            # For the moment, pick just the Linux probes.
            if 'Linux' in probes:
                for point in probes['Linux']:
                    commit_hash.append(point[0])
                    config_date.append(point[1])
                    probes_mean_time.append(point[2])

            itk_historical_benchmarks[itk_versions.index(itk_version),
                                      itk_modules.index(module_name)] = probes_mean_time[0]

    fig, ax = plt.subplots()

    im, cbar = heatmap(itk_historical_benchmarks, itk_versions, itk_modules, ax=ax,
                       cmap="YlGn", cbarlabel="Mean probes time (s)")
    _ = annotate_heatmap(im, valfmt="{x:.4f}")

    fig.tight_layout()
    plt.show()

    # ToDo
    # Print a report with the number and names of modules, the number and
    # names of versions, and the number of probes or data points in each
    # module/version pair.
    # This will help in conveying an idea of the variance of a module's
    # benchmarking (e.g. a single data point may not be representative of the
    # modules performance).
