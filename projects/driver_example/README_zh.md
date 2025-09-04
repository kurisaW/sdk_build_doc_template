# 驱动示例项目

这是一个外设驱动示例项目，展示了如何使用SDK中的各种驱动接口。

## 功能特性

- UART通信驱动
- SPI接口使用
- I2C设备访问
- ADC数据采集

## 快速开始

### 硬件要求

- 开发板一块
- 串口转USB模块
- SPI/I2C外设模块
- 模拟信号源

### 编译步骤

1. 配置硬件接口
2. 修改驱动参数
3. 编译项目
4. 下载运行

### 运行结果

程序会初始化各种外设驱动，并通过串口输出测试结果。

## 代码结构

```
driver_example/
├── src/
│   ├── main.c          # 主程序
│   ├── uart_drv.c      # UART驱动
│   ├── spi_drv.c       # SPI驱动
│   ├── i2c_drv.c       # I2C驱动
│   └── adc_drv.c       # ADC驱动
├── inc/
│   ├── uart_drv.h
│   ├── spi_drv.h
│   ├── i2c_drv.h
│   └── adc_drv.h
└── README.md
```

## 驱动接口

### UART驱动

```c
// 初始化UART
uart_init(115200);

// 发送数据
uart_send("Hello World\n");

// 接收数据
char data = uart_receive();
```

### SPI驱动

```c
// 初始化SPI
spi_init(SPI_MODE0, 1000000);

// 发送数据
spi_send(0x55);

// 接收数据
uint8_t data = spi_receive();
```

### I2C驱动

```c
// 初始化I2C
i2c_init(100000);

// 写数据
i2c_write(0x50, 0x00, 0x55);

// 读数据
uint8_t data = i2c_read(0x50, 0x00);
```

### ADC驱动

```c
// 初始化ADC
adc_init(ADC_CH0);

// 读取数据
uint16_t value = adc_read(ADC_CH0);
```

## 注意事项

- 检查硬件连接
- 确认驱动参数
- 观察串口输出
- 验证数据正确性

## 故障排除

常见问题及解决方案：

1. **串口无输出** - 检查波特率设置
2. **SPI通信失败** - 确认时钟极性和相位
3. **I2C设备无响应** - 检查地址和时序
4. **ADC数据异常** - 验证参考电压 