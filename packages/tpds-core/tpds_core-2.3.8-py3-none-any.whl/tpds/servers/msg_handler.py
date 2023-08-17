from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Any, Callable, Sequence
from urllib.parse import unquote as urlunquote

import markdown
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QDialog, QFileDialog, QInputDialog, QMessageBox
from tpds.app.vars import get_app_ref, get_url_base

from tpds.helper import log
from tpds.settings import TrustPlatformSettings
from tpds.usecase_collector import Collector

from .msg_handler_ta import (
    get_ta_appJSON,
    get_ta_handles_json,
    ta_appJSON,
    ta_open_app_handle,
    ta_proto_provisioning_handle,
    ta_provisioningXML_handle,
    ta_uno_appJSON,
    ta_uno_config_handle,
)
from .msg_handler_tcustom import trust_custom_read_config, trust_custom_write_config
from .msg_handler_tflx import tflx_proto_provisioning_handle, tflx_provisioningXML_handle
from .msg_handler_tflx_ecc204 import tflex_ecc204_json_handle, tflxecc204_proto_prov_handle
from .provision_user_inputs import ProvisionUserInputs
from .symm_auth_user_inputs import SymmAuthUserInputs, Sha10xSymmAuthUserInputs
from .wpc_user_inputs import WPCUserInputs


def default(args):
    return {"response": "unrecognized command", "status": "error"}


class Messages:
    msg_schema = {"msg_id": "int", "parameters": ["string"]}

    def __init__(self, parent=None) -> None:
        self._parent = parent

    def decode(self, message):
        log(f'received message op_code: {message["msg_id"]}')
        return json.dumps(
            op_codes.get(message["msg_id"], default)(self._parent, *message["parameters"])
        )


class TpdsMessage:
    """
    Wrap message handling with all of the common boilerplate
    """

    def __init__(self, *types: Sequence[type]) -> None:
        super().__init__()
        self._arg_cnt = len(types)

    def __call__(self, func) -> Callable[[Any], dict[str, str]]:
        def wrapper(ctx, *args: str) -> dict[str, str]:
            log(f"{func.__name__}: " + " ".join([str(x) for x in args[: self._arg_cnt]]))
            status, response = func(ctx, *args[: self._arg_cnt])
            return {"response": response, "status": status}

        return wrapper


def _get_jupyter_path(ctx, path):
    for js in ctx._voila:
        if os.path.exists(os.path.join(js._start_directory, urlunquote(path))):
            return f"{js._web_address}voila/render/{path}"


@TpdsMessage(str)
def open_notebook(ctx, usecase):
    resolved = None
    if path := getattr(Collector().get(usecase, {}), "url", None):
        if ".ipynb" in path.lower():
            if _base := get_app_ref():
                resolved = _get_jupyter_path(_base.backend, path)
                _base._view.basewebview.handlelink(QUrl(resolved))
            elif ctx:
                resolved = _get_jupyter_path(ctx, path)
        else:
            resolved = f"{path}"

    log(f"open_notebook: {resolved}")
    return (
        ("OK", resolved.replace("\\", "/"))
        if resolved
        else ("error", "Failed to resolve usecase path")
    )


@TpdsMessage(list)
def open_webview(ctx, link_to_open):
    _base = get_app_ref()
    if "Documentation.html#" in link_to_open:
        link_to_open = f"{get_url_base()}/{link_to_open}"
        _base._view.basewebview.handlelink(QUrl(link_to_open))
        return ("OK", link_to_open)

    if os.path.exists(link_to_open):
        render_path = os.path.join(
            os.path.dirname(link_to_open),
            "Help-" + os.path.basename(link_to_open).split(".", 1)[0] + ".html",
        )
        Path(render_path).write_text(
            markdown.markdown(Path(link_to_open).read_text(), extensions=["toc"])
        )
        if "win" in sys.platform:
            render_path = "/" + render_path
        render_path = "file://" + render_path.replace("\\", "/")
    else:
        render_path = link_to_open
    log(f"open_webview: {render_path}")
    _base._view.basewebview.handlelink(QUrl(render_path))
    return (
        ("OK", render_path)
        if render_path
        else ("error", "Failed to resolve usecase path")
    )


@TpdsMessage(list)
def loopback(ctx, args):
    return "OK", " ".join(args)


@TpdsMessage
def get_mplab_path(ctx):
    conf = TrustPlatformSettings()
    return "OK", conf.settings.mplab_path


@TpdsMessage(str)
def active_board(ctx, board_name):
    config = TrustPlatformSettings()
    config.settings.runtime_settings.active_board = board_name
    config.save()
    return "OK", config.settings.runtime_settings.active_board


@TpdsMessage(str, str, str)
def user_input_file_upload(ctx, *args):
    # [caption, file_filter, navigation_dir]
    if len(args) > 2:
        filepath = None
        file_filter = None
        file_filter = "("
        for arg in args[1]:
            file_filter += f"{arg} "
        file_filter += ")"
        log(f"File filter: {file_filter}")
        log(args[2])
        dlg = QFileDialog(None, caption=args[0], filter=file_filter, directory=args[2])
        result = dlg.exec()
        if result == QDialog.Accepted:
            filepath = dlg.selectedFiles()[0]
        log(filepath)
        return "OK", filepath

    return "error", "insufficient args"


@TpdsMessage(str, str)
def user_input_text_box(ctx, title, label):
    textvalue = None
    tB, accept = QInputDialog.getText(None, title, label)
    if accept:
        textvalue = tB
    return "OK", textvalue


@TpdsMessage(str, list, str)
def user_input_dropdown(ctx, title, items, label):
    response = None
    item, ok = QInputDialog.getItem(None, title, label, items, 0, False)
    if ok and item:
        log(item)
        response = item
    return "OK", response


@TpdsMessage(str, str)
def user_message_box(ctx, title, text):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    reply = msg_box.exec()
    response = "OK" if reply == QMessageBox.Ok else "Cancel"
    return "OK", response


@TpdsMessage(str, str)
def tflex_provisioningXML(ctx, data):
    tflx_provisioningXML_handle(json.dumps(json.loads(data)))
    return "OK", ""


@TpdsMessage(str)
def tflx_proto_provisioning(ctx, id):
    tflx_proto_provisioning_handle(id)
    return "OK", ""


@TpdsMessage
def ta_open_app(ctx):
    ta_open_app_handle()
    return "OK", ""


@TpdsMessage(str)
def ta_provisioningXML(ctx, xml_ver):
    ta_provisioningXML_handle(xml_ver, get_ta_handles_json())
    return "OK", xml_ver


@TpdsMessage(str)
def ta_proto_provisioning(ctx, id):
    ta_proto_provisioning_handle(id)
    return "OK", ""


@TpdsMessage(str, str, str)
def ta_uno_provisioningXML(ctx, xml_type, json_str):
    ta_uno_appJSON(xml_type, json_str)
    return "OK", ""


@TpdsMessage(str)
def tflex_ecc204_json(ctx, config):
    tflex_ecc204_json_handle(config)
    return "OK", ""


@TpdsMessage(str)
def tflex_ecc204_proto_prov(ctx, config):
    tflxecc204_proto_prov_handle(config)
    return "OK", ""


@TpdsMessage(list)
def symm_auth_user_inputs(ctx, args):
    obj = SymmAuthUserInputs()
    obj.exec()
    return "OK", f"{obj.user_data}"


@TpdsMessage(list)
def sha10x_symm_auth_user_inputs(ctx, args):
    obj = Sha10xSymmAuthUserInputs()
    obj.exec()
    return "OK", f"{obj.user_data}"


@TpdsMessage(list)
def wpc_user_inputs(ctx, args):
    obj = WPCUserInputs()
    obj.exec()
    return "OK", f"{obj.user_data}"


@TpdsMessage(list)
def provision_inputs(ctx, args):
    obj = ProvisionUserInputs(xml_type=args[0], cert_type=args[1])
    obj.exec()
    return "OK", f"{obj.user_data}"


@TpdsMessage(str)
def open_explorer_folder(ctx, path):
    try:
        if sys.platform == "darwin":
            subprocess.check_call(["open", str(Path(path))])
        elif sys.platform == "linux":
            subprocess.check_call(["nautilus", str(Path(path))])
        elif sys.platform == "win32":
            subprocess.check_call(["explorer", str(Path(path))])
        return "OK", ""
    except Exception as e:
        log(f"Error on opening explorer folder: {e}")
        return "error", ""


def check_package(pinfo):
    conf = TrustPlatformSettings()
    pdir = os.path.join(conf.settings.conda_path, pinfo)
    return (os.path.exists(pdir), pdir)


@TpdsMessage(str, str)
def open_configurator_page(ctx, device_type, directory):
    configurator_title = device_type
    package_info = {
        "ATECC": os.path.join("tpds_ecc_trustcustom", "assets", "TrustCUSTOM_configurator.html"),
        "TA": os.path.join("TA_Configurator", "dist", "index.html"),
    }
    product_name = re.search("TA|ATECC", device_type).group(0).strip()
    exists_bool, pdir = check_package(package_info.get(product_name, ""))

    if "TA" == product_name:
        pdir = "http://127.0.0.1:1304/"
        _base = get_app_ref()
        ctrack = _base._view.basewebview.checkInstance("TA_Configurator")
        if ctrack:
            pdir = "OK"
        else:
            ta_uno_config_handle("")

    log(f"Requested package {product_name}, " f"dir: {pdir}, exists: {exists_bool}")

    if not exists_bool:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setWindowTitle(configurator_title + " Configurator")
        msg_box.setTextFormat(Qt.RichText)
        display_msg = (
            f"<font color=#0000ff><b>{configurator_title} Configurator"
            f"</b></font><br><br>"
            f"Package is not found locally.  If package access is already granted, Click Cancel and Update from Package Manager. \
            If package access is required, Click OK to request from Microchip. <br>"
        )
        msg_box.setText(display_msg)
        reply = msg_box.exec()

        pdir = directory
        if reply == QMessageBox.Cancel:
            pdir = ""
    return "OK", pdir


@TpdsMessage(str)
def open_default_browser(ctx, page_str):
    try:
        webbrowser.open(page_str)
        return "OK", ""
    except Exception as e:
        log(f"Error on opening browser: {e}")
        return "OK", ""


@TpdsMessage(str)
def ta_uno_get_config(ctx, empty):
    config_file = os.path.join(
        getattr(Collector().get("ta100_config", {}), "_root", ""), "assets", "SampleConfig.taconfig"
    )
    config_info = {}
    if os.path.exists(config_file):
        config_info.update({"title": Path(config_file).name})
        config_info.update({"content": Path(config_file).read_text("'utf-8-sig'")})
    return "OK", json.dumps(config_info)


@TpdsMessage(str, str, str)
def tcustom_608_config_rw(ctx, cmd, addr, config):
    resp = "success"
    if cmd == "load":
        trust_custom_write_config(config, int(addr, 16))
    else:
        resp = trust_custom_read_config(int(addr, 16))
    return "OK", resp


# leave at the bottom of the file
op_codes = {
    0: loopback,
    1: get_mplab_path,
    2: open_notebook,
    3: open_webview,
    4: tflex_provisioningXML,
    5: active_board,
    6: get_ta_appJSON,
    7: ta_open_app,
    8: ta_provisioningXML,
    9: tflx_proto_provisioning,
    10: ta_proto_provisioning,
    11: user_input_file_upload,
    12: user_input_text_box,
    13: user_input_dropdown,
    14: open_explorer_folder,
    15: open_configurator_page,
    16: tcustom_608_config_rw,
    17: open_default_browser,
    18: user_message_box,
    20: tflex_ecc204_json,
    21: tflex_ecc204_proto_prov,
    40: symm_auth_user_inputs,
    41: wpc_user_inputs,
    42: sha10x_symm_auth_user_inputs,
    50: provision_inputs,
    80: ta_appJSON,
    81: ta_uno_provisioningXML,
    82: ta_uno_get_config,
}

__all__ = ["Messages", "TpdsMessage", "op_codes"]
