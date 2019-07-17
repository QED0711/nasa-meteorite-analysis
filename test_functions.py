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