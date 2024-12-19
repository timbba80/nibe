#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Copyright 2013 KNX-User-Forum e.V.           http://knx-user-forum.de/
#########################################################################
#  NIBE plugin for SmartHome.py.          https://github.com/smarthomeNG/
#
#  This plugin is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This plugin is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this plugin. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import logging
from lib.model.smartplugin import SmartPlugin
import serial
import re
import time
import termios
from struct import *

logger = logging.getLogger('NIBE')

class NIBE(SmartPlugin):

    ALLOW_MULTIINSTANCE = False
    PLUGIN_VERSION = "1.2.1"

    def __init__(self, smarthome, serialport):
        self._sh = smarthome
        self._nibe_regs = {}
        self._serial = serial.Serial(serialport, 19200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout=3)
        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = termios.tcgetattr(self._serial)
        CMSPAR = 0x40000000
        cflag |= termios.PARENB | CMSPAR | termios.PARODD # to select MARK parity
        termios.tcsetattr(self._serial, termios.TCSANOW, [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])

    def run(self):
        self.alive = True
        try:
            while self.alive:
                #time.sleep(0.0005)
                if self._serial.read(1)[0] != 0x03:
                    continue
                ret = self._serial.read(2)
                if ret[0] != 0x00 or ret[1] != 0x14:
                    continue

                self._serial.write(b"\x06")

                frm = bytes()
                frm += self._serial.read(4) #<C0> <00> <59> <len>
                if frm[0] == 0x03:
                    continue

                l = int(frm[3])
                frm += self._serial.read(l+1)

                self._serial.write(b"\x06")

                crc = 0
                for i in frm[:-1]:
                    crc ^= i
                if crc != frm[-1]:
                    logger.warning("frame crc error")
                    continue

                msg = frm[4:-1]
                l = len(msg)
                i = 4
                while i <= l:
                    reg = msg[i-3]
                    if i != l and (msg[i] == 0x00 or i == (l-1)):
                        raw = bytes([msg[i-2],msg[i-1]])
                        i+=4
                    else:
                        raw = bytes([msg[i-2]])
                        i+=3

                    if not reg in self._nibe_regs:
                        continue
                    if self._nibe_regs[reg]['raw'] == raw:
                        continue

                    value = self._decode(reg, raw)
                    logger.debug("update_item: reg:{0} = {1}".format(reg,value))
                    self._nibe_regs[reg]['raw'] = raw
                    for item in self._nibe_regs[reg]['items']:
                        item(value, 'NIBE', 'REG {}'.format(reg))

        except Exception as e:
            logger.warning("nibe: {0}".format(e))

    def stop(self):
        self.alive = False
        self._serial.close()

    def parse_item(self, item):
        if 'nibe_reg' in item.conf:
            logger.debug("parse item: {0}".format(item))
            nibe_reg = int(item.conf['nibe_reg'])
            if not nibe_reg in self._nibe_regs:
                self._nibe_regs[nibe_reg] = {'items': [item], 'logics': [], 'raw':0}
            else:
                self._nibe_regs[nibe_reg]['items'].append(item)
        return None

    def _decode(self, reg, raw):
        if len(raw) == 2:
            value = unpack('>H',raw)[0]
        else:
            value = unpack('B',raw)[0]

        if reg in [0,32,33,34,35,36,38,44,45,46,48,100,101,102,103,104,105]:
            #0    CPUID
            #32   Zusatzheizung erlaubt
            #33   Max dF Commpressor
            #34   Verd. Freq. regP
            #35   Min Startzeit Freq min
            #36   Minzeit konst. Freq min
            #38   Verd. Freq. GradMin
            #44   Pumpengeschwindigkeit %
            #45   Bw reg P
            #46   Bw reg Q
            #48   Bw reg Wert xP %
            #100  Datum - Jahr
            #101  Datum - Monat
            #102  Datum - Tag
            #103  Uhrzeit - Stunde
            #104  Uhrzeit - Minute
            #105  Uhrzeit - Sekunden
            return int(value)

        if reg == 31:
            #31   Status Heizung
            #1 Auto
            #3 Heizung
            #5 Brauchwasser
            #6 Zusatzheizung
            return int(value)

        if reg in [4,8]: #signed
            #4    Heizkurvenverschiebung
            #8    Gradminuten
            return int(unpack('h',pack('H',value))[0]/10)

        if reg == 25: #unsigned
            #25   Verdichterstarts
            return int(value/10)

        if reg in [1,5,6,7,11,12,13,14,15,16,17,18,21,23,27,37]: #signed
            #1    Aussentemp �C
            #5    Vorlauf Soll �C
            #6    Vorlauf Ist �C
            #7    Ruecklauf �C
            #11   Kondensator aus (MAX) �C
            #12   Brauchwasser oben �C
            #13   Brauchwasser unten �C
            #14   Verd. Temp. Tho-R1 �C
            #15   Verd. Temp. Tho-R2 �C
            #16   Sauggas Temp. Tho-S �C
            #17   Heissgas Temp. Tho-D �C
            #18   Fluessigkeitstemp AMS �C
            #21   Atemp. am AMS Tho-A �C
            #23   Invertertemp. Tho-IP �C
            #27   Vorlauf �C
            #37   Max Diff. soll-ber �C
            return float(unpack('h',pack('H',value))[0]/10)

        if reg in [9,10,19,20,22,24]: #unsigned
             #9    Verd. Freq. Soll Hz
            #10   Verd. Freq. Ist Hz
            #19   Hochdruck bar
            #20   Niederdruck bar
            #22   AMS Phase Ist A
            #24   Verdichterlaufzeit h
            return float(value/10)

        if reg in [40,47]: #unsigned
            #40   Hysterese �C
            #47   Bw reg xP
            return float(value/2)

        if reg in [43,49,50]:
            #43   Stopptemp. Heizen �C
            #49   Brauchwasser StartTemp �C 1.2
            #50   Brauchwasser StopTemp �C  1.3
            return float(value)

            #2    ?
            #3    ?
            #26   ?
            #28   ?
            #29   ?
            #30   ?
            #39   ?
            #41   ?
            #42   ?
        return value
