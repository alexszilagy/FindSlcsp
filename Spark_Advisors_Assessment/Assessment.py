# Spark Advisors take home assessment
import pandas as pd

# file names
zip_csv = 'zips.csv'
plans_csv = 'plans.csv'
slcsp_csv = 'slcsp.csv'

# constants
ZIPCODE = 'zipcode'
RATE_AREA = 'rate_area'
STATE = 'state'
RATE = 'rate'
METAL_LEVEL = 'metal_level'
SILVER = 'Silver'

'''
Talking point:
    1. There are rare cases where one zipcode can be in multiple states. The instructions did not discuss this possibility. 
    If I needed to exclude cases where a zipcode has multiple states, I would add the following code to lines 45 and 47 respectively:
        unique_state = pd.unique(zip_info[STATE])
        if len(unique_area) == 1 and len(unique_state) == 1:
    When running the code with these lines, the result is the exact same, so the rare case of a zipcode with multiple states is either not in this data,
    or it occurs when a zipcode already has multiple rate areas.
'''
def main():
    # Read all of the csvs
    zips = pd.read_csv(zip_csv)
    plans = pd.read_csv(plans_csv)
    slcsp = pd.read_csv(slcsp_csv)

    # Only get the metal level of Silver from the plans.csv
    silver_plans = plans.loc[plans[METAL_LEVEL] == SILVER]

    # Loop through every zipcode in slcsp.csv
    for i in range(len(slcsp)):
        zip = slcsp.loc[i, ZIPCODE]

        # Get every row from zips.csv that match the current zip code
        zip_info = zips.loc[zips[ZIPCODE] == zip]

        # Get only unique rates from the dataframe zip_info
        unique_area = pd.unique(zip_info[RATE_AREA])

        # If there is only one unique area, the slcsp can be found, otherwise, leave the rate blank
        if len(unique_area) == 1:
            zip_state = zip_info[STATE].iloc[0] # The corresponding state for the zip
            zip_rate_area = zip_info[RATE_AREA].iloc[0] # The corresponding rate for the zip

            # Only get the rates from plans.csv that have a matching state and rate_area
            rates = silver_plans.loc[(silver_plans[STATE] == zip_state) & (silver_plans[RATE_AREA] == zip_rate_area)][RATE]
            sorted_rates = pd.DataFrame(rates.sort_values()) # Sort by rates
            unique_rates = pd.unique(sorted_rates[RATE]) # Remove duplicate rates

            # There is no slcsp if there are less than 2 rates. Leave blank if 1 or less rates
            if len(unique_rates) >= 2:
                slcsp.loc[i, RATE] = unique_rates[1] # Add second lowest Silver rate to slcsp data
    
    # Modify slcsp
    slcsp.to_csv(slcsp_csv, index=False) 
    print(slcsp.to_string()) # print result to console

main()