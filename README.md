# zarstream
 Special reading mode for special web resources

 ## Features
 - no data stored on the computer: local storage of only hash sums of data for synchronization
 - no direct connection: connection via encrypted TOR-network
 - no windows only: cross-platform solution
 - no potential hazards: only simple text
 - no difficulties: full automatic mode

 ## Description
 The required portal data are requested through the TOR-network.
 The hash sum of each individual data is calculated and compared with the data already read before.
 If new data are found, data are parsed and normalized through the library, then output the data to the screen without using any temporary files (directly in the browser by modifying the HTTP request handler).
 At the end, the hash sum of the new data is saved for later analysis.

 ## Usage
 Set the parameters (base64-encoding url and xpath-like pattern) and just create a new instance of the class -- then the magic happens[^1] automatically.

 ## Examples
  ![GUI](/images/zarstream_1.png)
 ```python
 from zarstream import ZarStream
 url = b'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL21yLWpzL21hbWJhX2h1bnRlci9tYWluL0xJQ0VOU0U='
 pattern = '//p'
 zs = ZarStream(url, pattern)
 ```
  ![GUI](/images/zarstream_2.png)
 After you read the new content in your browser and close it, this content will not be displayed on a subsequent launch -- only the new content.

 ## Remarks
 The program may not display a final window under a non-Windows operating system.
[^1]: Tor browser must be running and active at this time
