# Junker Scrape

This is a stand-alone version of the scraper created inside the project *HACS Waste Collection Schedule* mentioned in the note below; it works with the limitation of handling only Junker registered municipalities in Italy.

**CREDITS**: I came up with this snipped by standing on the shoulders of giants: many thanks to Steffen Zimmermann and all the contributors to his great HACS integration for waste collection schedule! You can look at the complete work (and thank the author) over his [GitHub repository](https://github.com/mampfes/hacs_waste_collection_schedule).

## Usage

1. Create or reset the virtual environment through the provided script `reset_venv.sh`; if the venv was created previously, you may want to just load it with the following command:

```bash
source .venv/bin/activate
```
2. Run the `main.py` file through a Python interpreter, providing the municipality name and the area code

```bash
python3 main.py MUNICIPALITY AREA DATE
```

3. In absence of errors, the program will print a JSON list of dictionaries, one per each collected bin. I reused the same classes as the original scraper with minor modifications.

### Date

This is the third positional argument but it is also the easier to explain, so I am writing about it first: filter the results by date in the format `YYYY-MM-DD`. This argument is mandatory

### Municipality and Area

To get the correct strings for your specific location you can browse to the [Municipality Locator](https://junker.app/cerca-il-tuo-comune/) and input its name; wait for the suggestion to show up and click it.

If the municipality is subscribed tu Junker's service, a page with congratulations will load with another search box to input the street or area: input its name and click only on the suggestion (if it shows up)

Finally, a page will load with the municipality and area strings in the upper left corner and a menu on the left: look at the URL and extract the municipality name and area code from it, knowing that their positions inside the URL will be as follows:

```txt
https://differenziata.junkerapp.it/MUNICIPALITY/AREA/info
```

# Limitations

At the moment, I am ignoring the fact that the area is optional for some municipalities and it is instead a mandatory argument. This might break for those cases.
