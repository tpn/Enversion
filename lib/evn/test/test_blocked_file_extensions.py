#===============================================================================
# Imports
#===============================================================================
import unittest

from evn.test import (
    ensure_blocked,
    expected_roots,

    TestRepo,
    EnversionTest,
)

from evn.path import (
    join_path,
    format_dir,
)

from evn.util import (
    chdir,
    bulk_chargen,
)

from evn.config import (
    get_or_create_config,
)

from evn.test.dot import (
    dot,
)

from evn.constants import (
    e, # Errors
)
#===============================================================================
# Globals
#===============================================================================
conf = get_or_create_config()

#===============================================================================
# Helpers
#===============================================================================
def suite():
    return unittest.defaultTestLoader.loadTestsFromTestCase(
        TestBlockedFileExtensions,
    )

#===============================================================================
# Test Classes
#===============================================================================
class TestBlockedFileExtensions(EnversionTest, unittest.TestCase):
    def test_01_conf_setting(self):
        repo = self.create_repo()
        conf = repo.conf
        pattern = '\.(dll|exe|jar)$'

        dot()
        conf.set_blocked_file_extensions_iregex(pattern)

        actual = conf.get('main', 'blocked-file-extensions-iregex')
        self.assertEqual(pattern, actual)

        svn = repo.svn

    def test_02_add_new(self):
        repo = self.create_repo()
        conf = repo.conf
        svn = repo.svn

        #evnadmin = repo.evnadmin
        #evnadmin.enable_remote_debug(repo.path, hook='pre-commit')

        dot()
        tree = {
            'test.dll': bulk_chargen(100),
        }
        repo.build(tree, prefix='trunk')

        error = e.BlockedFileExtension
        with chdir(repo.wc):
            dot()
            svn.add('trunk/test.dll')
            with ensure_blocked(self, error):
                svn.ci('trunk/test.dll', m='Adding test.dll...')

    def test_03_rename(self):
        repo = self.create_repo()
        conf = repo.conf
        svn = repo.svn

        dot()
        tree = {
            'test.txt': bulk_chargen(100),
        }
        repo.build(tree, prefix='trunk')

        with chdir(repo.wc):
            dot()
            svn.add('trunk/test.txt')
            dot()
            svn.ci('trunk/test.txt', m='Adding test.txt...')

        dot()
        error = e.BlockedFileExtension
        with chdir(repo.wc):
            svn.mv('trunk/test.txt', 'trunk/test.dll')
            dot()
            with ensure_blocked(self, error):
                svn.ci('trunk', m='Renaming test.txt to test.dll...')
                dot()

def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == '__main__':
    main()

# vim:set ts=8 sw=4 sts=4 tw=78 et:
