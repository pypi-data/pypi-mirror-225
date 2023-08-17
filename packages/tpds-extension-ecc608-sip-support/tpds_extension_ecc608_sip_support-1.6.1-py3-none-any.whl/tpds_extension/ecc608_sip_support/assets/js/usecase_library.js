ws = new WebSocket("ws://localhost:1302/websocket");
function showTrainingVideos() {
    $(document.getElementById("training")).show();
    window.location.href = "#training";
}
var selectedBoard = ""

document.getElementById("prov_proto").addEventListener("click", provision_proto_fn);

function provision_proto_fn(){
    tflex_prov_proto(this.id);
}
/* Display the TrustGO usecase items */
$(document).ready(function() {
    for(var element =0; element<tng_usecases_list.length; element++){
        $('#tg_boardsContainer').append(
            $('<div>', {'class': 'col-md-4 col-sm-12'}).append(
                $('<div>', {'class': 'use_case_item'}).append(
                    $('<div>', {'class': 'use_case_head p-top-30 p-bottom-30 text-center'}).append(
                        $('<p>', {'class': '', text: UseCases[tng_usecases_list[element]].title}),
                    ),
                    $('<div>', {'class': 'use_case_text text-center',
                    'id': UseCases[tng_usecases_list[element]].name+'Item'}).append(
                        $('<p>', {text: UseCases[tng_usecases_list[element]].summary}),
                        $('<div>', {'class': 'image_btn text-center', 'id':tng_usecases_list[element]}).append(
                            $('<img>', {'src': UseCases[tng_usecases_list[element]].imgpath, 'class':'image_overlay_bottom', 'id':UseCases[tng_usecases_list[element]].name+'Img' }),
                            $('<div>', {'class': 'check_image'}).append(
                                $('<img>', {'src': "images/check-mark-png-11553206004impjy81rdu.png", 'class': 'image_overlay_top'}))
                        )))))
    }
    $('#open_notebook_btn_section').append(
        $('<div>', {'class': 'open_use_cases_btn', 'id': 'open_use_case_btn_box'}).append(
            $(document.createElement('a')).prop({
                id : 'open_notebookBtn',
                class : 'open_notebook_btn_text',
                style: 'font-size: 200%;',
                href: 'javascript:open_selected_notebooks()',
                text: 'Open Selected Use Case(s)'
            })
        )
    )
});

/* Display the TrustFLEX development boards */
$(document).ready(function() {
    for(var key in UseCases){
        if (parseInt(key) < 200)
        {
            $('#hexGrid').append(
                $('<li>', {'class':'hex'}).append(
                    $('<div>', {'class':'hexOut'}).append(
                        $('<div>', {'class':'hexIn'}).append(
                            $('<a>', {'class':'hexLink', 'id':key}).append(
                                // $('<img>', {'src':UseCases[key].imgpath}),
                                $('<p>', {'text':UseCases[key].title}),
                                $('<div>', {'class':"onclick_usecase"}).append(
                                    $('<img>', {'src':"images/check-mark-png-11553206004impjy81rdu.png"})
                                ))))))}
        }
});

function open_selected_notebooks() {
    console.log('open_selected_notebooks');
    var usecase_list = Boards[selectedBoard].usecases;
    console.log(selectedBoard);
    console.log(usecase_list.length);
    var notebook_paths = [];
    var element = 0;
    for(element; element<usecase_list.length; element++) {
        if(UseCases[usecase_list[element]].selected === true) {
            notebook_paths.push(String(UseCases[usecase_list[element]].notebook_path));
            console.log(notebook_paths);
        }
    }
    if(notebook_paths.length==0){
        alert("Select atleast one USECASE above!")
    }
    else{
    open_notebook(notebook_paths);}
}
/*  Handle the board SELECT click
    Display the TrustFLEX Use cases for the selected development board */
$(document).on("click", ".board_btn" , function() {
    clearSelectedUseCases($(this).attr('name'));
    $('.use_cases').hide();
    $('#open_notebook_btn_section').hide();
    $('#UseCaseContainer').empty();

    var selected_board = $(this).attr('name');
    if(Boards[selected_board].selected === false){
        $('.use_cases').show();
        $('#open_notebook_btn_section').show();
    }
    toggleBoards($(this).attr('name'));
    var element = 0;
    var active_board_name = Boards[selected_board].name;
    if(Boards[selected_board].selected){
        active_board(active_board_name);}
    else{
        active_board("");}
    var usecase_list = Boards[selected_board].usecases;
    for(element; element<usecase_list.length; element++){
        $('#UseCaseContainer').append(
            $('<div>', {'class': 'col-md-4 col-sm-12'}).append(
                $('<div>', {'class': 'use_case_item'}).append(
                    $('<div>', {'class': 'use_case_head p-top-30 p-bottom-30 text-center'}).append(
                        $('<p>', {text: UseCases[usecase_list[element]].title}),
                    ),
                    $('<div>', {'class': 'use_case_text text-center',
                    'id': UseCases[usecase_list[element]].name+'Item'}).append(
                        $('<p>', {text: UseCases[usecase_list[element]].summary}),
                        $('<div>', {'title': 'Click to Select/Deselect',
                        'class': 'image_btn text-center', 'id':usecase_list[element]}).append(
                            $('<img>', {'src': UseCases[usecase_list[element]].imgpath, 'class':'image_overlay_bottom', 'id':UseCases[usecase_list[element]].name+'Img' }),
                            $('<div>', {'class': 'tooltip', 'text':'Select'}),
                            $('<div>', {'class': 'check_image'}).append(
                                $('<img>', {'src': "images/check-mark-png-11553206004impjy81rdu.png", 'class': 'image_overlay_top'}))
                        )))))
    }
    $('#open_notebook_btn_section').empty();
    $('#open_notebook_btn_section').append(
        $('<div>', {'title':'Click to Open selected Usecases.', 'class': 'open_use_cases_btn', 'id': 'open_use_case_btn_box'}).append(
            $(document.createElement('a')).prop({
                id : 'open_notebookBtn',
                class : 'open_notebook_btn_text',
                style: 'font-size: 200%;',
                href: 'javascript:open_selected_notebooks()',
                text: 'Open Selected Use Case(s)'
            })
        )
    )
});

$(document).on("click", ".secure_provisioning_guide", function(){
    open_link('Documentation.html#'+$(this).attr('id'))
});

$(document).on("click", ".image_btn", function(){
    $(this).toggleClass('active');
    toggleUseCase($(this).attr('id'));
});

$(document).on("click", ".hexLink", function(){
    $(this).toggleClass('select');
    toggleUseCase($(this).attr('id'));
});

function clearSelected(arg_board) {
    for(var key in Boards){

        var boardName = Boards[key].name;
        var item = document.getElementById(boardName+"Item");
        var button = document.getElementById(boardName+"Btn");
        var usecase_list = Boards[key].usecases;

        if(Boards[key].selected === true && key!=arg_board){
            Boards[key].selected = false;
            button.style.backgroundColor = "#fff";
            button.innerHTML = "SELECT";
            button.classList.remove("board_btn_selected");
            for(var element; element<usecase_list.length; element++){
                UseCases[usecase_list[element]].selected = false;
            }
        }
    }
}

function clearSelectedUseCases(board) {
    for(var ele=0; ele < Boards[board].usecases.length; ele++){
        if(UseCases[Boards[board].usecases[ele]].selected === true){
            toggleUseCase(Boards[board].usecases[ele]);
        }
    }
}

function toggleBoards(board) {
    selectedBoard = board
    var boardName = Boards[board].name;
    var item = document.getElementById(boardName+"Item");
    var button = document.getElementById(boardName+"Btn");
    if(Boards[board].selected === false) {
        clearSelected(board);
        Boards[board].selected = true;
        button.style.backgroundColor = "#00bb00";
        button.innerHTML = "UNSELECT";
        button.classList.add("board_btn_selected");
    } else {
        Boards[board].selected = false;
        button.style.backgroundColor = "#fff";
        button.innerHTML = "SELECT";
        button.classList.remove("board_btn_selected");
    }
}

function toggleUseCase(useCase) {
    var useCaseName = UseCases[useCase].name;
    var item = document.getElementById(useCaseName + "Item");
    //var button = document.getElementById(useCaseName + "Btn");
    var img = document.getElementById(useCaseName + "Img")
    if (UseCases[useCase].selected === false) {
        var ids_l = UseCases[useCase].ids
        if(ids_l.includes("Slot10") == true){
            if(UseCases[useCase].certs == "custom"){
                document.getElementById("1001").checked = false;
                document.getElementById("1002").checked = true;
                cert10RadioHandler();
            }
            if(UseCases[useCase].prefix == 2){
                document.getElementById("cbid_devcertcn").checked = false;
                document.getElementById("cbid_devcertcn_pr").checked = true;
                document.getElementById("10certcommonname").disabled = false;
                document.getElementById("10certcommonname").value = '';
                document.getElementById("10certcommonname").placeholder = 'Avnet IoTConnect Company ID'
            }
        }
        else{
            document.getElementById("1001").checked = true;
            document.getElementById("1002").checked = false;
            document.getElementById("cbid_devcertcn").checked = true;
            document.getElementById("cbid_devcertcn_pr").checked = false;
            document.getElementById("10certcommonname").disabled = true;
            document.getElementById("10certcommonname").value = 'sn0123030405060708EE';
        }
        UseCases[useCase].ids.forEach(element => {
            var rowElement = document.getElementById(element);
            rowElement.style['backgroundColor'] = 'LightSalmon'
        });
        UseCases[useCase].selected = true;
        /*button.style.backgroundColor = "#00bb00";
        button.innerHTML = "UNSELECT";
        button.classList.add("use_case_btn_selected");*/
    } else {
        var ids_l = UseCases[useCase].ids
        if(ids_l.includes("Slot10") == true){
            if(UseCases[useCase].certs == "custom"){
                document.getElementById("1001").checked = true;
                document.getElementById("1002").checked = false;
                document.getElementById("cbid_devcertcn").checked = true;
                document.getElementById("cbid_devcertcn_pr").checked = false;
                document.getElementById("10certcommonname").disabled = true;
                document.getElementById("10certcommonname").value = 'sn0123030405060708EE';
                cert10RadioHandler();
            }
        }
        UseCases[useCase].ids.forEach(element => {
            var rowElement = document.getElementById(element);
            rowElement.style['backgroundColor'] = 'white';
        });
        UseCases[useCase].selected = false;
        /*button.style.backgroundColor = "#e40222";
        button.innerHTML = "SELECT";
        button.classList.remove("use_case_btn_selected");*/
    }
}

function validateUseCaseSlots() {
    //Object.keys(UseCases).length
    var usecaseElements;
    var alertUseCasesNames = "";
    var alertUseCaseSlots = "";
    var alertStatus = false;
    var radioName;

    for (usecaseElements in UseCases) {
        if (UseCases[usecaseElements].selected == true) {
            //console.log(UseCases[usecaseElements].ids);
            for (let i = 0; i < UseCases[usecaseElements].ids.length; i++) {
                var element = UseCases[usecaseElements].ids[i];
                if (element == "Slot10" || element == "Slot12") {
                    radioName = element.toLowerCase() + "certopt";
                    if (getFormRadioValue(formNameMain, radioName) == "MCHPCert") {
                        if (!alertUseCaseSlots.includes(element)) {
                            alertUseCaseSlots += element + "\r\n";
                            alertStatus = true;
                        }
                    }
                } else if (element == "custCertPubkey") {
                    radioName = "slot16" + "dataopt";
                    if (getFormRadioValue(formNameMain, radioName) == "unused") {
                        alertUseCaseSlots += "CA Public key data" + "\r\n";
                        alertStatus = true;
                    }
                } else {
                    radioName = element.toLowerCase() + "dataopt";
                    if (getFormRadioValue(formNameMain, radioName) == "unused") {
                        if (!alertUseCaseSlots.includes(element)) {
                            alertUseCaseSlots += element + "\r\n";
                            alertStatus = true;
                        }
                    }
                }
            }
        }
    }

    if (alertStatus) {
        var alertString = "For the usecases selected, data must be provided in the slots marked in LightSalmon. \r\n\nData is required in the following slots: \r\n" + alertUseCaseSlots;
        alert(alertString);
    }
    return alertStatus;
}