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
import shutil
from helper import (connect_to_prototyping_board, generate_custom_pki,
                    verify_cert_chain_custompki, verify_cert_chain,
                    verify_SE_with_random_challenge, generate_manifest,
                    restore_mchp_certs_on_device, generate_project_config_h)
from tpds.cloud_connect.azure_connect import AzureConnect
from tpds.tp_utils.tp_print import print
import tpds.tp_utils.tp_input_dialog as tp_userinput
from tpds.certs.cert_utils import get_certificate_CN


class AzureConnectBase():
    def __init__(self, boards, Azure_Connect):
        self.boards = boards
        self.azure_connection = Azure_Connect()
        self.az_credentials = self.azure_connection.az_credentials

    def connect_to_cloud(self, b=None):
        self.azure_login(b)
        self.get_user_inputs(b)
        self.azure_connection.connect_azure(self.az_credentials.get("resource_group"), self.az_credentials.get("iot_hub"))
        azure_connect = os.path.join(os.getcwd(), 'azure_connect.h')
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


class AzureCustomPKI(AzureConnectBase):
    def __init__(self, boards):
        super().__init__(boards, AzureConnect)

    def generate_resources(self, b=None):
        self.connect_to_board(b)

        print('Generating CustomPKI certs...', canvas=b)
        generate_custom_pki(b)
        self.root_crt = 'root_crt.crt'
        self.root_key = 'root_key.key'
        self.signer_crt = 'signer_FFFF.crt'
        self.signer_key = 'signer_FFFF.key'
        self.device_crt = f'device_{self.serial_number.hex().upper()}.crt'
        azure_support = self.is_cn_supports_azure(self.device_crt, b)
        generate_project_config_h(
            cert_type='CUSTOM', address=0xC0, azure_support=azure_support)
        assert azure_support, ((
            'Connected TFLX device doesn\'t support Azure.\n'
            'Cert CN contains space(s).'))

    def register_certificates(self, b=None):
        self.connect_to_cloud(b)

        # Register Signer
        signer_cert = self.signer_crt
        signer_cer = os.path.splitext(signer_cert)[0] + '.cer'
        shutil.copy(signer_cert, signer_cer)
        print(f'Registering {signer_cer} to Azure account...', canvas=b)
        self.azure_connection.register_signer_certificate(
            signer_cert=signer_cer,
            signer_key=self.signer_key)
        print('Completed...', canvas=b)

        # Register Device
        device_crt = self.device_crt
        print(f'Register {device_crt} to Azure account...', canvas=b)
        self.azure_connection.register_device_as_CA_signed(device_cert=device_crt)
        print('Completed...', canvas=b)

    def verify_cert_chain(self, b=None):
        device_cert, crt_template = verify_cert_chain_custompki(
            self.root_crt, self.root_key,
            self.signer_crt, self.signer_key,
            self.device_crt, b)
        self.device_crt = device_cert
        self.crt_template = crt_template

    def verify_SE_with_random_challenge(self, b=None):
        verify_SE_with_random_challenge(
            b, self.device_crt, device_crt_template=self.crt_template['device'])


class AzureIoTAuthentication(AzureConnectBase):
    def __init__(self, boards):
        super().__init__(boards, AzureConnect)

    def generate_resources(self, b=None):
        self.connect_to_board(b)

        mchp_certs, r_manifest = restore_mchp_certs_on_device(
            self.serial_number, b)
        self.device_crt = mchp_certs.get('device')
        self.signer_crt = mchp_certs.get('signer')
        self.root_crt = mchp_certs.get('root')
        if r_manifest:
            self.manifest = r_manifest
        else:
            self.manifest = generate_manifest(
                b, self.signer_crt.certificate, self.device_crt.certificate)
        azure_support = self.is_cn_supports_azure(
            self.device_crt.certificate, b)
        generate_project_config_h(
            cert_type='MCHP', address=0xC0, azure_support=azure_support)
        assert azure_support, ((
            'Connected TFLX device doesn\'t support Azure.\n'
            'Cert CN contains space(s).'))

    def register_device(self, b=None):
        self.connect_to_cloud(b)
        print('Registering device into azure account...', canvas=b)
        self.azure_connection.register_device_from_manifest(
            device_manifest=self.manifest.get('json_file'),
            device_manifest_ca=self.manifest.get('ca_cert'))
        print('Completed...', canvas=b)

    def verify_cert_chain(self, b=None):
        if (self.root_crt is not None):
            self.dev_cert = verify_cert_chain(
                b, self.signer_crt.certificate, self.device_crt.certificate, self.root_crt.certificate)
        else:
            self.dev_cert = verify_cert_chain(
                b, self.signer_crt.certificate, self.device_crt.certificate)
        if self.dev_cert is None:
            raise ValueError('Certificate chain validation is failed')

    def verify_SE_with_random_challenge(self, b=None):
        verify_SE_with_random_challenge(b, self.dev_cert)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    pass
