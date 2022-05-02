from Crypto import Random
from Crypto.PublicKey import RSA
import base64, os
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP


def assymetric_generate_keys():
   modulus_length = 256*4
   privatekey = RSA.generate(modulus_length, Random.new().read)
   publickey = privatekey.publickey()
   return privatekey, publickey

def assymetric_encrypt_message(a_message , publickey):
	encryptor = PKCS1_OAEP.new(publickey)
	encrypted_msg = encryptor.encrypt(a_message)
    # encrypted_msg = publickey.encrypt(a_message, 32)[0]
	encoded_encrypted_msg = base64.b64encode(encrypted_msg)
	return encoded_encrypted_msg

def assymetric_decrypt_message(encoded_encrypted_msg, privatekey):
	decryptor = PKCS1_OAEP.new(privatekey)
	decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	decoded_decrypted_msg = decryptor.decrypt(decoded_encrypted_msg)
	# decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
	return decoded_decrypted_msg


def symmetric_generate_key():
	AES_key_length = 16
	secret_key = os.urandom(AES_key_length)
	encoded_secret_key = base64.b64encode(secret_key)
	return encoded_secret_key

def symmetric_encrypt_message(private_msg, encoded_secret_key, padding_character):
	secret_key = base64.b64decode(encoded_secret_key)
	iv = os.urandom(16)
	cipher = AES.new(secret_key,AES.MODE_CBC,IV=iv)
	padded_private_msg = private_msg + (padding_character * ((16-len(private_msg)) % 16))
	encrypted_msg = cipher.encrypt(padded_private_msg.encode())
	encrypted_msg_with_iv = encrypted_msg+iv
	encoded_encrypted_msg = base64.b64encode(encrypted_msg_with_iv)
	return encoded_encrypted_msg

def symmetric_decrypt_message(encoded_encrypted_msg, encoded_secret_key, padding_character):
	secret_key = base64.b64decode(encoded_secret_key)
	encrypted_msg_with_iv = base64.b64decode(encoded_encrypted_msg)
	encrypted_msg = encrypted_msg_with_iv[:-16]
	iv = encrypted_msg_with_iv[-16:]
	cipher = AES.new(secret_key,AES.MODE_CBC, iv)
	decrypted_msg = cipher.decrypt(encrypted_msg).decode()
	unpadded_private_msg = decrypted_msg.rstrip(padding_character)
	return unpadded_private_msg