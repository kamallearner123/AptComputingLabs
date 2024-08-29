// write program to connect tcp client and send message to server pver port 8181 and ip 127.0.0.1

#include <iostream>
#include <string>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

int main() {
    // Create a socket
    int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket == -1) {
        std::cerr << "Error creating socket\n";
        return -1;
    }

    // Server address
    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(8182);
    server_address.sin_addr.s_addr = inet_addr("127.0.01");

    // Connect to server
    // Kernel sends SYN packet to server
    // Server responds with SYN-ACK packet
    // client sends ACK packet to server
    if (connect(client_socket, (struct sockaddr*)&server_address, sizeof(server_address)) == -1) {
        std::cerr << "Error connecting to server\n";
        return -1;
    }

    // Send data to server
    std::string message = "Hello from client";
    // client sends message to server
    // waits for ACK from server for time out period
    if (send(client_socket, message.c_str(), message.size(), 0) == -1) {
        std::cerr << "Error sending message to server\n";
        return -1;
    }

    // Receive data from server
    char buffer[256];
    memset(buffer, 0, sizeof(buffer));
    // client waits for message from server
    // waits for time out period
    if (recv(client_socket, buffer, sizeof(buffer), 0) == -1) {
        std::cerr << "Error receiving message from server\n";
        return -1;
    }

    std::cout << "Received message from server: " << buffer << "\n";
    
    // Close the socket
    // client sends FIN packet to server
    // server sends ACK packet to client
    // server sends FIN packet to client
    // client sends ACK packet to server
    close(client_socket);

    return 0;
}
