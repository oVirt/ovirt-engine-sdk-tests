

def time(method):
    import time
    def measure(*args, **kwargs):

        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()

        print 'executed in %2.2f sec' % (te - ts)

        return result

    return measure
