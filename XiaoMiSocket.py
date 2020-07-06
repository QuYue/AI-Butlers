import miio
import time
from miio.chuangmi_plug import ChuangmiPlug
# ip = '192.168.101.9'
# token = '8983016090f11f88ad81eecb82f4f20b'
# s = miio.device.Device(ip=ip, token=token)
# s.info()


class Maid1_Commander():
    def __init__(self):
        self.ip = '192.168.1.100'
        # self.token = '8983016090f11f88ad81eecb82f4f20b'
        # self.token = 'dab1a009edfcbcae231bfdcb57a6fdba'
        self.token = '6dbb62c0bcffe22f914b3a7c38c7744d'
        self.maid = ChuangmiPlug(ip=self.ip, token=self.token)
        
    def command1(self): # 开门
        x1 = self.maid.off()
        time.sleep(2)
        x2 = self.maid.on()
        #print(f"Open the door:{x1},{x2}")
        return f"Open the door:{x1[0]},{x2[0]}"
    
    def command2(self):
        x = self.maid.status()
        #print(x)
        return x
    
    def command3(self):
        x = self.maid.on()
        #print(f"Turn on the power:{x}")
        return x
    
    def command4(self):
        x = self.maid.off()
        #print(f"Turn off the power:{x}")
        return x
    
if __name__ == '__main__':
    maid1_commander = Maid1_Commander()
    x = maid1_commander.command2()
    print(f"Power:{x.power} | USB_power:{x.usb_power} | Temperature:{x.temperature} | Load_power:{x.load_power} | Wifi_led:{x.wifi_led}")



