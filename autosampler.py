import serial
import argparse
import logging

class Autosampler:
	def __init__(self,comport):
		self.serialcon = serial.Serial(comport,timeout=2)
		self.check()

	def advance(self):
		self.serialcon.write('2')
		resp = self.serialcon.read(7)
		
		if not resp.startswith('moved'):
			logging.error('Autosampler: unexpected response after advance')
		else:
			logging.info('Autosampler: advanced')

	def valve(self,state):
		if state:
			self.serialcon.write('1')
			expect = 'on'
		else:
			self.serialcon.write('0')
			expect = 'off'

		resp = self.serialcon.read(len(expect)+2)
		if not resp.startswith(expect):
			logging.error('Autosampler: unexpected response after valve %s command',expect)
		else:
			logging.info('Autosampler: valve %s',expect)


	def check(self):
		self.serialcon.write('?')
		expect = 'ready'
		resp = self.serialcon.read(len(expect)+2)
		
		if not resp.startswith(expect):
			logging.critical('Autosampler: status check failed')
		else:
			logging.info('Autosampler: status check passed')

# Command line options
# Run with -h flag to see help

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line interface to control TWP\'s Arduino autosampler')
    parser.add_argument('port',help='serial port')
    parser.add_argument('-a',dest='advance',help='advance position',action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-on',action='store_true',help='valve on')
    group.add_argument('-off',action="store_true",help='valve off')
    args = parser.parse_args()

    auto = Autosampler(args.port)

    if args.advance:
        auto.advance()

    if args.on:
        auto.valve(True)
    elif args.off:
        auto.valve(False)