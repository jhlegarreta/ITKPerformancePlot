# !/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

import matplotlib.pyplot as plt
import numpy as np

from visualization.heatmap_utils import heatmap, annotate_heatmap


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

    print('ToDo')


def plot_module_performance_errorbar(modules_performance):
    # ToDo
    # Plot the variation of the mean probes time of a given module for the
    # same ITK version but across different commits (i.e. the abscissa would
    # be the short commit hash along with the date).

    print('ToDo')


def plot_module_performance_errorbar(modules_performance):

    # ToDo
    # Deal with different OS versions

    for module_name, module_dict in modules_performance.items():
        module_errbar_data = []
        # Each probed version may have a different number of data points, so a
        # list of dictionaries needs to be kept
        for itk_version, probes in module_dict.items():
            # commit_hash, config_date, probes_mean_time = zip(*probes)
            commit_hash = []
            config_date = []
            probes_mean_time = []
            for point in probes:
                commit_hash.append(point[0])
                config_date.append(point[1])
                probes_mean_time.append(point[2])

            module_version_wise_data = dict(itk_version=itk_version, probes_mean_time=probes_mean_time)
            module_errbar_data.append(module_version_wise_data)

        # ToDo
        # Sort the values so that the itk versions and their corresponding
        # data points are always in ascending order. Regardless of the
        # order in which the files where processed. It may well happen
        # that the filename convention changes or old ITK versions are
        # re-tested.
        x = [elem['itk_version'] for elem in module_errbar_data]
        # ToDo
        # Compute the mean for every version and use that a y
        y = [elem['probes_mean_time'][0] for elem in module_errbar_data]
        # Todo
        # Once the mean computed, get all data points, and split them into
        # two groups, those above the mean and those below the mean to
        # properly build the yerr.
        # Each JSON file contains mean/min/max values for a number of
        # iterations performed on each module for a given commit. We are
        # interested in the mean/min/max values over the means across
        # different JSON files, though.
        # https://matplotlib.org/gallery/statistics/errorbar_features.html
        # yerr = [elem['probes_mean_time'] for elem in module_errbar_data]

        fig = plt.figure("Performance stats") # or benchmarking
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
    # another).


    # ToDo
    # Deal with renamed values (i.e. modules that have changed their name from one
    # version to another).

    # ToDo
    # Assume all modules were benchmarked on the same versions with no missing
    # values and that they contain only a data point per version.

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
            for point in probes:
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
