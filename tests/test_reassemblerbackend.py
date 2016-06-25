
import os.path

import nose.tools

from patcherex.backends import ReassemblerBackend
from patcherex.patches import *
from patcherex.techniques import ShadowStack

bin_location = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../binaries-private'))

#
# Functionality tests
#

def run_functionality(filename):

    filepath = os.path.join(bin_location, filename)

    p = ReassemblerBackend(filepath, debugging=True)
    r = p.save(os.path.join('/', 'tmp', os.path.basename(filename)))

    if not r:
        print "Compiler says:"
        print p._compiler_stdout
        print p._compiler_stderr

    nose.tools.assert_true(r, 'Reassembler fails on binary %s' % filename)

def test_functionality():
    binaries = [
        os.path.join('cgc_trials', 'CADET_00003'),
        os.path.join('cgc_trials', 'CROMU_00070'),
        os.path.join('cgc_trials', 'CROMU_00071'),
        os.path.join('cgc_trials', 'EAGLE_00005'),
    ]

    for b in binaries:
        run_functionality(b)

#
# Patching tests
#

def run_shadowstack(filename):
    filepath = os.path.join(bin_location, filename)

    p = ReassemblerBackend(filepath, debugging=True)

    cp = ShadowStack(filepath, p)
    patches = cp.get_patches()

    p.apply_patches(patches)

    r = p.save(os.path.join('/', 'tmp', os.path.basename(filename)))

    if not r:
        print "Compiler says:"
        print p._compiler_stdout
        print p._compiler_stderr

    nose.tools.assert_true(r, 'Shadowstack patching with reassembler fails on binary %s' % filename)

def test_shadowstack():
    binaries = [
        os.path.join('cgc_trials', 'CADET_00003'),
        os.path.join('cgc_trials', 'CROMU_00070'),
        os.path.join('cgc_trials', 'CROMU_00071'),
        os.path.join('cgc_trials', 'EAGLE_00005'),
    ]

    for b in binaries:
        run_shadowstack(b)

if __name__ == "__main__":
    test_functionality()
    test_shadowstack()