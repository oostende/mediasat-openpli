from enigma import iServiceInformation, iPlayableService
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from Tools.Transponder import ConvertToHumanReadable
from Tools.GetEcmInfo import GetEcmInfo
from Poll import Poll

def addspace(text):
    if text:
        text += ' '
    return text


class RRExtraInfo(Poll, Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.type = type
        self.poll_interval = 1000
        self.poll_enabled = True
        self.caid_data = (('0x1700',
          '0x17ff',
          'Beta',
          'B',
          True),
         ('0x600',
          '0x6ff',
          'Irdeto',
          'I',
          True),
         ('0x100',
          '0x1ff',
          'Seca',
          'S',
          True),
         ('0x500',
          '0x5ff',
          'Via',
          'V',
          True),
         ('0x1800',
          '0x18ff',
          'Nagra',
          'N',
          True),
         ('0xd00',
          '0xdff',
          'CryptoW',
          'CW',
          True),
         ('0x900',
          '0x9ff',
          'NDS',
          'ND',
          True),
         ('0xb00',
          '0xbff',
          'Conax',
          'CO',
          True),
         ('0x4ae0',
          '0x4ae1',
          'Dre',
          'DC',
          True),
         ('0x5581',
          '0x5581',
          'BulCrypt',
          'BU',
          True),
         ('0x2600',
          '0x2600',
          'Biss',
          'BI',
          True),
         ('0xe00',
          '0xeff',
          'PowerVU',
          'PV',
          True),
         ('0x4aee',
          '0x4aee',
          'BulCrypt',
          'BU',
          False))
        self.ca_table = (('CryptoCaidBetaAvailable', 'B', False),
         ('CryptoCaidIrdetoAvailable', 'I', False),
         ('CryptoCaidSecaAvailable', 'S', False),
         ('CryptoCaidViaAvailable', 'V', False),
         ('CryptoCaidNagraAvailable', 'N', False),
         ('CryptoCaidCryptoWAvailable', 'CW', False),
         ('CryptoCaidNDSAvailable', 'ND', False),
         ('CryptoCaidConaxAvailable', 'CO', False),
         ('CryptoCaidDreAvailable', 'DC', False),
         ('CryptoCaidBulCrypt2Available', 'BU', False),
         ('CryptoCaidBissAvailable', 'BI', False),
         ('CryptoCaidPowerVUAvailable', 'PV', False),
         ('CryptoCaidBulCrypt1Available', 'BU', False),
         ('CryptoCaidBetaSelected', 'B', True),
         ('CryptoCaidIrdetoSelected', 'I', True),
         ('CryptoCaidSecaSelected', 'S', True),
         ('CryptoCaidViaSelected', 'V', True),
         ('CryptoCaidNagraSelected', 'N', True),
         ('CryptoCaidCryptoWSelected', 'CW', True),
         ('CryptoCaidNDSSelected', 'ND', True),
         ('CryptoCaidConaxSelected', 'CO', True),
         ('CryptoCaidDreSelected', 'DC', True),
         ('CryptoCaidBulCrypt2Selected', 'BU', True),
         ('CryptoCaidBissSelected', 'BI', True),
         ('CryptoCaidPowerVUSelected', 'PV', True),
         ('CryptoCaidBulCrypt1Selected', 'BU', True))
        self.ecmdata = GetEcmInfo()
        self.feraw = self.fedata = self.updateFEdata = None
        return

    def getCryptoInfo(self, info):
        if info.getInfo(iServiceInformation.sIsCrypted) == 1:
            data = self.ecmdata.getEcmData()
            self.current_source = data[0]
            self.current_caid = data[1]
            self.current_provid = data[2]
            self.current_ecmpid = data[3]
        else:
            self.current_source = ''
            self.current_caid = '0'
            self.current_provid = '0'
            self.current_ecmpid = '0'

    def createCryptoBar(self, info):
        res = ''
        available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
        for caid_entry in self.caid_data:
            if int(self.current_caid, 16) >= int(caid_entry[0], 16) and int(self.current_caid, 16) <= int(caid_entry[1], 16):
                color = '\\c0000??00'
            else:
                color = '\\c007?7?7?'
                try:
                    for caid in available_caids:
                        if caid >= int(caid_entry[0], 16) and caid <= int(caid_entry[1], 16):
                            color = '\\c00????00'

                except:
                    pass

            if color != '\\c007?7?7?' or caid_entry[4]:
                if res:
                    res += ' '
                res += color + caid_entry[3]

        res += '\\c00??????'
        return res

    def createCryptoSpecial(self, info):
        caid_name = 'Free To Air'
        try:
            for caid_entry in self.caid_data:
                if int(self.current_caid, 16) >= int(caid_entry[0], 16) and int(self.current_caid, 16) <= int(caid_entry[1], 16):
                    caid_name = caid_entry[2]
                    break

            return caid_name + ':%04x:%04x:%04x:%04x' % (int(self.current_caid, 16),
             int(self.current_provid, 16),
             info.getInfo(iServiceInformation.sSID),
             int(self.current_ecmpid, 16))
        except:
            pass

        return ''

    def createResolution(self, info):
        xres = info.getInfo(iServiceInformation.sVideoWidth)
        if xres == -1:
            return ''
        yres = info.getInfo(iServiceInformation.sVideoHeight)
        mode = ('i', 'p', ' ')[info.getInfo(iServiceInformation.sProgressive)]
        fps = str((info.getInfo(iServiceInformation.sFrameRate) + 500) / 1000)
        return str(xres) + 'x' + str(yres) + mode + fps

    def createVideoCodec(self, info):
        return ('MPEG2', 'MPEG4', 'MPEG1', 'MPEG4-II', 'VC1', 'VC1-SM', '')[info.getInfo(iServiceInformation.sVideoType)]

    def createPIDInfo(self, info):
        vpid = info.getInfo(iServiceInformation.sVideoPID)
        apid = info.getInfo(iServiceInformation.sAudioPID)
        pcrpid = info.getInfo(iServiceInformation.sPCRPID)
        sidpid = info.getInfo(iServiceInformation.sSID)
        tsid = info.getInfo(iServiceInformation.sTSID)
        onid = info.getInfo(iServiceInformation.sONID)
        if vpid < 0:
            vpid = 0
        if apid < 0:
            apid = 0
        if pcrpid < 0:
            pcrpid = 0
        if sidpid < 0:
            sidpid = 0
        if tsid < 0:
            tsid = 0
        if onid < 0:
            onid = 0
        return '%d-%d:%05d:%04d:%04d:%04d' % (onid,
         tsid,
         sidpid,
         vpid,
         apid,
         pcrpid)

    def createTransponderInfo(self, fedata, feraw):
        if 'DVB-T' in feraw.get('tuner_type'):
            tmp = addspace(self.createChannelNumber(fedata, feraw)) + addspace(self.createFrequency(feraw)) + addspace(self.createPolarization(fedata))
        else:
            tmp = addspace(self.createFrequency(feraw)) + addspace(self.createPolarization(fedata))
        return addspace(self.createTunerSystem(fedata)) + tmp + addspace(self.createSymbolRate(fedata, feraw)) + addspace(self.createFEC(fedata, feraw)) + addspace(self.createModulation(fedata)) + addspace(self.createOrbPos(feraw))

    def createFrequency(self, feraw):
        frequency = feraw.get('frequency')
        if frequency:
            if 'DVB-T' in feraw.get('tuner_type'):
                return str(int(frequency / 1000000.0 + 0.5))
            else:
                return str(int(frequency / 1000 + 0.5))
        return ''

    def createChannelNumber(self, fedata, feraw):
        return 'DVB-T' in feraw.get('tuner_type') and fedata.get('channel') or ''

    def createSymbolRate(self, fedata, feraw):
        if 'DVB-T' in feraw.get('tuner_type'):
            bandwidth = fedata.get('bandwidth')
            if bandwidth:
                return bandwidth
        else:
            symbolrate = fedata.get('symbol_rate')
            if symbolrate:
                return str(symbolrate / 1000)
        return ''

    def createPolarization(self, fedata):
        return fedata.get('polarization_abbreviation') or ''

    def createFEC(self, fedata, feraw):
        if 'DVB-T' in feraw.get('tuner_type'):
            code_rate_lp = fedata.get('code_rate_lp')
            code_rate_hp = fedata.get('code_rate_hp')
            if code_rate_lp and code_rate_hp:
                return code_rate_lp + '-' + code_rate_hp
        else:
            fec = fedata.get('fec_inner')
            if fec:
                return fec
        return ''

    def createModulation(self, fedata):
        if fedata.get('tuner_type') == _('Terrestrial'):
            constellation = fedata.get('constellation')
            if constellation:
                return constellation
        else:
            modulation = fedata.get('modulation')
            if modulation:
                return modulation
        return ''

    def createTunerType(self, feraw):
        return feraw.get('tuner_type') or ''

    def createTunerSystem(self, fedata):
        return fedata.get('system') or ''

    def createOrbPos(self, feraw):
        orbpos = feraw.get('orbital_position')
        if orbpos > 1800:
            return str(float(3600 - orbpos) / 10.0) + '\xc2\xb0 W'
        if orbpos > 0:
            return str(float(orbpos) / 10.0) + '\xc2\xb0 E'
        return ''

    def createOrbPosOrTunerSystem(self, fedata, feraw):
        orbpos = self.createOrbPos(feraw)
        if orbpos is not '':
            return orbpos
        return self.createTunerSystem(fedata)

    def createProviderName(self, info):
        return info.getInfoString(iServiceInformation.sProvider)

    @cached
    def getText(self):
        service = self.source.service
        if service is None:
            return ''
        info = service and service.info()
        if not info:
            return ''
        if self.type == 'CryptoInfo':
            self.getCryptoInfo(info)
            if config.usage.show_cryptoinfo.value:
                return addspace(self.createCryptoBar(info)) + self.createCryptoSpecial(info)
            else:
                return addspace(self.createCryptoBar(info)) + addspace(self.current_source) + self.createCryptoSpecial(info)
        if self.type == 'CryptoBar':
            self.getCryptoInfo(info)
            return self.createCryptoBar(info)
        elif self.type == 'CryptoSpecial':
            self.getCryptoInfo(info)
            return self.createCryptoSpecial(info)
        elif self.type == 'ResolutionString':
            return self.createResolution(info)
        elif self.type == 'VideoCodec':
            return self.createVideoCodec(info)
        if self.updateFEdata:
            feinfo = service.frontendInfo()
            if feinfo:
                self.feraw = feinfo.getAll(config.usage.infobar_frontend_source.value == 'settings')
                if self.feraw:
                    self.fedata = ConvertToHumanReadable(self.feraw)
        feraw = self.feraw
        if not feraw:
            feraw = info.getInfoObject(iServiceInformation.sTransponderData)
            if not feraw:
                return ''
            fedata = ConvertToHumanReadable(feraw)
        else:
            fedata = self.fedata
        if self.type == 'All':
            self.getCryptoInfo(info)
            if config.usage.show_cryptoinfo.value:
                return addspace(self.createProviderName(info)) + self.createTransponderInfo(fedata, feraw) + '\n' + addspace(self.createCryptoBar(info)) + addspace(self.createCryptoSpecial(info)) + '\n' + addspace(self.createPIDInfo(info)) + addspace(self.createVideoCodec(info)) + self.createResolution(info)
            else:
                return addspace(self.createProviderName(info)) + self.createTransponderInfo(fedata, feraw) + '\n' + addspace(self.createCryptoBar(info)) + self.current_source + '\n' + addspace(self.createCryptoSpecial(info)) + addspace(self.createVideoCodec(info)) + self.createResolution(info)
        if self.type == 'ServiceInfo':
            return addspace(self.createProviderName(info)) + addspace(self.createTunerSystem(fedata)) + addspace(self.createFrequency(feraw)) + addspace(self.createPolarization(fedata)) + addspace(self.createSymbolRate(fedata, feraw)) + addspace(self.createFEC(fedata, feraw)) + addspace(self.createModulation(fedata)) + addspace(self.createOrbPos(feraw)) + addspace(self.createVideoCodec(info)) + self.createResolution(info)
        elif self.type == 'TransponderInfo':
            return self.createTransponderInfo(fedata, feraw)
        elif self.type == 'TransponderFrequency':
            return self.createFrequency(feraw)
        elif self.type == 'TransponderSymbolRate':
            return self.createSymbolRate(fedata, feraw)
        elif self.type == 'TransponderPolarization':
            return self.createPolarization(fedata)
        elif self.type == 'TransponderFEC':
            return self.createFEC(fedata, feraw)
        elif self.type == 'TransponderModulation':
            return self.createModulation(fedata)
        elif self.type == 'OrbitalPosition':
            return self.createOrbPos(feraw)
        elif self.type == 'TunerType':
            return self.createTunerType(feraw)
        elif self.type == 'TunerSystem':
            return self.createTunerSystem(fedata)
        elif self.type == 'OrbitalPositionOrTunerSystem':
            return self.createOrbPosOrTunerSystem(fedata, feraw)
        elif self.type == 'PIDInfo':
            return self.createPIDInfo(info)
        elif self.type == 'TerrestrialChannelNumber':
            return self.createChannelNumber(fedata, feraw)
        else:
            return _('invalid type')

    text = property(getText)

    @cached
    def getBool(self):
        service = self.source.service
        info = service and service.info()
        if not info:
            return False
        else:
            request_caid = None
            for x in self.ca_table:
                if x[0] == self.type:
                    request_caid = x[1]
                    request_selected = x[2]
                    break

            if request_caid is None:
                return False
            if info.getInfo(iServiceInformation.sIsCrypted) != 1:
                return False
            data = self.ecmdata.getEcmData()
            if data is None:
                return False
            current_caid = data[1]
            available_caids = info.getInfoObject(iServiceInformation.sCAIDs)
            for caid_entry in self.caid_data:
                if caid_entry[3] == request_caid:
                    if request_selected:
                        if int(current_caid, 16) >= int(caid_entry[0], 16) and int(current_caid, 16) <= int(caid_entry[1], 16):
                            return True
                    else:
                        try:
                            for caid in available_caids:
                                if caid >= int(caid_entry[0], 16) and caid <= int(caid_entry[1], 16):
                                    return True

                        except:
                            pass

            return False

    boolean = property(getBool)

    def changed(self, what):
        if what[0] == self.CHANGED_SPECIFIC:
            self.updateFEdata = False
            #if what[1] == iPlayableService.evNewProgramInfo:
            #    self.updateFEdata = True
            if what[1] == iPlayableService.evEnd:
                self.feraw = self.fedata = None
            Converter.changed(self, what)
        elif what[0] == self.CHANGED_POLL and self.updateFEdata is not None:
            self.updateFEdata = False
            Converter.changed(self, what)
        return