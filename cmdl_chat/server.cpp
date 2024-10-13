#include <sys/socket.h>
#include <netinet/in.h>
#include <fcntl.h>
#include <cstdio>
#include <stdlib.h> // macros such as EXIT_FAILURE
#include <unistd.h>
#include <string>

#define CONNECTION_PORT 3500

void init_server_address(struct sockaddr_in& server_address){
  server_address.sin_family = AF_INET;
  server_address.sin_addr.s_addr = INADDR_ANY; // binding to any local address
  server_address.sin_port = htons(CONNECTION_PORT); // specifying port to listen to
  server_address.sin_zero[8] = '\0';
}

// create server socket
void create_server(int& server_socket){
  server_socket = socket(AF_INET, SOCK_STREAM, 0);
  if(server_socket < 0){
    perror("Socket creation failed");
    exit(EXIT_FAILURE);
  }
}

// set socket options - enable (or disable) reusing address
void enable_option(const int server_socket, const int option_value){
  int status = setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &option_value, sizeof(option_value));
  if(status < 0){
    perror("Couldn't set options");
    exit(EXIT_FAILURE);
  }
}

void bind_socket(const int server_socket, const struct sockaddr_in& server_address){
  int status = bind(server_socket, (struct sockaddr*)&server_address, sizeof(struct sockaddr));
  if(status < 0){
    perror("Couldn't bind socket");
    exit(EXIT_FAILURE);
  }
}

void listen(const int server_socket){
  int status = listen(server_socket, 4); // listening on port - 4 requests maximum
  if(status < 0){
    perror("Couldn't listen for connections");
    exit(EXIT_FAILURE);
  }
}

void accept_signals(const int server_socket, int& client_socket, const struct sockaddr_in& server_address){
  struct sockaddr_in connection_address;
  unsigned int length_of_address = sizeof(connection_address);
  client_socket = accept(server_socket, (struct sockaddr*)&server_address, &length_of_address);
  if(client_socket < 0){
    perror("Couldn't establish connection with client");
    exit(EXIT_FAILURE);
  }
}

int main(){
  int server_socket; // value of the file descriptor
  int client_socket;
  char storage_buffer[80];
  int option_value = 1;
  char* message = "This is a message from the server";
  
  struct sockaddr_in server_address;
  init_server_address(server_address);

  create_server(server_socket);
  enable_option(server_socket, option_value);
  bind_socket(server_socket, server_address);
  listen(server_socket);
  accept_signals(server_socket, client_socket, server_address);

  // getting data from connection
  read(client_socket, storage_buffer, 80);
  storage_buffer[80-1] = '\0'; // '\0' - null
  printf("Message from client: %s \n", storage_buffer);

  // sending message
  send(client_socket, message, strlen(message), 0);

  // closing created sockets
  close(server_socket);
  close(client_socket);
  return 0;
}