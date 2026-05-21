import screen2
import time
import lvgl as lv
from machine import Pin, ADC, Timer

# 初始化屏幕
scrn = lv.screen_active()
scrn.set_style_bg_color(lv.color_hex(0x000000), 0)

class AnalogClock:
    def __init__(self, parent):
        self.scale = None
        self.second_hand = None
        self.minute_hand = None
        self.hour_hand = None
        # 获取当前时间
        now = time.localtime()
        self.hour = now[3] % 12  # 转换为12小时制
        self.minute = now[4]
        self.second = now[5]
        self.create_clock(parent)
        self.start_timer()

    def create_clock(self, parent):
        """创建模拟时钟组件"""
        # 创建表盘主体（保持120x120大小）
        self.scale = lv.scale(parent)
        self.scale.set_size(120, 120)
        self.scale.set_mode(lv.scale.MODE.ROUND_INNER)
        
        # 设置表盘样式
        self.scale.set_style_bg_opa(lv.OPA._60, 0)
        self.scale.set_style_bg_color(lv.color_hex(0x222222), 0)
        self.scale.set_style_radius(lv.RADIUS_CIRCLE, 0)
        self.scale.set_style_clip_corner(True, 0)
        self.scale.center()

        # 配置刻度系统
        self.scale.set_label_show(True)
        hour_labels = ["12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", None]
        self.scale.set_text_src(hour_labels)
        self.scale.set_style_text_font(lv.font_montserrat_12, 0)
        self.scale.set_total_tick_count(61)
        self.scale.set_major_tick_every(5)

        # 主刻度样式
        style_indicator = lv.style_t()
        style_indicator.init()
        style_indicator.set_text_color(lv.color_hex(0xFFFFFF))
        style_indicator.set_line_color(lv.color_hex(0xFFFFFF))
        style_indicator.set_length(3)
        style_indicator.set_line_width(2)
        self.scale.add_style(style_indicator, lv.PART.INDICATOR)

        # 次刻度样式
        style_minor = lv.style_t()
        style_minor.init()
        style_minor.set_line_color(lv.color_hex(0xAAAAAA))
        style_minor.set_length(2)
        style_minor.set_line_width(1)
        self.scale.add_style(style_minor, lv.PART.ITEMS)

        # 表盘边框样式
        style_main = lv.style_t()
        style_main.init()
        style_main.set_arc_color(lv.color_hex(0x222222))
        style_main.set_arc_width(2)
        self.scale.add_style(style_main, lv.PART.MAIN)

        # 设置量程和角度（保持不变）
        self.scale.set_range(0, 60)
        self.scale.set_angle_range(360)
        self.scale.set_rotation(270)

        # 创建秒针（白色，长度45px，细线）
        self.second_hand = lv.line(self.scale)
        self.second_hand.set_style_line_width(1, 0)  # 更细的线宽
        self.second_hand.set_style_line_rounded(True, 0)
        self.second_hand.set_style_line_color(lv.color_hex(0xFFFFFF), 0)

        # 创建分钟指针（橙色，长度40px）
        self.minute_hand = lv.line(self.scale)
        self.minute_hand.set_style_line_width(2, 0)
        self.minute_hand.set_style_line_rounded(True, 0)
        self.minute_hand.set_style_line_color(lv.color_hex(0xFFA500), 0)

        # 创建小时指针（红色，长度30px）
        self.hour_hand = lv.line(self.scale)
        self.hour_hand.set_style_line_width(3, 0)
        self.hour_hand.set_style_line_rounded(True, 0)
        self.hour_hand.set_style_line_color(lv.color_hex(0xFF0000), 0)

        # 添加中心点
        center = lv.obj(self.scale)
        center.set_size(8, 8)  # 稍微减小中心点大小
        center.center()
        center.set_style_radius(lv.RADIUS_CIRCLE, 0)
        center.set_style_bg_color(lv.color_hex(0xFFD700), 0)
        center.set_style_bg_opa(lv.OPA.COVER, 0)

        self.update_hands()

    def update_hands(self):
        """更新所有指针位置"""
        # 秒针（45px长度）
        lv.scale.set_line_needle_value(self.scale, self.second_hand, 50, self.second)
        
        # 分钟指针（40px长度）
        lv.scale.set_line_needle_value(self.scale, self.minute_hand, 40, self.minute)
        
        # 小时指针（30px长度），考虑分钟偏移
        hour_value = self.hour * 5 + (self.minute // 12)
        lv.scale.set_line_needle_value(self.scale, self.hour_hand, 30, hour_value)

    def timer_callback(self, timer):
        """定时器回调(每秒更新)"""
        # 获取当前时间
        now = time.localtime()
        self.hour = now[3] % 12
        self.minute = now[4]
        self.second = now[5]
        
        self.update_hands()

    def start_timer(self):
        """启动硬件定时器(每秒触发)"""
        self.timer = Timer(-1)
        self.timer.init(period=1000, mode=Timer.PERIODIC, callback=self.timer_callback)

# 创建时钟实例
clock = AnalogClock(scrn)

# 主循环
while True:
    lv.timer_handler()
    time.sleep_ms(5)