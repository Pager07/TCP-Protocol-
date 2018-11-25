import socket 
import sys
import select
import json
import time
from datetime import datetime

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()
    return None


def tell_connection_status(client_socket):
    data = client_socket.recv(1024)
    
    '''check for 'server is busy' or 'connected' from server'''
    if 'server is busy' in data:
        sys.stdout.write('Connection failed.Server is busy with another client. Try agian later.')
        
        '''Flush the buffer'''
        sys.stdout.flush()
        
        '''close the client socket'''
        client_socket.close()
        
        '''exit the program'''
        sys.exit(1)
    else:
        sys.stdout.write('Connection successful.You are now connected to the server.\n')
        sys.stdout.flush()
        return None

def songs_toString(songs_list):
    song_string = ""
    for song in songs_list:
        song_string = song_string + song + ',' 
    return song_string

def utf8len(songs_list):
    song_string = ""
    for song in songs_list:
        song_string = song_string + song  
    return len(song_string.encode('utf-8'))

def log_data(data):
    f= open('client.log' , 'a+')
    f.write(data)
    f.write('\n')
    f.close()      
    
    
'''Create a socket'''
try:
    client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
except socket.timeout:
    sys.stdout.write('Unable to connect\n')
    sys.stdout.flush()
    sys.exit(1)    
    
'''Make connection address'''
ip = socket.gethostbyname('localhost')
port = 1234
socket_address = (ip ,port)
    
'''Connect to the server'''
client_socket.connect(socket_address)

#'''Check for connection stauts and tell user'''
tell_connection_status(client_socket)
sock_list = [sys.stdin,client_socket]
sock_list_out = []

def client():
    artist= ""
    counter = 0
    while True:
        
        '''Start time'''
        start = 0
        
        read_sockets, write_sockets, error_sockets = select.select([],sock_list,[])
    
        for sock in write_sockets:
            
            '''if the sock is client socket'''
            if sock == client_socket:
                data = sock.recv(29) 
                
                '''what what data is'''
                if 'Recevied Message' in data:
                    sys.stdout.write('Server ' + data + '\n')
                    sys.stdout.flush()
                    
                    '''get artist validation message'''
                    data1 = sock.recv(5)

                    if 'true' in data1:
                        '''recv acutal message'''
                        data2 = sock.recv(1024)
                                                
                        '''stop the timer'''
                        end  = time.time() 
                        
                        '''log server reponse time'''
                        log_data('Server Response time,{}, seconds.'.format(end-start))
                                
                        songs_json = json.loads(data2.decode())
                        songs_list = songs_json.get('songs')
                        
                        '''log response length'''
                        log_data("Server response length for artist:{} is {}bytes.".format(artist,utf8len(songs_list)))
                        
                        '''log server response date and time'''
                        log_data("Response date and time from server for artist:{} is {}".format(artist ,datetime.now().strftime('%c')))
                        
                        '''Concatonate all the songs to a string'''
                        song_string = songs_toString(songs_list)
                        
                        '''Send the string to user'''
                        sys.stdout.write('Songs:' + song_string+'\n')
                        sys.stdout.flush()
                        
                        '''incidate new input and update counter (for asking to quit)'''
                        counter += 1
#                        prompt()
                        
                    elif 'false' in data1:
                        sys.stdout.write('There are no songs for this artist.\n')
                        sys.stdout.flush()
            else:                
                user_input = ""
                if counter > 0:
                    exit_status = raw_input("quit?>>")
                    if 'quit' in exit_status:
                        user_input  = 'quit'
                if 'quit' not in user_input:
                    user_input = raw_input("Enter artist>>")
                    counter += 1
                artist = ""
                artist += user_input 
                if len(user_input) == 0:
                    sys.stdout.write("Please enter an vaild artist.\n>>")
                    sys.stdout.flush()
#                    prompt()
                elif 'quit' in user_input:
                    sys.stdout.write('Processing request to close TCP connection.\n')
                    sys.stdout.flush()
                    
                    client_socket.send(user_input)
                    client_socket.close()
                    
                    sys.stdout.write('GoodBye!\n')
                    sys.stdout.flush()
                    sys.exit(0)
                else:
                    client_socket.send(user_input)
                    
                    '''Start a timer'''
                    start = time.time()
#                    prompt()
                    
client()
                
            
            

                    
                    
                    
                    
                
                
                
                
                
                
                
                
            
















        
        
        
        