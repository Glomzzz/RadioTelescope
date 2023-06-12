from machine import Pin, ADC, SoftI2C
import time
import sys
import _thread
import ssd1306
from time import sleep_ms

x_a = Pin(4, Pin.OUT)
x_b = Pin(5, Pin.OUT)
x_c = Pin(6, Pin.OUT)
x_d = Pin(7, Pin.OUT)

delay_time_ms = 5
BH1750_I2C_ADD = 0x23

oled_width = 128
oled_height = 64

# 创建i2c对象
i2c = SoftI2C(scl=Pin(12), sda=Pin(11))
# 创建oled屏幕对象
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


def move_right():
    x_a.value(1)
    x_b.value(0)
    x_c.value(0)
    x_d.value(0)
    sleep_ms(delay_time_ms)

    x_a.value(0)
    x_b.value(1)
    x_c.value(0)
    x_d.value(0)
    sleep_ms(delay_time_ms)

    x_a.value(0)
    x_b.value(0)
    x_c.value(1)
    x_d.value(0)
    sleep_ms(delay_time_ms)

    x_a.value(0)
    x_b.value(0)
    x_c.value(0)
    x_d.value(1)
    sleep_ms(delay_time_ms)


def move_left():

    x_a.value(0)
    x_b.value(0)
    x_c.value(0)
    x_d.value(1)
    sleep_ms(delay_time_ms)

    x_a.value(0)
    x_b.value(0)
    x_c.value(1)
    x_d.value(0)
    sleep_ms(delay_time_ms)

    x_a.value(0)
    x_b.value(1)
    x_c.value(0)
    x_d.value(0)
    sleep_ms(delay_time_ms)

    x_a.value(1)
    x_b.value(0)
    x_c.value(0)
    x_d.value(0)
    sleep_ms(delay_time_ms)


BH1750_CMD_H_RESOLUTION = 0x10

i2c = SoftI2C(scl=Pin(14), sda=Pin(21), freq=100000)
buf = bytearray(1)
buf[0] = BH1750_CMD_H_RESOLUTION
i2c.writeto(BH1750_I2C_ADD, buf)
time.sleep_ms(200)

scan = i2c.scan()


# 宽度高度
# oled_width = 128
# oled_height = 64

x = 0
y = 0

plots = [(0, 0)]

previous = (0, 0)

min_light = 0
max_light = 600
delta = max_light - min_light
pre = delta / oled_height


def normalize(light):
    return int(64 - min(light / pre, 64))


def plot(light, oled):
    previous = plots[len(plots)-1]
    previous_x = previous[0]
    if previous_x >= 128:
        plots.clear()
        previous_x = 0
    x = previous_x + 1
    plots.append((x, normalize(light)))
    for point in plots:
        oled.pixel(point[0], point[1], 1)

    return


def light():
    buf = i2c.readfrom(BH1750_I2C_ADD, 0x2)
    data = buf[0] * 256 + buf[1]
    oled.fill(0)
    plot(data, oled)
    text = 'Light: ' + str(data)
    oled.text(text, 0, 0)
    oled.show()


ps2_y = ADC(Pin(1))
ps2_y.atten(ADC.ATTN_11DB)  # 这里配置测量量程为3.3V
# ps2_x = ADC(Pin(2))
# ps2_x.atten(ADC.ATTN_11DB)  # 这里配置测量量程为3.3V


def is_still(v):
    return 1800 <= v and v >= 2200


def up(v):
    return v < 1800


def down(v):
    return v > 2200


def read_mode():
    y = ps2_y.read()  # 0-4095
#     x = ps2_x.read()  # 0-4095
#     print(x, y)
#     mode_x = 0
#     if up(x):
#         mode_x = 1
#     elif down(x):
#         mode_x = -1
    mode_y = 0
    if up(y):
        mode_y = 1
    elif down(y):
        mode_y = -1
#     return (mode_x, mode_y)
    return mode_y


# thread_1 = _thread.start_new_thread(light, ())

time = 0

while True:
    time = time + 1
    mode = read_mode()
    if mode == 1:
        move_right()
    elif mode == -1:
        move_left()
    if time >= 100:
        time = 0
        light()
    sleep_ms(5)
    # move_x()
