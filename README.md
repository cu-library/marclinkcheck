# marclinkcheck
<i>Includes three scripts: <str>marclinkcheck</str> (checks validity of links in MARC records), <str>invalidurldelete</str> (deletes 856 fields with invalid links from MARC records), <str>recordsplit2.py</str> (splits records into three files: records with no valid links, records with one valid link, and records with more than one valid link)</i><br />
<br />
<b>MARC Link Checker</b><br />
Accepts as input a file with records in MARC Binary (.mrc). Collects URLs from 856$u and checks using the following process:<br />
&nbsp;&bull;Creates a list of all record IDs and URLs in records from 856$u<br />
&nbsp;&bull;Checks all domains in list for validity<br />
&nbsp;&bull;Checks all URLs in list:<br />
&nbsp;&nbsp;&bull;If domain is invalid, marks URL as invalid and adds to list of broken links<br />
&nbsp;&nbsp;&bull;If domain is valid, sends a HEAD request to check status of result<br />
&nbsp;&nbsp;&bull;If HEAD request is denied, sends a GET request instead<br />
&nbsp;&nbsp;&bull;Returns status code. If status code != 200, adds to list of broken URLs<br />
Returns a CSV with record IDs, broken URLs, and HTTP status codes or error messages<br />
<br />
<br />
NOTES:<br />
&nbsp;&bull;Requests are sent in sequence, not concurrently, to avoid hitting rate limits or IP blocks<br />
&nbsp;&bull;Exponential backoff (up to 32 seconds) is implemented for URLs returning HTTP status code 429 (Too Many Requests)<br />
&nbsp;&bull;Does not account for status code 403/405 beyond retrying with GET<br />
<br />
<b>Invalid URL Deleter</b><br />
Accepts two inputs: the CSV output by marclinkcheck and a set of MARC records in MARC Binary. Checks each URL in the MARC records against the list of broken links and deletes any 856 fields with URLs that appear on the list. Saves the revised records to a new .mrc file.<br />
<br />
<b>Record Splitter</b><br />
Accepts a set of MARC records in MARC Binary and splits them into three files: records with no 856 fields with URLs in $u, records with a single 856 with a URL in $u, and records with multiple 856 fields with URLs in $u.
