import time
import hashlib

import grpc

from ams.thanos.v1 import cipher_pb2
from ams.thanos.v1.cipher_pb2_grpc import CipherServiceStub


class CipherClient(object):
    def __init__(self, addr, app_key, app_secret, authority=None, timeout=0.5, secure=False, **options):
        self._app_key = app_key
        self._app_secret = app_secret
        self.timeout = timeout

        channel_options = (
            ("grpc.keepalive_permit_without_calls", options.get('keepalive_permit_without_calls', True)),
            ("grpc.keepalive_time_ms", options.get('keepalive_time_ms', 30000)),
            ("grpc.http2.min_time_between_pings_ms", options.get('min_time_between_pings_ms', 60000)),
            ("grpc.http2.max_pings_without_data", options.get('max_pings_without_data', 50)),
        )
        if authority:
            channel_options = channel_options + (("grpc.default_authority", authority),)

        if secure:
            self.channel = grpc.secure_channel(addr, grpc.ssl_channel_credentials(), options=channel_options)
        else:
            self.channel = grpc.insecure_channel(addr, options=channel_options)
        self.stub = CipherServiceStub(self.channel)

    def hash(self, text, user_id, ip, multi=False):
        timestamp = int(time.time())
        request = cipher_pb2.HashRequest(text=text, user_id=user_id,
                                         ip=ip, multi=multi)
        signature = self.sign(request, timestamp)
        metadata = self._gen_metadata(signature, timestamp)
        return list(self.stub.Hash(request, timeout=self.timeout, metadata=metadata).texts)

    def hash_identity(self, text, user_id, ip):
        timestamp = int(time.time())
        request = cipher_pb2.HashIdentityRequest(text=text, user_id=user_id, ip=ip)
        signature = self.sign(request, timestamp)
        metadata = self._gen_metadata(signature, timestamp)
        return self.stub.HashIdentity(request, timeout=self.timeout, metadata=metadata).text

    def encrypt(self, text, user_id, ip):
        timestamp = int(time.time())
        request = cipher_pb2.EncryptRequest(text=text, user_id=user_id, ip=ip)
        signature = self.sign(request, timestamp)
        metadata = self._gen_metadata(signature, timestamp)
        return self.stub.Encrypt(request, timeout=self.timeout, metadata=metadata).text

    def decrypt(self, text, user_id, ip, mode=cipher_pb2.MASK, text_type=cipher_pb2.PHONE):
        timestamp = int(time.time())
        request = cipher_pb2.DecryptRequest(text=text, user_id=user_id,
                                            ip=ip, mode=mode,
                                            text_type=text_type)
        signature = self.sign(request, timestamp)
        metadata = self._gen_metadata(signature, timestamp)
        return self.stub.Decrypt(request, timeout=self.timeout, metadata=metadata).text

    def batch_encrypt(self, texts, user_id, ip):
        timestamp = int(time.time())
        request = cipher_pb2.BatchEncryptRequest(texts=texts, user_id=user_id, ip=ip)
        signature = self.sign(request, timestamp)
        metadata = self._gen_metadata(signature, timestamp)
        return list(self.stub.BatchEncrypt(request, timeout=self.timeout, metadata=metadata).texts)

    def batch_decrypt(self, texts, user_id, ip, mode=cipher_pb2.MASK, text_type=cipher_pb2.PHONE):
        timestamp = int(time.time())
        request = cipher_pb2.BatchDecryptRequest(texts=texts, user_id=user_id,
                                                 ip=ip, mode=mode,
                                                 text_type=text_type)
        signature = self.sign(request, timestamp)
        metadata = self._gen_metadata(signature, timestamp)
        return list(self.stub.BatchDecrypt(request, timeout=self.timeout, metadata=metadata).texts)

    def batch_hash(self, texts, user_id, ip, multi=False):
        timestamp = int(time.time())
        request = cipher_pb2.BatchHashRequest(texts=texts, multi=multi, user_id=user_id, ip=ip)
        signature = self.sign(request, timestamp)
        metadata = self._gen_metadata(signature, timestamp)
        batch_response = self.stub.BatchHash(request, timeout=self.timeout, metadata=metadata)
        return [list(resp.texts) for resp in batch_response.results]

    def sign(self, request, timestamp):
        field_names = sorted([field.name for field in request.DESCRIPTOR.fields] +
                             ['app_key', 'timestamp'])
        param_parts = []
        for field_name in field_names:
            if field_name == 'timestamp':
                field_value = timestamp
            elif field_name == 'app_key':
                field_value = self._app_key
            elif field_name == 'texts':
                field_value = ",".join(request.texts)
            else:
                field_value = getattr(request, field_name)
            param_parts.append('{}={}'.format(field_name, field_value))
        param_string = '&'.join(param_parts)
        m = hashlib.md5()
        m.update((param_string + self._app_secret).encode('utf-8'))
        signature = m.hexdigest()
        return signature

    def _gen_metadata(self, signature, request_timestamp):
        metadata = (('app-key', self._app_key),
                    ('signature', signature),
                    ('timestamp', str(request_timestamp)))
        return metadata

    def close(self):
        self._close()

    def _close(self):
        self.channel.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()
