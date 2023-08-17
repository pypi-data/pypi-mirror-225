# (c) 2021 Microchip Technology Inc. and its subsidiaries.

# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.

# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS".  NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR
# PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL,
# PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY
# KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP
# HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
# FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
# ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
# THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.

import os
import cryptography
import asn1crypto.csr
import asn1crypto.x509

from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from .ext_builder import ExtBuilder
from .timefix_backend import backend

_backend = None
def get_backend():
    """
    Gets backend from time fix backend file
    """
    global _backend
    if not _backend:
        _backend = backend
    return _backend


def create_eccp256_key_pair() -> ec.EllipticCurvePrivateKey:
    """
    Create a new ECC P256 key, returns ecc private key object
    and private key bytes with specified encoding style.

    Args:
        None

    Returns:
        eccp256r1 keyobject
    """
    # Generate new ECC P256 private key
    priv_key = ec.generate_private_key(
        curve=ec.SECP256R1(),
        backend=get_backend())
    return priv_key


def random_cert_sn(size: int)-> int:
    """
    Create a positive, non-trimmable serial number for X.509 certificates

    Args:
        size (int):             Serial number size in bytes.

    Returns:
        int: Serial number
    """
    raw_sn = bytearray(os.urandom(size))
    raw_sn[0] = raw_sn[0] & 0x7F # Force MSB bit to 0 to ensure positive integer
    raw_sn[0] = raw_sn[0] | 0x40 # Force next bit to 1 to ensure the integer won't be trimmed in ASN.1 DER encoding
    return int.from_bytes(raw_sn, byteorder='big', signed=False)


def pubkey_cert_sn(size: int, builder: ExtBuilder) -> int:
    """
    Cert serial number is the SHA256(Subject public key + Encoded dates)

    Args:
        size (int):             Serial number size in bytes.
        builder (ExtBuilder):   ExtBuilder instance.

    Returns:
        int: Serial number
    """

    # Get the public key as X and Y integers concatenated
    pub_nums = builder._public_key.public_numbers()
    pubkey =  pub_nums.x.to_bytes(32, byteorder='big', signed=False)
    pubkey += pub_nums.y.to_bytes(32, byteorder='big', signed=False)

    # Get the encoded dates
    expire_years = builder._not_valid_after.year - builder._not_valid_before.year
    if builder._not_valid_after.year == 9999:
        expire_years = 0 # This year is used when indicating no expiration
    elif expire_years > 31:
        expire_years = 1 # We default to 1 when using a static expire beyond 31

    enc_dates = bytearray(b'\x00'*3)
    enc_dates[0] = (enc_dates[0] & 0x07) | ((((builder._not_valid_before.year - 2000) & 0x1F) << 3) & 0xFF)
    enc_dates[0] = (enc_dates[0] & 0xF8) | ((((builder._not_valid_before.month) & 0x0F) >> 1) & 0xFF)
    enc_dates[1] = (enc_dates[1] & 0x7F) | ((((builder._not_valid_before.month) & 0x0F) << 7) & 0xFF)
    enc_dates[1] = (enc_dates[1] & 0x83) | (((builder._not_valid_before.day & 0x1F) << 2) & 0xFF)
    enc_dates[1] = (enc_dates[1] & 0xFC) | (((builder._not_valid_before.hour & 0x1F) >> 3) & 0xFF)
    enc_dates[2] = (enc_dates[2] & 0x1F) | (((builder._not_valid_before.hour & 0x1F) << 5) & 0xFF)
    enc_dates[2] = (enc_dates[2] & 0xE0) | ((expire_years & 0x1F) & 0xFF)
    enc_dates = bytes(enc_dates)

    # SAH256 hash of the public key and encoded dates
    digest = hashes.Hash(hashes.SHA256(), backend=cryptography.hazmat.backends.default_backend())
    digest.update(pubkey)
    digest.update(enc_dates)
    raw_sn = bytearray(digest.finalize()[:size])
    raw_sn[0] = raw_sn[0] & 0x7F # Force MSB bit to 0 to ensure positive integer
    raw_sn[0] = raw_sn[0] | 0x40 # Force next bit to 1 to ensure the integer won't be trimmed in ASN.1 DER encoding
    return int.from_bytes(raw_sn, byteorder='big', signed=False)


def is_key_file_password_protected(pem_data: bytes) -> bool:
    """
    Takes Private Key bytes encoded in PEM format and
    checks if it is encryted

    Args:
        pem_data (int):     Private key data encoded in bytes

    Returns:
        bool: True if the key is encrypted, False if it is nots
    """
    try:
        serialization.load_pem_private_key(data=pem_data, password=None, backend=get_backend())
        return False
    except TypeError:
        return True


def update_x509_certificate(
                certificate: x509.Certificate,
                certificate_new: x509.Certificate) -> x509.Certificate:
    """
    Compare the TBS portion of two X.509 certificates and save the new
    certificate (PEM format) if the TBS has changed.

    Args:
        certificate (x509.Certificate): Primary certificate
        certificate_new (x509.Certificate): New certificate

    Returns:
        x509.Certificate: Updated cerificate
    """
    is_new = False
    if certificate:
        # Check to see if the certificate has changed from what was saved
        certificate_tbs = asn1crypto.x509.Certificate.load(
            certificate.public_bytes(encoding=serialization.Encoding.DER))['tbs_certificate']
        certificate_new_tbs = asn1crypto.x509.Certificate.load(
            certificate_new.public_bytes(encoding=serialization.Encoding.DER))['tbs_certificate']
        is_new = (certificate_tbs.dump() != certificate_new_tbs.dump())
    else:
        is_new = True

    # Check if there is a difference
    if is_new:
        # Load the updated certificate
        certificate = certificate_new
    return certificate


def update_csr(
                csr,
                csr_new,
                encoding: serialization.Encoding):
    """
    Compare the certificationRequestInfo portion of two CSRs and save the new
    CSR (PEM format) if the certificationRequestInfo has changed.

    Args:
        csr (?): Primary csr
        csr_new (?): New csr
        encoding (serialization.Encoding): Encoding style
                                            (serialization.Encoding.DER
                                            or serialization.Encoding.PEM)

    Returns:
        ?: Updated CSR
    """
    is_new = False
    if csr:
        # Check to see if the CSR has changed from what was saved
        csr_cri = asn1crypto.csr.CertificationRequest.load(
            csr.public_bytes(encoding=serialization.Encoding.DER))['certification_request_info']
        csr_new_cri = asn1crypto.csr.CertificationRequest.load(
            csr_new.public_bytes(encoding=serialization.Encoding.DER))['certification_request_info']
        is_new = (csr_cri.dump() != csr_new_cri.dump())
    else:
        is_new = True

    if is_new:
        # Load the updated CSR
        csr = csr_new
    return csr

