import time
from grove.gpio import GPIO

usleep = lambda x: time.sleep(x / 1000000.0)


class UltrasonicRanger(object):
    def __init__(self, pin):
        self.dio =GPIO(pin)

    def get_distance(self):
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)

        self.dio.dir(GPIO.IN)

        t0 = time.time()
        count = 0
        while count < 1000:
            if self.dio.read():
                break
            count += 1
        
        t1 = time.time()

        count = 0
        while count < 10000:
            if not self.dio.read():
                break
            count += 1
        
        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 500:
            print('Warning: the distance from the ultrasonic ranger is not accurate')

        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm

        return distance


def main():
    sonar = UltrasonicRanger(32)

    for _ in range(100):
        print('{} cm'.format(sonar.get_distance()))
        time.sleep(1)


if __name__ == '__main__':
    main()


