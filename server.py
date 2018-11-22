#import socket
#
###Creat an socket object
#server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
#
##find adress
#ip = socket.gethostbyname(socket.gethostname)
#port = 1234
#socket_address = (ip ,port) 
#
##bind the object to the address
#server.bind(socket_address)
#
##wait for client connection
#server.listen(1)
#print("started listening on ip:{} , port:{}".format(ip,port))
#
#
#
##The server reads a textfile 
##maps the text file
#text_file_dir = "/Users/sandeep/Desktop/Year 2/Network and System/Networks/CourseWork/100worst.txt"
#f = open(text_file_dir , 'r')
#
#raw_text = [line for line in f.readlines() if line.strip()]
#
###clean top section
##find the starting point 
#found = False
#while found == False:
#    line = 0
#    if raw_text[line][0] != "1":
#        raw_text.pop(line)
#    elif raw_text[line][0] == "1":
#        found = True
#print("Top Successfully Cleaned!")  
#    
### clean bottom part
###find stopping point
#found = False
#num_of_X = 0
#while num_of_X <= 1:
#    line = -1
#    if raw_text[-1][0] == "X":
#        num_of_X = num_of_X + 1
#    raw_text.pop(line)   
#
##striping away /r/n
#raw_text = [string.rstrip() for string in raw_text] 
#
###Handle the song and name seperation
#for line_num,line in enumerate(raw_text):
#    ##check if the next line starts with space
#    next_line = line_num + 1
#    if next_line < len(raw_text):
#        if raw_text[next_line][0] == " ":
#            artist = raw_text[next_line].rstrip()
#            raw_text[line_num] = raw_text[line_num] + artist
#            raw_text.pop(next_line)
#
###Handle Removing the numbers and - of each line 
##100-Everybody Have Fun Tonight     Wang Chung                    1986   
#for line_num, line in enumerate(raw_text):
#   new_line = "".join([letter for word in line for letter in word if  not letter.isdigit()])
#   new_line = new_line.replace("-" , "")
#   new_line = new_line.strip()
#   raw_text[line_num] = new_line
#   
#
##Serperate Songs from artist 
##x/y mean 2 different artist
##Map Songs to artist 
#song_to_artist = {}
##1
#for line_num, line in enumerate(raw_text):
##    check for consequite spaces bars 
#    name_list = []
#    for pointer, letter in enumerate(line):
#        if letter == " ":
#            if line[pointer+1] == " ":
#                artist = line[pointer+2:].strip()
#                
##                print(artist)
#                song_name = line[0:pointer].strip()
#                if "/" in artist:
#                    names_listx = artist.split("/")
#                    for name in names_listx:
#                        name_list.append(name)
#                        
#                elif "featuring" in artist:
#                    names_listx = artist.split("featuring")
#                    for name in names_listx:
#                        name_list.append(name)
#                else:
##                 
#                    name_list.append(artist)
#                    song_to_artist[song_name] = name_list
##                for artist in name_list:
##                    artist_to_songs[artist] = song_name
#                break

#
#
#                
#client, client_address = server.accept()           
#print("Got connection from ip:{} , port:{}".format(client_address[0],client_address[1]))
#
#while True:
#    wanted_artist = client.recv(1024)
#    client.send("Request Successfully Recieved!")
#    song_names = song_to_artist.keys()
#    wanted_artist_songs = []
#    for song in song_names:
#        artists = song_to_artist[song]
#        if wanted_artist in artists:
#            wanted_artist.append(song)
#    if len(song_names) ==0:
#        client.send("No song for {} was found!".format(wanted_artist))
#
##
##eastablish connection with client 
#client , addr = server.accept()
#print("Got connection from ip:{} , port:{}".format(addr[0],addr[1]))
#
#
#
#client_connection = True 
#while client_connection:
#    text_file = client.recv()


def read_textfile(text_file_dir):
    f = open(text_file_dir , 'r')

    raw_text = [line for line in f.readlines() if line.strip()]
    
    ##clean top section
    #find the starting point 
    found = False
    while found == False:
        line = 0
        if raw_text[line][0] != "1":
            raw_text.pop(line)
        elif raw_text[line][0] == "1":
            found = True
    print("Top Successfully Cleaned!")  
        
    ## clean bottom part
    ##find stopping point
    found = False
    num_of_X = 0
    while num_of_X <= 1:
        line = -1
        if raw_text[-1][0] == "X":
            num_of_X = num_of_X + 1
        raw_text.pop(line)   
    
    #striping away /r/n
    raw_text = [string.rstrip() for string in raw_text] 
    
    ##Handle the song and name seperation
    for line_num,line in enumerate(raw_text):
        ##check if the next line starts with space
        next_line = line_num + 1
        if next_line < len(raw_text):
            if raw_text[next_line][0] == " ":
                artist = raw_text[next_line].rstrip()
                raw_text[line_num] = raw_text[line_num] + artist
                raw_text.pop(next_line)
    
    ##Handle Removing the numbers and - of each line 
    #100-Everybody Have Fun Tonight     Wang Chung                    1986   
    for line_num, line in enumerate(raw_text):
       new_line = "".join([letter for word in line for letter in word if  not letter.isdigit()])
       new_line = new_line.replace("-" , "")
       new_line = new_line.strip()
       raw_text[line_num] = new_line
       
    
    #Serperate Songs from artist 
    #x/y mean 2 different artist
    #Map Songs to artist 
    song_to_artist = {}
    #1
    for line_num, line in enumerate(raw_text):
    #    check for consequite spaces bars 
        name_list = []
        for pointer, letter in enumerate(line):
            if letter == " ":
                if line[pointer+1] == " ":
                    artist = line[pointer+2:].strip()
#                    print(artist)
    #                print(artist)
                    song_name = line[0:pointer].strip()
#                    print(song_name)
                    if "/" in artist:
                        names_listx = artist.split("/")
                        for name in names_listx:
                            name_list.append(name)
                            
                    elif "featuring" in artist:
                        names_listx = artist.split("featuring")
                        for name in names_listx:
                            name_list.append(name)
                    else:
    #                 
                        name_list.append(artist)
                        song_to_artist[song_name] = name_list
                    break
    return song_to_artist,raw_text

x,y= read_textfile("/Users/sandeep/Desktop/Year 2/Network and System/Networks/CourseWork/100worst.txt")
