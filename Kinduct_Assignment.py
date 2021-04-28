# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd

Goalies_df = pd.read_csv('//Users/gowthamvarmakanumuru/Desktop/Goalies_new.csv',error_bad_lines=False,
                usecols=['playerID', 'year', 'tmID', 'GP', 'Min', 'W', 'L',
       'T/OL', 'ENG', 'SHO', 'GA', 'SA'])

#1)tmID: stringConverting Data type as string 
Goalies_df['tmID'] = Goalies_df['tmID'].astype(pd.StringDtype())
print(Goalies_df['tmID'].dtype)

#2)year: Year covering the datatype of year 
Goalies_df['year'] =  pd.to_datetime(Goalies_df['year'], format='%Y')
print(Goalies_df['year'].dtype)

#3)Wins_agg: total wins / total players 
wins_agg_stg = Goalies_df.groupby(['tmID']).agg({'playerID':'count','W':'sum'})
wins_agg = wins_agg_stg['W']/wins_agg_stg['playerID']
print(wins_agg)

#4)Losses_agg: total losses / total players
Losses_agg_stg = Goalies_df.groupby(['tmID']).agg({'playerID':'count','L':'sum'})
Losses_stg = Losses_agg_stg['L']/Losses_agg_stg['playerID']
print(Losses_stg)


#5)GP_agg: total games played / total players
GP_agg_stg = Goalies_df.groupby(['tmID']).agg({'playerID':'count','GP':'sum'})
GP_agg = GP_agg_stg['GP']/GP_agg_stg['playerID']
print(GP_agg)

#6)Mins_over_GA_agg: total minutes played / total goals against
Mins_over_GA_agg = Goalies_df.groupby(['tmID','year']).Min.agg(['sum'])/Goalies_df.groupby(['tmID','year']).GA.agg(['sum'])
print(Mins_over_GA_agg)

#7)GA_over_SA_agg: total goals against / total shots against
GA_over_SA_agg = Goalies_df.groupby(['tmID','year']).GA.agg(['sum'])/Goalies_df.groupby(['tmID','year']).SA.agg(['sum'])
print(GA_over_SA_agg)

#8)avg_percentage_wins: calculate the percentage of games won for each player, then take the
#mean at team level
avg_perecentage_wins_stg_1 = Goalies_df.groupby(['tmID','playerID']).agg({'W': 'sum', 'GP': 'sum'})
avg_perecentage_wins_stg_2 =avg_perecentage_wins_stg_1['W'] /( avg_perecentage_wins_stg_1['GP'])*100
avg_perecentage_wins = avg_perecentage_wins_stg_2.groupby('tmID').mean()
print(avg_perecentage_wins)


#9)most_goals_stopped: {‘playerID’: playerID, ‘goals_stopped’: goals_stopped}
#Description: calculate goals stopped per player, then take the player with the max goals
#stopped and put the details in the dictionary
most_goals_stopped_stg = Goalies_df.groupby(['playerID'], sort='Desc').agg({'SA':'sum' })
most_goals_stopped_stg_index_reset = most_goals_stopped_stg.reset_index()
most_goals_stopped_final = most_goals_stopped_stg_index_reset[most_goals_stopped_stg_index_reset['SA'] == float(most_goals_stopped_stg_index_reset['SA'].max())]
most_goals_stopped_dict ={}
most_goals_stopped_dict['playerID']= list(most_goals_stopped_final['playerID'])
most_goals_stopped_dict['goals_stopped']= list(most_goals_stopped_final['SA'])
print(most_goals_stopped_dict)

#10)most_efficient_player: {‘playerID’: playerID, ‘efficiency’: goals_stopped / minutes played}
#Description: calculate the goals stopped per minutes of play for each player, then take the
#player with the max efficiency just calculated and put the details in the dictionary
efficient_player_groupby = Goalies_df.groupby(['playerID'], sort='Desc').agg({'Min':'sum', 'SA':'sum' })
efficient_player_stg = efficient_player_groupby['SA']/efficient_player_groupby['Min']
efficient_player_stg = efficient_player_stg.reset_index()
efficient_player_stg = efficient_player_stg[efficient_player_stg[0] == float(efficient_player_stg[0].max())]
most_efficient_player_dict ={}
most_efficient_player_dict['playerID']= list(efficient_player_stg['playerID'])
most_efficient_player_dict['efficiency']= list(efficient_player_stg[0])
print(most_efficient_player_dict)






