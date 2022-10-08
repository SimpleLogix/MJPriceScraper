# MJPriceScraper
Price Scraper tool to find the latest deals at your local dispensery! 🍃

Run the Jupyter Notebook either locally or on VSCode. Alternatively, you may run this on Google Colab but at the moment there are some bugs and not all products get scraped.
<br/>

## Customizing the scraper
As of now, only a handful of dispenseries are supported (from the dutchie menu), which can be found under the ```dispos dictionary``` . Adding custom dispenseries to the list is currently not supported.

The only thing you should really change is the ```filter``` variable, which should refer to a key in the ```filters dictionary```. Choose a preset filter to avoid unsupported links and runtime issues.

For example, if you want to search for flower you would set the filter to 'flower':
```
filter = filters["Flower"]
```

## Running the Scraper
After picking the filter, run all of the code blocks to scrape the menus. 

The main loop under code block [4] takes around a minute to run and gather the data, so be mindful.

## Results 
Results are stored under the logs folder. The destination can be chaged by editing the ```logs_destination``` variable found under the filter variable.

If running this from Google Colab, logs will be stored under a folder in your google drive.

## Roadmap

- [x] Scrape products data
- [ ] Add deals from dispo home blurb
- [ ] Clean names & Categorize (Wax, Sugar, Kief, Crumble, ...)
- [ ] Add 1g version of .5g products

- [ ] Add custom function for Sanctuary
- [ ] Store logs of data w/ timestamp
- [ ] Data visualization (tables and graphs)

- [ ] 

