# -*- coding: utf-8 -*-
# 2018 to present - Copyright Microchip Technology Inc. and its subsidiaries.

# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.

# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
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
import cryptoauthlib as cal
import ctypes
import platform
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
from pykitinfo import pykitinfo
from tpds.flash_program import FlashProgram
from tpds.secure_element import ECC608A, ECC608B
from tpds.tp_utils.tp_settings import TPSettings
from tpds.tp_utils.tp_print import print
import tpds.tp_utils.tp_input_dialog as tp_userinput
from tpds.certs.cert_utils import get_backend
from tpds.certs.cert import Cert
from tpds.resource_generation import TNGManifest
from tpds.proto_boards import get_board_path


def connect_to_prototyping_board(board, b):
    assert board is not None, "Prototyping board MUST be selected!"
    assert board.get_selected_board() is not None, \
        'Select board to run an Usecase!'

    print('Connecting to Secure Element: ', end='')
    kit_parser = FlashProgram()
    print(kit_parser.check_board_status())
    assert kit_parser.is_board_connected(), \
        'Check the Kit parser board connections'
    factory_hex = board.get_kit_hex()
    if not kit_parser.is_factory_programmed():
        assert factory_hex, \
            'Factory hex is unavailable to program'
        print('Programming factory hex...', canvas=b)
        tp_settings = TPSettings()
        path = os.path.join(
            tp_settings.get_tpds_core_path(),
            'assets', 'Factory_Program.X',
            factory_hex)
        print(f'Programming {path} file')
        kit_parser.load_hex_image(path)
    element = ECC608A(address=0x6A)
    print('OK')
    print('Device details: {}'.format(element.get_device_details()))
    return element


def kit_uart_atcab_init(i2c_address, port):
    cfg = cal.ATCAIfaceCfg()
    cfg.iface_type = int(cal.ATCAIfaceType.ATCA_UART_IFACE)
    cfg.devtype = int(cal.ATCADeviceType.ATECC608B)
    cfg.wake_delay = 1500
    cfg.rx_retries = 10
    cfg.cfg.atcauart.dev_interface = int(cal.ATCAKitType.ATCA_KIT_I2C_IFACE)
    cfg.cfg.atcauart.dev_identity = i2c_address
    if isinstance(port, str):
        cfg.cfg.cfg_data = ctypes.c_char_p(port.encode('ascii'))
    else:
        cfg.cfg.atcauart.port = port
    cfg.cfg.atcauart.baud = 115200
    cfg.cfg.atcauart.wordsize = 8
    cfg.cfg.atcauart.parity = 2
    cfg.cfg.atcauart.stopbits = 1
    return cal.atcab_init(cfg) == cal.Status.ATCA_SUCCESS


def connect_to_proto_board_VC(board, i2c_address, b):
    assert board is not None, "Prototyping board MUST be selected!"
    assert board.get_selected_board() is not None, \
        'Select board to run a Usecase!'
    board_connected = False
    kit_parser = FlashProgram('ATSAME54-XPRO')

    # Checking whether the board is connected
    kits = pykitinfo.detect_all_kits()
    for kit in kits:
        if kit.get('debugger', {}).get('kitname', '') ==\
                kit_parser.board_info.description:
            board_connected = True
            port = kit.get('debugger', {}).get('serial_port', '')
            if platform.system() == 'Windows':
                myCOMport = int(port[3:])
            else:
                myCOMport = port

            print(f'Your board is connected to port {myCOMport}')
        else:
            assert board_connected, 'Check the Kit parser board connections'

    # Checking whether it's factory programmed
    if kit_uart_atcab_init(i2c_address, myCOMport):
        print('Your Board is Factory programmed')
    else:
        factory_hex = board.get_kit_hex()
        assert factory_hex, \
            'Factory hex is unavailable to program'
        print('Programming factory hex...', canvas=b)
        tp_settings = TPSettings()
        print(tp_settings.get_mplab_paths())
        path = os.path.join(
            get_board_path(), 'ATSAME54-XPRO', 'ATSAME54-XPRO.hex')
        print(f'Programming {path} file')
        kit_parser.load_hex_image_with_ipe(path)

    print('Connecting to Secure Element..... ', end='')
    element = ECC608B(i2c_address, myCOMport)
    print('OK')
    print('Device details: {}'.format(element.get_device_details()))
    return element


def verify_cert_chain(b):
    print('Reading Root certificate: ', canvas=b)
    root_cert_der_size = cal.AtcaReference(0)
    assert cal.tng_atcacert_root_cert_size(
        root_cert_der_size) == cal.Status.ATCA_SUCCESS
    root_cert_der = bytearray(root_cert_der_size.value)
    assert cal.tng_atcacert_root_cert(
        root_cert_der,
        root_cert_der_size) == cal.Status.ATCA_SUCCESS
    root_cert = x509.load_der_x509_certificate(bytes(root_cert_der),
                                               get_backend())
    print('OK', canvas=b)

    print('Reading Signer certificate: ', canvas=b)
    signer_cert_der_size = cal.AtcaReference(0)
    assert cal.tng_atcacert_max_signer_cert_size(
        signer_cert_der_size) == cal.Status.ATCA_SUCCESS
    signer_cert_der = bytearray(signer_cert_der_size.value)
    assert cal.tng_atcacert_read_signer_cert(
        signer_cert_der,
        signer_cert_der_size) == cal.Status.ATCA_SUCCESS
    signer_cert = x509.load_der_x509_certificate(
                                    bytes(signer_cert_der),
                                    get_backend())
    print('OK', canvas=b)

    print('Reading device certificate: ', canvas=b)
    device_cert_der_size = cal.AtcaReference(0)
    assert cal.tng_atcacert_max_device_cert_size(
        device_cert_der_size) == cal.Status.ATCA_SUCCESS
    device_cert_der = bytearray(device_cert_der_size.value)
    assert cal.tng_atcacert_read_device_cert(
        device_cert_der,
        device_cert_der_size) == cal.Status.ATCA_SUCCESS
    device_cert = x509.load_der_x509_certificate(
                                        bytes(device_cert_der),
                                        get_backend())
    print('OK', canvas=b)

    root = Cert()
    signer = Cert()
    device = Cert()
    root.set_certificate(root_cert)
    signer.set_certificate(signer_cert)
    device.set_certificate(device_cert)

    print('Verify cert chain...', canvas=b)
    is_chain_valid = \
        root.is_signature_valid(
            root.certificate.public_key()) and \
        signer.is_signature_valid(
            root.certificate.public_key()) and \
        device.is_signature_valid(
            signer.certificate.public_key())
    if is_chain_valid:
        print('Valid', canvas=b)
        return device.certificate
    else:
        print('Invalid', canvas=b)
        return None


def verify_SE_with_random_challenge(device_crt, b):
    print('Generate challenge...', canvas=b)
    challenge = os.urandom(32)
    print(f'OK(Challenge: {challenge.hex().upper()}')

    print('Get response from SE...', canvas=b)
    response = bytearray(64)
    assert cal.atcacert_get_response(
        0,
        challenge, response) == cal.CertStatus.ATCACERT_E_SUCCESS
    print(f'OK(Response: {response.hex().upper()}')

    print('Verify response...', canvas=b)
    r = int.from_bytes(response[0:32], byteorder='big', signed=False)
    s = int.from_bytes(response[32:64], byteorder='big', signed=False)
    sign = utils.encode_dss_signature(r, s)
    try:
        device_crt.public_key().verify(
            sign, challenge, ec.ECDSA(
                utils.Prehashed(hashes.SHA256())))
        print('OK')
    except Exception as err:
        raise ValueError(err)


def get_user_option(b):
    print('Select Manifest option', canvas=b)
    item_list = ['Generate Manifest', 'Upload Manifest']
    dropdown_desc = (
        '''<font color=#0000ff><b>Select Manifest Option</b></font><br>
        <br>Generate Manifest - Generates Manifest file for connected device
        locally<br>
        Upload Manifest - Use existing Manifest file. Requires Manifest
        and its CA files <br>''')
    user_input = tp_userinput.TPInputDropdown(
                                item_list=item_list,
                                desc=dropdown_desc,
                                dialog_title='Manifest Selection')
    user_input.invoke_dialog()
    print(f'Selected option is: {user_input.user_option}', canvas=b)
    assert user_input.user_option is not None, \
        'Select valid Manifest Option'

    return user_input.user_option


def get_user_manifest(b):
    print('Select Manifest JSON file...', canvas=b)
    manifest = tp_userinput.TPInputFileUpload(
                                file_filter=['*.json'],
                                nav_dir=os.getcwd(),
                                dialog_title='Upload Manifest')
    manifest.invoke_dialog()
    print(
        f'Selected manifest file is: {manifest.file_selection}',
        canvas=b)

    print('Select Manifest CA file...', canvas=b)
    manifest_ca = tp_userinput.TPInputFileUpload(
                                file_filter=['*.crt'],
                                nav_dir=os.getcwd(),
                                dialog_title='Upload Manifest CA')
    manifest_ca.invoke_dialog()
    print(
        f'Selected manifest CA file is: {manifest_ca.file_selection}',
        canvas=b)

    return {
        'json_file': manifest.file_selection,
        'ca_cert': manifest_ca.file_selection
    }


def generate_manifest(b):
    print('Generating Manifest...', canvas=b)
    resources = TNGManifest()
    resources.generate_manifest()
    print('Completed', canvas=b)

    return {
        'json_file': 'TNGTLS_devices_manifest.json',
        'ca_cert': 'manifest_ca.crt'
    }


def generate_project_config_h(
        cert_type='MCHP', address=0x6A, azure_support=False):
    project_config = os.path.join(os.getcwd(), 'project_config.h')
    with open(project_config, 'w') as f:
        f.write('#ifndef _PROJECT_CONFIG_H\n')
        f.write('#define _PROJECT_CONFIG_H\n\n')

        f.write('#ifdef __cplusplus\n')
        f.write('extern "C" {\n')
        f.write('#endif\n\n')
        if cert_type == 'MCHP':
            f.write('#define CLOUD_CONNECT_WITH_MCHP_CERTS\n')
        else:
            f.write('#define CLOUD_CONNECT_WITH_CUSTOM_CERTS\n')
        if azure_support:
            f.write('#define DEVICE_CERT_SUPPORTS_AZURE_CONNECTION\n')
        f.write(f'#define SECURE_ELEMENT_ADDRESS 0x{address:02X}\n\n')
        f.write('#ifdef __cplusplus\n')
        f.write('}\n')
        f.write('#endif\n')
        f.write('#endif\n')


def get_tng_device_cert():
    try:
        device_cert_der_size = cal.AtcaReference(0)
        assert cal.tng_atcacert_max_device_cert_size(
            device_cert_der_size) == cal.Status.ATCA_SUCCESS
        device_cert_der = bytearray(device_cert_der_size.value)
        assert cal.tng_atcacert_read_device_cert(
            device_cert_der,
            device_cert_der_size) == cal.Status.ATCA_SUCCESS
        device_cert = x509.load_der_x509_certificate(
                                            bytes(device_cert_der),
                                            get_backend())
    except Exception as e:
        raise ValueError(f'Reading device cert failed with {e}')

    return device_cert


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    pass
