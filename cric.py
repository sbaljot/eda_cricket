import pandas as pd

df = pd.read_csv('Untitled spreadsheet - Sheet1.csv') #add the sheet
'''Problem statement: To predict the runs scored by each batsman if they played for 10 more years'''

df[['Player','Country']] = df['Player'].str.split('(', expand=True)

df['Country'] = df['Country'].str.split(')').str[0]

mask_country = df['Country'].str.contains('ICC')
df.loc[mask_country,'Country'] = df.loc[mask_country,'Country'].str.replace('ICC/','')

df[['Start_year','End_year']] = df['Span'].str.split('-', expand=True)

df.drop('Span',axis=1,inplace=True)

mask_hs = df['HS'].str.contains('*', regex=False)
df.loc[mask_hs,'HS'] = df.loc[mask_hs,'HS'].str.replace('*','')

df.rename(columns = {'SR':'Strike_rate',
                     'Ave':'Average',
                     'BF':'Balls_faced'}, inplace=True)

cols_w_plus = ['Balls_faced','4s','6s']
df[cols_w_plus] = df[cols_w_plus].apply(lambda x:x.str.replace('+','',regex=False))

df = df.astype({'HS':'int64',
                'Balls_faced':'int64',
                '4s':'int64',
                '6s':'int64',
                'Country':'str',
                'Start_year':'int64',
                'End_year':'int64',})

print(df.info())

#boxplot analysis for different variables
iqr = df['6s'].quantile(0.75) - df['6s'].quantile(0.25)
upper_fence = df['6s'].quantile(0.75) + 1.5*iqr
lower_fence = df['6s'].quantile(0.25) - 1.5*iqr
print(df[(df['6s']>upper_fence) & (df['6s']>lower_fence)])
sns.boxplot(df['6s'])
plt.show()
#covariance
runs_comp = df[["Runs","Mat","Inns","Strike_rate","NO","Average","Balls_faced"]]#"HS","100","50","0","4s","6s"
runs_comp = df[["Strike_rate","100","50","0","4s","6s"]]
runs_comp = df[["Mat","100","50","0","4s","6s"]]
print(runs_comp.cov())
#conditional probability
high_sr = df.loc[df['Strike_rate'] >= df['Strike_rate'].quantile(0.75), ['Player', 'Strike_rate']]
high_runs = df.loc[df['Runs'] >= df['Runs'].quantile(0.75), ['Player', 'Runs']]
srintersection = len(set(high_runs['Player']) & set(high_sr['Player']))
print(srintersection/high_sr['Player'].count())
print(high_runs['Player'].count())

high_centurion = df.loc[df['100'] >= df['100'].quantile(0.75), ['Player', '100']]
high_avg = df.loc[df['Average'] >= df['Average'].quantile(0.75), ['Player', 'Average']]
caintersection = len(set(high_centurion['Player']) & set(high_avg['Player']))
print(srintersection/high_avg['Player'].count())
print(high_centurion['Player'].count())

low_ducks = df.loc[df['0'] <= df['0'].quantile(0.25),['Player', '0']]
high_consistency = df.loc[df['Average'] >= df['Average'].quantile(0.75),['Player', 'Average']]
dcintersection = len(set(low_ducks) & set(high_consistency))
print(dcintersection/high_consistency['Player'].count())
print(low_ducks['Player'].count())

df['career_length'] = df['End_year'] - df['Start_year']
long_career = df.loc[df['career_length'] >= df['career_length'].quantile(0.75),['Player', 'career_length']]
high_balls = df.loc[df['Balls_faced'] >= df['Balls_faced'].quantile(0.75),['Player', 'Balls_faced']]
cbintersection = len(set(long_career) & set(high_balls))
print(dcintersection/high_balls['Player'].count())
print(long_career['Player'].count())

#z test

#H0 = high run players among high sr players are same compared to overall high run players
#H1 = high run players among high sr players are different compared to overall high run players
total_players = df['Player'].count()
total_high_run_players = df[df['Runs']>=df['Runs'].quantile(0.75)]['Player'].count()
total_high_sr_players = df[df['Strike_rate']>=df['Strike_rate'].quantile(0.75)]['Player'].count()
p_high_run_intersect_high_sr = set(df[df['Runs']>=df['Runs'].quantile(0.75)]['Player']) & set(df[df['Strike_rate']>=df['Strike_rate'].quantile(0.75)]['Player'])
p_high_run_given_high_sr = len(p_high_run_intersect_high_sr)/total_high_sr_players
p  = p_high_run_given_high_sr
p0 = total_high_run_players / total_players
n  = total_high_sr_players #because high run players are within high sr players so sr players is the base
degree_of_freedom = n-1
z = (p - p0) / ( (p0 * (1 - p0)) / n )**0.5
print('H0:',-1.96 <= z <= 1.96) #z table values for 0.9750
#H0 = centurions among high avg players are same as the global centurions
#H1 = centurions among high avg players are more as the global centurions
total_centurions = df['100'].count()
total_high_avg_players = df[df['Average']>=df['Average'].quantile(0.75)]['Average'].count()
p_centurion_intersect_high_avg = set(df[df['100']>=df['100'].quantile(0.75)]['Player']) & set(df[df['Average']>=df['Average'].quantile(0.75)]['Player'])
p_centurion_given_high_avg = len(p_centurion_intersect_high_avg)/total_high_avg_players
p  = p_centurion_given_high_avg
p0 = total_centurions / total_players
n  = total_high_avg_players
z = (p - p0) / ( (p0 * (1 - p0)) / n )**0.5
print('H0:',-1.96 <= z <= 1.96) #test failed because everyone is a centurion

#chi test

#H0: independence
#H1: association

high_sr_players = df[df['Strike_rate']>=df['Strike_rate'].quantile(0.75)]['Player']
low_sr_players = df[df['Strike_rate']<=df['Strike_rate'].quantile(0.25)]['Player']
high_runs = df[df['Runs']>=df['Runs'].quantile(0.75)]['Player']
low_runs = df[df['Runs']<=df['Runs'].quantile(0.25)]['Player']
#observed values
o11 = len(set(high_sr_players)&set(high_runs))
o12 = len(set(high_sr_players)&set(low_runs))
o21 = len(set(low_sr_players)&set(high_runs))
o22 = len(set(low_sr_players)&set(low_runs))
n=26
#expected values
e11 = ((o11+o12)*(o11+o21))/n
e12 = ((o11+o12)*(o12+o22))/n
e21 = ((o21+o22)*(o11+o21))/n
e22 = ((o21+o22)*(o12+o22))/n
#cell wise summed values
x11 = (o11-e11)**2/e11
x12 = (o12-e12)**2/e12
x21 = (o21-e21)**2/e21
x22 = (o22-e22)**2/e22
chi_sum = x11+x22+x12+x21
df = (2-1)*(2-1) #r-1.c-1
chi_table_value = 3.84
print(chi_sum)
