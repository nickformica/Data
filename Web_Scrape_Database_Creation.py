import sqlite3
import pandas as pd 

import requests
from bs4 import BeautifulSoup as BS 
import pandas as pd
from sys import argv

url = 'https://www.pro-football-reference.com/play-index/psl_finder.cgi?request=1&match=single&year_min=2019&year_max=2019&season_start=1&season_end=-1&pos%5B%5D=qb&pos%5B%5D=rb&pos%5B%5D=wr&pos%5B%5D=te&pos%5B%5D=e&pos%5B%5D=t&pos%5B%5D=g&pos%5B%5D=c&pos%5B%5D=ol&pos%5B%5D=dt&pos%5B%5D=de&pos%5B%5D=dl&pos%5B%5D=ilb&pos%5B%5D=olb&pos%5B%5D=lb&pos%5B%5D=cb&pos%5B%5D=s&pos%5B%5D=db&pos%5B%5D=k&pos%5B%5D=p&draft_year_min=1936&draft_year_max=2020&draft_slot_min=1&draft_slot_max=500&draft_pick_in_round=pick_overall&conference=any&draft_pos%5B%5D=qb&draft_pos%5B%5D=rb&draft_pos%5B%5D=wr&draft_pos%5B%5D=te&draft_pos%5B%5D=e&draft_pos%5B%5D=t&draft_pos%5B%5D=g&draft_pos%5B%5D=c&draft_pos%5B%5D=ol&draft_pos%5B%5D=dt&draft_pos%5B%5D=de&draft_pos%5B%5D=dl&draft_pos%5B%5D=ilb&draft_pos%5B%5D=olb&draft_pos%5B%5D=lb&draft_pos%5B%5D=cb&draft_pos%5B%5D=s&draft_pos%5B%5D=db&draft_pos%5B%5D=k&draft_pos%5B%5D=p&c5val=1.0&order_by=pass_td'

res = requests.get(url)
soup = BS(res.content, 'html.parser')
table = soup.find('table', {'id': 'results'})
df = pd.read_html(str(table))[0]
df.columns = df.columns.droplevel(level = 0)

defColumnSettings = {
    'axis': 1,
    'inplace': True
}

df.to_csv('QB_DF.csv')


conn = sqlite3.connect('BaseCannon.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

# Create table - rbdata
c.execute('''CREATE TABLE  IF NOT EXISTS rbs
             ([generated_id] INTEGER PRIMARY KEY,[Rk] integer, [Player] text, [Yds] integer,[Pos] text,
             [Age] integer,[TD] integer)''')
conn.commit()

read_csv = pd.read_csv (r'QB_DF.csv')
rbs = read_csv.to_sql('rbs', conn, if_exists='replace', index = False)


df = pd.DataFrame(rbs, columns=['Player','Yds','TD','Pos'])

c.execute(''' Select Player, Yds
                from rbs
                ''')

for row in c.fetchall():
    print(row)