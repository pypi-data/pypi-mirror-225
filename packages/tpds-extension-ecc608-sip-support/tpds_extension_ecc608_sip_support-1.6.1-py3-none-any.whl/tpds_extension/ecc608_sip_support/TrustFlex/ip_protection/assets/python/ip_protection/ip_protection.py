import os
import cryptoauthlib as cal
from pathlib import Path
from tpds.resource_generation import TFLXResources, TFLXSlotConfig
from tpds.flash_program import FlashProgram
from tpds.secure_element import ECC608A
from tpds.tp_utils.tp_settings import TPSettings
from tpds.tp_utils.tp_print import print
from tpds.tp_utils.tp_keys import TPSymmetricKey
from tpds.tp_utils.tp_utils import pretty_print_hex

class IPProtection():
    """Authenticates a connected device using Symmetric Key.
    """
    def __init__(self, boards, symm_key_slot):
        """Constructs required resources.

        Args:
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        self.boards = boards
        self.shared_secret_slot = symm_key_slot
        self.mac_mode = 0x41

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
        self.element = ECC608A(address=0xC0)
        print('OK', canvas=b)
        print('Device details: {}'.format(self.element.get_device_details()))
        self.ser_num = self.element.get_device_serial_number().hex().upper()

    def generate_resources(self, b=None):
        """Generated required resources.
        Symmetric Key is generated.
        Slot 5 that holds a shared Symmetric Key.

        Args:
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        self.__connect_to_SE(b)

        print('Generating crypto assets for Usecase...', canvas=b)
        resources = TFLXResources()
        tflex_slot_config = TFLXSlotConfig().tflex_slot_config

        symm_slot = self.shared_secret_slot
        symm_key_slot_config = tflex_slot_config.get(symm_slot)
        assert symm_key_slot_config.get('type') == 'secret', \
            "Invalid Slot, It is expected to be secret"

        enc_slot = symm_key_slot_config.get('enc_key', None)
        enc_key = Path('slot_{}_secret_key.pem'.format(
                enc_slot)) if enc_slot else None

        # Load encrypted Key
        if enc_key is not None:
            secret_key = Path('slot_{}_secret_key.pem'.format(enc_slot))
            assert resources.load_secret_key(
                    enc_slot, enc_key, None,
                    None) == cal.Status.ATCA_SUCCESS, \
                "Loading encrypted key into slot{} failed".format(enc_slot)

        # Load symmetric Key
        secret_key = Path('slot_{}_secret_key.pem'.format(symm_slot))
        assert resources.load_secret_key(
                symm_slot, secret_key, enc_slot,
                enc_key) == cal.Status.ATCA_SUCCESS, \
            "Loading secret key into slot{} failed".format(symm_slot)
        print('OK', canvas=b)

    def host_initiate_auth(self, b=None):
        print('Generating challenge input value...', canvas=b)
        self.num_in = os.urandom(20)
        print("Nonce Input value:")
        print(pretty_print_hex(self.num_in, li=10, indent=''))
        print('OK', canvas=b)

    def generate_mac_on_device(self, b=None):
        """Calculating the MAC on ECC608A device.

        The MAC is generated with the symmetric key in slot,
        Random number and with device serial number.

        Args:
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        print('Getting MAC from device...', canvas=b)
        self.rand_out = self.element.get_device_random_nonce(self.num_in)
        self.device_mac = self.element.get_device_mac_response(
                                            self.shared_secret_slot,
                                            0,
                                            self.mac_mode)
        print("MAC Received from device:")
        print(pretty_print_hex(self.device_mac, indent=''))
        print('OK', canvas=b)

    def generate_mac_on_host(self, b=None):
        """Using Symmetric Key, random nonce and the TFLXTLS serial number,
        the host generates expected MAC.

        Args:
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        print('Calculating MAC on Host...', canvas=b)
        host = self.element.host_calc_nonce(
                                            self.num_in,
                                            self.rand_out['rand_out'])
        symm_key = TPSymmetricKey(
            key='slot_{}_secret_key.pem'.format(
                                            self.shared_secret_slot))
        resp = self.element.host_calc_mac_resp(
                                            symm_key.key_bytes,
                                            host['nonce'],
                                            self.mac_mode,
                                            self.shared_secret_slot)
        self.host_mac = resp['response']
        print('MAC calculated on host:')
        print(pretty_print_hex(self.host_mac, indent=''))
        print('OK', canvas=b)

    def compare_generated_macs(self, b=None):
        """Checks if both the MACs are the same and authenticate the connected device.

        Args:
            b (canvas object, optional): If Usecase Diagram canvas is used,
                                        these messages go onto popup window.
                                        Defaults to None.
        """
        if self.host_mac == self.device_mac:
            print('\nApplication authenticated successfully!', canvas=b)
        else:
            print('\nApplication is not authenticated...', canvas=b)
