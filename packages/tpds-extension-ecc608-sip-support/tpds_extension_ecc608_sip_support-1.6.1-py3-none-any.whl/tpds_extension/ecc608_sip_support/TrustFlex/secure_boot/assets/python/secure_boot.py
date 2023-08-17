import os
import cryptoauthlib as cal
from intelhex import IntelHex
import cryptography
from cryptography.hazmat.primitives import hashes

from tpds.resource_generation import ResourceGeneration
from tpds.flash_program import FlashProgram
from tpds.secure_element import ECC608A
from tpds.tp_utils.tp_settings import TPSettings
import tpds.tp_utils.tp_input_dialog as tp_userinput
from tpds.tp_utils.tp_print import print
from tpds.tp_utils.tp_keys import TPAsymmetricKey, TPSymmetricKey
from tpds.tp_utils.tp_utils import sign_on_host
from tpds.tp_utils.tp_utils import pretty_print_hex
import MCU32 as mcu


class SecureBootUsecase():
    def __init__(self, boards, secboot_pubkey_slot=15,
                 io_protection_key_slot=6,
                 boot_start_addr=0x00000000,
                 boot_end_addr=0x0000BFFF,
                 app_start_addr=0x0000C000,
                 app_end_addr=0x0003FBFF,
                 sign_start_addr= 0x0002A9C0, #0x0002A1C0, #This might need to be changed according to what dimitri said
                 app_len_str_addr=0x0003FD00):
        self.boards = boards
        self.io_protection_key_slot = io_protection_key_slot
        self.secboot_pubkey_slot = secboot_pubkey_slot
        self.boot_start_addr = boot_start_addr
        self.boot_end_addr = boot_end_addr
        self.app_start_addr = app_start_addr
        self.app_end_addr = app_end_addr
        self.sign_start_addr = sign_start_addr
        self.app_len_str_addr = app_len_str_addr

    def generate_resources(self, b=None):
        self.__connect_to_SE(b)

        print('Generating crypto assets for Usecase...', canvas=b)
        privkey_file = self.__get_private_key_file(b)
        self.secbootkey = TPAsymmetricKey(privkey_file)
        self.secbootkey.get_private_pem(privkey_file)
        self.resources = ResourceGeneration()
        #secure boot public key
        assert self.resources.load_public_key(
                    self.secboot_pubkey_slot,
                    self.secbootkey.get_public_key_bytes()) \
               == cal.Status.ATCA_SUCCESS, \
               "Loading Secure Boot public key failed"

    def generate_io_key(self, b=None):
        # io protection key
        print('Generating IOPROT Key...', canvas=b)
        ip_key_file = 'slot_{}_secret_key'.format(
                                self.io_protection_key_slot) + '.pem'
        self.ip_key = TPSymmetricKey(ip_key_file)
        assert self.resources.load_secret_key(
                    self.io_protection_key_slot,
                    self.ip_key.get_bytes()) \
               == cal.Status.ATCA_SUCCESS, \
               "Loading io protection key failed"
        print('IOPROT Key:', canvas=b)
        print(pretty_print_hex(self.ip_key.get_bytes()), canvas=b)
        print('OK', canvas=b)

    def load_hex_file(self, b=None):
        print('Loading Hex File...', canvas=b)

        #load data from hex file
        self.hex_file = IntelHex()
        self.hex_file.fromfile(self.__get_hex_file(b), format='hex')

        print("\nConfigured BOOTOPT for this HEX file is :"+str(mcu.getBootopt(self.hex_file)))
        BNSC_SIZE, BOOTPROT_SIZE = mcu.getRegions(self.hex_file)
        print("\nBNSC size: ", str(BNSC_SIZE))
        print("\nBOOTPROT size: ", str(BOOTPROT_SIZE))

        #calculate digest
        data = self.hex_file.tobinarray(start=0x00000000, size=BOOTPROT_SIZE-64)

        print("\nHashing "+str(len(data))+" bytes in BS Region")
        hasher = hashes.Hash(
            hashes.SHA256(),
            backend=cryptography.hazmat.backends.default_backend()
        )
        hasher.update(data)
        self.digest = hasher.finalize()[:32]
        print('Digest:', canvas=b)
        print(pretty_print_hex(self.digest), canvas=b)

        #hasher = mcu.calculateDigest(self.hex_file)
        #print("\nSHA-256 Application Digest")
        #print(pretty_print_hex(hasher))

        # Sign the hex file
        self.signature = sign_on_host(
                        self.digest,
                        self.secbootkey.get_private_key())
        print('Signature:', canvas=b)
        print(pretty_print_hex(self.signature), canvas=b)

        #print("\nECDSA Application Signature")
        #self.signature = mcu.signDigest(hasher, self.secbootkey.get_private_key())
        #print(pretty_print_hex(self.signature))


    def save_app_hex(self, b=None):
        BNSC_SIZE, BOOTPROT_SIZE = mcu.getRegions(self.hex_file)

        self.signedFinalHex = "signed.hex"

        print("Saving new Hex file...", canvas=b)
        #self.signedHex = mcu.addSignatureToHex(self.hex_file, self.signature)
        #finalHex = mcu.setupBOCORioprotkey(self.ip_key.get_bytes(),self.signedHex)
        #mcu.saveHex(self.signedFinalHex, finalHex)

        ip_addr = mcu.getIOPROTaddress()
        self.hex_file.puts(ip_addr, self.ip_key.get_bytes())

        self.hex_file.puts(BOOTPROT_SIZE-64, self.signature) #removed sign start address and replaced it with BOOTPROTSIZE-64 - 2/15/22
        #app_len = self.end_addr - self.app_start_addr
        print("Writing boot signature starting at location: ", str(BOOTPROT_SIZE-BNSC_SIZE-64))
        #self.hex_file.puts(
                        #self.app_len_str_addr,
                        #app_len.to_bytes(4, 'little'))
        self.hex_file.tofile(self.signedFinalHex, format='hex')

    def flash_firmware(self, b=None):
        flash_firmware = FlashProgram(board_name='EV76R77A')
        print(f'Programming {self.signedFinalHex} file...', canvas=b)
        flash_firmware.load_hex_image_with_ipe(self.signedFinalHex)
        print('Success', canvas=b)

    def __connect_to_SE(self, b=None):
        print('Connect to Secure Element: ', canvas=b)
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

    def __get_private_key_file(self, b=None):
        print('Select secure boot private key option', canvas=b)
        item_list = ['Generate Private key', 'Upload Private key']
        dropdown_desc = (
        '''<font color=#0000ff><b>Select Secure Boot private key option</b>
        </font><br>
        <br>Generate Private key - Generates new Secure Boot private key<br>
        Upload Private key - Use existing private key file. Requires
        private key file .pem<br>''')
        user_input = tp_userinput.TPInputDropdown(
                                    item_list=item_list,
                                    desc=dropdown_desc,
                                    dialog_title='Private key selection')
        user_input.invoke_dialog()
        print(f'Selected option is: {user_input.user_option}', canvas=b)
        assert user_input.user_option is not None, \
            'Select valid private key Option'

        if user_input.user_option == 'Upload Private key':
            print('Select private key file...', canvas=b)
            privkey = tp_userinput.TPInputFileUpload(
                                        file_filter=['*.pem'],
                                        nav_dir = os.getcwd(),
                                        dialog_title='Upload Private key')
            privkey.invoke_dialog()
            print(
                f'Selected private key file is: {privkey.file_selection}',
                canvas=b)
            assert privkey.file_selection is not None, \
                    'Select valid private key file'
            return privkey.file_selection
        else:
            privkey_file = 'slot_{}_ecc_private_key'.format(
                                self.secboot_pubkey_slot) + '.pem'
            return privkey_file

    def __get_hex_file(self, b=None):
        print('Select hex file to load...', canvas=b)
        hexfile = tp_userinput.TPInputFileUpload(
                                    file_filter=['*.hex'],
                                    nav_dir = os.getcwd(),
                                    dialog_title='Upload Hex File')
        hexfile.invoke_dialog()
        print(
            f'Selected hex file is: {hexfile.file_selection}',
            canvas=b)
        assert hexfile.file_selection is not None, \
                'Select valid hex file'
        return hexfile.file_selection
