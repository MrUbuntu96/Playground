import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns


def plot_pdf():
    # generate the skew normal PDF for reference:

    def skew_norm_pdf(x, e=0, w=1, a=0):
        # adapated from:
        # http://stackoverflow.com/questions/5884768/skew-normal-distribution-in-scipy
        t = (x-e) / w
        return 2.0 * w * stats.norm.pdf(t) * stats.norm.cdf(a*t)

    location = 0.0
    scale = 1.0
    x = np.linspace(-5,5,100)

    plt.subplots(figsize=(12,4))
    SKEW_PARAMS = [(4.0, 2.0, -50.0), (0.0, 1.0, 0.0), (-1.0, 0.5, 30.0)]
    for p in SKEW_PARAMS:
        dist = skew_norm_pdf(x, e=p[0], w=p[1], a=p[2])
        # n.b. note that alpha is a parameter that controls skew, but the 'skewness'
        # as measured will be different. see the wikipedia page:
        # https://en.wikipedia.org/wiki/Skew_normal_distribution
        plt.plot(x,dist)


def generate_distribution():
    '''
        alpha: skewness. alpha > 0 => right skewness otherwise left
        loc  : shift of the distribution
        scale: the larger the scale, the more spread out the distribution
    '''
    def randn_skew_fast(N, alpha=0.0, loc=0.0, scale=1.0):
        sigma = alpha / np.sqrt(1.0 + alpha**2)
        u0 = np.random.randn(N)
        v  = np.random.randn(N)
        u1 = (sigma*u0 + np.sqrt(1.0 - sigma**2)*v) * scale
        u1[u0 < 0] *= -1
        u1 = u1 + loc
        return u1

    # lets check again
    #plt.subplots(figsize=(18,6))
    NUM_SAMPLES = 100000
    print "NUM_SAMPLES=%d" % NUM_SAMPLES
    #SKEW_PARAMS = [(0.0, 0.0, 1.0), (2.0, 0.0, 4.0), (8.0, 0.0, 8.0), (16.0, 0.0, 16.0)]
    SKEW_PARAMS = [(0.0, 0.0, 0.1), (0.0, 0.0, 1.0)]

    # mu, sigma2
    def histo_normal_dist(mu, sigma, mn, mx):
        return np.histogram(mu + sigma * np.random.standard_normal(NUM_SAMPLES),
                         bins=users, range=(mn, mx))[0]

    mn, mx = -50, 50
    users = 100
    hist = []
    i = 0
    for s in [(-40.0, 1.0), (38.0, 3.0), (0.0, 10.0)]:
        hist.append( histo_normal_dist(s[0], s[1], mn, mx))
        print hist[i]
        i += 1
        print

    #print (hist[2] + hist[3] + np.random.randint(10, size=users))


'''
for p in SKEW_PARAMS:
    samples = randn_skew_fast(NUM_SAMPLES, alpha=p[0], loc=p[1], scale=p[2])
    hist.append(np.histogram(samples, bins=users, range=(mn, mx))[0])
    print 'scale=%f' % p[2]
    print 'max=%f, min=%f' % (max(samples), min(samples))
    print hist[i]
    i += 1
    #print bins
    print

        #sns.distplot(s)

        #print s
        #mn, mx = max(s), min(s)
        bucket = (mx - mn) / users
        print 'bucket=%f' % bucket
        interactions.append([0] * users)
        for m in samples:
            j = int((m - mn) / bucket) - 1
            interactions[i][j] += 1
        print [m + 4 for m in interactions[i]]
        print 'sum=%d' % sum(interactions[i])
        i += 1
        print

    print "combined 1 + 2"
    print interactions[1]
    print interactions[2]
    #combined = [sum(x) for x in zip(interactions[1], interactions[2])]
    #print combined
    #print [m + 4 for m in combined]
'''
#------------
# main
#------------
if __name__ == '__main__':
    generate_distribution()
    #plt.show()


'''print p
    c = [int(round(m*100000)) for m in p]
    print c
    print



c = ['%d: %s' % (m, '*' * int(round(f * l.count(m)))) for m in xrange(min(l)-1, max(l)+2)]

for i in xrange(len(c)):
    if '*' in c[i]:
        print c[i]

print
'''
