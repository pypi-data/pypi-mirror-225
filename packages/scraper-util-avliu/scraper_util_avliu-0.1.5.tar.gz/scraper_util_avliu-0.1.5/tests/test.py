from src.scraper_util_avliu import example
from src.scraper_util_avliu import util


# Recognize that testing this way cannot test whether requirements are valid,
# e.g. cannot test whether "boto-3" is the correct name to put in the pyproject.toml
# example.test()


soup = util.get_soup('https://www.kbb.com/cars-for-sale/vehicledetails.xhtml?listingId=690270863&city=Mount%20Pleasant&firstRecord=300&isNewSearch=false&listingTypes=USED&marketExtension=include&numRecords=100&referrer=%2Fcars-for-sale%2Fused%2Fmount-pleasant-mi%3FsearchRadius%3D200%26zip%3D48858%26marketExtension%3Dinclude%26isNewSearch%3Dfalse%26showAccelerateBanner%3Dfalse%26sortBy%3Drelevance%26numRecords%3D100%26firstRecord%3D300&searchRadius=200&sortBy=relevance&state=MI&zip=48858&clickType=listing')
s = soup.prettify()

# TODO: Start here for finding sale date
soup.find('window.__BONNET_DATA__=')