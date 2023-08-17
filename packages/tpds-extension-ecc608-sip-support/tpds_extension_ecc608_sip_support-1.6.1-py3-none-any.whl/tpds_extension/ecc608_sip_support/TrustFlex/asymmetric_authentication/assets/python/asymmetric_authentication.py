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
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
import cryptoauthlib as cal
from tpds.resource_generation import TFLXResources
from tpds.flash_program import FlashProgram
from tpds.secure_element import ECC608A
from tpds.tp_utils.tp_settings import TPSettings
from tpds.tp_utils.tp_print import print
import tpds.tp_utils.tp_input_dialog as tp_userinput
from tpds.certs.tflex_certs import TFLEXCerts
from tpds.certs.cert_utils import get_backend


class AsymmetricAuthentication():
    def __init__(self, boards):
        self.boards = boards
        self.ser_num = None

    def __connect_to_SE(self, b=None):
        print('Connecting to Secure Element: ', canvas=b)
        if self.boards is None:
            print('Prototyping board MUST be selected!', canvas=b)
            return
        assert self.boards.get_selected_board(), \
            'Select board to run an Usecase'

        kit_parser = FlashProgram(board_name='EV76R77A')
        print(kit_parser.check_board_status())
        assert kit_parser.is_board_connected(), \
            'Check the Kit parser board connections'
        factory_hex = self.boards.get_kit_hex()
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
            kit_parser.load_hex_image_with_ipe(path)
        element = ECC608A(address=0xC0)
        print('OK', canvas=b)
        print('Device details: {}'.format(element.get_device_details()))
        self.ser_num = element.get_device_serial_number().hex().upper()

    def generate_resources(self, b=None):
        self.__connect_to_SE(b)

        print('Generating crypto assets for Usecase...', canvas=b)
        resources = TFLXResources()
        mchp_certs = resources.get_mchp_certs_from_device()
        if mchp_certs:
            print('MCHP Certs are available on device')
            if not resources.get_mchp_backup_certs():
                print('MCHP Certs backup is unavailable... Take backup!')
                resources.backup_mchp_certs(mchp_certs)

        text_box_desc = (
            '''<font color=#0000ff><b>Enter Org Name for Custom PKI</b></font><br>
            <br>The organization name entered here would be used to
            generate TFLXTLS certificates.<br>''')
        custom_org = tp_userinput.TPInputTextBox(
                                            desc=text_box_desc,
                                            dialog_title='CustomPKI Org')
        custom_org.invoke_dialog()
        print(f'User Org Name: {custom_org.user_text}', canvas=b)
        assert (
            (custom_org.user_text is not None)
            and (len(custom_org.user_text))), \
            'Enter valid custom Org name'
        resources.generate_custom_pki(custom_org.user_text)
        custom_certs = TFLEXCerts()
        custom_certs.set_tflex_certificates(
                        root_cert='root_crt.crt',
                        signer_cert='signer_FFFF.crt',
                        device_cert=f'device_{self.ser_num}.crt')
        custom_certs.save_tflex_py_definitions(
                        signer_def_file='signer_pydef.txt',
                        device_def_file=f'device_{self.ser_num}_pydef.txt')

    def read_certs_from_device(self, b=None):
        if self.ser_num is None:
            self.__connect_to_SE(b)

        print('Select Root certificate...', canvas=b)
        root_crt = tp_userinput.TPInputFileUpload(
                                        file_filter=['*.crt'],
                                        nav_dir = os.getcwd(),
                                        dialog_title='Upload Root')
        root_crt.invoke_dialog()
        assert root_crt.file_selection is not None, \
            'Select valid root certificate'
        print(
            f'Selected Root certificate is: {root_crt.file_selection}',
            canvas=b)

        print('Select Signer definition/template file...', canvas=b)
        signer_def = tp_userinput.TPInputFileUpload(
                                        file_filter=['*.txt'],
                                        nav_dir = os.getcwd(),
                                        dialog_title='Upload Signer pyDef')
        signer_def.invoke_dialog()
        assert signer_def.file_selection is not None, \
            'Select valid signer definition file'
        print(
            f'Selected Signer def file is: {signer_def.file_selection}',
            canvas=b)

        print('Select Device definition/template file...', canvas=b)
        device_def = tp_userinput.TPInputFileUpload(
                                        file_filter=['*.txt'],
                                        nav_dir = os.getcwd(),
                                        dialog_title='Upload Device pyDef')
        device_def.invoke_dialog()
        assert device_def.file_selection is not None, \
            'Select valid device definition file'
        print(
            f'Selected device def file is: {device_def.file_selection}',
            canvas=b)

        self.dev_certs = TFLEXCerts()
        self.dev_certs.root.set_certificate(root_crt.file_selection)
        crt_template = self.dev_certs.get_tflex_py_definitions(
                                  signer_def_file=signer_def.file_selection,
                                  device_def_file=device_def.file_selection)

        print('Reading certificates from device: ', canvas=b)
        signer_cert_der_len = cal.AtcaReference(0)
        assert cal.CertStatus.ATCACERT_E_SUCCESS == cal.atcacert_max_cert_size(
            crt_template['signer'],
            signer_cert_der_len)
        signer_cert_der = bytearray(signer_cert_der_len.value)
        assert cal.CertStatus.ATCACERT_E_SUCCESS == cal.atcacert_read_cert(
            crt_template['signer'],
            self.dev_certs.root.certificate.public_key().public_bytes(
                format=serialization.PublicFormat.UncompressedPoint,
                encoding=serialization.Encoding.X962)[1:],
            signer_cert_der,
            signer_cert_der_len)
        signer_cert = x509.load_der_x509_certificate(
            bytes(signer_cert_der), get_backend())
        self.dev_certs.signer.set_certificate(signer_cert)

        device_cert_der_len = cal.AtcaReference(0)
        assert cal.CertStatus.ATCACERT_E_SUCCESS == cal.atcacert_max_cert_size(
            crt_template['device'],
            device_cert_der_len)
        device_cert_der = bytearray(device_cert_der_len.value)
        assert cal.CertStatus.ATCACERT_E_SUCCESS == cal.atcacert_read_cert(
            crt_template['device'],
            self.dev_certs.signer.certificate.public_key().public_bytes(
                format=serialization.PublicFormat.UncompressedPoint,
                encoding=serialization.Encoding.X962)[1:],
            device_cert_der,
            device_cert_der_len)
        device_cert = x509.load_der_x509_certificate(
            bytes(device_cert_der), get_backend())
        print('OK')
        self.dev_certs.device.set_certificate(device_cert)

        print(self.dev_certs.root.get_certificate_in_text())
        print(self.dev_certs.signer.get_certificate_in_text())
        print(self.dev_certs.device.get_certificate_in_text())

    def verify_cert_chain(self, b=None):
        print('Verfying Root certificate...', end='', canvas=b)
        is_cert_valid = self.dev_certs.root.is_signature_valid(
           self.dev_certs.root.certificate.public_key())
        print('Valid' if is_cert_valid else 'Invalid', canvas=b)

        print('Verfying Signer certificate...', end='', canvas=b)
        is_cert_valid = self.dev_certs.signer.is_signature_valid(
            self.dev_certs.root.certificate.public_key())
        print('Valid' if is_cert_valid else 'Invalid', canvas=b)

        print('Verfying Device certificate...', end='', canvas=b)
        is_cert_valid = self.dev_certs.device.is_signature_valid(
            self.dev_certs.signer.certificate.public_key())
        print('Valid' if is_cert_valid else 'Invalid', canvas=b)

    def send_random_challenge_to_SE(self, b=None):
        print('Generate challenge...', canvas=b)
        self.challenge = os.urandom(32)
        print('OK', canvas=b)
        print(f'(Challenge: {self.challenge.hex().upper()}')

        crt_template = self.dev_certs.get_tflex_py_definitions()
        print('Get response from SE...', canvas=b)
        self.response = bytearray(64)
        assert cal.atcacert_get_response(
            crt_template['device'].private_key_slot,
            self.challenge, self.response) == cal.CertStatus.ATCACERT_E_SUCCESS
        print('OK', canvas=b)
        print(f'(Response: {self.response.hex().upper()}')

    def verify_SE_response(self, b=None):
        print('Verify response from SE...', canvas=b)
        r = int.from_bytes(self.response[0:32],
                           byteorder='big', signed=False)
        s = int.from_bytes(self.response[32:64],
                           byteorder='big', signed=False)
        sign = utils.encode_dss_signature(r, s)
        try:
            self.dev_certs.device.certificate.public_key().verify(
                sign, self.challenge, ec.ECDSA(
                    utils.Prehashed(hashes.SHA256())))
            print('OK', canvas=b)
        except Exception as err:
            raise ValueError(err)
