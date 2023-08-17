ws = new WebSocket("ws://localhost:1302/websocket");
var applicationCategory_arr = [100, 101, 102, 103, 104];
var applicationCategory = {
    100: {
        name: "accessoryauthentication",
        title: "Accessory Authentication",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/applicationCategory/accessories-red.jpg",
        _prodcat: [200],
        _prodlist: [302, 303, 304, 310, 311],
        _usecaselist: [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 511, 514, 515]
    },
    101: {
        name: "disposableauthentication",
        title: "Disposable Authentication",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/applicationCategory/disposable-red.jpg",
        _prodcat: [200],
        _prodlist: [302, 303, 304, 310, 311],
        _usecaselist: [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 511, 514, 515]
    },
    102: {
        name: "iot",
        title: "IoT",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/applicationCategory/IoT-red.jpg",
        _prodcat: [200, 203, 204],
        _prodlist: [300, 301, 302, 303, 305, 306],
        _usecaselist: [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 511, 512, 514, 515]
    },
    103: {
        name: "automotive",
        title: "Automotive",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/applicationCategory/automotive-red.jpg",
        _prodcat: [200],
        _prodlist: [307],
        _usecaselist: [503, 504, 513, 510]
    },
    104: {
        name: "wirelesscharging",
        title: "Wireless Charging",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/applicationCategory/wireless-power-red.jpg",
        _prodcat: [],
        _prodlist: [309],
        _usecaselist: [510]
    },
}

var productCategory_arr = [200, 201, 202, 203, 204];
var productCategory = {
    200: {
        name: "secureelements",
        title: "Secure Elements",
        selected: false,
        imgpath: "assets/html/images/productCategory/secure-element-red.jpg",
        highlight: true,
        _applist: [100, 101, 102, 103],
        _prodlist: [300, 301, 302, 303, 304, 307],
        _usecaselist: [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515]
    },
    201: {
        name: "16bitmcu",
        title: "16-Bit MCU",
        selected: false,
        imgpath: "assets/html/images/productCategory/MCU16.jpg",
        highlight: true,
        _applist: [],
        _prodlist: [],
        _usecaselist: []
    },
    202: {
        name: "32bitmcu",
        title: "32-Bit MCU",
        selected: false,
        imgpath: "assets/html/images/productCategory/MCU32.jpg",
        highlight: true,
        _applist: [],
        _prodlist: [],
        _usecaselist: []
    },
    203: {
        name: "32bitmpu",
        title: "32-Bit MPU",
        selected: false,
        imgpath: "assets/html/images/productCategory/MPU.jpg",
        highlight: true,
        _applist: [102],
        _prodlist: [305],
        _usecaselist: [500, 501, 502]
    },
    204: {
        name: "wireless",
        title: "Wireless",
        selected: false,
        imgpath: "assets/html/images/productCategory/Wireless.jpg",
        highlight: true,
        _applist: [102],
        _prodlist: [306],
        _usecaselist: [500, 501, 502]
    }
}

var products_arr = [300, 301, 302, 303, 304, 305, 306, 307, 309, 310, 311];
var products = {
    300: {
        name: "ecc608b-tngtls",
        title: "ATECC608B-TNGTLS",
        category: "TrustnGO",
        selected: false,
        highlight: true,
        _applist: [102],
        _prodcat: [200],
        _usecaselist: [500, 501, 502],
        _boardslist: [600, 602, 605, 606]
    },
    301: {
        name: "ecc608b-tnglora",
        title: "ATECC608B-TNGLORA",
        category: "TrustnGO",
        selected: false,
        highlight: true,
        _applist: [102],
        _prodcat: [200],
        _usecaselist: [512],
        _boardslist: [],
        resource_page: "https://github.com/MicrochipTech/cryptoauthlib/wiki/TTI-Getting-Started"
    },
    302: {
        name: "eec608b-tflxtls",
        title: "ATECC608B-TFLXTLS",
        category: "TrustFLEX",
        selected: false,
        secret_exchange_page: 'assets/html/TrustFLEX configurator.html',
        highlight: true,
        _applist: [100, 101, 102],
        _prodcat: [200],
        _usecaselist: [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 511, 514, 515],
        _boardslist: [600, 602]
    },
    303: {
        name: "ecc608b-tcsm",
        title: "ATECC608B-TCSM",
        category: "TrustCUSTOM",
        selected: false,
        secret_exchange_page: 'https://www.microchip.com/en-us/product/SW-ATECC608B',
        highlight: true,
        _applist: [100, 101, 102],
        _prodcat: [200],
        _usecaselist: [503, 504, 505, 506, 507, 508, 509, 511, 514, 515],
        _boardslist: [600]
    },
    304: {
        name: "sha204a-tcsm",
        title: "ATSHA204A-TCSM",
        category: "TrustCUSTOM",
        selected: false,
        secret_exchange_page: 'assets/html/ATSHA204A TrustCustom.html',
        highlight: true,
        _applist: [100, 101],
        _prodcat: [200],
        _usecaselist: [508],
        _boardslist: []
    },
    305: {
        name: "atsama5d27-wlsom1",
        title: "ATSAMA5D27-WLSOM1",
        category: "TrustnGO",
        selected: false,
        highlight: true,
        _applist: [102],
        _prodcat: [203],
        _usecaselist: [500, 501, 502],
        _boardslist: [],
        resource_page: "https://www.microchip.com/wwwproducts/en/ATSAMA5D27-WLSOM1"
    },
    306: {
        name: "wfi32e01",
        title: "WFI32E01",
        category: "TrustnGO",
        selected: false,
        highlight: true,
        _applist: [102],
        _prodcat: [204],
        _usecaselist: [500, 501, 502],
        _boardslist: [],
        resource_page: "https://www.microchip.com/wwwproducts/en/WFI32E01PC"
    },
    307: {
        name: "ta100-vao",
        title: "TA100-VAO",
        category: "TrustCUSTOM",
        selected: false,
        secret_exchange_page: 'https://www.microchip.com/en-us/product/SW-TA100',
        highlight: true,
        _applist: [103],
        _prodcat: [200],
        _usecaselist: [503, 504, 510, 513],
        _boardslist: [607]
    },
    // 308: {
    //     name: "pic32cmls60",
    //     title: "PIC32CMLS60",
    //     category: "TrustFLEX",
    //     selected: false,
    //     secret_exchange_page: 'assets/html/PIC32CMLS60_Secret_Exchange.html',
    //     highlight: true,
    //     _applist: [100, 101, 102],
    //     _prodcat: [202],
    //     _usecaselist: [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 511],
    //     _boardslist: []
    // },
    309: {
        name: "ecc608-tflxwpc",
        title: "ECC608-TFLXWPC",
        category: "TrustFLEX",
        selected: false,
        highlight: true,
        secret_exchange_page: 'https://www.microchip.com/en-us/product/SW-ECC608-TFLXWPC',
        _applist: [104],
        _prodcat: [],
        _usecaselist: [510],
        _boardslist: []
    },
    310: {
        name: "NextGen-ECC-tflxauth",
        title: "NextGen ECC-TFLXAUTH",
        category: "TrustFLEX",
        selected: false,
        secret_exchange_page: 'https://www.microchip.com/en-us/product/SW-ECC204-TFLXAUTH',
        highlight: true,
        _applist: [100, 101],
        _prodcat: [200],
        _usecaselist: [508, 509],
        _boardslist: [600]
    },
    311: {
        name: "NextGen-TA-tflxauth",
        title: "NextGen TA-TFLXAUTH",
        category: "TrustFLEX",
        selected: false,
        secret_exchange_page: 'https://www.microchip.com/en-us/product/SW-TA010-TFLXAUTH',
        highlight: true,
        _applist: [100, 101],
        _prodcat: [200],
        _usecaselist: [508, 509],
        _boardslist: [600]
    },
}

var usecaselist_arr = [500, 501, 502, 503, 504, 505, 514, 506, 515, 507, 508, 509, 510, 511, 512, 513];
var usecaselist = {
    500: {
        name: "aws_iot",
        title: "AWS IoT Authentication",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/AWS.png",
        _applist: [100, 101, 102],
        _prodcat: [200, 203, 204],
        _prodlist: [300, 302, 305, 306],
        nbpath: {
            300: ["TrustnGO/05_cloud_connect/AWS Connect-IoT Auth-TNG.ipynb"],
            302: ["TrustFLEX/10_cloud_connect/AWS Connect-IoT Auth-TFLEX.ipynb"]
        }
    },
    501: {
        name: "azure",
        title: "Azure IoT Authentication",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/Azure.png",
        _applist: [100, 101, 102],
        _prodcat: [200, 203, 204],
        _prodlist: [300, 302, 305, 306],
        nbpath: {
            300: ["TrustnGO/05_cloud_connect/Azure Connect-IoT Auth-TNG.ipynb"],
            302: ["TrustFLEX/10_cloud_connect/Azure Connect-IoT Auth-TFLEX.ipynb"]
        }
    },
    502: {
        name: "gcp",
        title: "GCP IoT Authentication",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/GCP.png",
        _applist: [100, 101, 102],
        _prodcat: [200, 203, 204],
        _prodlist: [300, 302, 305, 306],
        nbpath: {
            300: ["TrustnGO/05_cloud_connect/Google Connect-IoT Auth-TNG.ipynb"],
            302: ["TrustFLEX/10_cloud_connect/Google Connect-IoT Auth-TFLEX.ipynb"]
        }
    },
    503: {
        name: "firmwarevalidation",
        title: "Firmware Validation",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/Firmware validation.png",
        _applist: [100, 101, 102, 103],
        _prodcat: [200],
        _prodlist: [302, 303, 307],
        nbpath: {
            302: ["TrustFLEX/02_firmware_validation/Firmware Validation.ipynb"]
        }
    },
    504: {
        name: "firmwareupgradeauthentication",
        title: "Firmware Upgrade Validation",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/OTA upgrade authentication.png",
        _applist: [100, 101, 102, 103],
        _prodcat: [200],
        _prodlist: [302, 303, 307],
        nbpath: {}
    },
    505: {
        name: "custompkiaws",
        title: "Custom PKI AWS",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/AWS.png",
        _applist: [100, 101, 102],
        _prodcat: [200],
        _prodlist: [302, 303],
        nbpath: {
            302: ["TrustFLEX/10_cloud_connect/AWS Connect-Custom PKI-TFLEX.ipynb"]
        }
    },
    506: {
        name: "custompkimsazure",
        title: "Custom PKI MS Azure",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/Azure.png",
        _applist: [100, 101, 102],
        _prodcat: [200],
        _prodlist: [302, 303],
        nbpath: {
            302: ["TrustFLEX/10_cloud_connect/Azure Connect-Custom PKI-TFLEX.ipynb"]
        }
    },
    507: {
        name: "pubkeyrotation",
        title: "Public Key Rotation",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/Public key rotation.png",
        _applist: [100, 101, 102],
        _prodcat: [200],
        _prodlist: [302, 303],
        nbpath: {
            302: ["TrustFLEX/05_public_key_rotation/Public Key Rotation.ipynb"],
            308: ["TrustFLEX/05_public_key_rotation/Public Key Rotation_LifeGuard.ipynb"]
        }
    },
    508: {
        name: "symmetricAccessory",
        title: "Symmetric Authentication",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/symmetric key auth.png",
        _applist: [100, 101, 102],
        _prodcat: [200],
        _prodlist: [302, 303, 304, 310, 311],
        nbpath: {
            302: ["TrustFLEX/01_accessory_authentication/Accessory Authentication.ipynb"]
        }
    },
    509: {
        name: "asymmetricaccessory",
        title: "Asymmetric Authentication",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/asymmetric key auth.png",
        _applist: [100, 101, 102],
        _prodcat: [200],
        _prodlist: [302, 303, 310, 311],
        nbpath: {
            302: ["TrustFLEX/08_asymmetric_authentication/Asymmetric Authentication.ipynb"]
        }
    },
    510: {
        name: "wpc",
        title: "WPC Qi 1.3 Authentication",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/WPC Qi.png",
        _applist: [103, 104],
        _prodcat: [200],
        _prodlist: [307, 309],
        nbpath: {}
    },
    511: {
        name: "ipprotection",
        title: "IP Protection",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/IP protection.png",
        _applist: [100, 101, 102],
        _prodcat: [200],
        _prodlist: [302, 303],
        nbpath: {
            302: ["TrustFLEX/04_ip_protection/IP Protection.ipynb"]
        }
    },
    512: {
        name: "lorawanauthetication",
        title: "LoRaWAN authentication",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/LoRawan.png",
        _applist: [102],
        _prodcat: [200],
        _prodlist: [301],
        nbpath: {}
    },
    513: {
        name: "canmessageauthentication",
        title: "CAN Message Authentication",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/CAN.jpg",
        _applist: [103],
        _prodcat: [200],
        _prodlist: [307],
        nbpath: {}
    },
    514: {
        name: "avnetiotconnectcustompki",
        title: "Custom PKI Avnet IoTConnect",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/Avnet.png",
        _applist: [100, 101, 102],
        _prodcat: [200],
        _prodlist: [302, 303],
        nbpath: {
            302: ["TrustFLEX/10_cloud_connect/avnet_iotconnect/Avnet IoTConnect.ipynb"]
        }
    },
    515: {
        name: "gcp",
        title: "Custom PKI GCP",
        selected: false,
        highlight: true,
        imgpath: "assets/html/images/usecases/GCP.png",
        _applist: [100, 101, 102],
        _prodcat: [200],
        _prodlist: [302, 303],
        nbpath: {
            302: ["TrustFLEX/10_cloud_connect/Google Connect-Custom PKI-TFLEX.ipynb"]
        }
    },
}

var evalboardselection_arr = [600, 601, 602, 603, 604, 605, 606];
var evalboardselection = {
    600: {
        name: "atecc608 dm320118",
        title: "ATECC608 DM320118",
        imgpath: "assets/html/images/kits/DM320118.jpg",
        weblink: "https://www.microchip.com/developmenttools/productdetails/DM320118",
    },
    601: {
        name: "mcu32 ev76r77a",
        title: "MCU32 EV76R77A",
        imgpath: "",
        weblink: "#",
    },
    602: {
        name: "evb-iot secure shield",
        title: "EBV-IoT Secure Shield",
        imgpath: "assets/html/images/kits/EBV-IoT Secure Shield.jpg",
        weblink: "https://iotconnect.io/ebv/ebv-mchp-secure-solution.html",
    },
    603: {
        name: "arrow shield96",
        title: "Arrow Shield96",
        imgpath: "",
        weblink: "#",
    },
    604: {
        name: "dt100104",
        title: "DT100104",
        imgpath: "assets/html/images/kits/DT100104.jpg",
        weblink: "https://www.microchip.com/developmenttools/ProductDetails/DT100104"
    },
    605: {
        name: "wfi32e01",
        title: "WFI32E01",
        imgpath: "assets/html/images/kits/WFI32E01PE.png",
        weblink: "https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/EV12F11A"
    },
    606: {
        name: "atsama5d27-wlsom1",
        title: "ATSAMA5D27-WLSOM1",
        imgpath: "assets/html/images/kits/ATSAMA5D27-WLSOM1.png",
        weblink: "https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM320117"
    },
    607: {
        name: "socketboard",
        title: "DM320118 + TA100 Socket Board",
        imgpath: "assets/html/images/kits/DM320118_AC164167.jpg",
        weblink: "https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/AC164167"
    }
}

var resource_page_items = [301, 305, 306]
var not_available_items = [201, 202, 104, 309];
var trustGO = [];
var trustFLEX = [];
var trustCUSTOM = [];
for(var key in products){
    if(products[key].category == "TrustnGO"){
        trustGO.push(Number(key));
    }
    else if(products[key].category == "TrustFLEX"){
        trustFLEX.push(Number(key));
    }
    else{
        trustCUSTOM.push(Number(key));
    }
}
var dark = "#5B9BD5";
var light = "white";

var track_app = [];
var track_prodcat = [];
var track_usecase = [];

var coll = document.getElementsByClassName("collapsible");
var i;
for (i = 0; i < coll.length; i++) {
coll[i].addEventListener("click", function() {
    this.classList.toggle("active1");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
});
}

$(document).ready(function(){
    for(var ele in applicationCategory_arr){
        var key = applicationCategory_arr[ele];
        append_applicationCategory(key);}
    for(var ele in productCategory_arr){
        var key = productCategory_arr[ele];
        append_productCategory(key);}
    for(var ele in usecaselist_arr){
        var key = usecaselist_arr[ele];
        append_usecases(key);}
    for(var key in trustGO){append_trustgo_p(key);}
    for(var key in trustFLEX){append_trustflex_p(key);}
    for(var key in trustCUSTOM){append_trustcustom_p(key);}
});

function append_applicationCategory(key){
    $('#application_category').append(
    $('<div>', {'class': 'app_item'}).append(
        $('<div>', {'style':'width: 15%;'}).append(
            $('<img>', {'src': applicationCategory[key].imgpath, 'style':'width:60%'}),
        ),
        $('<div>', {'style':'width: 85%;'}).append(
            $('<div>', {'title': 'Click to Select/Deselect',
            'class': 'image_btn_1 app_item_head', 'id':key}).append(
                $('<p>', {'text': applicationCategory[key].title, 'class':'image_overlay_bottom_app', 'id':applicationCategory[key].name+'Img' }),
                $('<div>', {'class': 'tooltip'}),
                $('<div>', {'class': 'forbidden_image'}).append(
                    $('<img>', {'src': "assets/html/images/1200px-ProhibitionSign2.png", 'class': 'image_overlay_top_fd'})),
                $('<div>', {'class': 'check_image'}).append(
                    $('<img>', {'src': "assets/html/images/check-mark-png-11553206004impjy81rdu.png", 'class': 'image_overlay_top'}))
    ))))
    if(not_available_items.indexOf(key)>-1){
        $('#'+key).append(
            $('<div>', {'class': 'available_soon_img'}).append(
                $('<img>', {'src': "assets/html/images/available_soon.png", 'style':' width: 70px; height: 35px;'}))
    )}
}
function append_productCategory(key){
    $('#product_category').append(
    $('<div>', {'class': 'app_item'}).append(
        $('<div>', {'style':'width: 15%;'}).append(
            $('<img>', {'src': productCategory[key].imgpath, 'style':'width:60%'}),
        ),
        $('<div>', {'style':'width: 85%;'}).append(
            $('<div>', {'title': 'Click to Select/Deselect',
            'class': 'image_btn_2 app_item_head', 'id':key}).append(
                $('<p>', {'text': productCategory[key].title, 'class':'image_overlay_bottom_app', 'id':productCategory[key].name+'Img' }),
                $('<div>', {'class': 'tooltip'}),
                $('<div>', {'class': 'forbidden_image'}).append(
                    $('<img>', {'src': "assets/html/images/1200px-ProhibitionSign2.png", 'class': 'image_overlay_top_fd'})),
                $('<div>', {'class': 'check_image'}).append(
                    $('<img>', {'src': "assets/html/images/check-mark-png-11553206004impjy81rdu.png", 'class': 'image_overlay_top'}))
    ))))
    if(not_available_items.indexOf(key)>-1){
        $('#'+key).append(
            $('<div>', {'class': 'available_soon_img'}).append(
                $('<img>', {'src': "assets/html/images/available_soon.png", 'style':' width: 70px; height: 35px;'}))
    )}
}
function append_usecases(key){
    $('#usecases').append(
            $('<div>', {'class': 'app_item'}).append(
                $('<div>', {'style':'width: 15%;'}).append(
                    $('<img>', {'src': usecaselist[key].imgpath, 'style':'width:60%'}),
                ),
                $('<div>', {'style':'width: 85%;'}).append(
                    $('<div>', {'title': 'Click to Select/Deselect',
                    'class': 'image_btn_3 app_item_head', 'id':key}).append(
                        $('<p>', {'text': usecaselist[key].title, 'class':'image_overlay_bottom_app', 'id':usecaselist[key].name+'Img' }),
                        $('<div>', {'class': 'tooltip'}),
                        $('<div>', {'class': 'forbidden_image'}).append(
                            $('<img>', {'src': "assets/html/images/1200px-ProhibitionSign2.png", 'class': 'image_overlay_top_fd'})),
                        $('<div>', {'class': 'check_image'}).append(
                            $('<img>', {'src': "assets/html/images/check-mark-png-11553206004impjy81rdu.png", 'class': 'image_overlay_top'}))
    ))))
    if(not_available_items.indexOf(key)>-1){
        $('#'+key).append(
            $('<div>', {'class': 'available_soon_img'}).append(
                $('<img>', {'src': "assets/html/images/available_soon.png", 'style':' width: 70px; height: 35px;'}))
    )}
}
function append_trustgo_p(key){
    $('#trustgo_p').append(
            $('<div>', {'class': 'app_item_p'}).append(
                $('<div>', {'id': 'option_div'+trustGO[key]}).append(
                    $('<div>', {'title': 'Click to Select/Deselect',
                    'class': 'image_btn_4 app_item_head_go', 'id':trustGO[key]}).append(
                        $('<p>', {text: products[trustGO[key]].title, 'class':'image_overlay_bottom_app app_item_head_base', 'id':products[trustGO[key]].name+'Img' }),
                        $('<div>', {'class': 'tooltip'}),
                        $('<div>', {'class': 'forbidden_image'}).append(
                            $('<img>', {'src': "assets/html/images/1200px-ProhibitionSign2.png", 'class': 'image_overlay_top_fd'})),
                        $('<div>', {'class': 'check_image'}).append(
                            $('<img>', {'src': "assets/html/images/check-mark-png-11553206004impjy81rdu.png", 'class': 'image_overlay_top'}))),
    )))
    if(resource_page_items.indexOf(trustGO[key])>-1){
        $('#option_div'+trustGO[key]).append(
        $('<div>', {'class': 'open_notebook_option'}).append(
            $('<input>', {'class':'resource_page','id':'nb'+trustGO[key], 'type':'button', 'value':'Resource Page', 'onclick':'resource_page_fn('+trustGO[key]+')', 'disabled':false, 'style':'background-color:#FBDB65;color:black'})))}
    else{
        $('#option_div'+trustGO[key]).append(
        $('<div>', {'class': 'open_notebook_option'}).append(
            $('<input>', {'class':'notebook','id':'nb'+trustGO[key], 'type':'button', 'value':'Usecase', 'disabled':true, 'style':''})))
    }
    if(not_available_items.indexOf(trustGO[key])>-1){
        $('#'+trustGO[key]).append(
            $('<div>', {'class': 'available_soon_img'}).append(
                $('<img>', {'src': "assets/html/images/available_soon.png", 'style':' width: 70px; height: 35px;'}))
    )}

}
function append_trustflex_p(key){
    $('#trustflex_p').append(
            $('<div>', {'class': 'app_item_p'}).append(
                $('<div>').append(
                    $('<div>', {'title': 'Click to Select/Deselect',
                    'class': 'image_btn_4 app_item_head_flex', 'id':trustFLEX[key]}).append(
                        $('<p>', {text: products[trustFLEX[key]].title, 'class':'image_overlay_bottom_app app_item_head_base', 'id':products[trustFLEX[key]].name+'Img' }),
                        $('<div>', {'class': 'tooltip'}),
                        $('<div>', {'class': 'forbidden_image'}).append(
                            $('<img>', {'src': "assets/html/images/1200px-ProhibitionSign2.png", 'class': 'image_overlay_top_fd'})),
                        $('<div>', {'class': 'check_image'}).append(
                            $('<img>', {'src': "assets/html/images/check-mark-png-11553206004impjy81rdu.png", 'class': 'image_overlay_top'}))),
                        $('<div>', {'class': 'open_notebook_option'}).append(
                            $('<input>', {'class':'notebook','id':'nb'+trustFLEX[key], 'type':'button', 'value':'Usecase', 'disabled':true, 'style':''}),
                            $('<input>', {'class':'configurator','id':'c'+trustFLEX[key], 'type':'button', 'value':'Configurator', 'onclick':'configurator_fn('+trustFLEX[key]+')','disabled':false, 'style':'background-color:#F68D2E;color:black'}))
    )))
    if(not_available_items.indexOf(trustFLEX[key])>-1){
        $('#'+trustFLEX[key]).append(
            $('<div>', {'class': 'available_soon_img'}).append(
                $('<img>', {'src': "assets/html/images/available_soon.png", 'style':' width: 70px; height: 35px;'}))
    )}
}
function append_trustcustom_p(key){
    $('#trustcustom_p').append(
            $('<div>', {'class': 'app_item_p'}).append(
                $('<div>').append(
                    $('<div>', {'title': 'Click to Select/Deselect',
                    'class': 'image_btn_4 app_item_head_custom', 'id':trustCUSTOM[key]}).append(
                        $('<p>', {text: products[trustCUSTOM[key]].title, 'class':'image_overlay_bottom_app app_item_head_base', 'id':products[trustCUSTOM[key]].name+'Img' }),
                        $('<div>', {'class': 'tooltip'}),
                        $('<div>', {'class': 'forbidden_image'}).append(
                            $('<img>', {'src': "assets/html/images/1200px-ProhibitionSign2.png", 'class': 'image_overlay_top_fd'})),
                        $('<div>', {'class': 'check_image'}).append(
                            $('<img>', {'src': "assets/html/images/check-mark-png-11553206004impjy81rdu.png", 'class': 'image_overlay_top'}))),
                        $('<div>', {'class': 'open_notebook_option'}).append(
                            $('<input>', {'class':'configurator','id':'c'+trustCUSTOM[key], 'type':'button', 'value':'Configurator', 'onclick':'configurator_package('+trustCUSTOM[key]+')', 'disabled':false, 'style':'background-color:#F68D2E;color:black'}))
    )))
    if(not_available_items.indexOf(trustCUSTOM[key])>-1){
        $('#'+trustCUSTOM[key]).append(
            $('<div>', {'class': 'available_soon_img'}).append(
                $('<img>', {'src': "assets/html/images/available_soon.png", 'style':' width: 70px; height: 35px;'}))
    )}
}
function configurator_fn(key) {
    if([309, 310, 311].includes(key)){
        open_configurator_page(products[key].title, products[key].secret_exchange_page)
    }
    else{
        window.open(products[key].secret_exchange_page)}
}
function configurator_package(key) {
    if(key == 304){
        window.open(products[key].secret_exchange_page)
    }
    else{
    open_configurator_page(products[key].title, products[key].secret_exchange_page)}
}
function resource_page_fn(key) {
    window.open(products[key].resource_page);
}

$(document).on("click", ".notebook", function(){
    var temp_id = $(this).attr('id');
    var iId = temp_id.substr(2, 3);
    iId = parseInt(iId);
    var templist = products[iId]._usecaselist;
    var no_nb = [];
    for(var key in templist){
        if(usecaselist[templist[key]].selected == true){
            if(usecaselist[templist[key]].nbpath[iId] == undefined){
                no_nb.push(usecaselist[templist[key]].title);
            }
            else{
                open_notebook(usecaselist[templist[key]].nbpath[iId]);
            }
        }
    }
    if(no_nb.length > 0){
        alert('Notebook is not yet available for below usecases\n'+no_nb);}
});

$(document).on("click", ".reset_selected", function(){
    track_app = [];
    track_prodcat = [];
    track_usecase = [];
    $('#application_category').empty();
    $('#product_category').empty();
    $('#usecases').empty();
    $('#trustgo_p').empty();
    $('#trustflex_p').empty();
    $('#trustcustom_p').empty();
    var eb = document.getElementById("eval_board_section");
    if (eb.style.display == "block") {
        eb.style.display = "none";
    }
    $('#eval_boards').empty();
    for(var ele in applicationCategory_arr){
        var key = applicationCategory_arr[ele];
        applicationCategory[key].highlight = true;
        if(applicationCategory[key].selected == true){
            applicationCategory[key].selected = false;
            $('#'+key).removeClass('active')
        }
        append_applicationCategory(key);
    }
    for(var ele in productCategory_arr){
        var key = productCategory_arr[ele];
        productCategory[key].highlight = true;
        if(productCategory[key].selected == true){
            productCategory[key].selected = false;
            $('#'+key).removeClass('active')
        }
        append_productCategory(key);
    }
    for(var ele in usecaselist_arr){
        var key = usecaselist_arr[ele];
        usecaselist[key].highlight = true;
        if(usecaselist[key].selected == true){
            usecaselist[key].selected = false;
            $('#'+key).removeClass('active')
        }
        append_usecases(key);
    }
    for(var key in trustGO){
        products[trustGO[key]].highlight = true;
        if(products[trustGO[key]].selected == true){
            products[trustGO[key]].selected = false;
            $('#'+trustGO[key]).removeClass('active')
        }
        append_trustgo_p(key);
    }
    for(var key in trustFLEX){
        products[trustFLEX[key]].highlight = true;
        if(products[trustFLEX[key]].selected == true){
            products[trustFLEX[key]].selected = false;
            $('#'+trustFLEX[key]).removeClass('active')
        }
        append_trustflex_p(key);
    }
    for(var key in trustCUSTOM){
        products[trustCUSTOM[key]].highlight = true;
        if(products[trustCUSTOM[key]].selected == true){
            products[trustCUSTOM[key]].selected = false;
            $('#'+trustCUSTOM[key]).removeClass('active')
        }
        append_trustcustom_p(key);
    }
});

function add_dependency(){
    var eb = document.getElementById("eval_board_section");
    if (eb.style.display == "block") {
        eb.style.display = "none";
    }
    $('#eval_boards').empty();
    var flag = 0;
    // app_cat_items = [];
    // prod_cat_items = [];
    // usecase_items = [];
    for(var in_key in applicationCategory){
        if((applicationCategory[in_key].selected == true)){
            var templist = applicationCategory[in_key]._prodcat;
            for(var key in productCategory){
                if(templist.find(element => element == key)){
                    if(productCategory[key].highlight == false){
                        productCategory[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{

                    if(flag == 0){
                    if((productCategory[key].highlight == true) && (productCategory[key].selected == false)){
                        productCategory[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            var templist = applicationCategory[in_key]._usecaselist;
            for(var key in usecaselist){
                if(templist.find(element => element == key)){
                    if(usecaselist[key].highlight == false){
                        usecaselist[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{
                    if(flag == 0){
                    if((usecaselist[key].highlight == true) && (usecaselist[key].selected == false)){
                        usecaselist[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            var templist = applicationCategory[in_key]._prodlist;
            for(var key in products){
                if(templist.find(element => element == key)){
                    if(products[key].highlight == false){
                        products[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{
                    if(flag == 0){
                    if((products[key].highlight == true) && (products[key].selected == false)){
                        products[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            flag = flag + 1;
        }
    }
    for(var in_key in productCategory){
        if((productCategory[in_key].selected == true)){
            var templist = productCategory[in_key]._applist;
            for(var key in applicationCategory){
                if(templist.find(element => element == key)){
                    if(applicationCategory[key].highlight == false){
                        applicationCategory[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{

                    if(flag == 0){
                    if((applicationCategory[key].highlight == true) && (applicationCategory[key].selected == false)){
                        applicationCategory[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            var templist = productCategory[in_key]._usecaselist;
            for(var key in usecaselist){
                if(templist.find(element => element == key)){
                    if(usecaselist[key].highlight == false){
                        usecaselist[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{
                    if(flag == 0){
                    if((usecaselist[key].highlight == true) && (usecaselist[key].selected == false)){
                        usecaselist[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            var templist = productCategory[in_key]._prodlist;
            for(var key in products){
                if(templist.find(element => element == key)){
                    if(products[key].highlight == false){
                        products[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{
                    if(flag == 0){
                    if((products[key].highlight == true) && (products[key].selected == false)){
                        products[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            flag = flag + 1;
        }
    }
    for(var in_key in usecaselist){
        if((usecaselist[in_key].selected == true)){
            var templist = usecaselist[in_key]._applist;
            for(var key in applicationCategory){
                if(templist.find(element => element == key)){
                    if(applicationCategory[key].highlight == false){
                        applicationCategory[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{

                    if(flag == 0){
                    if((applicationCategory[key].highlight == true) && (applicationCategory[key].selected == false)){
                        applicationCategory[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            var templist = usecaselist[in_key]._prodcat;
            for(var key in productCategory){
                if(templist.find(element => element == key)){
                    if(productCategory[key].highlight == false){
                        productCategory[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{
                    if(flag == 0){
                    if((productCategory[key].highlight == true) && (productCategory[key].selected == false)){
                        productCategory[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            var templist = usecaselist[in_key]._prodlist;
            for(var key in products){
                if(templist.find(element => element == key)){
                    if(products[key].highlight == false){
                        products[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{
                    if(flag == 0){
                    if((products[key].highlight == true) && (products[key].selected == false)){
                        products[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            flag = flag + 1;
        }
    }
    for(var in_key in products){
        if((products[in_key].selected == true)){
            var templist = products[in_key]._applist;
            for(var key in applicationCategory){
                if(templist.find(element => element == key)){
                    if(applicationCategory[key].highlight == false){
                        applicationCategory[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{

                    if(flag == 0){
                    if((applicationCategory[key].highlight == true) && (applicationCategory[key].selected == false)){
                        applicationCategory[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            var templist = products[in_key]._prodcat;
            for(var key in productCategory){
                if(templist.find(element => element == key)){
                    if(productCategory[key].highlight == false){
                        productCategory[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{
                    if(flag == 0){
                    if((productCategory[key].highlight == true) && (productCategory[key].selected == false)){
                        productCategory[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            var templist = products[in_key]._usecaselist;
            for(var key in usecaselist){
                if(templist.find(element => element == key)){
                    if(usecaselist[key].highlight == false){
                        usecaselist[key].highlight = true;
                        // $('#'+key).removeClass('forbidden');
                    }
                }
                else{
                    if(flag == 0){
                    if((usecaselist[key].highlight == true) && (usecaselist[key].selected == false)){
                        usecaselist[key].highlight = false;
                        // $('#'+key).addClass('forbidden');
                    }
                    }
                }
            }
            flag = flag + 1;
        }
    }
    $('#application_category').empty();
    $('#product_category').empty();
    $('#usecases').empty();
    $('#trustgo_p').empty();
    $('#trustflex_p').empty();
    $('#trustcustom_p').empty();
    for(var ele in applicationCategory_arr){
        var key = applicationCategory_arr[ele];
        if(applicationCategory[key].highlight == true){
            append_applicationCategory(key);
            if(applicationCategory[key].selected == true){
                $('#'+key).addClass('active');
            }
        }
    }
    for(var ele in productCategory_arr){
        var key = productCategory_arr[ele];
        if(productCategory[key].highlight == true){
           append_productCategory(key);
            if(productCategory[key].selected == true){
                $('#'+key).addClass('active');
            }
        }
    }
    for(var ele in usecaselist_arr){
        var key = usecaselist_arr[ele];
        if(usecaselist[key].highlight == true){
            append_usecases(key);
            if(usecaselist[key].selected == true){
                $('#'+key).addClass('active');
            }
        }
    }
    for(var key in trustGO){
        if(products[trustGO[key]].highlight == true){
            append_trustgo_p(key);
            if(products[trustGO[key]].selected == true){
                $('#'+trustGO[key]).addClass('active');
            }
        }
    }
    for(var key in trustFLEX){
        if(products[trustFLEX[key]].highlight == true){
            append_trustflex_p(key);
            if(products[trustFLEX[key]].selected == true){
                $('#'+trustFLEX[key]).addClass('active');
            }
        }
    }
    for(var key in trustCUSTOM){
        if(products[trustCUSTOM[key]].highlight == true){
            append_trustcustom_p(key);
            if(products[trustCUSTOM[key]].selected == true){
                $('#'+trustCUSTOM[key]).addClass('active');
            }
        }
    }
    var hl_product =[];
    if(track_usecase.length){
        for(var key in products){
            if(products[key].highlight == true){
                var temp_s;
                var app_loop = true;
                var templist = products[key]._applist;
                for(temp_s =0; temp_s<track_app.length; temp_s++){
                    if(templist.find(element => element == track_app[temp_s])==undefined){
                        app_loop = false;
                    }
                }
                var prod_loop = false;
                var templist = products[key]._prodcat;
                for(temp_s =0; temp_s<track_prodcat.length; temp_s++){
                    if(templist.find(element => element == track_prodcat[temp_s])){
                        prod_loop = true;
                    }
                }
                if(track_prodcat.length==0){
                    prod_loop = true;
                }
                var break_loop = true;
                var templist = products[key]._usecaselist;
                for(temp_s =0; temp_s<track_usecase.length; temp_s++){
                    if(templist.find(element => element == track_usecase[temp_s])==undefined){
                        break_loop = false;
                    }
                }
                if(break_loop && app_loop && prod_loop){
                    hl_product.push(key);
                    var temp_nb = '#'+'nb'+key;
                    $(temp_nb).attr('disabled', false);
                    $(temp_nb).attr('style', 'background-color:#FBDB65;color:black');
                    // var temp_nb = '#'+'c'+key;
                    // if($(temp_nb).length){
                    //     $(temp_nb).attr('disabled', false);
                    //     $(temp_nb).attr('style', 'background-color:#F68D2E;color:black');
                    // }
                }
                else{
                    var temp_nb = '#'+'nb'+key;
                    $(temp_nb).attr('disabled', true);
                    $(temp_nb).attr('style', '');
                    // var temp_nb = '#'+'c'+key;
                    // if($(temp_nb).length){
                    //     $(temp_nb).attr('disabled', true);
                    //     $(temp_nb).attr('style', '');
                    // }
                }
            }
        }
    }
    var eval_board_list = [];
    for(var item in hl_product){
        var temp_list = products[hl_product[item]]._boardslist;
        for(var i in temp_list){
            if(eval_board_list.includes(temp_list[i])==false){
                eval_board_list.push(temp_list[i]);
            }
        }
    }
    if(eval_board_list.length != 0){
        var eb = document.getElementById("eval_board_section");
        if (eb.style.display == "none") {
            eb.style.display = "block";
        }
    }
    for(var i in eval_board_list){
        $('#eval_boards').append(
            $('<div>', {'class':'h_level text-center', 'style':'display: inline-block; margin: 15px;'}).append(
                $('<p>', {'text':evalboardselection[eval_board_list[i]].title}),
                $('<a>', {'href':evalboardselection[eval_board_list[i]].weblink, 'target':'_blank'}).append(
                    $('<img>', {'src':evalboardselection[eval_board_list[i]].imgpath, 'style':'height: 200px;'}))
            )
        )
    }
    if ($('#application_category').is(':empty')){
        $('#application_category').append(
            $('<div>', {'class': 'unavailable_items'}).append(
                $('<p>', {'text': 'No items under Application Category are available based on the selection'})))}
    if ($('#product_category').is(':empty')){
        $('#product_category').append(
            $('<div>', {'class': 'unavailable_items'}).append(
                $('<p>', {'text': 'No items under Product Category are available based on the selection'})))}
    if ($('#usecases').is(':empty')){
        $('#usecases').append(
            $('<div>', {'class': 'unavailable_items'}).append(
                $('<p>', {'text': 'No Use Cases are available based on the selection'})))}
    if ($('#trustgo_p').is(':empty')){
        $('#trustgo_p').append(
            $('<div>', {'class': 'unavailable_items'}).append(
                $('<p>', {'text': 'No products under Trust&Go are available based on the selection'})))}
    if ($('#trustflex_p').is(':empty')){
        $('#trustflex_p').append(
            $('<div>', {'class': 'unavailable_items'}).append(
                $('<p>', {'text': 'No products under TrustFLEX are available based on the selection'})))}
    if ($('#trustcustom_p').is(':empty')){
        $('#trustcustom_p').append(
            $('<div>', {'class': 'unavailable_items'}).append(
                $('<p>', {'text': 'No products under TrustCUSTOM are available based on the selection'})))}
}

$(document).on("click", ".image_btn_1", function(){
    var lId = $(this).attr('id');
    if(applicationCategory[lId].highlight == true){
        if(applicationCategory[lId].selected == false){
            applicationCategory[lId].selected = true;
            $(this).addClass('active');
            track_app.push(lId);
            add_dependency();
        }
        else{
            applicationCategory[lId].selected = false;
            $(this).removeClass('active');
            for(var i = 0; i < track_app.length; i++){
                if (track_app[i] == lId) {
                    track_app.splice(i, 1);
                }
            }
            trav_check();
        }
    }
});

$(document).on("click", ".image_btn_2", function(){
    var lId = $(this).attr('id');
    if(productCategory[lId].highlight == true){
        if(productCategory[lId].selected == false){
            productCategory[lId].selected = true;
            $(this).addClass('active');
            track_prodcat.push(lId);
            add_dependency();
        }
        else{
            productCategory[lId].selected = false;
            $(this).removeClass('active');
            for(var i = 0; i < track_prodcat.length; i++){
                if (track_prodcat[i] == lId) {
                    track_prodcat.splice(i, 1);
                }
            }
            trav_check();
        }
    }
});

$(document).on("click", ".image_btn_3", function(){
    var lId = $(this).attr('id');
    if(usecaselist[lId].highlight == true){
        if(usecaselist[lId].selected == false){
            usecaselist[lId].selected = true;
            $(this).addClass('active');
            track_usecase.push(lId);
            add_dependency();
        }
        else{
            usecaselist[lId].selected = false;
            $(this).removeClass('active');
            for(var i = 0; i < track_usecase.length; i++){
                if (track_usecase[i] == lId) {
                    track_usecase.splice(i, 1);
                }
            }
            rem_function_3(lId);
        }
    }
});
function rem_function_3(ID){
    var templist = usecaselist[ID]._prodlist;
    for(var key in templist){
            var temp_nb = '#'+'nb'+templist[key];
            $(temp_nb).attr('disabled', true);
            $(temp_nb).attr('style', '');
            // var temp_nb = '#'+'c'+templist[key];
            // if($(temp_nb).length){
            //     $(temp_nb).attr('disabled', true);
            //     $(temp_nb).attr('style', '');
            // }

    }
    trav_check();
}
$(document).on("click", ".image_btn_4", function(){
    var lId = $(this).attr('id');
    if(products[lId].highlight == true){
        if(products[lId].selected == false){
            products[lId].selected = true;
            $(this).addClass('active');
            add_dependency();
        }
        else{
            products[lId].selected = false;
            $(this).removeClass('active');
            trav_check();
        }
    }
});
function trav_check(){
    for(var key in applicationCategory){
        if(applicationCategory[key].highlight == false){
            applicationCategory[key].highlight = true;
            $('#'+key).removeClass('forbidden');
        }
    }
    for(var key in productCategory){
        if(productCategory[key].highlight == false){
            productCategory[key].highlight = true;
            $('#'+key).removeClass('forbidden');
        }
    }
    for(var key in products){
        if(products[key].highlight == false){
            products[key].highlight = true;
            $('#'+key).removeClass('forbidden');
        }
    }
    for(var key in usecaselist){
        if(usecaselist[key].highlight == false){
            usecaselist[key].highlight = true;
            $('#'+key).removeClass('forbidden');
        }
    }
    add_dependency();

}