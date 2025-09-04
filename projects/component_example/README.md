# Component Example Project

This is a network component example project that demonstrates how to use various network components and protocol stacks in the SDK.

## Features

* TCP/IP network communication
* MQTT message transmission
* HTTP client
* Network configuration management

## Quick Start

### Hardware Requirements

* One development board
* Ethernet connection
* Wi-Fi module (optional)
* Network debugging tools

### Build Steps

1. Configure network parameters
2. Set the server address
3. Compile the project
4. Download and run

### Running Result

The program will connect to the network, establish various network connections, and perform data transmission tests.

## Code Structure

```
component_example/
├── src/
│   ├── main.c              # Main program
│   ├── tcp_client.c        # TCP client
│   ├── mqtt_client.c       # MQTT client
│   ├── http_client.c       # HTTP client
│   └── network_config.c    # Network configuration
├── inc/
│   ├── tcp_client.h
│   ├── mqtt_client.h
│   ├── http_client.h
│   └── network_config.h
└── README.md
```

## Network Components

### TCP Client

```c
// Create a TCP connection
tcp_connect("192.168.1.100", 8080);

// Send data
tcp_send("Hello Server\n");

// Receive data
char buffer[1024];
int len = tcp_receive(buffer, sizeof(buffer));
```

### MQTT Client

```c
// Connect to MQTT server
mqtt_connect("mqtt.example.com", 1883);

// Subscribe to a topic
mqtt_subscribe("sensor/data");

// Publish a message
mqtt_publish("device/status", "online");

// Receive messages
void mqtt_message_callback(const char* topic, const char* message) {
    printf("Message received: %s -> %s\n", topic, message);
}
```

### HTTP Client

```c
// Send GET request
http_get("http://api.example.com/data");

// Send POST request
http_post("http://api.example.com/upload", "{\"data\":\"value\"}");

// Handle response
void http_response_callback(int status, const char* body) {
    printf("HTTP Status: %d\n", status);
    printf("Response Body: %s\n", body);
}
```

### Network Configuration

```c
// Configure IP address
network_set_ip("192.168.1.100");

// Configure gateway
network_set_gateway("192.168.1.1");

// Configure DNS
network_set_dns("8.8.8.8");

// Start network
network_start();
```

## Network Protocols

### Supported Protocols

* **TCP/UDP** – Transport layer protocols
* **HTTP/HTTPS** – Application layer protocols
* **MQTT** – Message queue protocol
* **CoAP** – Constrained Application Protocol
* **WebSocket** – Real-time communication protocol

### Security Features

* TLS/SSL encryption
* Certificate validation
* Authentication
* Data integrity

## Notes

* Ensure the network connection is stable
* Check the server address and port
* Verify network configuration parameters
* Monitor network status indicators

## Troubleshooting

Common network issues and solutions:

1. **Unable to connect to the network** – Check IP configuration and gateway
2. **TCP connection failed** – Verify server address and port
3. **MQTT connection timeout** – Check network latency and firewall
4. **HTTP request failed** – Validate URL format and server status