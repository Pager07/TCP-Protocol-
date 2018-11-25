import socket
from datetime import datetime
import select
import time
import sys
import json

'''Returns a dictionary key = song names, value= list of artistnames'''
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
                    ''' get artist_name and song_name string'''
                    '''song = "xx- song_name" '''
                    ''' artist_name = "name   XXXX" '''
                    artist = line[pointer+2:].strip()
                    
                    
                    song_name = line[0:pointer].strip()
                    
                    
                    '''Remove number- form songname'''
                    song_name = song_name.split('-',1)[-1].strip().lower()
                    
                    '''Removing date from artist name'''
                    artist = ''.join([letter for letter in artist if not letter.isdigit()]).strip().lower()
                                    
                    if "/" in artist:
                        names_listx = artist.split("/")
                        for name in names_listx:
                            name_list.append(name)
                        song_to_artist[song_name] = name_list
                            
                    elif "featuring" in artist:
                        names_listx = artist.split("featuring")
                        for name in names_listx:
                            name_list.append(name)
                        song_to_artist[song_name] = name_list
                    else:
    #                 
                        name_list.append(artist)
                        song_to_artist[song_name] = name_list
                    break
    return song_to_artist,raw_text

'''Read file'''
song_to_artist,y= read_textfile("/Users/sandeep/Desktop/Year 2/Network and System/Networks/CourseWork/100worst.txt")

def handle_client(server_socket,sock_list):
#    
    while True:
        counter = 0
        read_sockets, write_sockets, error_sockets = select.select(sock_list,[],[])
        for sock in read_sockets:
                       
            '''if it is server socket and read_sockets length is less than 2 accpet'''
            '''read_socket/socket_list should only have sever_socket and 1 client socket at any given time'''
            if sock == server_socket:
                if len(sock_list)>=2:
                    
                    '''Get client socket'''
                    client_socket , address = server_socket.accept()
                    if client_socket not in sock_list:
                        
                        '''Log client adrress and unsuccesfull request'''
                        log_data("Unsuccessful Request from {},{} at {}".format(address[0],address[1],datetime.now().strftime('%c')))
                       
                        print("Client ({}, {}) connection rejected".format(address[0], address[1]))
                        
                        client_socket.send('server is busy')
                       
                        '''close the socket'''
                        client_socket.close()
                    
                elif len(sock_list)<2:
                    
                    '''Get client socket'''
                    client_socket , address = server_socket.accept()
                        
                    print('connected to',address[0])
                    counter += 1
                    
                    '''Start timer'''
                    start_time = time.time()
                    
                    '''Add client to socket_list'''
                    sock_list.append(client_socket)
                    print("Client ({}, {}) connected" .format(address[0], address[1]))
                    
                    client_socket.send('connected')
                   
                    '''Log client address'''
                    log_data("Successful Connection from client on {},{} : At {}".format(address[0],address[1],datetime.now().strftime('%c')))
            else:
                '''get the artist'''
                data = get_artist(sock) 
                
                if 'quit' in data:
                    sock.send('dissconnected')
                    end_time = time.time()
                    
                    '''Log length of time connected to server'''
                    log_data("Connection time for client on {},{} is {} seconds".format(address[0],address[1],(end_time - start_time)))                
                    counter = 0
                    client_socket.close()
                    sock_list.remove(sock)
                    server_socket.close()
                    sys.exit(0)
                else:              
                    print('Recevied Message:{}'.format(data))
                    sock.send('Recevied Message Succesfully!')
                    
                    
                    log_data("Client on {},{} : Artist requested {}".format(address[0],address[1],data))
                    
                    '''get song by requested artist'''
                    artist_songs = get_songs(data , song_to_artist)
                    
                    '''check if the artist exist/we need list of artist songs'''
                    '''if not stop serving their 1st request''' 
                    try:
                        check_artist(artist_songs)
                        sock.send('truee')
                        
                        send_songs(sock , artist_songs)
                    except Exception:
                      sock.send('false')
                           
                    

                  
def send_songs(client_socket, artist_songs):
    data = json.dumps({'songs':artist_songs})
    client_socket.send(data.encode())
           
def get_artist(client_socket):
    request = client_socket.recv(1024).lower()
    return request

def get_songs(artist,song_artist_dict):
    '''get all the songs/keys'''
    songs = song_artist_dict.keys()
    
    '''get songs made by artist'''
    artist_songs = [song for song in songs if artist in song_artist_dict[song]]  
    
    return artist_songs

def check_artist(artist_songs):
    if len(artist_songs) == 0:
        raise Exception('The artist does not exist.Try again!')

def send_client_songs(client_sock,artist_songs):
    for song in artist_songs:
        client_sock.send(song)

def log_data(data):
    f= open('server.log' , 'a+')
    f.write(data)
    f.write('\n')
    f.close()

def server():
    
    '''Socket list'''
    socket_list = []
    
    '''Create a socket'''
    server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server.setblocking(0)
    '''Make binding adress'''
    ip = socket.gethostbyname('localhost')
    port = 1234
    socket_address = (ip ,port) 
    
    '''Bind socket to bind adress'''
    server.bind(socket_address)
    
    '''Start listening/set up how many connection to be hold in queue at max'''
    '''1 is called the backlog value = length of pendding connection queue'''
    server.listen(1)
    
    '''Add server socket to socket list'''
    socket_list.append(server)
    
    print('Listening on ip:{} , port:{}'.format(ip,port))
    
    '''Log server start date and time '''
    log_data("Server started at:{}".format(datetime.now().strftime('%c')))
    
    '''handle client'''
    handle_client(server,socket_list)
    
server()
    
    
  


  
  
  
  