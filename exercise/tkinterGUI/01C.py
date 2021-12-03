
import serial
import time
import serial.tools.list_ports

class TkinterSerial:
    def __init__(self,serial_port, serial_bps, serial_timeout) -> None:

        self.serial_port = serial_port
        self.serial_bps = serial_bps
        self.serial_timeout = serial_timeout

    def get_serial(self):
        '''获取端口'''
        serial_com = []
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            return "找不到串口"
        else: 
            for i in plist: 
                serial_com.append(i[0])  
            return serial_com

    def write_serial(self,date="None"):
        ''' 发送数据'''
        serialFd = serial.Serial(self.serial_port, self.serial_bps, timeout=self.serial_timeout)
        serialFd.write(date.encode('utf8'))

        return serialFd.read()


# 以下是调试用的
if __name__=='__main__':
	# # F 上 , N 下
    flg=1
    ts  = TkinterSerial("COM5", 9600, 5)
    while(True):
        
        s= ts.write_serial(r"SET,MOT,009,01,N13000,53")
        time.sleep(13)
        print("向下转动次数:{flg}，回复指令：{name}".format(name=s,flg=flg))
        
        s= ts.write_serial(r"SET,MOT,009,01,F23000,53")
        time.sleep(24)
        print("向上转动次数:{flg}，回复指令：{name}".format(name=s,flg=flg))

        flg += 1

