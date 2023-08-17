
//TODO: Need to have this as JSON object and use in the appropriate JS files.

var Boards = {
    100: {
        name: "DM320118",
        imgpath: "images/kits/190717-SPG-PHOTO-DM320118-Angle-Transparent.png",
        weblink: "https://www.microchip.com/developmenttools/productdetails/DM320118",
        kitparser_hex: "",
        selected: false,
        usecases: [100, 101, 102, 103, 104]
    },
};

var UseCases = {
    // TFLEX Usecases list starts.....
    100: {
        title: "Secure Boot",
        selected: false,
        ids: ["Slot15"],
        imgpath: "images/trustflex_usecase_img/Firmware_validation.png"
    },
    101: {
        title: "Firmware Upgrade Validation",
        selected: false,
        ids: ["Slot15"],
        imgpath: "images/trustflex_usecase_img/Firmware_upgrade_validation.png"
    },
    102: {
        title: "Public Key Rotation",
        selected: false,
        ids: ["Slot13", "Slot14"],
        imgpath: "images/trustflex_usecase_img/Public_key_rotation.png"
    },
    103: {
        title: "IP Protection",
        selected: false,
        ids: ["Slot5"],
        imgpath: "images/trustflex_usecase_img/IP_Protection.png"
    },
    104: {
        title: "Asymmetric Authentication",
        selected: false,
        ids: ["Slot10", "Slot12", "custCertPubkey"],
        certs: "custom",
        prefix: 2, //custom selection
        imgpath: "images/trustflex_usecase_img/Asymmetric_authentication.png"
    },
    105: {
        title: "Symmetric Authentication",
        selected: false,
        ids: ["Slot5"],
        imgpath: "images/trustflex_usecase_img/Symmetric_authentication.png"
    },
    107: {
        title: "Google Authentication",
        selected: false,
        ids: [],
        imgpath: "images/trustflex_usecase_img/GCP.png"
    },
    108: {
        title: "AWS Authentication",
        selected: false,
        ids: [],
        imgpath: "images/trustflex_usecase_img/AWS.png"
    },
    109: {
        title: "MS Azure Authentication",
        selected: false,
        ids: [],
        imgpath: "images/trustflex_usecase_img/MS_Azure.png"
    },
    110: {
        title: " Custom PKI AWS Authentication",
        selected: false,
        ids: ["Slot10", "Slot12", "custCertPubkey"],
        certs: "custom",
        prefix: 1, //default selection
        imgpath: "images/trustflex_usecase_img/AWS_custom_pki.png"
    },
    111: {
        title: " Custom PKI MS Azure Authentication",
        selected: false,
        ids: ["Slot10", "Slot12", "custCertPubkey"],
        certs: "custom",
        prefix: 1,
        imgpath: "images/trustflex_usecase_img/MS_Azure_custom_pki.png"
    },

    // TNG Usecases list starts.....
    200: {
        name: "cloud_aws_tng",
        title: "Cloud Connect - Amazon",
        summary: "",
        notebook_path: "",
        selected: false,
        ids: [],
        imgpath: "images/usecases/default_usecase.png"
    },
    201: {
        name: "cloud_gcp_tng",
        title: "Cloud Connect - Google",
        summary: "",
        notebook_path: "",
        selected: false,
        ids: [],
        imgpath: "images/usecases/default_usecase.png"
    },
    202: {
        name: "cloud_azure_tng",
        title: "Cloud Connect - Microsoft",
        summary: "",
        notebook_path: "",
        selected: false,
        ids: [],
        imgpath: "images/usecases/default_usecase.png"
    },
};

//TODO: TNG usecase list should also contain details similar to TFLX.
// Notebook should be opened based on board and usecase selected
var tng_usecases_list = [200, 201, 202]
