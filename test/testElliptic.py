import unittest
import elliptic
import rational

class EllipticTest(unittest.TestCase):
    def testInit(self):
        a = elliptic.EC([0,-1,1,0,0], 0)
        assert a.c4 == 16
        assert a.c6 == -152
        assert a.disc == -11
        assert a.j == rational.Rational(a.c4**3, a.disc)

        b = elliptic.EC([1,0], 0)
        assert b.c4 == -48
        assert b.c6 == 0
        assert b.disc == -64
        assert b.j == rational.Rational(b.c4**3, b.disc)

def suite():
    suite = unittest.makeSuite(EllipticTest, 'test') 
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
