Sign and verify data or messages using RSA cryptography.

Optionally exchange signed data via QR codes.

# Usage

1. create and store an RSA keypair (default key length 1024 bits)
1. sign a message using the private key, store the signature (binary data, SHA-256 hash)
1. verify the message using the public key and signature

```sh
python QRSA.py create --out priv.key --pubout pub.key
python QRSA.py sign   --message "Joost K;2021-01-22;My Company" --key priv.key --out signature.bin
python QRSA.py verify --message "Joost K;2021-01-22;My Company" --key pub.key --sig signature.bin
```
```
SHA-256
```

If one changes the message (or signature), verification fails:

```sh
python QRSA.py verify --message "Joost K;2021-01-23;My Company" --key pub.key --sig signature.bin
```
```
VerificationError: Verification failed
```

You can also store the message + signature combined in a binary QR code:

```sh
python QRSA.py signqr --message "Joost K;2021-01-22;My Company" --key priv.key
```
```

    █▀▀▀▀▀█ █▄▀▀█ ▄▄█ █▄▀ ▀██▀█▄▀▄ ▀▄██▀██ ▀▄ █▄  █▀▀▀▀▀█
    █ ███ █ ▀█▄▀ ▀█▄▄▀█▀▀██▄██▄ ▀▄▀▀██▀▄ ▄▀ ▀▄▄▀▄ █ ███ █
    █ ▀▀▀ █ ▀▀▄▄ █████▀█▀▄ ▀█▀▀▀█▀ ▀▀   ▀▀█▄▄▄█   █ ▀▀▀ █
    ▀▀▀▀▀▀▀ ▀▄▀▄▀ ▀ █▄█ █ ▀ █ ▀ █▄█ █▄▀ ▀ ▀ ▀ █▄█ ▀▀▀▀▀▀▀
    █▄▄▀██▀█▀██ ▀▀▄██▄█▄ █▄ █▀▀▀█▀ ▀██ ▄█▀█ ▀██▄▀▀▄ █▄█▀▀
    ▄▄█▀ ▄▀ █ ▄ ▄█▄█▄▀ ▄▀  ▀█▄▀██▀▀▄ ▄█ ██ ▀▀█ █▄▀▀▄▀█▀
    ▄ ▀▄▀▀▀▄▄▄▄▄▀ █▄▄█▀█▄▄  █▄█▀▄ █ ▀▀█▀ ▀██▄▄█▀▀█▀ ▄▀▄▀
    ▄██▄▄ ▀██  ▀▀ ▀▄▀ █▀▄▄▄█▄▀█▄▄▄▀▀▄ ▀▀▄▀  ▀▄▀ ▀ ██ ▄ █
    ▀▄█ █ ▀  █ ▄ █ ▄█▀▄  ▄▄▄ █▀▀▄▄█▄██▀▀  █ ▄ ██▄ ▄ ██▀█▀
    ▀▄▄▄ ▀▀▀▀█▀▄█▀▄▀▀▄▄   ▄▀▄▄▄▄█   ▀▀ █▀██▄█▄  ▀▄█ ▀██ ▀
    ▀▄▄ ▀█▀█▀█▀█▀█ █▄▀▀▄  ▄▀▄▄▀▀▄ ▄██▀▄ ▀▀▄███ ██ █ ▀██▄
    ▄█▀▀▀ ▀▀ ▄▀ ▀ ▀▀ ▀▄ ▄▀ ▀▀▀▀ ▀▀▄▄▄▄▀█▀▄▄▀█ ▄  █ █▀ ▀▄▀
     █  █▀▀▀█▄▀▀█▄  ▄ ▀▄  ███▀▀▀█▄▀██▀█▄ ▀▄▀▄▀█▄█▀▀▀█▀  ▄
       ▀█ ▀ █▄▄▄ █ ██▀██ ▀▄██ ▀ █▄██▄██▄▄▀█ █▄▀▄█ ▀ █▄█▄▀
    ▀██▄█▀▀▀▀▄▄ ▀ ▀▀▄▄  ▀▄▀▀▀▀██▀▀   █▀▄█▀▀ ▄▀▄▀▀▀█▀█  ▀▄
      ▀▄▀ ▀ ▄███ ▄▀▀▀▀▀▄▀█ ▄▄▄ ▄▀█ ▀▀ ▀▄ ▄ ▄█▀ ▄█▀  ▄ █▄▀
    ▀▄█▀ ▄▀█▄▀▀▄ ▄▄███▄█▄▄▀▄▀ ██ ▄ ██ ▀▄ ▀▀  ▄ ██▀██▄ ▀▀
    ▀█▀█▀▄▀▀██▄▄█ ▄▀█▄  ▀█▄█▄ ▄▀▄██▄▀ ▀▄▀▄█ ▀ ██▄ ▄▄▄█▀▀█
    ▄▀ ▄▀ ▀▄  ▀▄ █ ▀▄▀▀▀ ▄▄▄▀ █ ▀▀▄ █▀ █▀▀  ██  █▄███▄ ▄█
    ▀▀█▀▀ ▀ ▀▀█▄▀ █▀  ▄▀▀██  ▄▀▀ █ ▄█ █▄ █  ▄  ▄▀██ ███▄▄
    █▀ ▀▀▄▀█▄▀██ ▄▄ ▄ ▀▀▀█▄█▀███ ▄▀▄  ▄▀▀▄▄▄▀  █ ▄▀▀██▄██
    ▀█▄▀▀▀▀█▀▀▄▄█▄▄▀█▀▀  ▄█▀█▄▄  ▄▀  █ █▄▄▀▀ ██  ▄██ █▀▀
       ▀  ▀▀█▄▀▀  █ ▀▄██▄██▄█▀▀▀█▄▀█▄ ▄▀▀ █ █  ██▀▀▀█▄ █▀
    █▀▀▀▀▀█ █▄▀▄   ▄█▄█▀▄ ▀██ ▀ █ █▀ ███ ▀ ▄█▀█▀█ ▀ ██ ▄▄
    █ ███ █ █▄▀ █▀ █▄ ██   ███▀▀█▄▄ █   ▀▄ ▄█▄█ ▀▀███▄▄ █
    █ ▀▀▀ █   ▀▄█▀▀▄  █▀▀ ▄ ▀  ██ ▄█   ▄▀▀██ ▄▄ ██▄ ▀██▀▄
    ▀▀▀▀▀▀▀ ▀▀      ▀▀ ▀   ▀ ▀▀▀  ▀▀▀ ▀  ▀ ▀ ▀   ▀▀

```

The generated barcode cannot be read back and verified, yet. 
We plan on using opencv `cv2.QRCodeDetector()` for this.