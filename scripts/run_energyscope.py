# -*- coding: utf-8 -*-
"""
This script modifies the input data and runs the EnergyScope model

@author: Paolo Thiran, Matija Pavičević, Xavier Rixhon, Gauthier Limpens
"""

import os
from pathlib import Path
import energyscope as es

if __name__ == '__main__':
    analysis_only = False
    compute_TDs = True

    # define project path
    project_path = Path(__file__).parents[1]

    # To change the whole Demand matrix of 2050, set changecsv to True and write the name of the new csv (located in
    # Personal/Demand) as filename
    es.choose_demand_csv(changecsv=True, filename='Demand_Baudson.csv', project_path=project_path)

    # loading the config file into a python dictionnary
    config = es.load_config(config_fn='config_ref.yaml', project_path=project_path)
    config['Working_directory'] = os.getcwd() # keeping current working directory into config
    
   # Reading the data of the csv
    es.import_data(config)

    if compute_TDs:
        es.build_td_of_days(config)

    # Adjust biomass data (from Hugo Baudson) + set emissions to 0
    config['all_data']['Resources'].loc['WOOD', 'gwp_op'] = 0.0
    config['all_data']['Resources'].loc['WOOD', 'avail'] = 9450
    config['all_data']['Resources'].loc['WOOD', 'c_op'] = 0.0213
    config['all_data']['Resources'].loc['WET_BIOMASS', 'gwp_op'] = 0.0
    config['all_data']['Resources'].loc['WET_BIOMASS', 'avail'] = 14100
    config['all_data']['Resources'].loc['WET_BIOMASS', 'c_op'] = 0.0096

    # Adjust public mobility max share
    # config['all_data']['Misc']['share_mobility_public_max'] = 0.8   # LD: 0.8, Climact-BEH: 0.6, CLEVER: 0.5
                                                                    # EnergyVille: 0.21, EU-ref: 0.205


    # Adjust industry demand
    # ind_dem = 44517  # Total industry EUD excluding NED (New LD: 44517, BEH: 57899, CLEVER: 70482, EnergyVille: 101643)
    #
    # config['all_data']['Demand'].loc['ELECTRICITY', 'INDUSTRY'] = ind_dem * 0.357
    # config['all_data']['Demand'].loc['LIGHTING', 'INDUSTRY'] = ind_dem * 0.118
    # config['all_data']['Demand'].loc['HEAT_HIGH_T', 'INDUSTRY'] = ind_dem * 0.395
    # config['all_data']['Demand'].loc['HEAT_LOW_T_SH', 'INDUSTRY'] = ind_dem * 0.103
    # config['all_data']['Demand'].loc['HEAT_LOW_T_HW', 'INDUSTRY'] = ind_dem * 0.027
    # config['all_data']['Demand'].loc['NON_ENERGY', 'INDUSTRY'] = ind_dem * 0.383
    # config['all_data']['Demand'].loc['NON_ENERGY', 'INDUSTRY'] = 11927  # Don't forget to adjust the shares in
                # misc.json : 11927 for New LD (.688, .124, .188) - 19313 for SPF-BEH (.923, .077, 0)
                # 31633 for CLEVER (.736, .047, .217)) - 51094 for Energyville (.779, .029, .192)

    if not analysis_only:
        # Printing the .dat files for the optimisation problem       
        es.print_data(config)

        # Running EnergyScope
        es.run_es(config)

    # Example to print the sankey from this script
    if config['print_sankey']:
        sankey_path = config['cs_path']/ config['case_study'] / 'output' / 'sankey'
        es.drawSankey(path=sankey_path)

    # Reading outputs
    outputs = es.read_outputs(config['case_study'], hourly_data=True, layers=['layer_ELECTRICITY','layer_HEAT_LOW_T_DECEN'])

    # Plots (examples)
    # primary resources used
    fig2, ax2 = es.plot_barh(outputs['resources_breakdown'][['Used']], title='Primary energy [GWh/y]')
    # elec assets
    elec_assets = es.get_assets_l(layer='ELECTRICITY', eff_tech=config['all_data']['Layers_in_out'],
                                  assets=outputs['assets'])
    fig3, ax3 = es.plot_barh(elec_assets[['f']], title='Electricity assets [GW_e]',
                             x_label='Installed capacity [GW_e]')
    # layer_ELECTRICITY for the 12 tds
    elec_layer_plot = es.plot_layer_elec_td(outputs['layer_ELECTRICITY'])
    # layer_HEAT_LOW_T_DECEN for the 12 tds
    fig,ax = es.hourly_plot(plotdata=outputs['layer_HEAT_LOW_T_DECEN'], nbr_tds=12)
    
    
    