# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import pytest

def Load_csv_to_Dataframe(path,cols):
    """
    Load a csv and coverts into a dataframe wtth the required columns and skips if there any .

            Parameters:
                    path (string): File path
                    cols (list): list of column names

            Returns:
                    Goalies_df (dataframe)
    """
    assert len(path)>0, 'The path is invalid'
    assert type(cols)==list, 'The format of columns give in not in list format' 
    Goalies_df = pd.read_csv(path,error_bad_lines=False,usecols=cols)
    assert len(Goalies_df)>0, 'The Dataframe is empty' 
    assert ~Goalies_df.duplicated().any()
    return(Goalies_df)


def Change_column_to_StringDatattype():
    """
     Changes the column of Goalies_df dataframe into datatype String 
           
            Returns:
                    The datatype of the column changed
    """
    Goalies_df['tmID'] = Goalies_df['tmID'].astype(pd.StringDtype())
    assert (Goalies_df['tmID'].dtype)=='string','the datatype has not changed datatype error' 
    return(Goalies_df['tmID'].dtype)


def Change_Column_to_yearDatatype():
   """
     Changes the column of Goalies_df dataframe into datatype datetime format 
           
            Returns:
                    The datatype of the column changed
   """
   Goalies_df['year'] = pd.to_datetime(Goalies_df['year'])
   Goalies_df['year']=pd.DatetimeIndex(Goalies_df['year']).year
   assert Goalies_df['year'].dtype== 'int64', 'Conversion of datatype error'
   return(Goalies_df['year'].dtype)
        

def Caluclate_Wins_Loses_GP_Agg():
    """
     Function to caluclate the wins , losses & Games Played Aggregare
           
            Returns:
                wins_agg: Pandas Series object of Wins_agg per each of the team
                losses_agg: Pandas Series object of Losses_agg per each of the team
                GP_agg: Pandas Series object of GP_agg per each of the team    
   """
    Groupby_stg = Goalies_df.groupby(['tmID']).agg({'playerID':'count','W':'sum','L':'sum','GP':'sum'})
    wins_agg = Groupby_stg['W']/Groupby_stg['playerID']
    losses_agg = Groupby_stg['L']/Groupby_stg['playerID']
    GP_agg = Groupby_stg['GP']/Groupby_stg['playerID']
    
    assert len(wins_agg)==len(losses_agg)==len(GP_agg),'All are grouped by teamid' 
    return(wins_agg,losses_agg,GP_agg)


def Caluclate_agg_Stg():
    """
     Function to caluclate the Mins_over_GA_agg,GA_over_SA_agg
           
            Returns:
            Mins_over_GA_agg, GA_over_SA_agg
    """
    
    Mins_over_GA_agg = Goalies_df.groupby(['tmID','year']).Min.agg(['sum'])/Goalies_df.groupby(['tmID','year']).GA.agg(['sum'])
    GA_over_SA_agg = Goalies_df.groupby(['tmID','year']).GA.agg(['sum'])/Goalies_df.groupby(['tmID','year']).SA.agg(['sum'])
    
    assert len(Mins_over_GA_agg)==len(GA_over_SA_agg), 'Len of both of them as they are grouped by Teamid,year'
    return(Mins_over_GA_agg,GA_over_SA_agg)


def avg_percentage_wins():
    """
    Function to caluclate avg_perecentage_wins
           
            Returns:
                avg_perecentage_wins
    """
    avg_perecentage_wins_stg_1 = Goalies_df.groupby(['tmID','playerID']).agg({'W': 'sum', 'GP': 'sum'})
    avg_perecentage_wins_stg_2 =avg_perecentage_wins_stg_1['W'] /( avg_perecentage_wins_stg_1['GP'])*100
    avg_perecentage_wins = avg_perecentage_wins_stg_2.groupby('tmID').mean()
    
    return(avg_perecentage_wins)

def most_goals_stopped_efficency():
    """
     Function to caluclate miost goals played player, most effiecient player 
           
            Returns:
                most_goals_stopped_dict: returns a dict with 1 value of the most goals scored player 
                most_efficient_player_dict:returns a dict with 1 value of the most efficeint player 
                   
    """
    #caluclate the most goals scored player
    most_goals_stopped_stg = Goalies_df.groupby(['playerID'], sort='Desc').agg({'SA':'sum','GA':'sum' ,'Min':'sum'})
    most_goals_stopped_stg_1 = (most_goals_stopped_stg['SA']-most_goals_stopped_stg['GA'])
    most_goals_stopped_stg_index_reset = most_goals_stopped_stg_1.reset_index()
    most_goals_stopped_final = most_goals_stopped_stg_index_reset[most_goals_stopped_stg_index_reset[0] == float(most_goals_stopped_stg_index_reset[0].max())]
        
    most_goals_stopped_dict ={}
    most_goals_stopped_dict['playerID']= list(most_goals_stopped_final['playerID'])
    most_goals_stopped_dict['goals_stopped']= list(most_goals_stopped_final[0])
    
    # Caluclate the most efficient player
    most_goals_stopped_eff = (most_goals_stopped_stg['SA']-most_goals_stopped_stg['GA'])/most_goals_stopped_stg['Min']
    most_goals_stopped_eff = most_goals_stopped_eff.reset_index()
    most_goals_stopped_eff = most_goals_stopped_eff[most_goals_stopped_eff[0] == float(most_goals_stopped_eff[0].max())]
    most_efficient_player_dict ={}
    most_efficient_player_dict['playerID']= list(most_goals_stopped_eff['playerID'])
    most_efficient_player_dict['efficiency']= list(most_goals_stopped_eff[0])
    
    assert len(most_goals_stopped_dict)==len(most_goals_stopped_dict), 'The length of both of them should be same as the return a dictionay with 1 player'
    return(most_goals_stopped_dict,most_efficient_player_dict)
        


if __name__ == "__main__":
    
    Goalies_df = Load_csv_to_Dataframe('//Users/gowthamvarmakanumuru/Desktop/Goalies_new.csv',['playerID', 'year', 'tmID', 'GP', 'Min', 'W', 'L',
       'T/OL', 'ENG', 'SHO', 'GA', 'SA'])   
    
 #1)tmID: stringConverting Data type as string    
    print(Change_column_to_StringDatattype())
    
 #2)year: Year covering the datatype of year 
    print(Change_Column_to_yearDatatype())
    
    wins_agg,losses_agg,GP_agg=Caluclate_Wins_Loses_GP_Agg()
    
  #3)Wins_agg: total wins / total players 
    print(wins_agg)
    
  #4)Losses_agg: total losses / total players
    print(losses_agg)
    
  #5)GP_agg: total games played / total players
    print(GP_agg)
    
    Mins_over_GA_agg,GA_over_SA_agg=Caluclate_agg_Stg()
    
   #6)Mins_over_GA_agg: total minutes played / total goals against
    print(Mins_over_GA_agg)
    
   #7)GA_over_SA_agg: total goals against / total shots against
    print(GA_over_SA_agg)
    
    """8)avg_percentage_wins: calculate the percentage of games won for each player, then take the
       mean at team level"""
       
    print(avg_percentage_wins())
    
    most_goals_stopped_dict,most_efficient_player_dict=most_goals_stopped_efficency()
    
    """9)most_goals_stopped: {‘playerID’: playerID, ‘goals_stopped’: goals_stopped}
    #escription: calculate goals stopped per player, then take the player with the max goals
    stopped and put the details in the dictionary"""

    print(most_goals_stopped_dict)
    
    """10)most_efficient_player: {‘playerID’: playerID, ‘efficiency’: goals_stopped / minutes played}
     Description: calculate the goals stopped per minutes of play for each player, then take the
    player with the max efficiency just calculated and put the details in the dictionary"""
    
    print(most_efficient_player_dict)
    



