# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from data import data_loader
from visualization import performance_visualization


def main(argv):

    data_dir = argv[1]
    modules_performance = data_loader.load_benchmarking_modules_performance_data(data_dir)

    performance_visualization.plot_module_performance_errorbar(modules_performance)
    performance_visualization.plot_historical_performance_heatmap(modules_performance)


if __name__ == "__main__":
    main(sys.argv)
