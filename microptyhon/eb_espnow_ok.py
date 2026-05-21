import network, espnow, time
from time import sleep_ms
from machine import SPI, Pin
from driver import st7735_buf
from easydisplay import EasyDisplay
from lib.easybutton import EasyButton

# 定义五个动作函数
def action_up():
    print("前进")
    ed.text("前进", 70, 50)
    e.send(peer1, "up", True)
    
def action_back():
    print("后退")
    ed.text("后退", 70, 50)
    e.send(peer1, "back", True)
    
def action_left():
    print("左转")
    ed.text("左转", 70, 50)
    e.send(peer1, "left", True)
    
def action_right():
    print("右转")
    ed.text("右转", 70, 50)
    e.send(peer1, "right", True)
    
def action_stop():
    print("待命")
    ed.text("待命", 70, 50)
    e.send(peer1, "stop", True)

# 创建EasyDisplay对象，初始化LCD屏幕
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))
dp = st7735_buf.ST7735(width=160, height=128, spi=spi, cs=5, dc=4, res=19, rotate=1, bl=None,
                       invert=False, rgb=True)
ed = EasyDisplay(display=dp, font="/font/text_lite_16px_2312.v3.bmf", show=True, color=0xFFFF, clear=True,
                 color_type="RGB565")

# 初始化ESPNow通信协议
sta = network.WLAN(network.STA_IF)    # 启用站点模式
sta.active(True)
sta.disconnect()        # 断开WIFI连接

e = espnow.ESPNow()     # 启动ESPNOW
e.active(True)
peer1 = b'\x80e\x99\xa0~\xfc'   # 接收器的mac地址
e.add_peer(peer1)               #如果有多个接收器就增加peer2...

print("Starting...")
ed.text("ESPNOW已就绪", 30, 50)# 在显示屏上显示就绪信息

# 初始化按键，设置GPIO引脚
k_u = EasyButton(Pin(2,Pin.IN, Pin.PULL_UP))
k_d = EasyButton(Pin(13,Pin.IN, Pin.PULL_UP))
k_l = EasyButton(Pin(27,Pin.IN, Pin.PULL_UP))
k_r = EasyButton(Pin(35,Pin.IN, Pin.PULL_UP))

def main():      
    # 设置各个按键按下时的动作
    k_u.down_func = action_up
    k_d.down_func = action_back
    k_l.down_func = action_left
    k_r.down_func = action_right
    # 设置各个按键释放时的动作，这里统一为停止动作
    k_u.up_func = action_stop
    k_d.up_func = action_stop
    k_l.up_func = action_stop
    k_r.up_func = action_stop
    

if __name__ == "__main__":
    main()
