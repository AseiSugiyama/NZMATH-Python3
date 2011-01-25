"""
plugins -- plug-in mechanism
"""
from sandbox.config import PLUGIN_MATH

# math plug-ins
MATHPLUGIN_CHOICE = ('mpmath', None)

if PLUGIN_MATH == MATHPLUGIN_CHOICE[0]:
    from sandbox.plugin.math._mpmath import *
else:
    from sandbox.plugin.math.default import *


__all__ = ['MATHMODULE', 'CMATHMODULE', 'FLOATTYPE', 'COMPLEXTYPE',
	   'CHECK_REAL_OR_COMPLEX',
	   'PRECISION_CHANGEABLE', 'SETPRECISION']
