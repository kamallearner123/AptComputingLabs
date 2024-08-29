// // tcp server which listens on port 8080 and accepts incoming connections and crate a new thread for each connection and reply with "Hello from server" to all clients
// // use c++ 11 thread library

// #include <iostream>
// #include <thread>
// #include <vector>
// #include <string>
// #include <cstring>
// #include <sys/socket.h>
// #include <netinet/in.h>
// #include <unistd.h>


// void handle_client(int client_socket) {
//     char buffer[256];
//     memset(buffer, 0, sizeof(buffer));
//     int read_size = read(client_socket, buffer, sizeof(buffer));
//     if (read_size < 0) {
//         std::cerr << "Error reading from socket\n";
//         return;
//     }
//     std::cout << "Received message from client: " << buffer << "\n";
//     std::string reply = "Hello from server";
//     int write_size = write(client_socket, reply.c_str(), reply.size());
//     if (write_size < 0) {
//         std::cerr << "Error writing to socket\n";
//         return;
//     }
//     close(client_socket);
// }


// // Function to handle incoming connections
// void handle_connections(int server_socket) {
//     while (true) {
//         struct sockaddr_in client_address;
//         socklen_t client_address_len = sizeof(client_address);
//         int client_socket = accept(server_socket, (struct sockaddr*)&client_address, &client_address_len);
//         if (client_socket < 0) {
//             std::cerr << "Error accepting connection\n";
//             continue;
//         }
//         std::thread client_thread(handle_client, client_socket);
//         client_thread.detach();
//     }
// }


// // Main function
// int main() {
//     int server_socket = socket(AF_INET, SOCK_STREAM, 0);
//     if (server_socket < 0) {
//         std::cerr << "Error creating socket\n";
//         return 1;
//     }

//     struct sockaddr_in server_address;
//     server_address.sin_family = AF_INET;
//     server_address.sin_addr.s_addr = INADDR_ANY;
//     server_address.sin_port = htons(8080);

//     if (bind(server_socket, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
//         std::cerr << "Error binding socket\n";
//         return 1;
//     }

//     if (listen(server_socket, 5) < 0) {
//         std::cerr << "Error listening on socket\n";
//         return 1;
//     }

//     std::thread connection_thread(handle_connections, server_socket);
//     connection_thread.join();

//     return 0;
// }

// Write C++ code to create TCP server on 8181 which listens and sends response back in html format
// use c++ 11 thread library
// each connection should be handled in different thread
// use the following html code as response
// "<html><body><h1>Hello from server</h1></body></html>"
// Maintain message count seperately for each client and send the message count in the response
// Maintain client count and send the client count in the response

#include <iostream>
#include <thread>
#include <vector>
#include <string>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <map>
#include <mutex>

std::map<int, int> message_count;
std::mutex message_count_mutex;
int client_count = 0;
std::mutex client_count_mutex;

// Function to handle client
void handle_client(int client_socket) {
    // Increment client count
    {
        std::lock_guard<std::mutex> lock(client_count_mutex);
        ++client_count;
    }

    // Get client id
    int client_id = client_count;

    // Initialize message count for this client
    {
        std::lock_guard<std::mutex> lock(message_count_mutex);
        message_count[client_id] = 0;
    }

    while (true) {
        char buffer[256];
        memset(buffer, 0, sizeof(buffer));
        // kernel waits for incoming message from client
        // when message is received, kernel sends ack packet to client
        int read_size = read(client_socket, buffer, sizeof(buffer));
        if (read_size < 0) {
            std::cerr << "Error reading from socket\n";
            break;
        }
        if (read_size == 0) {
            std::cout << "Client disconnected\n";
            break;
        }
        std::cout << "Received message from client " << client_id << ": " << buffer << "\n";

        // Increment message count for this client
        {
            std::lock_guard<std::mutex> lock(message_count_mutex);
            ++message_count[client_id];
        }

        std::string reply = "<html><body><h1>Hello from server</h1>";
        reply += "<p>Message count: " + std::to_string(message_count[client_id]) + "</p>";
        reply += "<p>Client count: " + std::to_string(client_count) + "</p>";
        reply += "</body></html>";
        int write_size = write(client_socket, reply.c_str(), reply.size());
        if (write_size < 0) {
            std::cerr << "Error writing to socket\n";
            break;
        }
    }

    // Decrement client count
    {
        std::lock_guard<std::mutex> lock(client_count_mutex);
        --client_count;
    }

    // Close socket
    close(client_socket);
}



// Function to handle incoming connections
void handle_connections(int server_socket) {
    while (true) {
        struct sockaddr_in client_address;
        socklen_t client_address_len = sizeof(client_address);
        // User is asking kernel to accept the incoming connection; until accept is blocked
        // kernel waits for incoming connection: tcp sync packet from client
        // kernel sends ack packet to client
        // client sends ack packet to server
        // kernel creates new socket descriptor for this connection
        int client_socket = accept(server_socket, (struct sockaddr*)&client_address, &client_address_len);
        if (client_socket < 0) {
            std::cerr << "Error accepting connection\n";
            continue;
        }
        std::thread client_thread(handle_client, client_socket);
        client_thread.detach();
    }
}


// Main function
int main() {
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    printf("server_socket: %d\n", server_socket); //3

    // 1) User is asking kernel to create socket descriptor: TCP: Connection oriented over IP



    if (server_socket < 0) {
        std::cerr << "Error creating socket\n";
        return 1;
    }

    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    // function to cover ip address in string to binary format  INADDR_ANY: 
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(8182);

    // 2) Binding the socket descriptor to the address and port
    // Asking kernel to start listening on the port 8181: over IP address INADDR_ANY
    if (bind(server_socket, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
        std::cerr << "Error binding socket\n";
        return 1;
    }

    // 3) Listen to the incoming connections, Max 5 connections can be queued: handled parallely
    if (listen(server_socket, 5) < 0) {
        std::cerr << "Error listening on socket\n";
        return 1;
    }

    std::thread connection_thread(handle_connections, server_socket);
    connection_thread.join();

    return 0;
}

// Compile the code using the following command:
// g++ -std=c++11 -pthread tcp_server_multi_task.cpp -o tcp_server_multi_task







