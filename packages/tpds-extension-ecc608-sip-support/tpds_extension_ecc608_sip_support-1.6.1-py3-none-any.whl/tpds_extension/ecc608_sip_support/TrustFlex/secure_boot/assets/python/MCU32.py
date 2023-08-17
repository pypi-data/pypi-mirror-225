
##### SOme constants used
boot_start = 0x00000000
bootprotHashStart = 0x00000000
Conf_bootprot_start = 0x00080C005   #Config word addresses
Conf_bootprot_end = 0x00080C007
Conf_bnsc_start = 0x0080C002
Conf_bnsc_end = 0x0080C004
Conf_bootopt_start = 0x0080C004
Conf_ioprot_start = 0x0080C090
sigsize = 64                        #Sign of the Signature/Digest



def getBootopt(memory):
    #This function decodes the BOOTOPT value for use later
    temp = memory[Conf_bootopt_start]
    BOOTOPT = (temp & 0xff)

    #original
    #temp = memory[Conf_bootopt_start:Conf_bootopt_start+1]
    #BOOTOPT = (temp[0] & 0xff)
    return BOOTOPT

def getRegions(memory):
    #This function takes a memory object and pulls IDAU_BOOTPROT + IDAU_BNSC sizes
    #BNSC = memory[Conf_bnsc_start:Conf_bnsc_end]
    BNSC_start = memory[Conf_bnsc_start]
    BNSC_end = memory[Conf_bnsc_start+1]

    BNSC_SIZE = ((((BNSC_end & 0x0F) << 8) + (BNSC_start & 0xf8)) >> 3) * 0x20
    #BNSC_SIZE = ((((BNSC[1] & 0x0F) << 8) + (BNSC[0] & 0xf8)) >> 3) * 0x20
    #print("\nConfig Word BOCOR_WORD_0 IDAU_BNSC Size: "+str(BNSC_SIZE)+" Bytes")

    BOOTPROT_start = memory[Conf_bootprot_start]
    BOOTPROT_end = memory[Conf_bootprot_start+1]
    #BOOTPROT = memory[Conf_bootprot_start:Conf_bootprot_end]

    BOOTPROT_SIZE = (((BOOTPROT_end & 0x07) << 8) + (BOOTPROT_start & 0xff)) * 0x100
    #BOOTPROT_SIZE = (((BOOTPROT[1] & 0x07) << 8) + (BOOTPROT[0] & 0xff)) * 0x100
    #print("\nConfig Word BOCOR_WORD_1 IDAU_BOOTPROT Size: "+str(BOOTPROT_SIZE)+" Bytes")
    # print("\n[!] Getting boot partition sizes")
    # print("\t[x] Config Word BOCOR_WORD_0 IDAU_BNSC Size: "+str(BNSC_SIZE)+" Bytes")
    # print("\t[x] Config Word BOCOR_WORD_1 IDAU_BOOTPROT Size: "+str(BOOTPROT_SIZE)+" Bytes")
    return BNSC_SIZE, BOOTPROT_SIZE

def getIOPROTaddress():
#def setupBOCORioprotkey(io_key, signedHex):
    #signedHex.write(Conf_ioprot_start, io_key)
    return Conf_ioprot_start


