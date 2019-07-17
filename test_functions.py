import pandas as pd
import statsmodels.api as sm

from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind

import warnings
warnings.filterwarnings('ignore')



def test_classification_masses(df, classification_names=("Chondrite", "Achondrite", "Iron", "Stony-Iron")):
    """
    Accepts the names of the classifications (or a subset of classifications)
    
    For each classification, runs a t test against all others to determine if their masses are from the same population
    
    Returns a dataframe with the results. 
    (For the aplha columns, True and False refers to the rejection of the null hypothesis) 
    """
    
    
    classification_mass = []
    # append a list of masses to the classification_mass list for each name
    for name in classification_names:
        classification_mass.append(df[df.major_classification == name].mass)
    
    test_results = [] # where we will be appending all our results
    alpha_list = (0.1, 0.05, 0.01) # the different alpha levels to test
    for i in range(len(classification_mass)):
        for j in range(i + 1, len(classification_mass)):
            samp1, samp2 = (classification_names[i],classification_names[j]) 
            # test each classification against the others. 
            t_stat, p_value = ttest_ind(classification_mass[i], classification_mass[j], equal_var=False)
            # given the p values, check against list of alphas
            alpha_1, alpha_05, alpha_01 = (p_value < alpha_list[0],p_value < alpha_list[1], p_value < alpha_list[2])
            #  append everything to the rest results as a tuple
            test_results.append((samp1, samp2, t_stat, p_value, alpha_1, alpha_05, alpha_01))
    # create and return a dataframe of the results        
    return pd.DataFrame(test_results, columns=("sample_1", "sample_2", "t_stat", "p_value", "alpha 10%", "alpha 5%", "alpha 1%"))



# FOUND VS FALL MASSES

def test_found_vs_fall_masses(df):
    test_results = [] # where we will be appending all our results
    alpha_list = (0.1, 0.05, 0.01) # the different alpha levels to test
    samp1, samp2 = ("Found", "Fell" )

    # test each classification against the others. 
    t_stat, p_value = ttest_ind(df[df.fall == 'Found'].mass, df[df.fall == 'Fell'].mass, equal_var=False)
    # given the p values, check against list of alphas
    alpha_1, alpha_05, alpha_01 = (p_value < alpha_list[0],p_value < alpha_list[1], p_value < alpha_list[2])
    #  append everything to the rest results as a tuple
    test_results.append((samp1, samp2, t_stat, p_value, alpha_1, alpha_05, alpha_01))

    # create and return a dataframe of the results 
    t_result = pd.DataFrame(test_results, columns=("Sample 1", "Sample 2", "t-stat", "p-value", "alpha 10 %", "aplha 5 %", "alpha 1 %"))
    return t_result



# PROPORTION TEST SIGHTINGS OVER YEARS


def test_fall_sightings_dates(df, start_date, split_date, end_date):
    
    range_1 = df[(df.year >= start_date) & (df.year < split_date)]
    range_2 = df[(df.year >= split_date) & (df.year <= end_date )]
    
    range_1_name = f"{start_date} - {split_date - 1}"
    range_2_name = f"{split_date} - {end_date}"
    
    range_1_total = len(range_1.fall)
    range_2_total = len(range_2.fall)
    
    range_1_sightings = len(range_1[range_1.fall == "Fell"])
    range_2_sightings = len(range_2[range_2.fall == "Fell"])
    
    z_stat, p_value = proportions_ztest((range_1_sightings, range_2_sightings), (range_1_total, range_2_total))
                                        
    return pd.DataFrame(
        [(range_1_name, range_2_name, z_stat, p_value)],
        columns=("Date Range 1", "Date Range 2", "z-stat", "p-value")
    )



# TEST QUADRANTS

def test_quadrants(df):
    # Subset the various quadrants
    ne = df[(df.reclat >= 0) & (df.reclong >= 0)].mass
    nw = df[(df.reclat >= 0) & (df.reclong <= 0)].mass
    sw = df[(df.reclat <= 0) & (df.reclong <= 0)].mass
    se = df[(df.reclat <= 0) & (df.reclong >= 0)].mass 
    
    quadrant_data = (ne, nw, sw, se)
    quadrant_names = ("NE", "NW", "SW", "SE")
    
    test_results = [] # where we will be appending all our results
    alpha_list = (0.1, 0.05, 0.01) # the different alpha levels to test
    
    for i in range(4):
        for j in range(i + 1, 4):
            # Run the test for each quadrant comparing it to each other quadrant. 
            samp1, samp2 = quadrant_names[i], quadrant_names[j]
            t_stat, p_value = ttest_ind(quadrant_data[i], quadrant_data[j], equal_var=False)
            alpha_1, alpha_05, alpha_01 = (p_value < alpha_list[0],p_value < alpha_list[1], p_value < alpha_list[2])
            
            test_results.append((samp1, samp2, t_stat, p_value, alpha_1, alpha_05, alpha_01))
    
    return pd.DataFrame(test_results, columns=["quadrant_1", "quadrant_2", "t_stat", "p_value", "alpha 10%", "alpha 5%", "alpha 1%"])







# TEST REGIONS


def test_regions(df):
    
    region = list(df.region_wb.unique())

    samples = []

    for r in region:
        samples.append(df[df.region_wb == r].num_strikes)

    test_results = []
    alpha_list = (0.1, 0.05, 0.01) # the different alpha levels to test
    for i in range(len(samples)):
        for j in range(i + 1, len(samples)):
            samp1, samp2 = samples[i], samples[j]
            t_stat, p_value = ttest_ind(samp1, samp2, equal_var=False)
            alpha_1, alpha_05, alpha_01 = (p_value < alpha_list[0],p_value < alpha_list[1], p_value < alpha_list[2])

            test_results.append((region[i], region[j], t_stat, p_value, alpha_1, alpha_05, alpha_01))

    results = pd.DataFrame(test_results, columns=["Region 1", "Region 2", "t-stat", "p-value", "alpha 10%", "alpha 5%", "alpha 1%"])
    
    results.dropna(inplace=True)
    return results



# TEST POPULATION IMPACT ON REPORTING

def test_population_impact(df, pop_split):
    # Dataframe subsetting
    df = df[(df.year >= 1990) & (df.year <= 2010)]
    
    columns = [    
        "country",
        "2000_pop_thousands", 
    ]

    strikes_per_country = pd.DataFrame(df.country.value_counts()).reset_index()
    strikes_per_country.columns = ["country", "strikes"]
    country_populations = df[columns].drop_duplicates(subset="country")

    strikes_around_2000 = country_populations.merge(strikes_per_country, on="country").copy()[["country", "2000_pop_thousands", "strikes"]]
    
    
    # get number of sightings for "small" and "large" countries 
    sm_countries_strikes = list(strikes_around_2000[strikes_around_2000["2000_pop_thousands"] >= pop_split].strikes)
    large_countries_strikes = list(strikes_around_2000[strikes_around_2000["2000_pop_thousands"] < pop_split].strikes)
    
    t_stat, p_value = ttest_ind(sm_countries_strikes, large_countries_strikes, equal_var=False)
    
    return pd.DataFrame([(f"< {pop_split * 1000}", f"> {pop_split * 1000}",t_stat, p_value)], columns=("Population 1", "Population 2", "t-stat", "p-value"))
    
    

    
    
            