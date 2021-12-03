import serial
import serial.tools.list_ports
import datetime
import threading
import time
import sys


class Communication:
    datalist = []

    # 初始化
    def __init__(self, com, bps, timeout):
        self.port = com
        self.bps = bps
        self.timeout = timeout
        self.exit_thread = 0
        global Ret
        try:
            # 打开串口，并得到串口对象
            self.main_engine = serial.Serial(self.port, self.bps, timeout=self.timeout)
            # 判断是否打开成功
            if (self.main_engine.is_open):
                Ret = True
                self.recth = threading.Thread(target=self.Recive_data, args=())
                self.recth.setDaemon(True)
                self.recth.start()

        except Exception as e:
            print("---异常---：", e)

    # 打印设备基本信息
    def Print_Name(self):
        print(self.main_engine.name)  # 设备名字
        print(self.main_engine.port)  # 读或者写端口
        print(self.main_engine.baudrate)  # 波特率
        print(self.main_engine.bytesize)  # 字节大小
        print(self.main_engine.parity)  # 校验位
        print(self.main_engine.stopbits)  # 停止位
        print(self.main_engine.timeout)  # 读超时设置
        print(self.main_engine.writeTimeout)  # 写超时
        print(self.main_engine.xonxoff)  # 软件流控
        print(self.main_engine.rtscts)  # 软件流控
        print(self.main_engine.dsrdtr)  # 硬件流控
        print(self.main_engine.interCharTimeout)  # 字符间隔超时

    # 打开串口
    def Open_Engine(self):
        self.main_engine.open()

    # 关闭串口
    def Close_Engine(self):
        self.main_engine.close()
        print(self.main_engine.is_open)  # 检验串口是否打开

    # 打印可用串口列表
    @staticmethod
    def Print_Used_Com():
        port_list = [c.device for c in serial.tools.list_ports.comports()]
        # port_list = list(serial.tools.list_ports.comports())
        print(port_list)

    # 接收指定大小的数据
    # 从串口读size个字节。如果指定超时，则可能在超时后返回较少的字节；如果没有指定超时，则会一直等到收完指定的字节数。
    def Read_Size(self, size):
        return self.main_engine.read(size=size)

    # 接收一行数据
    # 使用readline()时应该注意：打开串口时应该指定超时，否则如果串口没有收到新行，则会一直等待。
    # 如果没有超时，readline会报异常。
    def Read_Line(self):
        return self.main_engine.readline()

    # 发数据
    def Send_data(self, data):
        self.main_engine.write(data)
        data = data.hex()
        self.datalist += [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' SEND ' + str(data) + '\n']

    # 更多示例
    # self.main_engine.write(chr(0x06).encode("utf-8"))  # 十六制发送一个数据
    # print(self.main_engine.read().hex())  #  # 十六进制的读取读一个字节
    # print(self.main_engine.read())#读一个字节
    # print(self.main_engine.read(10).decode("gbk"))#读十个字节
    # print(self.main_engine.readline().decode("gbk"))#读一行
    # print(self.main_engine.readlines())#读取多行，返回列表，必须匹配超时（timeout)使用
    # print(self.main_engine.in_waiting)#获取输入缓冲区的剩余字节数
    # print(self.main_engine.out_waiting)#获取输出缓冲区的字节数
    # print(self.main_engine.readall())#读取全部字符。

    # 接收数据
    # 一个整型数据占两个字节
    # 一个字符占一个字节

    def Recive_data(self):
        # 循环接收数据，此为死循环，可用线程实现
        print("开始接收数据：")
        while True:
            time.sleep(0.01)
            try:
                # 一个字节一个字节的接收
                if self.main_engine.in_waiting:
                    # 整体接收
                    data = self.main_engine.read_all()  # 方式二print("接收ascii数据：", data)
                    data = data.hex()
                    self.datalist += [
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' REC ' + str(data) + '\n']
                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' REC:' + str(data) + '\n')
                    # print('a')
            except Exception as e:
                print("异常报错：", e)
                break


def test_data(com):
    testDatList1 = ['SET,MOT,009,01,N01000,00',
                    'SET,D01,006,01,N,00',
                    'SET,D02,006,01,N,00',
                    'SET,D03,006,01,N,00',
                    'SET,D04,006,01,N,00',
                    'SET,D05,006,01,N,00',
                    'SET,D06,006,01,N,00',
                    'SET,L09,021,01,0500000000000000,00',
                    'SET,L10,021,01,0500000000000000,00',
                    'SET,L11,021,01,0500000000000000,00',
                    'SET,L12,021,01,0500000000000000,00',
                    'SET,D08,006,01,F,00',
                    'SET,D01,006,01,F,00',
                    'SET,D02,006,01,F,00',
                    'SET,D03,006,01,F,00',
                    'SET,D04,006,01,F,00',
                    'SET,D05,006,01,F,00',
                    'SET,L09,021,01,0000010000000000,00',
                    'SET,L10,021,01,0000010000000000,00',
                    'SET,L11,021,01,0000010000000000,00',
                    'SET,L12,021,01,0000010000000000,00',
                    'SET,D08,006,01,N,00',
                    'SET,D06,006,01,F,00',
                    'SET,MOT,009,01,F01000,00',
                    'SET,BOOT,019,01,00600000000600,63',
                    ]
    testDatList2 = ['XHFYJ,0,3+2,3+5,AA,END',
                    ]
    testDatList = testDatList2
    for dat in testDatList:
        com.Send_data(dat.encode())
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' send:' + dat + '\n')
        time.sleep(1)
    # com.exit_thread = 1
    for t in com.datalist:
        print(t)
    for i in range(1, 30):
        time.sleep(60)
        print(str(i) + '分钟:\n')
    com.Close_Engine()


class mytest:
    testDatList3 = [{'hexstr': '53447345730000000621000101', 'tim': 3},
                    {'hexstr': '53447345730000000621000102', 'tim': 3},
                    {'hexstr': '53447345730000000621000103', 'tim': 3},
                    {'hexstr': '53447345730000000621000201', 'tim': 3},
                    {'hexstr': '53447345730000000621000202', 'tim': 3},
                    {'hexstr': '53447345730000000621000203', 'tim': 3},
                    {'hexstr': '53447345730000000621000301', 'tim': 3},
                    {'hexstr': '53447345730000000621000302', 'tim': 3},
                    {'hexstr': '53447345730000000621000303', 'tim': 3},
                    {'hexstr': '53447345730000000621000401', 'tim': 3},
                    {'hexstr': '53447345730000000621000402', 'tim': 3},
                    {'hexstr': '53447345730000000621000403', 'tim': 3},
                    {'hexstr': '53447345730000000621000501', 'tim': 3},
                    {'hexstr': '53447345730000000621000502', 'tim': 3},
                    {'hexstr': '53447345730000000621000503', 'tim': 3},
                    {'hexstr': '53447345730000000621000601', 'tim': 3},
                    {'hexstr': '53447345730000000621000602', 'tim': 3},
                    {'hexstr': '53447345730000000621000603', 'tim': 3},
                    ]
    testDatList1 = [{'hexstr': '53447345730000000621010001', 'tim': 3},
                    {'hexstr': '53447345730000000621010000', 'tim': 1},
                    {'hexstr': '53447345730000000621010101', 'tim': 3},
                    {'hexstr': '53447345730000000621010100', 'tim': 1},
                    {'hexstr': '53447345730000000621010201', 'tim': 3},
                    {'hexstr': '53447345730000000621010200', 'tim': 1},
                    {'hexstr': '53447345730000000621010301', 'tim': 3},
                    {'hexstr': '53447345730000000621010300', 'tim': 1},
                    {'hexstr': '53447345730000000621010401', 'tim': 3},
                    {'hexstr': '53447345730000000621010400', 'tim': 1},
                    {'hexstr': '53447345730000000621010501', 'tim': 3},
                    {'hexstr': '53447345730000000621010500', 'tim': 1},
                    {'hexstr': '53447345730000000621010601', 'tim': 3},
                    {'hexstr': '53447345730000000621010600', 'tim': 1},
                    {'hexstr': '53447345730000000621010701', 'tim': 3},
                    {'hexstr': '53447345730000000621010700', 'tim': 1},
                    {'hexstr': '53447345730000000621010801', 'tim': 3},
                    {'hexstr': '53447345730000000621010800', 'tim': 1},
                    {'hexstr': '53447345730000000621010901', 'tim': 3},
                    {'hexstr': '53447345730000000621010900', 'tim': 1},
                    {'hexstr': '53447345730000000621011001', 'tim': 3},
                    {'hexstr': '53447345730000000621011000', 'tim': 1},
                    {'hexstr': '53447345730000000621011101', 'tim': 3},
                    {'hexstr': '53447345730000000621011100', 'tim': 1},
                    {'hexstr': '53447345730000000621011201', 'tim': 3},
                    {'hexstr': '53447345730000000621011200', 'tim': 1},
                    {'hexstr': '53447345730000000621011301', 'tim': 3},
                    {'hexstr': '53447345730000000621011300', 'tim': 1},
                    {'hexstr': '53447345730000000621011401', 'tim': 3},
                    {'hexstr': '53447345730000000621011400', 'tim': 1},
                    {'hexstr': '53447345730000000621011501', 'tim': 3},
                    {'hexstr': '53447345730000000621011500', 'tim': 1},
                    {'hexstr': '53447345730000000621011601', 'tim': 3},
                    {'hexstr': '53447345730000000621011600', 'tim': 1},
                    {'hexstr': '53447345730000000621011701', 'tim': 3},
                    {'hexstr': '53447345730000000621011700', 'tim': 1},
                    {'hexstr': '53447345730000000621012001', 'tim': 3},
                    {'hexstr': '53447345730000000621012000', 'tim': 1},
                    {'hexstr': '53447345730000000621012101', 'tim': 3},
                    {'hexstr': '53447345730000000621012100', 'tim': 1},
                    {'hexstr': '53447345730000000621013000', 'tim': 1},
                    {'hexstr': '53447345730000000621013001', 'tim': 3},
                    {'hexstr': '53447345730000000621013002', 'tim': 3},
                    {'hexstr': '53447345730000000621013100', 'tim': 1},
                    {'hexstr': '53447345730000000621013101', 'tim': 3},
                    {'hexstr': '53447345730000000621013102', 'tim': 3},
                    ]

    def __init__(self, com):
        self.com = com

    def crc16one(self, dat):
        Crc16CCITT_Table = [
            0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
            0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef]
        outcrc = 0
        for d in dat[5:]:
            temp = ((outcrc >> 8) & 0xff) >> 4
            outcrc <<= 4
            outcrc &= 0xffff
            outcrc ^= Crc16CCITT_Table[temp ^ int(d / 16)]
            temp = ((outcrc >> 8) & 0xff) >> 4
            outcrc <<= 4
            outcrc &= 0xffff
            outcrc ^= Crc16CCITT_Table[(temp ^ d) & 0x0f]
        return outcrc & 0xffff

    def test_intput(self):
        print('s数字:发衣服 例如s 1 1')
        print('m数字:电机测试 例如m 1 0-17 发衣电机 20 21 出口电机 30 31步进电机')
        print('exit:退出')
        print('all:自动全测试')
        while 1:
            print('请输入:')
            s = sys.stdin.readline()[:-1]  # 去掉回车符
            if s == 'exit':
                print('aqsw')
                break
            elif s[0] == 's':
                s1 = s.split(' ')
                n = (int(s1[1]) - 1) * 3 + int(s1[2]) - 1
                testDatList = self.testDatList3
                if n < 18:
                    self.send_hex(testDatList[n]['hexstr'])
                else:
                    print('输入错误')
            elif s[0] == 'm':
                s1 = s.split(' ')
                n = int(s1[1])
                testDatList = self.testDatList1
                if 0 <= n < 18:
                    n = n * 2
                    self.send_hex(testDatList[n]['hexstr'])
                    time.sleep(testDatList[n]['tim'])
                    self.send_hex(testDatList[n + 1]['hexstr'])
                    time.sleep(testDatList[n + 1]['tim'])
                elif 20 <= n < 22:
                    n = (n - 20) * 2 + 36
                    self.send_hex(testDatList[n]['hexstr'])
                    time.sleep(testDatList[n]['tim'])
                    self.send_hex(testDatList[n + 1]['hexstr'])
                    time.sleep(testDatList[n + 1]['tim'])
                elif 30 <= n < 32:
                    n = (n - 30) * 3 + 40
                    self.send_hex(testDatList[n + 1]['hexstr'])
                    time.sleep(testDatList[n + 1]['tim'])
                    self.send_hex(testDatList[n]['hexstr'])
                    time.sleep(testDatList[n]['tim'])
                    self.send_hex(testDatList[n + 2]['hexstr'])
                    time.sleep(testDatList[n + 2]['tim'])
                    self.send_hex(testDatList[n]['hexstr'])
                    time.sleep(testDatList[n]['tim'])
                else:
                    print('输入错误')
            elif s == 'all':
                self.test_data_hex()

    def send_hex(self, dat):
        dat1 = bytes.fromhex(dat)
        dats = dat + "{:04X}".format(self.crc16one(dat1))
        dat2 = bytes.fromhex(dats)
        self.com.Send_data(dat2)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' send:' + dat2.hex() + '\n')

    def test_data_hex(self):
        testDatList = self.testDatList3 + self.testDatList1
        for dat in testDatList:
            self.send_hex(dat['hexstr'])
            time.sleep(dat['tim'])
        # com.exit_thread = 1
        for t in self.com.datalist:
            print(t)


if __name__ == '__main__':
    Communication.Print_Used_Com()

    Engine1 = Communication("com16", 115200, 0.5)
    # test_data(Engine1)
    # test_data_hex(Engine1)
    test1 = mytest(Engine1)
    test1.test_intput()
