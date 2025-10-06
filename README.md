# marclinkcheck
Accepts as input a file with records in MARC Binary (.mrc). Collects URLs from 856$u and checks using the following process:<br />
&nsbp;&bull;Creates a list of all record IDs and URLs in records from 856$u<br />
&nsbp;&bull;Checks all domains in list for validity<br />
&nsbp;&bull;Checks all URLs in list:<br />
&nsbp;&nsbp;&bull;If domain is invalid, marks URL as invalid and adds to list of broken links<br />
&nsbp;&nsbp;&bull;If domain is valid, sends a HEAD request to check status of result<br />
&nsbp;&nsbp;&bull;If HEAD request is denied, sends a GET request instead<br />
&nsbp;&nsbp;&bull;Returns status code. If status code != 200, adds to list of broken URLs<br />
Returns a CSV with record IDs, broken URLs, and HTTP status codes or error messages<br />
<br />
<br />
NOTES:<br />
&nbsp;&bull;Requests are sent in sequence, not concurrently, to avoid hitting rate limits or IP blocks<br />
&nbsp;&bull;Exponential backoff (up to 32 seconds) is implemented for URLs returning HTTP status code 429 (Too Many Requests)<br />
&nbsp;&bull;Does not account for status code 403/405 beyond retrying with GET
