# -*- coding: utf-8 -*-

import time
import httplib
import urllib,urllib2
import json
import base64
import rsa
from base64 import b64decode
import hashlib

class BandAPI(object):

    """ appkey
        iOS 9eb263daa9d764fd41b0ba3e4c093dcf
        Android bcb6d11b685d94a08f5b1965896b50c8 
    """
    me2_application_key = '9eb263daa9d764fd41b0ba3e4c093dcf'


    """ sign key
        iOS b927bc247fade80ef66fdd97caad74a3
        Android de68d80d34ec9e30c7a5120fbd7ee829
    """
    sign_key = 'b927bc247fade80ef66fdd97caad74a3'
    
    base_url = 'https://api.band.us/'
    api_version = 'v1/'
    api_url = base_url + api_version
    
    device_id = '3CEAAD93-1543-6303-13DD-214203234E32_com.nhncorp.m2app' # uuid random
    device_model = 'iPhone3,1'
    app_version = '3.2.3'
    os_name = 'iPhone OS'
    os_version = '7.1.2'
    timezone = 'Asia/Seoul'
    
    """ user_agent
        iOS 'BAND/3.2.3 (iPhone OS 7.1.2; iPhone3,1)'
        Android 'BAND/3.2.3 (Android OS 4.1;samsung SHW-M250S)'   # (MANUFACTURER MODEL)
    """
    user_agent = 'BAND/%s (%s %s; %s)' % (app_version,os_name,os_version,device_model)



    authorization = None


    def __init__(self):
        pass
    

    def __getAppSign(self):
        ti = int(round(time.time()))
        step1 = str(ti)+'bybuam.q' + self.me2_application_key + self.sign_key         #bybuam.q  (random 6 letter word , android  'ffffff')
        m = hashlib.md5()
        m.update(step1)
        step1md5 =  m.hexdigest()
        step2Str = str(ti)+'$$bybuam.q$$'+step1md5
        step2byte = str.encode(step2Str)
        encoded = base64.b64encode(step2byte)
        return encoded

    def __getCredential(self,byte_token):
        
        n =0xCDF0CE20515E9758CF74849061B5A228A9D1583BC3CF6C7DFB73D46F4DBFE079A9A7C44BDBB32708770C9E779D5D4983A13FF191F624CB9443A4FFE12EC9888264F9DBB62F2E2D7E0B131B3F3D5E4485FA1A7826887335394A353EA25D5AA6D13AA09648C6268714EFA38EAE32089DC6A91EB3A77E1DA442B826C9EA35510AD9

        exponent = 0x010001

        keyPub = rsa.PublicKey(n, exponent)
        credential = rsa.encrypt(byte_token, keyPub)
        return base64.b64encode(credential)


    def __getToken(self):
        url = self.api_url + 'get_start_token'
        headers = self.__defaultHeader()
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)
        data = response.read()
        data = json.loads(data ,encoding='utf-8')
        return data
    
    def __defaultHeader(self):
        headers = {
            'User-Agent' : self.user_agent,
            'me2_application_key' : self.me2_application_key,
            'me2_asig' : self.__getAppSign(),
            'user_locale' : 'ko_KR',
            'locale' : 'ko_KR',
            'version' : '20140725',
            'language' : 'ko',
            'country' : 'KR',
        }
        return headers
    
    def createAuthToken(self , user_id , auth_token):
        auth = '%s:full_auth_token %s' % (user_id , auth_token)
        authByte = str.encode(str(auth))
        encoded = base64.b64encode(authByte)
        return 'Basic ' + encoded
    
    def __add_stat(self ):
        url = self.api_url + 'add_stat'
        
        headers = self.__defaultHeader()
        
        headers['Authorization'] = self.authorization

        query_args = {
                'app_version':self.app_version,
                'code':'3',
                'device_id':self.device_id,
                'device_model':self.device_model,
                'os_name':self.os_name,
                'os_version':self.os_version,
                'timezone':self.timezone,
                'user_id':data['result_data']['user_id'],
        }
        
        data = urllib.urlencode(query_args)
        request = urllib2.Request(url, data, headers)
        
        response = urllib2.urlopen(request)
        data = response.read()
        return data

    def __login_by_email(self,credential,email,password):
        url = self.api_url + 'login_by_email'
        headers = self.__defaultHeader()
        
        query_args = {
                'credential':credential,
                'device_id':self.device_id,
                'device_model':self.device_model,
                'device_type':'2',
                'language':'ko',
                'password':password,
                'email':email
        }
        
        
        data = urllib.urlencode(query_args)
        request = urllib2.Request(url, data, headers)
        
        response = urllib2.urlopen(request)
        data = response.read()
        return data

    def __login_by_phone(self,credential , phone_number, password):
        url = self.api_url + 'login_by_phone'
        headers = self.__defaultHeader()
        
        query_args = {
                'credential':credential,
                'device_id':self.device_id,
                'device_model':self.device_model,
                'device_type':'2',
                'language':'ko',
                'password': password,
                'phone_number': phone_number
        }
        
        
        data = urllib.urlencode(query_args)
        request = urllib2.Request(url, data, headers)
        
        response = urllib2.urlopen(request)
        data = response.read()
        return data
    
    def __callAPI(self, api = None, query_args = None):
        if not ( self.authorization ):
            message = "login first or setAuthToken(token)"
            self.raise_msg(message)
        
        headers = self.__defaultHeader()
        headers['Authorization'] = self.authorization
        if query_args:
            query_args = urllib.urlencode(query_args)

        request = urllib2.Request(api, query_args, headers)
        response = urllib2.urlopen(request)
        data = response.read()
        return data
    
    def raise_msg(self, msg):
        raise Exception("Error: %s" % msg)


    def login(self , email=None , phone_number=None , password=None):  # phone : +821012345678
    
        result_data = self.__getToken()
        token = result_data['result_data']['token']
        byte_token = str.encode(str(token))
        credential = self.__getCredential(byte_token)
        print "[*] SIGN"

        if (email):
            data = self.__login_by_email(credential,email,password)
        else:
            data = self.__login_by_phone(credential,phone_number,password)
        
        return data

    
    def setAuthToken(self,token):
        self.authorization = token


        """
            API
        """

    def getProfile(self):
        api = self.api_url + 'get_profile'
        return self.__callAPI(api,None)
    
    def getBandList(self):
        api = self.api_url + 'get_band_list'
        return self.__callAPI(api,None)

    def getHomeInfo(self):
        api = self.api_url + 'get_home_info'
        return self.__callAPI(api,None)
    
    
    def createBand(self,name):
        api = self.api_url + 'create_band'
        query_args = {
            'name':name,
            'theme_color':'BAND_1',
            'without_tutorial':'true'
        }
        return self.__callAPI(api,query_args)
    
    def deleteBand(self,band_id):
        api = self.base_url + 'api/m2/delete_band.json'
        query_args = {
            'band_id':band_id,
        }
        return self.__callAPI(api,query_args)

    def getBandInfo(self,band_no):
        api = self.api_url + 'get_band_information'
        query_args = {
            'band_no':band_no,
        }

    def getMembersOfBands(self,band_no,limit):  # band_no , limit = count
        api = self.api_url + 'get_members_of_bands'
        query_args = {
            'band_no':band_no,
            'limit':limit
        }
        return self.__callAPI(api,query_args)

    def getPosts(self,band_id = None, count = '20',include_video = '1',resolution_type = '4'):
        api = self.api_url + 'get_posts'
        query_args = {
            'band_id':band_id,
            'count':count,
            'include_video':include_video,
            'resolution_type':resolution_type
        }
        return self.__callAPI(api,query_args)

    def createPost(self,band_id,body):
        api = self.api_url + 'create_post'
        query_args = {
            'band_id':band_id,
            'body':body
        }
        return self.__callAPI(api,query_args)

    def deletePost(self,band_id,post_id):
        api = self.api_url + 'delete_post'
        query_args = {
            'band_id':band_id,
            'post_id':post_id
        }
        return self.__callAPI(api,query_args)


    def getPostDetail(self,band_id,post_id):
        api = self.api_url + 'get_post_detail'
        query_args = {
            'band_id':band_id,
            'post_id':post_id
        }
        return self.__callAPI(api,query_args)


    def createComment(self,post_id,body):
        api = self.api_url + 'create_comment'
        query_args = {
            'post_id':post_id,
            'body':body
        }
        return self.__callAPI(api,query_args)


    def deleteComment(self,comment_id):
        api = self.api_url + 'delete_comment'
        query_args = {
            'comment_id':comment_id
        }
        return self.__callAPI(api,query_args)




