# -*- coding: utf-8 -*-
"""
This script modifies the input data and runs the EnergyScope model

@author: Paolo Thiran, Matija Pavičević, Xavier Rixhon, Gauthier Limpens
"""

import os
from pathlib import Path
import energyscope as es

if __name__ == '__main__':
    # define project path
    project_path = Path(__file__).parents[1]

    # loading the config file
    config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
    config['Working_directory'] = os.getcwd() # keeping curretn working directory into config


   # Reading the data
    es.import_data(config)

    ##TODO Student work: Write the updates in data HERE
    # Example to change data: update wood availability to 23 400 GWh (ref value here)
    config['all_data']['Resources'].loc['WOOD', 'avail'] = 23400
    # Example to change share of public mobility into passenger mobility into 0.5 (ref value here)
    config['all_data']['Misc']['share_mobility_public_max'] = 0.5

    # Printing the .dat files for the optimisation problem
    es.print_data(config)

    # Running EnergyScope
    es.run_ES(config)

    # Example to print the sankey from this script
    if config['print_sankey']:
        sankey_path = config['cs_path']/ config['case_study'] / 'output' / 'sankey'
        es.drawSankey(path=sankey_path)