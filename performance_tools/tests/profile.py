import unittest

class ProfileTestCase(unittest.TestCase):
    def test_basic(self):

        from performance_tools.profile import Profiler

        def fib(n):
            if n == 0:
                return 0
            elif n == 1:
                return 1
            else:
                return fib(n - 1) + fib(n - 2)
                  
        p = Profiler()
        p.profile(fib, (25,))
        
        stats = p.stats()

        self.assertEqual(len(stats), 1)
        self.assertEqual(len(stats[0]['calls']), 1)
        self.assertEqual(stats[0]['call_count'], 242785)
        self.assertEqual(stats[0]['recursive_call_count'], 242784)

if __name__ == '__main__':
    unittest.main()
