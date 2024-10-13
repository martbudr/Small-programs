#include <sys/socket.h> // socket
#include <netinet/in.h> // sockaddr_in structure
#include <fcntl.h> // read and write
#include <cstdio>
#include <stdlib.h> // EXIT_FAILURE
#include <unistd.h>
#include <string>

#define CONNECTION_PORT 3500

int main(){
  char* message = "This is a message sent by the client";

  char receive_buffer[100];

  struct sockaddr_in server_address;
  int client_socket = socket(AF_INET, SOCK_STREAM, 0);
  if(client_socket < 0){
    perror("Socket creation failed");
    exit(EXIT_FAILURE);
  }

  server_address.sin_family = AF_INET;
  server_address.sin_addr.s_addr = INADDR_ANY; // binding to any local address
  server_address.sin_port = htons(CONNECTION_PORT); // specifying port to listen to
  server_address.sin_zero[8] = '\0';

  int status=0;
  status = connect(client_socket, (struct sockaddr*)&server_address, sizeof(server_address));
  if(status<0){
    perror("Couldn't connect with the server");
    exit(EXIT_FAILURE);
  }

  write(client_socket, message, strlen(message));

  read(client_socket, receive_buffer, 100);
  printf("Message from server: %s \n", receive_buffer);

  close(client_socket);
  return 0;
}