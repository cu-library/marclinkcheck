# marclinkcheck
Accepts as input a file with records in MARC Binary (.mrc). Collects URLs from 856$u and checks using the following process:
&nsbp;&bull;Creates a list of all record IDs and URLs in records from 856$u
&nsbp;&bull;Checks all domains in list for validity
&nsbp;&bull;Checks all URLs in list:
&nsbp;&nsbp;&bull;If domain is invalid, marks URL as invalid and adds to list of broken links
&nsbp;&nsbp;&bull;If domain is valid, sends a HEAD request to check status of result
&nsbp;&nsbp;&bull;If HEAD request is denied, sends a GET request instead
&nsbp;&nsbp;&bull;Returns status code. If status code != 200, adds to list of broken URLs
Returns a CSV with record IDs, broken URLs, and HTTP status codes or error messages
<br />
<br />
NOTES:
&nbsp;&bull;Requests are sent in sequence, not concurrently, to avoid hitting rate limits or IP blocks
&nbsp;&bull;Exponential backoff (up to 32 seconds) is implemented for URLs returning HTTP status code 429 (Too Many Requests)
&nbsp;&bull;Does not account for status code 403/405 beyond retrying with GET
