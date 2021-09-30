# Instagram Location Search

## Prerequisites

This Python application requires installation of the requirements.txt file.

This can be done with `pip3 install -r requirements.txt`.

## Example usage

Start the web application by running the command.

```python3 app.py ```

In the terminal the server address should be provided.

The application allows for some interaction with the user providing:
- sessionid
- longitude
- latitude
- date

![Login step](loc-1.gif)

The list of locations can be saved as a CSV file at output.csv

![View and download](loc-2.gif)

Note that this requires an Instagram session ID in order to work! See below for how to obtain one from your account.

## Example usage with date

When using the `--date` argument, links to Instagram location pages will be filtered to show posts created on this date or earlier.
Instagram will usually first show a 3x3 grid of "Top Images and Videos" that are more recent, however once you scroll past that
there is a section labeled "Most recent" which will show the posts sorted by date (if any).
Note: Instagram treats these dates as "UTC", which is a timezone near Great Britain. If your target location is far from this zone,
it's worth adding a couple of days to your filter to make sure you capture all relevant posts. Also, this only specifies the
*maximum* post date that can be displayed. If nothing was posted that day at that location, it will show older posts (sometimes
even multiple years older).

### Other output formats

- To be expanded on.

## Sample Usage with `instagram-scraper`

- To be expanded on. Forked notes below.

The ID list generated with the `--ids` flag can be passed into `instagram-scraper` to pull down image metadata.

### :rotating_light: Undocumented API :rotating_light:
`instagram-scraper` relies on an undocumented API for the mobile apps. YMMV.

Be sure to install `instagram-scraper`:
```
pip install instagram-scraper
```

Location scraping requires an authenticated request. Save your creds in a local file:
```sh
echo "-u=<your username>" >> creds.txt
echo "-p=<your password>" >> creds.txt
```

Now use `instagram-scraper` to pull down all the photos at those locations:
```sh
instagram-scraper @creds.txt --filename @location_ids.txt --location --include-location --destination <output dir>
```

## Getting an Instagram session ID

__Important: an Instagram session ID should be treated like a password — it provides full access to the Instagram account. Using this session ID in multiple places or on multiple computers may trigger Instagram to invalidate all session IDs. Using this session ID for any purpose other than the official Instagram website or application may be a violation of the Instagram Terms of Service and could lead to account suspension.__

1. In Google Chrome, log-in to Instagram.
2. Right click on the page and press "Inspect" to bring up the Chrome Developer Tools.
3. Click the "Application" tab in the Developer Tools Box.
4. Under "Cookies" select "https://www.instagram.com."
5. The value next to "sessionid" is your Instagram session ID.

![Finding the Instagram cookie](docs/cookies.jpg)
