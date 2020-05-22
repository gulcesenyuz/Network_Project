# P2P File Sharing Application

Group Members: Turgay Barkın Türkşen (1802548), Gülce Külahçıoğlu (1731380)

This is a networking project where we make a peer to peer network to share files among peers on the same local network.

The application is developed using python3 on Windows 10 and MacOS Catalina. 

LIST OF FILES:
- p2p_server.py *** divides the requested file into N-byte 5 chunks and stores them in separate file. Send the file requested over the TCP connection
- service_announcer.py  *** peer starts  UDP broadcasting the list of all files they have once per minute.
- p2p_downloader.py *** user specifies the name of the file to download. TCP connection opens to download all chunks of the file requested. After all chunks are downloaded, the program closes TCP connection.
- service_listener.py *** listens for UDP broadcast messages and logs detected Client tags and file combinations in a text file 
(tags.txt).  

***** UDP broadcasts containts username, files in JSON format.
***** client.log includes the download history.
***** server.log includes succesful client connection history.
***** downloads folder gets created and includes fully downloaded files.
***** temp folder gets created and includes downloaded/seperated chunks.


Attention:
	*tags.txt needs to cleared if a client deltes a chunk from their computer. Otherwise the download operation fails.
	
    *p2p_server.py assumes the root folder of the project as the referance path. The project root folder has to include the file to be served.
    
    *Run Hamachi, then replace h_ip's value with your own Hamachi IP. [p2p_server.py ---> //line 9 :: h_ip = "IPv4",
                                                                       service_listener.py --->//line 7 :: h_ip = "IPv4" ]

    *For a client to be able to serve it's downloaded chunks, client tag needs to be defined under service_announcer.py UI.

    The system designed is not capable of collecting missing chunks of a single file from different clients serving the same file as an Torrent system would do. It can only download if the users hosting the chunks have all of them. Otherwise the file downloads with missing parts.

    When downloading from the server is done, chunks get combined and the final file is created at the 'downloads' folder.

Steps to execute the project:
- 1: run python3 p2p_server.py
- 2: run python3 service_announcer.py
- 3: run python3 p2p_downloader.py
- 4: run python3 service_listener.py


Protocol Design:
The protocol is designed to work on the application level with user input/output in terminal.

 
