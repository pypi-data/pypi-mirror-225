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
from helper import (
    connect_to_prototyping_board, get_user_option,
    get_user_manifest, generate_manifest, connect_to_proto_board_VC,
    verify_cert_chain, verify_SE_with_random_challenge,
    generate_project_config_h, get_tng_device_cert)
import yaml
import tpds.tp_utils.tp_input_dialog as tp_userinput
from tpds.tp_utils.tp_print import print
import cryptoauthlib as cal
from tpds.cloud_connect.azure_connect import AzureConnect
from tpds.cloud_connect.azureRTOS_connect import AzurertosConnect
from tpds.certs.cert_utils import get_certificate_CN
from pathlib import Path


class AzureConnectBase():
    def __init__(self, boards, Azure_Connect):
        self.boards = boards
        self.azure_connection = Azure_Connect()
        self.az_credentials = self.azure_connection.az_credentials

    def connect_to_board(self, b=None):
        self.element = connect_to_prototyping_board(self.boards, b)
        assert self.element, 'Connection to Board failed'
        self.serial_number = self.element.get_device_serial_number()

    def is_cn_supports_azure(self, device_cert, b=None):
        return (' ' not in get_certificate_CN(device_cert))

    def get_user_inputs(self, b=None):
        if self.az_credentials.get('subscription_id', '') == '':
            text_box_desc = (
                '''
                <font color=#0000ff><b>Enter your subscription ID</b></font><br>
                <br>Your Azure Subscription needs to be active.<br>
                '''
            )
            subscription = tp_userinput.TPInputTextBox(
                desc=text_box_desc,
                dialog_title='Azure Subscription ID')
            subscription.invoke_dialog()
            if (subscription.user_text is None or subscription.user_text == ""):
                raise ValueError("Subscription ID cannot be empty")

            self.azure_connection.set_subscription_id(subscription.user_text)
            self.az_credentials.update({'subscription_id': subscription.user_text})
            self.azure_connection.save_credentials()
        else:
            self.azure_connection.set_subscription_id(self.az_credentials.get('subscription_id'))

        print(f'Azure Subscription ID: {self.az_credentials.get("subscription_id")}', canvas=b)

        if self.az_credentials.get('resource_group', '') == '':
            text_box_desc = (
                '''
                <font color=#0000ff><b>Enter Your Resource Group</b></font><br>
                <br>A resource group is a container that holds your Azure solution related resources. <br>
                <br>If a resource group is not available in the Subscription, usecase will create the resource. <br>
                '''
            )
            resourceGroup = tp_userinput.TPInputTextBox(
                desc=text_box_desc,
                dialog_title='Resource Group Name')
            resourceGroup.invoke_dialog()
            if (resourceGroup.user_text is None or resourceGroup.user_text == ""):
                raise ValueError("Resource Group cannot be empty")

            self.azure_connection.az_group_create(resourceGroup.user_text)
            self.az_credentials.update({'resource_group': resourceGroup.user_text})
            self.azure_connection.save_credentials()
        print(f'Azure Resource Group Name: {self.az_credentials.get("resource_group")}', canvas=b)

        if self.az_credentials.get('iot_hub') == '':
            text_box_desc = (
                f'''
                <font color=#0000ff><b>Enter your Azure IoT Hub </b></font><br>
                <br>The Hub name needs to be globally unique. <br>
                <br>If a Azure IoT Hub name is not available in the Resource Group {self.az_credentials.get('resource_group', '')}, usecase will create the Azure IoT hub. <br>
                '''
            )
            hostName = tp_userinput.TPInputTextBox(
                desc=text_box_desc,
                dialog_title='Azure IoT Hub Name')
            hostName.invoke_dialog()
            if (hostName.user_text is None or hostName.user_text == ""):
                raise ValueError("IoT Hub cannot be empty")

            self.azure_connection.az_hub_create(self.az_credentials.get("resource_group"), hostName.user_text)
            self.az_credentials.update({'iot_hub': hostName.user_text})
            self.azure_connection.save_credentials()
        print(f'Azure IoT Hub: {self.az_credentials.get("iot_hub")}', canvas=b)

    def azure_login(self, b=None):
        print("login Azure...")
        self.azure_connection.login()
        print("Ok")


class AzureConnectUsecase(AzureConnectBase):
    def __init__(self, boards):
        super().__init__(boards, AzureConnect)
        self.element = None

    def generate_or_upload_manifest(self, b=None):
        user_option = get_user_option(b)
        if user_option == 'Upload Manifest':
            self.manifest = get_user_manifest(b)
            assert self.manifest.get('json_file') is not None, \
                'Select valid Manifest file'
            assert self.manifest.get('ca_cert') is not None, \
                'Select valid Manifest CA file'
        else:
            self.__perform_device_connect(b)
            self.manifest = generate_manifest(b)

    def connect_to_cloud(self, b=None):
        self.azure_login(b)
        self.get_user_inputs(b)
        self.azure_connection.connect_azure(self.az_credentials.get("resource_group"), self.az_credentials.get("iot_hub"))

        azure_connect = os.path.join(os.getcwd(), 'azure_connect.h')
        with open(azure_connect, 'w') as f:
            f.write('#ifndef _AZURE_CONNECT_H\n')
            f.write('#define _AZURE_CONNECT_H\n\n')
            f.write('#include "cryptoauthlib.h"\n\n')
            f.write('#ifdef __cplusplus\n')
            f.write('extern "C" {\n')
            f.write('#endif\n\n')
            cloud_endpoint = (
                f'''#define CLOUD_ENDPOINT "{self.az_credentials.get('iot_hub')}.azure-devices.net"\n\n''')
            f.write(cloud_endpoint)
            f.write('#ifdef __cplusplus\n')
            f.write('}\n')
            f.write('#endif\n')
            f.write('#endif\n')

        files = [file for file in os.listdir('.') if (
            os.path.isfile(file) and file.startswith('cust_def'))]
        if not files:
            # create dummy definition files for compilation
            Path('cust_def_1_signer.c').write_text(
                '//Empty file for compilation')
            Path('cust_def_1_signer.h').write_text(
                '//Empty file for compilation')
            Path('cust_def_2_device.c').write_text(
                '//Empty file for compilation')
            Path('cust_def_2_device.h').write_text(
                '//Empty file for compilation')
        return 'Success'

    def register_device(self, b=None):
        self.connect_to_cloud(b)
        print('Registering device into azure account...', canvas=b)
        self.azure_connection.register_device_from_manifest(
            device_manifest=self.manifest.get('json_file'),
            device_manifest_ca=self.manifest.get('ca_cert'))
        print('Completed...', canvas=b)

    def verify_cert_chain(self, b=None):
        if self.element is None:
            self.__perform_device_connect(b)
        self.device_cert = verify_cert_chain(b)
        if self.device_cert is None:
            raise ValueError('Certificate chain validation is failed')

    def verify_SE_with_random_challenge(self, b=None):
        verify_SE_with_random_challenge(self.device_cert, b)

    def __perform_device_connect(self, b=None):
        self.element = connect_to_prototyping_board(self.boards, b)
        assert self.element, 'Connection to Board failed'
        device_cert = get_tng_device_cert()
        azure_support = self.is_cn_supports_azure(device_cert, b)
        generate_project_config_h(
            cert_type='MCHP', address=0x6A, azure_support=azure_support)
        assert azure_support, ((
            'Connected TNG device doesn\'t support Azure.\n'
            'Cert CN contains space(s).'))


class AzureRTOS(AzureConnectBase):
    def __init__(self, boards, i2c_address):
        super().__init__(boards, AzurertosConnect)
        self.i2c_address = i2c_address
        self.boards = boards

    def connect_to_bo(self, b=None):
        self.element = connect_to_proto_board_VC(
            self.boards, self.i2c_address, b)
        self.port = self.element.port
        assert self.element, 'Connection to Board failed'
        self.serial_number = self.element.get_device_serial_number()
        device_cert = get_tng_device_cert()
        self.is_cn_supports_azure(device_cert, b)

    def generate_or_upload_manifest(self, b=None):
        user_option = get_user_option(b)
        if user_option == 'Upload Manifest':
            self.manifest = get_user_manifest(b)
            assert self.manifest.get('json_file') is not None, \
                'Select valid Manifest file'
            assert self.manifest.get('ca_cert') is not None, \
                'Select valid Manifest CA file'
        else:
            self.connect_to_bo(b)
            self.manifest = generate_manifest(b)

    def Azure_DPS_setup(self, b):
        self.azure_login(b)
        self.get_user_inputs(b)

        if self.az_credentials.get('dps_name', '') == '':
            text_box_desc = (
                '''
                <font color=#0000ff><b>Enter a name for your DPS instance</b></font><br>
                <br>DPS is the device provisioning helper service for your IoT Hub that will provides all the means to provision your devices in a secure and scalable manner .<br>
                '''
            )
            dpsName = tp_userinput.TPInputTextBox(
                desc=text_box_desc,
                dialog_title='DPS Name')
            dpsName.invoke_dialog()
            if (dpsName.user_text is None or dpsName.user_text == ""):
                raise ValueError("DPS cannot be empty")
            self.azure_connection.az_dps_create(self.az_credentials.get("resource_group"), dpsName.user_text)
            self.az_credentials.update({'dps_name': dpsName.user_text})
            self.azure_connection.save_credentials()

        print(f'Azure DPS name: {self.az_credentials.get("dps_name")}', canvas=b)
        self.azure_connection.connect_azure(self.az_credentials.get("resource_group"), self.az_credentials.get("dps_name"))
        print('OK')

    def register_device(self, b=None):
        self.azure_connection.enroll_device(self.i2c_address, self.port, self.manifest, b)
        self.azure_connection.saveDataSlot(self.i2c_address, self.port)

    def verify_cert_chain(self, b=None):
        if self.element is None:
            self.connect_to_bo(b)
        self.azure_connection.kit_atcab_init(self.i2c_address, self.port)
        self.device_cert = verify_cert_chain(b)
        if self.device_cert is None:
            raise ValueError('Certificate chain validation is failed')

    def verify_SE_with_random_challenge(self, b=None):
        self.azure_connection.kit_atcab_init(self.i2c_address, self.port)
        verify_SE_with_random_challenge(self.device_cert, b)
        cal.atcab_release()


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    pass
