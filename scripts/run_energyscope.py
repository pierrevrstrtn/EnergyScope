# -*- coding: utf-8 -*-
"""
This script modifies the input data and runs the EnergyScope model

@author: Paolo Thiran, Matija Pavičević, Xavier Rixhon, Gauthier Limpens
"""

import os
from pathlib import Path
import energyscope as es
import energyscope.postprocessing.plots

if __name__ == '__main__':
    # define project path
    project_path = Path(__file__).parents[1]

    # loading the config file into a python dictionnary
    config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
    config['Working_directory'] = os.getcwd() # keeping current working directory into config

   # Reading the data of the csv
    es.import_data(config)

    ##TODO Student work: Write the updates in data HERE
    # Example to change data: update wood availability to 23 400 GWh (ref value here)
    config['all_data']['Resources'].loc['WOOD', 'avail'] = 23400
    # Example to change share of public mobility into passenger mobility into 0.5 (ref value here)
    config['all_data']['Misc']['share_mobility_public_max'] = 0.5

    # Printing the .dat files for the optimisation problem
    es.print_data(config)

    # Running EnergyScope
    # es.run_ES(config)

    # Example to print the sankey from this script
    if config['print_sankey']:
        sankey_path = config['cs_path']/ config['case_study'] / 'output' / 'sankey'
        es.drawSankey(path=sankey_path)

    # Reading outputs
    outputs = es.read_outputs(config['case_study'], hourly_data=True, layers=['layer_ELECTRICITY'])

    elec_year_ts = es.from_td_to_year(outputs['layer_ELECTRICITY'], config['td_data']['t_h_td'])
    elec_assets = es.get_assets_l(layer='ELECTRICITY', eff_tech=config['all_data']['Layers_in_out'], assets=outputs['assets'])

    # plots
    elec_plot = energyscope.postprocessing.plots.plot_layer_elec_td(outputs['layer_ELECTRICITY'])
    fig, ax = es.plot_barh(outputs['resources_breakdown'][['Used']])
    fig2, ax2 = es.plot_barh(elec_assets[['f']])

    # TODO test plots, etc into postprocessing