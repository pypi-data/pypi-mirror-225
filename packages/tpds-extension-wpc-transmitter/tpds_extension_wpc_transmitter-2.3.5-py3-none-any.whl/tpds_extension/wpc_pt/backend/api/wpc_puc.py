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

from datetime import datetime, timezone
from typing import Optional
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from .certs_common import get_backend, pubkey_cert_sn
from .ext_builder import ExtBuilder, TimeFormat


def create_wpc_puc_cert(
        qi_id: int,
        rsid: int,
        public_key: ec.EllipticCurvePublicKey,
        ca_private_key: ec.EllipticCurvePrivateKey,
        ca_certificate: x509.Certificate,
        old_certificate: Optional[x509.Certificate] = None
) -> x509.Certificate:
    builder = ExtBuilder()
    builder = builder.issuer_name(ca_certificate.subject)
    if old_certificate:
        builder = builder.not_valid_before(old_certificate.not_valid_before, format=TimeFormat.GENERALIZED_TIME)
    else:
        # Force times to use generalized time regardless of year so there are no issues at the 2050 transition
        builder = builder.not_valid_before(
            datetime.utcnow().replace(tzinfo=timezone.utc, minute=0, second=0),
            format=TimeFormat.GENERALIZED_TIME
        )
    builder = builder.not_valid_after(
        datetime(year=9999, month=12, day=31, hour=23, minute=59, second=59, tzinfo=timezone.utc)
    )
    builder = builder.public_key(public_key)
    builder = builder.serial_number(pubkey_cert_sn(8, builder))
    builder = builder.subject_name(
        x509.Name([
            x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, f'{qi_id:06d}')
        ])
    )
    # Raw RSID value is stored as big endian bytes in the certificate extension
    rsid_bytes = rsid.to_bytes(9, byteorder='big', signed=False)
    # Extension is an octet string (tag 0x04)
    rsid_extension_value = bytes([0x04, len(rsid_bytes)]) + rsid_bytes
    builder = builder.add_extension(
        x509.UnrecognizedExtension(x509.ObjectIdentifier('2.23.148.1.2'), rsid_extension_value),
        critical=True
    )

    # Sign certificate
    certificate = builder.sign(
        private_key=ca_private_key,
        algorithm=hashes.SHA256(),
        backend=get_backend()
    )

    return certificate
