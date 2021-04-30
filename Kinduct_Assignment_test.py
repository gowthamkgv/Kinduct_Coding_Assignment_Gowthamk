#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 17:00:19 2021

@author: gowthamvarmakanumuru
"""

import Kinduct_Assignment as A
import pytest 
import pandas as pd
import datatest as dt


@pytest.fixture(scope='module')
@dt.working_directory(__file__)
def df():
    return pd.read_csv('//Users/gowthamvarmakanumuru/Desktop/Goalies_new.csv',usecols=['playerID', 'year', 'tmID', 'GP', 'Min', 
                                                                                       'W', 'L','T/OL', 'ENG', 'SHO', 'GA', 'SA'])



def test_columns(df):
    dt.validate(
        df.columns,
        {'playerID', 'year', 'tmID', 'GP', 'Min', 'W', 'L',
       'T/OL', 'ENG', 'SHO', 'GA', 'SA'},
    )

@pytest.mark.mandatory
def test_year(df):
    dt.validate(df['tmID'], int)


@pytest.mark.mandatory
def test_runtime(df):
    dt.validate(df['year'], int)
    
    
    """
def test_for_missing_maxSales():
    assert maxSale.maxSale(data) != "Mazda"

def test_for_ok_mostSaleType():
    assert maxSale.mostSaleType(data) == "Passenger"

def test_for_missing_mostSaleType():
    assert maxSale.mostSaleType(data) == "Car"""

if __name__ == '__main__':
    import sys
    sys.exit(pytest.main(sys.argv))