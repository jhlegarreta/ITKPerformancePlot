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

import sys

from data import data_loader
from visualization import performance_visualization


def main(argv):

    data_dir = argv[1]
    summary_filename = argv[2]
    modules_performance = data_loader.load_benchmarking_modules_performance_data(data_dir, summary_filename)

    performance_visualization.plot_version_module_performance_errorbar(modules_performance)
    performance_visualization.plot_module_performance_os_scatter(modules_performance)
    performance_visualization.plot_historical_performance_heatmap(modules_performance)


if __name__ == "__main__":
    main(sys.argv)
