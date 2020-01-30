import sys

msg = sys.argv[1]

loops = 1
if len(sys.argv) > 2:
    loops = int(sys.argv[2])

# Encode
for _ in xrange(loops):
    msg = ' '.join("{:0>8}".format(bin(ord(c))[2:]) for c in msg)

print msg

# Decode
# for _ in xrange(loops):
#     msg = ''.join(chr(int(x, 2)) for x in msg.split(' '))
#     print msg
