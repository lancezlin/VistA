#---------------------------------------------------------------------------
# Copyright 2013 PwC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#---------------------------------------------------------------------------

## @class Actions
## VistA Actions (base class)

'''
Action class. Extends object.

Created on Apr 20, 2012
@author: pbradley
@copyright PwC
@license http://www.apache.org/licenses/LICENSE-2.0
'''

import time
import TestHelper

class Actions (object):
    ''' This class extends the object class with methods specific to actions performed
    through the VistA Roll and Scroll interface.'''
    def __init__(self, VistAconn, scheduling=None, user=None, code=None):
        self.sched = scheduling
        self.acode = user
        self.vcode = code
        self.VistA = VistAconn

    def signon (self):
        ''' This provides a signon via ^XUP or ^ZU depending on the value of acode'''
        print 'in Actions:', self.acode
        if self.acode is None:
            self.VistA.wait('');
            self.VistA.write('S DUZ=1 D ^XUP')
        else:
            self.VistA.wait('');
            self.VistA.write('D ^ZU')
            self.VistA.wait('ACCESS CODE:');
            self.VistA.write(self.acode)
            self.VistA.wait('VERIFY CODE:');
            self.VistA.write(self.vcode)
            self.VistA.wait('//');
            self.VistA.write('')

    def signoff (self):
        '''Signoff and halt'''
        if self.acode is None:
            self.VistA.write('^\r^\r^\rh\r')
        else:
            self.VistA.write('^\r^\r^\r\r\r\r')

    def logflow(self, rlist):
        ''' This method call XTFCR to create flow diagrams of routines'''
        self.VistA.write('S DUZ=1 D ^XUP')
        self.VistA.wait('OPTION NAME')
        self.VistA.write('')
        self.VistA.write('D ^XTFCR')
        rval = self.VistA.multiwait(['All Routines', 'Routine:'])
        if rval == 0:
            self.VistA.write('No')
            for ritem in rlist:
                self.VistA.wait('Routine:')
                self.VistA.write(ritem)
        elif rval == 1:
            self.VistA.write('?')
            for ritem in rlist:
                self.VistA.wait('Routine:')
                self.VistA.write(ritem)
        self.VistA.wait('Routine:')
        self.VistA.write('')
        self.VistA.wait('DEVICE')
        self.VistA.write('')
        if self.VistA.type == 'cache':
            self.VistA.wait('Right Margin')
            self.VistA.write('')
        while True:
            rval = self.VistA.multiwait(['to halt...', self.VistA.prompt])
            if rval == 0:
                self.VistA.write('')
            elif rval == 1:
                break
            elif rval[0] == -1:
                break
            else:
                print "HOW DID I GET HERE: " + str(rval)
