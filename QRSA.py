#!/bin/env python3

import sys

import argh
import rsa


def fwrite(filename, content):
    with open(filename, mode="wb") as fh:
        fh.write(content)


def fread(filename):
    with open(filename, mode="rb") as fh:
        return fh.read()


def get_message(data, message):
    if data is None:
        if message is None:
            if sys.stdin.isatty():
                raise argh.CommandError("data/message/STDIN required")

            else:
                message = sys.stdin.buffer.read()

        elif hasattr(message, "encode"):
            message = message.encode()

    else:
        message = fread(data)

    return message


def create(size=1024, out=None, pubout=None):
    """
    Create a new RSA key.
    """
    pubkey, privkey = rsa.newkeys(size)
    privkey_pkcs = privkey.save_pkcs1()

    if pubout:
        fwrite(pubout, pubkey.save_pkcs1())

    if out:
        fwrite(out, privkey_pkcs)

    else:
        return privkey_pkcs[:-1]


@argh.arg("--key", "-k", required=True)
@argh.wrap_errors([ValueError, rsa.pkcs1.VerificationError])
def sign(data=None, message=None, out=None, key=None, hash_method='SHA-256'):
    """
    Sign a message or data file/stream.
    """
    privkey = rsa.PrivateKey.load_pkcs1(fread(key))
    message = get_message(data, message)
    signature = rsa.sign(message, priv_key=privkey, hash_method=hash_method)

    if out:
        fwrite(out, signature)

    else:
        return signature


def load_pubkey(data):
    """
    Assume data contains pkcs1 PEM notation of a public key.
    Or take it as private key and create public key from it.
    """
    try:
        return rsa.PublicKey.load_pkcs1(data)
    except ValueError:
        key = rsa.PrivateKey.load_pkcs1(data)
        return rsa.PublicKey(key.n, key.e)


@argh.arg("--sig", "-s", required=True)
@argh.arg("--key", "-k", required=True)
@argh.wrap_errors([ValueError, rsa.pkcs1.VerificationError])
def verify(data=None, message=None, sig=None, key=None):
    """
    Verify a message or data file/stream.
    """
    pubkey = load_pubkey(fread(key))
    signature = fread(sig)
    message = get_message(data, message)

    return rsa.verify(message, signature, pubkey)


@argh.arg("--key", "-k", required=True)
@argh.wrap_errors([ValueError, rsa.pkcs1.VerificationError])
def signqr(data=None, message=None, out=None, key=None, hash_method='SHA-256'):
    """
    Sign a message or data file/stream and wrap it into a QR code.
    """
    import qrcode

    message = get_message(data, message)
    signature = sign(message=message, key=key, hash_method=hash_method)

    payload = message + signature
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(payload)
    qr.make()

    if out:
        if out.endswith(".txt"):
            with open(out, "w") as fh:
                qr.print_ascii(out=fh)

        else:
            img = qr.make_image()
            img.save(out)

    else:
        qr.print_tty()


def gen_power(base, power=1):
    while True:
        yield base ** power
        power += 1


def extract_payload(payload, size):
    if len(payload) < size:
        raise ValueError(f"payload smaller than {size}")

    return payload[:-size], payload[-size:]


@argh.arg("--qr", required=True)
@argh.arg("--key", "-k", required=True)
@argh.wrap_errors([rsa.pkcs1.VerificationError, ValueError])
def verifyqr(qr=None, size=0, key=None):
    """
    Verify a QR code, given the public key.
    """
    pubkey = load_pubkey(fread(key))


    # https://www.thepythoncode.com/article/generate-read-qr-code-python

    import cv2
    detector = cv2.QRCodeDetector()

    img = cv2.imread(qr)
    data, bbox, _ = detector.detectAndDecode(img)

    if bbox is None or not data:
        raise ValueError("no QR in this image")

    payload = data

    if size:
        message, signature = extract_payload(payload, size)
        return rsa.verify(message, signature, pubkey)

    # without --size, try the first 16 binary powers
    for pow in range(2, 16):
        size = 2 ** pow

        try:
            message, signature = extract_payload(payload, size)
            return rsa.verify(message, signature, pubkey)
        except ValueError:
            raise rsa.pkcs1.VerificationError("Verification failed or try provide --size")
        except rsa.pkcs1.VerificationError:
            pass

    else:
        raise rsa.pkcs1.VerificationError("provide --size")


if __name__ == "__main__":
    argh.dispatch_commands([create, sign, verify, signqr])
