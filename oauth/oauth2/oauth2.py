#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import urllib
import time
import random
import urlparse
import hmac
import binascii
import os
import rsa
from binascii import b2a_hex, a2b_hex

import base64
import json
from cache import Cache

VERSION = '1.0'
HTTP_METHOD = 'GET'
SIGNATURE_METHOD = 'PLAINTEXT'

CACHE_TIMEOUT = 60 * 1000

class OAuthError(RuntimeError):
    """Generic exception class."""
    def __init__(self, message='OAuth error occured.'):
        self.message = message

def build_authenticate_header(realm=''):
    """Optional WWW-Authenticate header (401 error)"""
    return {'WWW-Authenticate': 'OAuth realm="%s"' % realm}

def escape(s):
    """Escape a URL including any /."""
    return urllib.quote(s, safe='~')

def _utf8_str(s):
    """Convert unicode to utf-8."""
    if isinstance(s, unicode):
        return s.encode("utf-8")
    else:
        return str(s)

def generate_timestamp():
    """Get seconds since epoch (UTC)."""
    return int(time.time())

def generate_nonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])



class Request(object):
    """Request represents the request and can be serialized.

    OAuth parameters:
        - oauth_consumer_key 
        - oauth_token
        - oauth_signature_method
        - oauth_signature 
        - oauth_timestamp 
        - oauth_nonce
        - oauth_version
        - oauth_verifier
        ... any additional parameters, as defined by the Service Provider.
    """
    parameters = None # OAuth parameters.
    http_method = HTTP_METHOD
    uri = None
    version = VERSION
    path =  None
    def __init__(self, http_method=HTTP_METHOD, uri=None, parameters=None):
        self.http_method = http_method
        self.uri = uri or self.get_uri()
        self.parameters = parameters or {}
        self.path = self.get_normalized_uri()

    @staticmethod
    def from_request(uri,http_method=HTTP_METHOD, headers=None, parameters=None,
            query_string=None):
        """Combines multiple parameter sources."""
        if parameters is None:
            parameters = {}

        # Headers
        if headers and 'Authorization' in headers:
            auth_header = headers['Authorization']
            # Check that the authorization header is OAuth.
            if auth_header[:6] == 'OAuth ':
                auth_header = auth_header[6:]
                try:
                    # Get the parameters from the header.
                    header_params = Request._split_header(auth_header)
                    parameters.update(header_params)
                except Exception:
                    raise OAuthError('Unable to parse OAuth parameters from '
                        'Authorization header.')

        # GET or POST query string.
        if query_string:
            query_params = Request._split_url_string(query_string)
            parameters.update(query_params)

        param_str = urlparse.urlparse(uri)[4] # query
        url_params = Request._split_url_string(param_str)
        parameters.update(url_params)

        if parameters:
            return Request(http_method, uri, parameters)
        return None

    def set_parameter(self, parameter, value):
        self.parameters[parameter] = value

    def get_parameter(self, parameter):
        try:
            return self.parameters[parameter]
        except KeyError:
            raise OAuthError('Parameter not found: %s' % parameter)

    def _get_timestamp_nonce(self):
        return self.get_parameter('oauth_timestamp'), self.get_parameter(
            'oauth_nonce')

    def get_nonoauth_parameters(self):
        """Get any non-OAuth parameters."""
        parameters = {}
        for k, v in self.parameters.iteritems():
            # Ignore oauth parameters.
            if k.find('oauth_') < 0:
                parameters[k] = v
        return parameters

    def to_header(self, realm=''):
        """Serialize as a header for an HTTPAuth request."""
        auth_header = 'OAuth realm="%s"' % realm
        # Add the oauth parameters.
        if self.parameters:
            for k, v in self.parameters.iteritems():
                if k[:6] == 'oauth_':
                    auth_header += ', %s="%s"' % (k, escape(str(v)))
        return {'Authorization': auth_header}

    def to_postdata(self):
        """Serialize as post data for a POST request."""
        return '&'.join(['%s=%s' % (escape(str(k)), escape(str(v))) \
            for k, v in self.parameters.iteritems()])

    def get_uri(self):
        """Serialize as a URL for a GET request."""
        return '%s?%s' % (self.get_normalized_uri(), self.to_postdata())

    def get_normalized_parameters(self):
        """Return a string that contains the parameters that must be signed."""
        params = self.parameters
        try:
            # Exclude the signature if it exists.
            del params['oauth_signature']
        except KeyError:
            pass
        # Escape key values before sorting.
        key_values = [(escape(_utf8_str(k)), escape(_utf8_str(v))) \
            for k,v in params.items()]
        # Sort lexicographically, first after key, then after value.
        key_values.sort()
        # Combine key value pairs into a string.
        return '&'.join(['%s=%s' % (k, v) for k, v in key_values])

    def get_normalized_http_method(self):
        """Uppercases the http method."""
        return self.http_method.upper()

    def get_normalized_uri(self):
        """Parses the URL and rebuilds it to be scheme://host/path."""
        parts = urlparse.urlparse(self.uri)
        scheme, netloc, path = parts[:3]
        # Exclude default port numbers.
        if scheme == 'http' and netloc[-3:] == ':80':
            netloc = netloc[:-3]
        elif scheme == 'https' and netloc[-4:] == ':443':
            netloc = netloc[:-4]
        return '%s://%s%s' % (scheme, netloc, path)

    def sign_request(self, signature_method, consumer, token):
        """Set the signature parameter to the result of build_signature."""
        # Set the signature method.
        self.set_parameter('oauth_signature_method',
            signature_method.get_name())
        # Set the signature.
        self.set_parameter('oauth_signature',
            self.build_signature(signature_method, consumer, token))

    def build_signature(self, signature_method, consumer, token):
        """Calls the build signature method within the signature method."""
        return signature_method.build_signature(self, consumer, token)

    def from_consumer_and_token(oauth_consumer, token=None,
            callback=None, verifier=None, http_method=HTTP_METHOD,
            uri=None, parameters=None):
        if not parameters:
            parameters = {}

        defaults = {
            'oauth_consumer_key': oauth_consumer.key,
            'oauth_timestamp': generate_timestamp(),
            'oauth_nonce': generate_nonce(),
            'oauth_version': Request.version,
        }

        defaults.update(parameters)
        parameters = defaults

        if token:
            parameters['oauth_token'] = token.key
            if token.callback:
                parameters['oauth_callback'] = token.callback
            # 1.0a support for verifier.
            if verifier:
                parameters['oauth_verifier'] = verifier
        elif callback:
            # 1.0a support for callback in the request token request.
            parameters['oauth_callback'] = callback

        return Request(http_method, uri, parameters)
    from_consumer_and_token = staticmethod(from_consumer_and_token)

    def from_token_and_callback(token, callback=None, http_method=HTTP_METHOD,
            uri=None, parameters=None):
        if not parameters:
            parameters = {}

        parameters['oauth_token'] = token.key

        if callback:
            parameters['oauth_callback'] = callback

        return Request(http_method, uri, parameters)
    from_token_and_callback = staticmethod(from_token_and_callback)

    def _split_header(header):
        """Turn Authorization: header into parameters."""
        params = {}
        parts = header.split(',')
        for param in parts:
            # Ignore realm parameter.
            if param.find('realm') > -1:
                continue
            # Remove whitespace.
            param = param.strip()
            # Split key-value.
            param_parts = param.split('=', 1)
            # Remove quotes and unescape the value.
            params[param_parts[0]] = urllib.unquote(param_parts[1].strip('\"'))
        return params
    _split_header = staticmethod(_split_header)

    def _split_url_string(param_str):
        """Turn URL string into parameters."""
        parameters = cgi.parse_qs(param_str, keep_blank_values=False)
        for k, v in parameters.iteritems():
            parameters[k] = urllib.unquote(v[0])
        return parameters
    _split_url_string = staticmethod(_split_url_string)


class SignatureMethod(object):
    """
        A strategy class that implements a signature method.
        一个实现签名方法的策略类
    """
    def get_name(self):
        """-> str."""
        raise NotImplementedError

    def build_signature_base_string(self, oauth_request, oauth_consumer, oauth_token):
        """-> str key, str raw."""
        raise NotImplementedError

    def build_signature(self, oauth_request, oauth_consumer, oauth_token):
        """-> str."""
        raise NotImplementedError

    def check_signature(self, oauth_request, consumer, token, signature):
        built = self.build_signature(oauth_request, consumer, token)
        return built == signature

class SignatureMethod_HMAC_SHA1(SignatureMethod):

    def get_name(self):
        return 'HMAC-SHA1'
    def build_signature(self, payload, header):
        """Builds the base signature string."""


        # HMAC object.
        try:
            import hashlib # 2.5
            print payload, header ,'1111'
            hashed = hmac.new(payload, header, hashlib.sha1)
            hashed.update(payload)
        except ImportError:
            import sha # Deprecated
            hashed = hmac.new(payload, header, sha)
            hashed.update(payload)

        # Calculate the digest base 64.
        return hashed.hexdigest()

#auth :suyf
class SignatureMethod_MD5(object):
    def build_signature(self, payload, header):
        import hashlib
        _str = payload[::-1]+'.'+header[::-1]
        m = hashlib.md5()
        m.update(_str)
        return m.hexdigest()

class RsaEncryption(object):

    def __init__(self):
        self.pubkey,self.privkey = self.get_key()

    def get_key(self):
        """初始化公钥秘钥"""
        if not os.path.exists('public.pem'):
            (pubkey, privkey) = rsa.newkeys(1024)
            with open('public.pem','w+') as f:
                f.write(pubkey.save_pkcs1().decode())
            with open('private.pem','w+') as f:
                f.write(privkey.save_pkcs1().decode())
        with open('public.pem','r') as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
        with open('private.pem','r') as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())
        return pubkey,privkey

    def encrypt(self,message):
        #加密
        message = rsa.encrypt(message.encode(), self.pubkey)
        message = b2a_hex(message)
        return message
    def decrypt(self,message):
        #解密
        message = a2b_hex(message)
        message = rsa.decrypt(message, self.privkey).decode()
        return message



def base64tojson(_base64):
    try:
        _base64 = base64.b64decode(_base64)
        result = json.loads(_base64)
        return result
    except Exception as e:
         raise OAuthError('数据错误 %s' % _base64)

def jsontobase64(_json):
    try:
        result = base64.b64encode( json.dumps(_json))
        return result
    except Exception as e:
         raise OAuthError('数据错误 %s' % _json)

class AppToken(object):

    """
        payload:{
        'owner':xxx,
        'client_id':xxx
        }
    """

    TOKEN_TIMEOUT = 640000
    HEADER = {
    "typ": "JWT",
    "alg": "HS256"
    }

    def get_token(self,payload,header=HEADER):

        owner = payload.get('owner','')
        if owner and Cache().get_redis(__conf__.CACHE_HOST).get(owner):
            Cache().get_redis(__conf__.CACHE_HOST).delete(owner)
        payload['start'] = time.time()

        payload = jsontobase64(payload)
        header = jsontobase64(header)
        sha_token= SignatureMethod_HMAC_SHA1().build_signature(payload,header)
        Cache().get_redis(__conf__.CACHE_HOST).setex(owner,sha_token, self.TOKEN_TIMEOUT)
        return payload+'.'+header,self.TOKEN_TIMEOUT

    def serialization(self,token):
        base64_payload = token.split('.')[0]
        base64_header = token.split('.')[-1]
        payload = base64tojson(base64_payload)
        header = base64tojson(base64_header)
        return payload,header

    def verify(self,token):
        base64_payload = token.split('.')[0]
        base64_header = token.split('.')[-1]
        payload = base64tojson(base64_payload)
        sha= SignatureMethod_HMAC_SHA1().build_signature(base64_payload,base64_header)
        tokentime = payload.get('start')
        owner = payload.get('owner')
        if owner and \
        sha == Cache().get_redis(__conf__.CACHE_HOST).get(owner) \
        and time.time()-float(tokentime)<self.TOKEN_TIMEOUT:
            return True ,'验证成功'
        else:
            return False ,'验证失败请重新授权'
    def remove(self):
        Cache().get_redis(__conf__.CACHE_HOST).delete(self.owner)
        return True

class Code(object):
    def set(self,owner):
        code = uuid.uuid1()
        Cache().get_redis(__conf__.CACHE_HOST).setex(code,owner, CACHE_TIMEOUT)
        return code
    def get(self,code):
        owner = Cache().get_redis(__conf__.CACHE_HOST).get(code)
        Cache().get_redis(__conf__.CACHE_HOST).delete(code)
        return owner