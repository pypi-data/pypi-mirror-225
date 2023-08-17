$(document).ready(function() {
    $('#part_number_selection_table').append(
        $('<tr>', {'id':'table_header'})
    )
    for(var e = 0; e<selection_table_titles.length; e++){
        $('#table_header').append(
            $('<th>', {'text': selection_table_titles[e]})
        )
    }
    for(var d = 0; d<partNoSelection["data"].length;d++){
        $('#part_number_selection_table').append(
            $('<tr>', {'id':'table_value'+d})
        )
    }
    for(var d = 0; d<partNoSelection["data"].length;d++){
        var each_row = partNoSelection["data"][d];
        for(var c =0; c<selection_table_titles.length; c++){
            if(each_row["TPDS 2.0 release"]=="yes"){
                if(selection_table_titles[c] == "Part Number"){
                    if(each_row["target_page"] !== undefined){
                        $('#table_value'+d).append(
                            $('<td>').append(
                                $('<a>', {'href':each_row['target_page'], 'text':each_row[selection_table_titles[c]], 'target':"_blank"})
                            ))}
                    else{
                        $('#table_value'+d).append(
                            $('<td>', {'text': each_row[selection_table_titles[c]]}))}}
                else{
                    $('#table_value'+d).append(
                        $('<td>', {'text': each_row[selection_table_titles[c]]})
                    )}}
        }
    }
});
