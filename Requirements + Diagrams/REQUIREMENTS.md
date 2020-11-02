# Requirements analysis

## 1. Introduction
### 1.1 Application's overview
Mechanism that allows a user to have the email server extract emails that contain a particular keyword, while the email server and other parties excluding said user _do not_ learn anything else about the email.
### 1.2 Actors
- The end user
- The public key system
- The message
- The encypted message
- The trapdoor
- The email server

### 1.3 Possible clients
- Any company which needs to communicate secrets over a text communication medium.

## 2. Use case
### 2.1 Encryption
The end user can send an encrypted mail using the recipient's public key.
### 2.2 Decryption
The end user can decrypt recieved mails using it's own private key.
### 2.3 Specify keywords
The end user can specify keywords to filter the mails by them, without decrypting their content.
