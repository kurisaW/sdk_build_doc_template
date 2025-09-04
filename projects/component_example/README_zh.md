# 组件示例项目

这是一个网络组件示例项目，展示了如何使用SDK中的各种网络组件和协议栈。

## 功能特性

- TCP/IP网络通信
- MQTT消息传输
- HTTP客户端
- 网络配置管理

## 快速开始

### 硬件要求

- 开发板一块
- 以太网连接
- WiFi模块（可选）
- 网络调试工具

### 编译步骤

1. 配置网络参数
2. 设置服务器地址
3. 编译项目
4. 下载运行

### 运行结果

程序会连接到网络，建立各种网络连接，并进行数据传输测试。

## 代码结构

```
component_example/
├── src/
│   ├── main.c              # 主程序
│   ├── tcp_client.c        # TCP客户端
│   ├── mqtt_client.c       # MQTT客户端
│   ├── http_client.c       # HTTP客户端
│   └── network_config.c    # 网络配置
├── inc/
│   ├── tcp_client.h
│   ├── mqtt_client.h
│   ├── http_client.h
│   └── network_config.h
└── README.md
```

## 网络组件

### TCP客户端

```c
// 创建TCP连接
tcp_connect("192.168.1.100", 8080);

// 发送数据
tcp_send("Hello Server\n");

// 接收数据
char buffer[1024];
int len = tcp_receive(buffer, sizeof(buffer));
```

### MQTT客户端

```c
// 连接MQTT服务器
mqtt_connect("mqtt.example.com", 1883);

// 订阅主题
mqtt_subscribe("sensor/data");

// 发布消息
mqtt_publish("device/status", "online");

// 接收消息
void mqtt_message_callback(const char* topic, const char* message) {
    printf("收到消息: %s -> %s\n", topic, message);
}
```

### HTTP客户端

```c
// 发送GET请求
http_get("http://api.example.com/data");

// 发送POST请求
http_post("http://api.example.com/upload", "{\"data\":\"value\"}");

// 处理响应
void http_response_callback(int status, const char* body) {
    printf("HTTP状态: %d\n", status);
    printf("响应内容: %s\n", body);
}
```

### 网络配置

```c
// 配置IP地址
network_set_ip("192.168.1.100");

// 配置网关
network_set_gateway("192.168.1.1");

// 配置DNS
network_set_dns("8.8.8.8");

// 启动网络
network_start();
```

## 网络协议

### 支持协议

- **TCP/UDP** - 传输层协议
- **HTTP/HTTPS** - 应用层协议
- **MQTT** - 消息队列协议
- **CoAP** - 受限应用协议
- **WebSocket** - 实时通信协议

### 安全特性

- TLS/SSL加密
- 证书验证
- 身份认证
- 数据完整性

## 注意事项

- 确保网络连接正常
- 检查服务器地址和端口
- 验证网络配置参数
- 观察网络状态指示

## 故障排除

常见网络问题及解决方案：

1. **无法连接网络** - 检查IP配置和网关
2. **TCP连接失败** - 确认服务器地址和端口
3. **MQTT连接超时** - 检查网络延迟和防火墙
4. **HTTP请求失败** - 验证URL格式和服务器状态 