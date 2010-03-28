import sys, os

try:
	from fract4d import fract4dcgmp as fract4dc
except ImportError, err:
    from fract4d import fract4dc

# stub class for selecting a suitable readwrite method depending on platform, 
# to be used whenever a file desciptor returned from fract4dc.pipe() is used.

class gtkio:
	def read(self, fd, len):
		if 'win' in sys.platform:
			return fract4dc.read(fd, len)
		else:
			return os.read(fd, len)
