from random import gauss

def aa(l):
    print 'max=%0.3f, min=%0.3f, avg=%0.3f' % (max(l), min(l), sum(l)/len(l))
    print ['%0.3f' % m for m in l]

#aa([gauss(8,0.01) for i in xrange(50)])

print
print

avg = 50
std = 10
population = 100000
l = [int(round(gauss(avg, std))) for i in xrange(population)]
f = 45.0 / l.count(avg)

c = ['%d: %s' % (m, '*' * int(round(f * l.count(m)))) for m in xrange(min(l)-1, max(l)+2)]

for i in xrange(len(c)):
    if '*' in c[i]:
        print c[i]

print


# CSV writer
import csv
import sys

f = open(sys.argv[1], 'wt')
try:
    writer = csv.writer(f)
    writer.writerow( ('Title 1', 'Title 2', 'Title 3') )
    for i in range(10):
        writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )
finally:
    f.close()
