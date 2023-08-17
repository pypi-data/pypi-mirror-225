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
from typing import Tuple
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from .certs_common import (
            get_backend, update_x509_certificate,
            random_cert_sn)
from .ext_builder import ExtBuilder


def create_wpc_root_cert(
        ca_private_key: ec.EllipticCurvePrivateKey,
        root_cn: str,
        root_sn: int
) -> Tuple[ec.EllipticCurvePrivateKeyWithSerialization, x509.Certificate]:
    """
    Create a root CA certificate that looks like the WPCCA1 real
    root, but with a different key for testing purposes.
    """
    # Look for root certificate
    certificate = None

    # Build new certificate
    builder = ExtBuilder()
    if root_sn:
        builder = builder.serial_number(root_sn)
    else:
        builder = builder.serial_number(random_cert_sn(8))
    builder = builder.subject_name(x509.Name([x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, root_cn)]))
    builder = builder.issuer_name(builder._subject_name)  # Names are the same for a self-signed certificate
    builder = builder.not_valid_before(datetime(2021, 3, 3, 16, 4, 1, tzinfo=timezone.utc))
    builder = builder.not_valid_after(datetime(9999, 12, 31, 23, 59, 59, tzinfo=timezone.utc))
    builder = builder.public_key(ca_private_key.public_key())
    builder = builder.add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)

    # Sign certificate with its own key
    certificate_new = builder.sign(
                            private_key=ca_private_key,
                            algorithm=hashes.SHA256(),
                            backend=get_backend())

    certificate = update_x509_certificate(certificate, certificate_new)

    return certificate
