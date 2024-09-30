import scraper as sc
import pandas as pd

driver = sc.create_new_driver()
links = sc.scrape_fragrance_links(driver)
print(links)
# all_data = []
# #for link in links:
# print(links[0])
# fragrance_data = sc.scrape_fragrance_data(links, driver)
# all_data.append(fragrance_data)
#
# df = pd.DataFrame(all_data)
# df.to_csv("../data/fragrance-data.csv")
# driver.quit()
