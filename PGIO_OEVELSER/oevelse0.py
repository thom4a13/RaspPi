import pigpio
from time import sleep

LED_GPIO_PIN = 21
pi = pigpio.pi()
pi.set_PWM_range(LED_GPIO_PIN, 100)

level = 0
dir = 1

while True:
    pi.set_PWM_dutycycle(LED_GPIO_PIN, level)
    sleep(0.01)
    level += dir
    
    if level >= 99 or level <= 0:
        dir *= -1



