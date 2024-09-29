import scraper as sc
import pandas as pd

links = sc.scrape_fragrance_links()
all_data = []
#for link in links:
print(links[0])
fragrance_data = sc.scrape_fragrance_data(links[0])
all_data.append(fragrance_data)

df = pd.DataFrame(all_data)
df.to_csv("fragrance-data.csv")
print(df.head)
