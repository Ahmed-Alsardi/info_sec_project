# info_sec_project

- Encryption

  - encryption context
  - init(is_new_user:bool, password:str)
  - 1: encrypt(plaintext)
  - 2: decrypt(ciphertext)
- DB:
  - add_user(username:str, password:str)
  - get_user_by_username(username:str)
  - add_user_public_key(username:str, public_key:str)
  - get_user_public_key(username:str)
  - send_user_message(from:str, message:str, file_type:str, to:str, session_key:bytes)
  - get_user_messages(username:str)
  - get_user_messages_by_id(username:str, message_id:str)


