from __future__ import absolute_import

print "================mod==========================="
print "mod:__package__:", __package__
print "mod:__name__:", __name__

import string
#print dir(string)
print "Absolute String.file:", string.__file__

from .. pythonpath import bamboo
from . import string
#print dir(string)
print "String.file:", string.__file__
print "===============mod end====================="
