from machine import SPI, Pin, ADC
from driver import st7735_buf
from lib.easydisplay import EasyDisplay
from lib.easymenu import EasyMenu, MenuItem, BackItem, ValueItem, ToggleItem
from lib.easybutton import EasyButton
from lib.buzzer_lib import BUZZER, mario, jingle
import network, espnow, time

# 定义一个函数，用于获取光线传感器的值
def get_light():
    light_v = Light.read()
    return light_v

# 定义一个函数，用于蜂鸣器播放
def buzzer_play(song):
    buzzer.play(song, 150, 200)
    em.show()

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

def espnow_go():
    global espnow_initialized
    if not espnow_initialized:
        # 初始化ESPNow通信协议
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        sta.disconnect()

        global e
        global peer1
        e = espnow.ESPNow()
        e.active(True)
        peer1 = b'\x80e\x99\xa0~\xfc'   # 接收器的mac地址
        e.add_peer(peer1)

        print("Starting...")
        espnow_initialized = True

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
        
        k_a.down_func = lambda: None
        k_b.down_func = lambda: None

        # 显示遥控器状态
        ed.text("ESPNOW已就绪", 30, 50)

# 创建EasyDisplay对象，初始化LCD屏幕
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23))
dp = st7735_buf.ST7735(width=160, height=128, spi=spi, cs=5, dc=4, res=19, rotate=1, bl=None,
                       invert=False, rgb=True)
ed = EasyDisplay(display=dp, font="/font/text_lite_16px_2312.v3.bmf", show=True, color=0xFFFF, clear=True,
                 color_type="RGB565")

# 使用EasyButton库，初始化按键
k_u = EasyButton(Pin(2,Pin.IN, Pin.PULL_UP))
k_d = EasyButton(Pin(13,Pin.IN, Pin.PULL_UP))
k_l = EasyButton(Pin(27,Pin.IN, Pin.PULL_UP))
k_r = EasyButton(Pin(35,Pin.IN, Pin.PULL_UP))
k_a = EasyButton(Pin(34,Pin.IN, Pin.PULL_UP))
k_b = EasyButton(Pin(12,Pin.IN, Pin.PULL_UP))

# 初始化ADC，用于读取光线传感器的值
Light = ADC(Pin(36))
Light.atten(ADC.ATTN_11DB)

# 初始化蜂鸣器
buzzer = BUZZER(14)

# 全局变量，用于跟踪ESPNow是否已经初始化
espnow_initialized = False

# 定义父菜单，指定：标题，布局，选项间隔
menu = MenuItem(title=('ESP32掌机', 'c', 0), layout=[1, 6], spacing=[160, 16])

#创建子菜单项，添加到父菜单中
menu1 = MenuItem('ESPNOW遥控器')  # 设置菜单1的选项
menu1.add(ValueItem(name='启动遥控器', callback=espnow_go))

menu2 = MenuItem('光线传感器')  # 设置菜单2的选项
menu2.add(ValueItem(name='光线强度',  value=(get_light, 'r', 'c'), callback=get_light))

menu3 = MenuItem('蜂鸣器')  # 设置菜单5的选项
menu3.add(ValueItem(name='超级马里奥', callback=lambda: buzzer_play(mario)))
menu3.add(ValueItem(name='铃儿响叮当', callback=lambda: buzzer_play(jingle)))

menu.add(menu1)  # 将选项添加到菜单
menu.add(menu2)
menu.add(menu3)

# 添加一个说明项，用于按键提示
menu.add(ValueItem(('A：确认 B：返回', 'c', 'c'),skip=True))

#创建EasyMenu对象，将EasyDisplay和菜单项关联起来
em = EasyMenu(ed, menu)
em.show()

# 为按键设置按下时的回调函数
k_u.down_func = lambda: em.prev()
k_d.down_func = lambda: em.next()
k_l.down_func = None
k_r.down_func = None
k_a.down_func = lambda: em.click()
k_b.down_func = lambda: em.back()