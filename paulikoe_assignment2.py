import RPi.GPIO
import time

try:
    RPi.GPIO.cleanup()
except:
    pass
# Nastavení pinů pro rotační enkodér
clk = 27
dt = 17
sw = 22  # Předpokládám, že používáte 3-pinový rotační enkodér s tlačítkem

# Nastavení pinů pro RGB LED
red = 23 
green = 24
blue = 25

brn = RPi.GPIO.setmode(RPi.GPIO.BCM)


#Set up every channel as an input
RPi.GPIO.setup(clk, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
RPi.GPIO.setup(dt, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
RPi.GPIO.setup(sw, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

#Set up every channel as an output
RPi.GPIO.setup(red, RPi.GPIO.OUT)
RPi.GPIO.setup(green, RPi.GPIO.OUT)
RPi.GPIO.setup(blue, RPi.GPIO.OUT)

fr = 100
''' 
PWM je technika modulace signálu, která se používá k regulaci množství energie 
dodávané do zařízení, jako jsou motory, světla nebo ventilátory. 
PWM funguje tak, že cyklicky zapíná a vypíná výstupní signál 
s různými poměry zapnutí a vypnutí. 
'''
red_pwm = RPi.GPIO.PWM(red, fr)
green_pwm = RPi.GPIO.PWM(green, fr)
blue_pwm = RPi.GPIO.PWM(blue, fr)


barva = [0,0,0] #r,g,b
s = 0
h = RPi.GPIO.input(clk)

#Zapnutí ledky
red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)


'''
Funkce button_callback:
Tato funkce slouží k ovládání LED diody pomocí otáčení enkodéru.
Funkce je vytvořená jako callback. Pokud je pin dt ve vysokém
stavu, přičte se hodnota 10 do proměnné "barva". Pokud ne, naopak
se hodnota 10 odečte. 
'''
def button_callback(_):
    global barva
    time.sleep(0.001)
    h = RPi.GPIO.input(clk)
    if h:
        if RPi.GPIO.input(dt) == RPi.GPIO.HIGH: 
            time.sleep(0.001)
            barva[s]+=10
        else:
            barva[s]-=10
             
    
    barva[s] = min(barva[s],100)
    barva[s] = max(barva[s],0)
    print(barva[s])
    red_pwm.ChangeDutyCycle(barva[0])
    blue_pwm.ChangeDutyCycle(barva[2])
    green_pwm.ChangeDutyCycle(barva[1])
    return

'''
Funkce "GPIO.add_event_detect" slouží k detekci událostí na pinu GPIO. 
Navíc možňuje programu reagovat na různé události, jako jsou změny stavu na daném pinu
'''

RPi.GPIO.add_event_detect(clk,RPi.GPIO.FALLING, callback=button_callback, bouncetime=20)

'''
Funkce switch:
Tato funkce složí jako callback. Jakmile dojde k použití
tlačítka na enkodéru, bude se měnit proměnná "s" podle seznamu "d".
Tím bude docházet k ukládání hodnot +10 nebo -10 do proměnné
"barva" podle zvolené proměnné "s". A tím se bude měnit jas
zrovna vybrané barvy.
'''
def switch (_):
    global s
    d = [0,1,2]
    s = (s + 1) % len(d)
    print(s)

RPi.GPIO.add_event_detect(sw,RPi.GPIO.FALLING, callback=switch, bouncetime=20)    


while True: #Pro spuštění kódu