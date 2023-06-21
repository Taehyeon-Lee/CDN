CS5700 - SP2023
Project 5: Roll Your Own CDN
Tae-Hyeon Lee + Mitchell Neides


High-level approach:

We began by researching in-depth the process for how CDNs work as well as the protocols for DNS and (reviewed) for HTTP 
servers. Next, we split the work so that Tae-Hyeon focused on the HTTP implementation and Mitchell focused on the DNS 
implementation. This involved reading the documentation for dnslib, socketserver and the http python library. Then, we 
each started attempting to implement our respective servers while testing to see if we are able to both send data as 
well as receive responses. Once this was working, we focused on properly forming our packets and finally parsing the 
data and forming the proper responses. Finally, once our implementations were working as expected, we wrote our deploy, 
run and stop scripts. This involved researching bash scripting and a lot of iterations of testing to ensure that they 
behave as required.
After the milestone, we switched who was focusing on DNS/HTTP so that we would both have a comprehensive understanding 
of each of the two processes. That is, Tae-Hyeon focused on the DNS implementation incorporating all 7 replica servers 
now and Mitchell focused on the HTTP implementation's caching strategy. Both of these strategies will be elaborated on 
in the following section.


How we implemented our DNS and HTTP Servers:

DNS - The program first parses command line arguments to receive the port and CDN domain that the CDN is running on. 
Then, the IP addresses of the DNS server and the replica server are determined. Finally, a UDPHandler (from the 
socketserver library) handles the receiving of UDP DNS packets, parses the data, and creates and sends the appropriate 
response.
After the milestone, a geolocation api was used to determine location of the client making the request. An algorithm 
was implemented to determine which replica server the client is closest to, and the DNS response prioritizes that 
replica as the ideal DNS response. We then cache the client's IP and the replica server it is closest to so that we 
do not need to look up the geolocation every time a repeat client makes a request.
We hoped to then use scamper to make the final decision as to whether or not that server is overloaded, and if so go on 
to check the next closest replica server, but we found that these checks were adding significant time to our 
response that was too costly. Therefore, we decided to remove this from the equation and 
for now respond just based on geolocation. We plan to continue working on the scamper implementation to see if we can 
bring down the response time, but for the sake of the competition we decided to leave it out.

HTTP - The program first parses command line arguments to receive the port, origin server hostname and port that the 
origin server is running on. Then, a RequestHandler (from the http.server library) handles the receiving of HTTP 
requests from the client and forwards them to the origin server. Once the response is received back from the origin 
server containing the http response, the data is finally forwarded back to the client using the socket that they had 
requested the data from.
After the milestone we implemented a caching strategy to serve files to the client as quickly as possible. We gzip all 
files in the cache so that we can cache more files, and we use both disk storage as well as ram storage to be able to 
cache slightly over 25% of the total files. We chose to cache all of the same files in every replica server since the 
requests come in a zipf distribution, meaning we decided to play the odds and cache as many of the most likely to be 
requested files as possible. If a file is cached, we send the compressed version to shorten our transmission size and 
save time by putting the decompression at the expense of the client.
NOTE: We implemented a way for compression to be turned on or off. The files will always be stored in compressed version
, but in the event that someone does not want to serve compressed files, they simply need to uncomment/comment the 2 
specified areas in the 'httpserver' file inside the do_GET method (though it will, of course, slow down the service).
We also thought of a cool strategy to efficiently pre-populate our cache, which will be discussed in the section that 
follows ('after the milestone' section).


Challenges faced:

Probably the biggest challenge faced was figuring out how to receive data back from the DNS server. Initially, we were 
trying to use the standard socket.socket(socket.AF_INET, socket.SOCK_DGRAM) socket from the socket library, but our OS 
was incapable of receiving a response back from the server (although it could send packets out without any problems). 
After doing some research, we found an alternative way to send UDP packets using a UDPHandler from the socketserver 
library. With this implementation we were able to both send and receive packets and therefore continue implementing our 
DNS server.
We also initially tried to implement the HTTP server from scratch using a standard socket. However, as we did more 
research on the HTTP server, we found out that using the HTTP RequestHandler is a more efficient way of doing it 
because later we will need to handle caching, and when we send a response back to the client we need to include headers.
 We found that using this library was much more efficient than trying to create the headers ourselves.

After the milestone, we came up with our strategy to cache as many of the higher priority files as possible, but we 
struggled greatly with how to pre-populate our cache in a timely manner. Our first implementation required every replica
 to request all cached files from the origin, but this took a VERY long time and greatly congested our network. After 
some brainstorming, we realized that we could lighten the load by having the replica servers communicate with each 
other. Rather than each replica populating its own cache, we had the server closest to the replica make the requests 
for all the files that should be in cache, and then we started a cascade of forwarding these files to the next node 
in the MST of our replica servers. This meant that we cut down the load on the origin to 1/7 of what it originally was, 
and it took our cache population time from ~10 minutes to ~2 minutes. We also started these processes in our deploy and 
run scripts, and since they take about 2 minutes total to complete, this means that our cache is just about completely 
populated by the time that our CDN is up and running!


Work breakdown:

As mentioned earlier, Tae-Hyeon took the lead for the HTTP server and Mitchell took the lead for the DNS server. 
We then began implementing the respective servers on our own while keep each other updated with our processes. Once our 
servers were running, we wrote the scripts and did our testing together.
After the milestone, we switched so that Mitchell took the lead for the HTTP server and Tae-Hyeon took the lead for the 
DNS server. As we got our base implementations running, we then worked together to implement the efficiency upgrades.
