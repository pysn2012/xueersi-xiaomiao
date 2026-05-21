import lcd_bus
from micropython import const
import machine
import lcd_utils

# 创建SPI总线对象
spi_bus = machine.SPI.Bus(
    host=1,
    mosi=23,
    miso=19,
    sck=18,    
)

# 创建显示屏的SPI通信对象
display_bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    freq=40000000,
    dc=4,
    cs=5
)


import st7735  # NOQA
import lvgl as lv  # NOQA

# 创建显示屏对象
display = st7735.ST7735(
    data_bus=display_bus,
    display_width=128,
    display_height=160,
    color_space=lv.COLOR_FORMAT.RGB565,
    color_byte_order=st7735.BYTE_ORDER_RGB,
    rgb565_byte_swap=True,
)

import task_handler

# 初始化显示屏
display.init(2)

# 旋转显示
display.set_rotation(lv.DISPLAY_ROTATION._90)

# 创建一个任务处理器实例
th = task_handler.TaskHandler()
