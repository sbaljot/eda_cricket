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
