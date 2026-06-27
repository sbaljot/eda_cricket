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
