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
import binascii
from helper import (
            connect_to_prototyping_board, get_user_option,
            get_user_manifest, generate_manifest,
            verify_cert_chain, verify_SE_with_random_challenge,
            generate_project_config_h)
import yaml
import tpds.tp_utils.tp_input_dialog as tp_userinput
from tpds.tp_utils.tp_print import print
from tpds.cloud_connect.aws_connect import AWSConnect
from pathlib import Path

class AWSConnectUsecase():
    def __init__(
            self, boards, user_input=None):
        self.boards = boards
        self.connection = AWSConnect()
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

    def register_device(self, b=None):
        resp_data = self.__config_aws_cli(b)
        assert resp_data == 'Success', f'''AWS cli config failed with "{resp_data}"'''

        # Register Device
        print('Registering device to AWS account...', canvas=b)
        self.connection.register_from_manifest(
            self.manifest.get('json_file'),
            self.manifest.get('ca_cert'))
        print('Completed...', canvas=b)

    def verify_cert_chain(self, b=None):
        if self.element is None:
            self.__perform_device_connect(b)
        self.device_cert = verify_cert_chain(b)
        if self.device_cert is None:
            raise ValueError('Certificate chain validation is failed')

    def verify_SE_with_random_challenge(self, b=None):
        verify_SE_with_random_challenge(self.device_cert, b)

    def prompt_aws_gui(self, qtuifile, b=None):
        thing_id = binascii.b2a_hex(self.ser_num).decode('ascii')
        self.connection.execute_aws_gui(thing_id=thing_id.lower(),
                                        qtUiFile=qtuifile)

    def __config_aws_cli(self, b=None):
        print('Configure AWS CLI...', canvas=b)
        with open(self.connection.creds_file) as f:
            aws_credentials = yaml.safe_load(f)
        if all(dict((k, v.strip()) for k, v in aws_credentials.items()).values()):
            self.connection.set_credentials(aws_credentials)
            aws_connect = os.path.join(os.getcwd(), 'aws_connect.h')
            with open(aws_connect, 'w') as f:
                f.write('#ifndef _AWS_CONNECT_H\n')
                f.write('#define _AWS_CONNECT_H\n\n')
                f.write('#include "cryptoauthlib.h"\n\n')
                f.write('#ifdef __cplusplus\n')
                f.write('extern "C" {\n')
                f.write('#endif\n\n')
                cloud_endpoint = self.connection.iot.describe_endpoint(
                    endpointType='iot:Data').get(
                    'endpointAddress')
                f.write(
                    f'#define CLOUD_ENDPOINT "{cloud_endpoint}"\n\n')
                f.write('#ifdef __cplusplus\n')
                f.write('}\n')
                f.write('#endif\n')
                f.write('#endif\n')

            files = [file for file in os.listdir('.') if (os.path.isfile(file) and file.startswith('cust_def'))]
            if not files:
                # create dummy definition files for compilation
                Path('cust_def_1_signer.c').write_text('//Empty file for compilation')
                Path('cust_def_1_signer.h').write_text('//Empty file for compilation')
                Path('cust_def_2_device.c').write_text('//Empty file for compilation')
                Path('cust_def_2_device.h').write_text('//Empty file for compilation')
            return 'Success'
        else:
            msg_box_info = (
                '<font color=#0000ff><b>Invalid AWS account credentials'
                '</b></font><br>'
                '<br>To setup an AWS account, please refer Usecase help guide<br>')
            acc_cred_diag = tp_userinput.TPMessageBox(
                title="AWS account credentials",
                info=msg_box_info)
            acc_cred_diag.invoke_dialog()
            return 'Credentials are unavailable'

    def __perform_device_connect(self, b=None):
        self.element = connect_to_prototyping_board(self.boards, b)
        assert self.element, 'Connection to Board failed'
        self.ser_num = self.element.get_device_serial_number()
        generate_project_config_h(cert_type='MCHP', address=0x6A)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    pass
