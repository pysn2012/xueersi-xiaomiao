import time
from machine import SPI, Pin, ADC
from driver import st7735_buf
from easydisplay import EasyDisplay

# 初始化SPI
spi = SPI(2, baudrate=30000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))

# 初始化ST7735显示屏，设置参数如宽度、高度、SPI接口、cs、dc等
dp = st7735_buf.ST7735(width=160, height=128, spi=spi, cs=5, dc=4, res=19, rotate=1, bl=None, invert=False, rgb=False)

# 使用EasyDisplay简化显示操作，设置显示参数如颜色格式、字体文件、是否立即显示等
ed = EasyDisplay(dp, "RGB565", font="/font/text_lite_16px_2312.v3.bmf", show=True, color=0xFFFF, clear=True)

# 初始化ADC模块
Light = ADC(Pin(36))
# 设置ADC的增益，11dB为最高分辨率
Light.atten(ADC.ATTN_11DB)

while True:
    # 读取光线传感器的值
    light_v=Light.read()
    print(str(light_v))
    # 在LCD屏上显示光线强度
    ed.text('光线强度为：' + str(light_v), 0, 10)
    time.sleep(1)