from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
import urllib, urllib2
import cookielib
import json
#import urlresolver
import simplejson
import re
import base64
import time

def _decode(data):
    def O1l(string):
        ret = ""
        i = len(string) - 1
        while i >= 0:
            ret += string[i]
            i -= 1
        return ret

    def l0I(string):
        enc = ""
        dec = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        i = 0
        while True:
            h1 = dec.find(string[i])
            i += 1
            h2 = dec.find(string[i])
            i += 1
            h3 = dec.find(string[i])
            i += 1
            h4 = dec.find(string[i])
            i += 1
            bits = h1 << 18 | h2 << 12 | h3 << 6 | h4
            o1 = bits >> 16 & 0xff
            o2 = bits >> 8 & 0xff
            o3 = bits & 0xff
            if h3 == 64:
                enc += unichr(o1)
            else:
                if h4 == 64:
                    enc += unichr(o1) + unichr(o2)
                else:
                    enc += unichr(o1) + unichr(o2) + unichr(o3)
            if i >= len(string):
                break
        return enc

    escape = re.search("var _escape=\'([^\']+)", l0I(O1l(data))).group(1)
    return escape.replace('%', '\\').decode('unicode-escape')


def _decode2(file_url):
    def K12K(a, typ='b'):
        codec_a = ["G", "L", "M", "N", "Z", "o", "I", "t", "V", "y", "x", "p", "R", "m", "z", "u", "D", "7", "W", "v",
                   "Q", "n", "e", "0", "b", "="]
        codec_b = ["2", "6", "i", "k", "8", "X", "J", "B", "a", "s", "d", "H", "w", "f", "T", "3", "l", "c", "5", "Y",
                   "g", "1", "4", "9", "U", "A"]
        if 'd' == typ:
            tmp = codec_a
            codec_a = codec_b
            codec_b = tmp
        idx = 0
        while idx < len(codec_a):
            a = a.replace(codec_a[idx], "___")
            a = a.replace(codec_b[idx], codec_a[idx])
            a = a.replace("___", codec_b[idx])
            idx += 1
        return a

    def _xc13(_arg1):
        _lg27 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        _local2 = ""
        _local3 = [0, 0, 0, 0]
        _local4 = [0, 0, 0]
        _local5 = 0
        while _local5 < len(_arg1):
            _local6 = 0
            while _local6 < 4 and (_local5 + _local6) < len(_arg1):
                _local3[_local6] = _lg27.find(_arg1[_local5 + _local6])
                _local6 += 1
            _local4[0] = ((_local3[0] << 2) + ((_local3[1] & 48) >> 4))
            _local4[1] = (((_local3[1] & 15) << 4) + ((_local3[2] & 60) >> 2))
            _local4[2] = (((_local3[2] & 3) << 6) + _local3[3])

            _local7 = 0
            while _local7 < len(_local4):
                if _local3[_local7 + 1] == 64:
                    break
                _local2 += chr(_local4[_local7])
                _local7 += 1
            _local5 += 4
        return _local2

    return _xc13(K12K(file_url, 'e'))


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'netu'
	self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
	self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName
    
    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('http://hqq.tv/watch_video.php?v=','http://hqq.tv/player/embed_player.php?vid=')

    
    def __getIdFromUrl(self):
        sPattern = 'http:..hqq.tv.player.embed_player.php\?vid=(.{12})'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
        return ''
        
    def __modifyUrl(self, sUrl):
        api = ('http://rutube.ru/api/play/trackinfo/%s/?format=json') % (self.__getIdFromUrl())

        oRequest = cRequestHandler(api)
        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\\', '').replace('//', '')
        
        sPattern = 'src="(.+?)"'
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            self.__sUrl = 'http://' + aResult[1][0]
            return self.__sUrl
            
        return


    def getPluginIdentifier(self):
        return 'netu'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
    
        api_call = ''
    
        id = self.__getIdFromUrl()
        self.__sUrl = 'http://hqq.tv/player/embed_player.php?vid=' + id + '&autoplay=no'

        UA = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
        UA = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us)'
        headers = {'User-Agent': UA ,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Content-Type': 'text/html; charset=utf-8'}
        
        player_url = self.__sUrl
        
        print player_url
        
        req = urllib2.Request(player_url, None, headers)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print e.read()
            print e.reason
            
        data = response.read()
        response.close()
        
        b64enc = re.search('base64([^\"]+)', data, re.DOTALL)
        b64dec = b64enc and base64.decodestring(b64enc.group(1))
        enc = b64dec and re.search("\'([^']+)\'", b64dec).group(1)
        if enc:
            data = re.compile('<input name="([^"]+?)" [^>]+? value="([^"]+?)">').findall(_decode(enc))
            post_data = {}
            for idx in range(len(data)):
                post_data[data[idx][0]] = data[idx][1]

            postdata = urllib.urlencode(post_data)
            print postdata
            print player_url
            req = urllib2.Request(player_url,postdata,headers)
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError, e:
                print e.read()
                print e.reason
                
            data = response.read()
            response.close()
            
            #fh = open('c:\\test.txt', "w")
            #h.write(data)
            #fh.close()
                       
            b64enc = re.search('base64([^\"]+)', data, re.DOTALL)
            b64dec = b64enc and base64.decodestring(b64enc.group(1))
            enc = b64dec and re.search("\'([^']+)\'", b64dec).group(1)

            if enc:
                data = re.compile('<input name="([^"]+?)" [^>]+? value="([^"]*)">').findall(_decode(enc))
                post_data = {}
                for idx in range(len(data)):
                    post_data[data[idx][0]] = data[idx][1]
                              
                req = urllib2.Request("http://hqq.tv/sec/player/embed_player.php?" + urllib.urlencode(post_data),None,headers)
                response = urllib2.urlopen(req)
                data = response.read()
                response.close()

                data = urllib.unquote(data)
                vid_server = re.search(r'var\s*vid_server\s*=\s*"([^"]*?)"', data)
                vid_link = re.search(r'var\s*vid_link\s*=\s*"([^"]*?)"', data)
                at = re.search(r'var\s*at\s*=\s*"([^"]*?)"', data)
                if vid_server and vid_link and at:
                    #get_data = {'server': vid_server.group(1), 'link': vid_link.group(1), 'at': at.group(1), 'adb': '0\\'}
                    get_data = {'server': vid_server.group(1), 'link': vid_link.group(1), 'at': at.group(1), 'adb': '1/'}
                    
                    print 'pp'
                    
                    req = urllib2.Request("http://hqq.tv/player/get_md5.php?" + urllib.urlencode(get_data),None,headers)
                    response = urllib2.urlopen(req)
                    data = response.read()
                    response.close()
                    
                    #fh = open('c:\\test.txt', "w")
                    #fh.write(data)
                    #fh.close()
                    
                    file_url = re.search(r'"file"\s*:\s*"([^"]*?)"', data)
                    if file_url:
                        #return [{'url': _decode2(file_url.group(1).replace('\\', '')), 'quality': '???'}]
                        list_url = _decode2(file_url.group(1).replace('\\', '')) + '='
                        
        #print list_url
        
        #normallmeent on a une liste de lien en
        #EXTM3U
        #EXT-X-MEDIA-SEQUENCE:0
        #EXT-X-ALLOW-CACHE:NO
        #EXT-X-VERSION:2
        #EXT-X-TARGETDURATION:20
        #EXTINF:20,
        #1397939972cecbe.mp4Frag1Num0.ts
        #EXTINF:20,
        #1397939972cecbe.mp4Frag1Num1.ts
        
        
        api_call = list_url
        #api_call = list_url.replace('?socket=','.mp4Frag1Num0.ts')
        
        #use a fake headers
        Header = 'User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X)'
        #Header = urllib.urlencode(Header)
        api_call = api_call + '|' + Header
        
        print api_call
        #api_call = api_call.split('|')[0]

        #time.sleep(1)
        
        if not (api_call == False):
            return True, api_call          
            
        return False, False