
from ups import Ups

def main():
    ups = Ups()
    ups.print_raspberry_info()
    ups.print_batteries_info()
#     ups.mcu()

if __name__ == '__main__':
   main()