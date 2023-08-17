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

from pydantic import BaseModel
from typing import Optional


class WPCRootCertParams(BaseModel):
    # Mfg cert ca key
    ca_key: str
    # Root cert Common Name
    root_cn: Optional[str] = 'WPCCA1'
    # Root cert serial number - 8 bytes, Use 0 to generare random value
    root_sn: Optional[int] = 0x776112B411479AAC


class WPCMfgCertParams(BaseModel):
    # Mfg cert ca key
    ca_key: str
    # Mfg cert ca certificate
    ca_cert: str
    # Mfg cert PTMC value
    ptmc: Optional[int] = 0x010B
    # Mfg cert Sequence ID value - 1 byte
    sequence_id: Optional[int] = 0x01
    # Mfg cert Qi Policy value - 4 bytes
    qi_policy: Optional[int] = 0x00000001


class WPCPucCertParams(BaseModel):
    # PUC cert ca key
    ca_key: str
    # PUC cert ca certificate
    ca_cert: str
    # PUC cert Qi ID value (:06d in cert)
    qi_id: Optional[int] = 11430
    # PUC cert RSID value (9 bytes in cert)
    rsid: Optional[int] = 1
