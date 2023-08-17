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

from fastapi.routing import APIRouter
from cryptography import x509
from cryptography.hazmat.primitives import serialization

from .certs_common import get_backend, create_eccp256_key_pair
from .wpc_root import create_wpc_root_cert
from .wpc_mfg import create_wpc_mfg_cert
from .wpc_puc import create_wpc_puc_cert

from .certs_schema import WPCRootCertParams, WPCMfgCertParams, WPCPucCertParams

router = APIRouter(prefix="/wpc", tags=["wpc_tag"])


@router.post('/create_root_cert')
def create_root_cert(
    root_cert_params: WPCRootCertParams
) -> dict :
    """
    Creates a fake WPCCA1 root CA for template and testing purposes

    Parameters
    ----------

        root_cert_params (WPCRootCertParams):       Pydantic WPCRootCertParams instance

    Returns
    -------

        Returns root key and root certificate string encoded in ASN.1 PEM
    """
    # Load CA private key
    if root_cert_params.ca_key == '':
        ca_key = create_eccp256_key_pair()
    else:
        ca_key = serialization.load_pem_private_key(
                                data=root_cert_params.ca_key.encode(),
                                password=None,
                                backend=get_backend())

    # Create root key pair and root certificate
    root_certificate = create_wpc_root_cert(
                            ca_private_key=ca_key,
                            root_cn=root_cert_params.root_cn,
                            root_sn=root_cert_params.root_sn)

    # Convert to transferable bytes
    root_private_key_str = ca_key.private_bytes(
                                encoding=serialization.Encoding.PEM,
                                format=serialization.PrivateFormat.PKCS8,
                                encryption_algorithm=serialization.NoEncryption()).decode()
    # Convert to transferable bytes
    root_certificate_str = root_certificate.public_bytes(encoding=serialization.Encoding.PEM).decode()

    return {
            "priv_key": root_private_key_str,
            "certificate": root_certificate_str
            }


@router.post('/create_mfg_cert')
def create_mfg_cert(
    mfg_cert_params: WPCMfgCertParams
) -> dict:

    """
    Create a test WPC manufacturer CA certificate

    Parameters
    ----------

        mfg_cert_params (WPCMfgCertParams):       Pydantic WPCMfgCertParams instance

    Returns
    -------

        Returns key and mfg certificate string as dict
    """
    # Load CA private key
    ca_private_key = serialization.load_pem_private_key(
                                data=mfg_cert_params.ca_key.encode(),
                                password=None,
                                backend=get_backend())

    # Load CA certificate
    ca_certificate = x509.load_pem_x509_certificate(mfg_cert_params.ca_cert.encode(), backend=get_backend())

    # Create a private keypair for WPC manufacturer CA certificate
    wpc_mfg_ca_priv_key = create_eccp256_key_pair()
    # Extract public key from private keypair
    wpc_mfg_ca_pub_key = wpc_mfg_ca_priv_key.public_key()
    # Create a certificate with specified parameters
    wpc_mfg_ca_certificate = create_wpc_mfg_cert(
                                ptmc=mfg_cert_params.ptmc,
                                sequence_id=mfg_cert_params.sequence_id,
                                qi_policy=mfg_cert_params.qi_policy,
                                public_key=wpc_mfg_ca_pub_key,
                                ca_private_key=ca_private_key,
                                ca_certificate=ca_certificate)
    # Convert to transferable bytes
    wpc_mfg_ca_priv_key_str = wpc_mfg_ca_priv_key.private_bytes(
                                encoding=serialization.Encoding.PEM,
                                format=serialization.PrivateFormat.PKCS8,
                                encryption_algorithm=serialization.NoEncryption()).decode()
    # Convert to transferable bytes
    wpc_mfg_ca_certificate_str = wpc_mfg_ca_certificate.public_bytes(encoding=serialization.Encoding.PEM).decode()
    return {
            "priv_key": wpc_mfg_ca_priv_key_str,
            "certificate": wpc_mfg_ca_certificate_str
        }


@router.post('/create_puc_cert')
def create_puc_cert(
    puc_cert_params: WPCPucCertParams
) -> dict:
    """
    Create a test WPC product unit certificate

    Parameters
    ----------

        puc_cert_params (WPCPucCertParams):       Pydantic WPCPucCertParams instance

    Returns
    -------

        Returns key and product certificate string encoded in ASN.1 PEM
    """
    # Load CA private key
    ca_private_key = serialization.load_pem_private_key(
        data=puc_cert_params.ca_key.encode(),
        password=None,
        backend=get_backend()
    )
    # Load CA certificate
    ca_certificate = x509.load_pem_x509_certificate(
        data=puc_cert_params.ca_cert.encode(),
        backend=get_backend()
    )
    # Create a private keypair for WPC product unit certificate
    wpc_product_unit_priv_key = create_eccp256_key_pair()
    # Extract public key from private keypair
    wpc_product_unit_pub_key = wpc_product_unit_priv_key.public_key()
    # Create a certificate with specified parameters
    wpc_product_unit_cert = create_wpc_puc_cert(
        qi_id=puc_cert_params.qi_id,
        rsid=puc_cert_params.rsid,
        public_key=wpc_product_unit_pub_key,
        ca_private_key=ca_private_key,
        ca_certificate=ca_certificate
    )
    # Convert to transferable bytes
    wpc_product_unit_priv_key_str = wpc_product_unit_priv_key.private_bytes(
                                encoding=serialization.Encoding.PEM,
                                format=serialization.PrivateFormat.PKCS8,
                                encryption_algorithm=serialization.NoEncryption()).decode()
    # Convert to transferable bytes
    wpc_product_unit_cert_str = wpc_product_unit_cert.public_bytes(encoding=serialization.Encoding.PEM).decode()
    return {
            "priv_key": wpc_product_unit_priv_key_str,
            "certificate": wpc_product_unit_cert_str
            }

