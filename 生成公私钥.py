from ecdsa import SigningKey, VerifyingKey, NIST256p
from ecdsa.util import sigdecode_der
import hashlib

# 生成私钥和公钥
sk = SigningKey.generate(curve=NIST256p)
# print(sk)
a=sk.to_string()
# print(a)
b=a.hex();
print("sk",b)
c=bytes.fromhex(b)
# print(c)
d=SigningKey.from_string(c,curve=NIST256p)
# print(d)

vk = sk.get_verifying_key()
s1=vk.to_string()
# print(s1)
s2=s1.hex()
print("vk",s2)
s3=bytes.fromhex(s2)
# print(s3)
s4=VerifyingKey.from_string(s3,curve=NIST256p)
# 签名消息
message = "This is a test message".encode()
print(message.decode())
hash_obj = hashlib.sha256(message).digest()
signature = d.sign(hash_obj)
print(signature)

# 验证签名
valid = s4.verify(signature, hash_obj)
print("Signature valid:", valid) # True
