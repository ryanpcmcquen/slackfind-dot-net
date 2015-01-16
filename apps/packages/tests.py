
from django import test

from packages.models import Package

class PackageTestCase(test.TestCase):

    def setUp(self):
        self.package = Package()

    def test_raw_name(self):

        self.package.raw_name = 'yakuake-2.8.1-i486-2as.txz'
        
        self.assertEqual(self.package.name, 'yakuake')
        self.assertEqual(self.package.version, '2.8.1')
        self.assertEqual(getattr(Package.archs, 'i486'), self.package.arch)
        self.assertEqual(self.package.build, '2as')
        self.assertEqual(self.package.extension, 'txz')


