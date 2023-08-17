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
from typing import List, Mapping, Optional, Sequence

from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel

from tpds.usecase_collector.collector import Collector
from tpds.usecase_collector.usecase import UsecaseEntrypoint

usecase_router = APIRouter()

Collector().add_usecase(
    UsecaseEntrypoint(
        path=None,
        root=os.path.dirname(__file__),
        name="atecc608_tflx_config",
        title="ATECC608B-TFLXTLS Configurator",
        entry="ECC608 TFLXTLS Configurator.html",
        applications=["configurator"],
        devices=["ATECC608B-TFLXTLS"],
    )
)


class UsecaseDetails(BaseModel):
    # Usecase Name
    name: Optional[str]
    # Usecase Title
    title: Optional[str]
    # Usecase Comment
    description: Optional[str]
    # Application types that apply to the usecase
    applications: Optional[Sequence[str]]
    # Devices supported by the usecase
    devices: Optional[Sequence[str]]
    # Boards supported by the usecase
    boards: Optional[Sequence[str]]


_usecase_icon_responses = {
    200: {
        "content": {
            "image/png": {},
            "image/jpeg": {},
            "image/vnd.microsoft.icon": {},
        }
    },
}


def _usecase_details(uc):
    return uc.__dict__


def _usecase_first_match(usecase_name):
    usecases = Collector()
    for uc in usecases:
        if uc.name == usecase_name:
            return _usecase_details(uc)


@usecase_router.get("/details/{usecase_name}", response_model=UsecaseDetails)
def get_usecase_details(usecase_name: str):
    """
    Fetches the usecase details

    Parameters
    ----------
        usecase_name (str):       Name of the usecase as string

    Returns
    -------
        Return the usecase details based on the name
    """
    return _usecase_first_match(usecase_name)


@usecase_router.get(
    "/icon/{usecase_name}", response_class=FileResponse, responses=_usecase_icon_responses
)
def get_usecase_icon(usecase_name: str):
    """
    Fetches the usecase icon/image

    Parameters
    ----------
        usecase_name (str):       Name of the usecase as string

    Returns
    -------
        Return the usecase icon/image based on the name
    """
    details = _usecase_first_match(usecase_name)
    image_path = None

    if details:
        if isinstance(ico := details.get("icon", None), Mapping):
            image_path = ico["path"]

    if image_path is None:
        image_path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "../assets/favicon.ico")
        )

    return FileResponse(image_path)


def filter_usecase(uc):
    if "configurator" in uc.applications:
        return False
    elif isinstance(uc, UsecaseEntrypoint):
        return True
    elif fe := getattr(uc, "frontend", None):
        return fe.path and fe.entrypoints is None
    return False


@usecase_router.get("/list", response_model=List)
def get_usecases():
    """
    Return the installed usecases

    Parameters
    ----------
        None

    Returns
    -------
        Return the installed usecases
    """

    usecases = [uc.name for uc in filter(filter_usecase, Collector())]
    return usecases


@usecase_router.get("/list_details", response_model=Sequence[UsecaseDetails])
def get_usecases_details():
    """
    List the installed usecases with details

    Parameters
    ----------
        None

    Returns
    -------
        Return the installed usecases
    """
    usecases = [_usecase_details(uc) for uc in Collector() if filter_usecase(uc)]
    return usecases
