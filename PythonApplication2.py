
import pandas as pd
import duckdb
from scipy.stats import *
pd.set_option('display.max_columns', None)
file = r'C:\Users\steam\OneDrive\Desktop\tiktok_shop_viral_video_sales_attribution_cac.csv'
val = pd.read_csv(file, sep=',')

#print(val.head())

duckdb.query(''' CREATE OR REPLACE TABLE clear AS
SELECT hook_category, 

QUANTILE_CONT(creator_followers, 0.25) AS q25_follow,
QUANTILE_CONT(creator_followers, 0.75) AS q75_follow,

AVG(creator_followers) AS avg_follow,
MEDIAN(creator_followers) AS median_follow,

SUM(product_page_view_flag) AS view,
(count(*) - SUM(product_page_view_flag)) AS no_view,
count(*) AS total_views

FROM val

WHERE hook_category IN ('Emotional', 'Rational')
AND data_quality_flag = 1
AND anomaly_flag = 0
AND creator_followers IS NOT NULL
AND product_page_view_flag IS NOT NULL

GROUP BY hook_category
ORDER BY hook_category
''')

clear = duckdb.query("SELECT * FROM clear").to_df()
print(clear)

table1 = clear[['hook_category','view', 'total_views']].copy() #konv
table1['conversion'] = (
    (table1['view'] / table1['total_views']) *100
    )
print(table1)



print('_________________________')

table2 = clear[['view', 'no_view']].values #chi2
chi2, p, dof, final = chi2_contingency(table2) 

print('_________________________')
print('x2=', chi2)
print('_________________________')
print('p-value = ', p)
print('_________________________')
print('freedom=', dof)
print('_________________________')
print('final_table =', final)