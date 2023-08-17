# (c) Copyright (c) 2018-2023 Microchip Technology Inc. and its subsidiaries.
#
# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.
#
# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
# PARTICULAR PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT,
# SPECIAL, PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE
# OF ANY KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF
# MICROCHIP HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE
# FORESEEABLE. TO THE FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL
# LIABILITY ON ALL CLAIMS IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED
# THE AMOUNT OF FEES, IF ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR
# THIS SOFTWARE.
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

from cffi import VerificationError
from fastapi import File, UploadFile
from fastapi.routing import APIRouter
from tpds.manifest import Manifest, ManifestIterator

router = APIRouter()


def decoder(manifest, certificate_file):
    if not isinstance(manifest, list):
        raise ValueError("Unsupported manifest format to process")

    if len(manifest) <= 0:
        raise ValueError("The Manifest file has no record")

    manifest_iterator = ManifestIterator(manifest)
    decoded = []
    # Process all the entries in the manifest
    while manifest_iterator.index != 0:
        se = Manifest().decode_manifest(manifest_iterator.__next__(), certificate_file)
        if se == {}:
            raise VerificationError("Verification is failed")
        decoded.append(se)

    return decoded


@router.post("/decode/")
async def manifest_decode(
    manifest_file: UploadFile = File(...), certificate_file: Optional[UploadFile] = File(None)
):
    try:
        manifest = json.load(manifest_file.file)

        certificate_list = []
        if certificate_file:
            # custom certificate
            contents = await certificate_file.read()
            certificate = NamedTemporaryFile("wb", delete=False)
            Path(certificate.name).write_bytes(contents)
            certificate_list.append(certificate.name)
        else:
            # MCHP signer certificates
            path = os.path.join(os.path.dirname(__file__), "MCHP_manifest_signer")
            for cert_file in os.listdir(path):
                certificate_list.append(os.path.join(path, cert_file))

        result = None
        for certificate in certificate_list:
            try:
                result = decoder(manifest, certificate)
                break  # Since the verification is complete, breaking the loop
            except VerificationError:
                continue
            except Exception as exp:
                return {"message": "Error", "data": f"Manifest decoding is failed with: {exp}"}

        if result is None:
            return {
                "message": "Verification is failed",
                "data": "Verification of SignedSecureElement objects failed. Check Manifest Signer Certificate and try again.",
            }
        return {"message": "Success", "data": json.dumps(result)}

    except Exception as exp:
        return {"message": "Error", "data": f"Manifest decoding is failed with: {exp}"}
