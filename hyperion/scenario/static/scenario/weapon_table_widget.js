/*!
 * Scenario Weapon Table Template
 * Nate Willis
 * Delta Solutions
 * Date: 2020-07-31
 */

// initialize new weapon index
var newWeaponIndex = 'new_0';

// function for incrementing weapon index
var incrementNewWeaponIndex = function(weaponIndex) {
    var getPart = weaponIndex.replace ( /[^\d.]/g, '' ); // returns number
    var num = parseInt(getPart); // returns integer number
    var newVal = num+1; // increments
    var reg = new RegExp(num); // create dynamic regexp
    var incrWeaponIndex = weaponIndex.replace ( reg, newVal ); // returns incremented index
    return incrWeaponIndex;
}

// formatter function for add warhead table button
var addWarheadIcon = function(cell, formatterParams) {
    return "<i class='fa fa-bomb'></i><i class='fa fa-plus'></i>";
};

// formatter for delete weapon table button
var removeMissileIcon = function(cell, formatterParams) {
    return "<i class='fa fa-rocket'></i><i class='fa fa-minus'></i>";
};

// formatter function for location picker
var locationPickerIcon = function(cell, formatterParams) {
    return "<i class='fa fa-crosshairs'></i>";
};

// formatter for hyperion datetime
var hyperionDateTimeFormatter = function(cell, formatterParams, onRendered) {
    //cell - the cell component
    //formatterParams - parameters set for the column
    //onRendered - function to call when the formatter has been rendered

    moDate = moment(cell.getValue());
    return moDate.format('M/D/YY H:mm'); //return the contents of the cell;
};

// editor for hyperion datetime picker feat. flatpickr
var hyperionDateTimeEditor = function(cell, onRendered, success, cancel, editorParams){
    //cell - the cell component for the editable cell
    //onRendered - function to call when the editor has been rendered
    //success - function to call to pass the successfuly updated value to Tabulator
    //cancel - function to call to abort the edit and return to a normal cell
    //editorParams - params object passed into the editorParams column definition property

    //create and style editor
    var editor = document.createElement("input");

    // Run Flatpickr on value in input
    editor.flatpickr({
        enableTime: true,
        time_24hr: true,
        minuteIncrement: 1,
        defaultDate: cell.getValue(),
        dateFormat: 'Z',
        onClose: function (selectedDates, dateStr, instance) {
            evt = window.event;
            var isEscape = false;
            if ("key" in evt) {
                isEscape = (evt.key === "Escape" || evt.key === "Esc");
            } else {
                isEscape = (evt.keyCode === 27);
            }
            if (isEscape) {
               // user hit escape
               cancel();
            } else {
               success(dateStr);
            }
        }
    });

    //create and style input
    editor.style.padding = "3px";
    editor.style.width = "100%";
    editor.style.boxSizing = "border-box";

    //set focus on the select box when the editor is selected (timeout allows for editor to be added to DOM)
    onRendered(function(){
        editor.focus();
        editor.style.css = "100%";
    });

    //return the editor element
    return editor;
};

// Asynchronous Data Loading Before Document Code

// Prep variables for async loading
var countryCodes = {};

// Main Load Table Function
var loadWeaponTable = function(scenarioID, cesiumReloadData) {

    // Load the location picker
    var map = L.map('locationPickerMap').setView([48.86, 2.35], 11);
    var marker;
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);


    // Update map from inputs function
    updateMapFromInputs = function() {
        var newLatLng = L.latLng( $('#locationPickerLat').val(),  $('#locationPickerLon').val());
        if(typeof(marker)==='undefined') {
            marker = new L.marker(newLatLng);
        } else {
            marker.setLatLng(newLatLng);
        }
        marker.addTo(map);
        map.panTo(marker.getLatLng());
    }

    // Map Click Function
    map.on('click', function(e) {
        $('#locationPickerLat').val(e.latlng.lat);
        $('#locationPickerLon').val(e.latlng.lng);
        updateMapFromInputs();
    });

    // Update map from change in inputs
    $('#locationPickerLat').change(updateMapFromInputs);
    $('#locationPickerLon').change(updateMapFromInputs);

    // Update map size when modal appears
    $('#locationPickerModal').on('shown.bs.modal', function() {
        map.invalidateSize();
        updateMapFromInputs();
        map.setZoom(10);
    });

    // Setup .when to allow all the calls to run asyncronously, but synchronously as a whole
    $.when(
        $.getJSON('/world/api/worldborders_name/'), //Country names
        $.getJSON('/scenario/api/waves/?scenario='+scenarioID.toString()),
    ).done(function(worldData, waveData) {

        // Get data out of returned array
        worldData = worldData[0];
        waveData = waveData[0];

        // Parse country codes into tabulator selector
        countries = {};
        $.each( worldData, function( item ) {
            countries[worldData[item]['id']] = worldData[item]['name'];
        });

        // Parse wave into wave selector
        waves = {};
        $.each( waveData, function( item ) {
            waves[waveData[item]['id']] = waveData[item]['name'];
        });

        // Parse waves into wave start_time lookup
        waveStartTimes = {};
        $.each( waveData, function( item ) {
            waveStartTimes[waveData[item]['id']] = waveData[item]['name'];
        });

        // Get div height
        var tableDivHeight = $("#table-widget").height();
        var controlDivHeight = $(".table-controls").outerHeight(true);
        var tableHeight = tableDivHeight - controlDivHeight;

        // Create Tabulator Table
        var table = new Tabulator("#shot-table", {
            ajaxURL:"/scenario/api/weapons_table/?wave__scenario="+scenarioID.toString(), //ajax URL,
            height: tableHeight,
            columns:[
                {title: "Wave", field:"wave", editor:"select", formatter: "lookup", formatterParams: waves, editorParams: {values:waves}},
                {title: "Name", field:"page_display_name", editor:"input"},
                {title: "Launch Latitude", field:"latitude",  editor:"number", editorParams:{min:-90, max:90, step:0.000000000001}},
                {title: "Launch Longitude", field:"longitude",  editor:"number", editorParams:{min:-180, max:180, step:0.000000000001}},
                {formatter:locationPickerIcon, width:20, align:"center", headerSort:false, cellClick:function(e, cell){

                    // get row information
                    thisRow = cell.getRow();
                    launchName = thisRow.getCell('page_display_name').getValue();
                    latitude = thisRow.getCell('latitude').getValue();
                    longitude = thisRow.getCell('longitude').getValue();

                    // Setup modal for this row in particular
                    $("#locationPickerModal").find('.modal-title').html("Select a launch location for " + launchName);
                    $('#locationPickerLat').val(latitude);
                    $('#locationPickerLon').val(longitude);

                    // Setup save function
                    $('#locationPickerSave').click(function() {
                        thisRow.getCell('latitude').setValue($('#locationPickerLat').val());
                        thisRow.getCell('longitude').setValue($('#locationPickerLon').val());
                        $('#locationPickerModal').modal("hide")
                    })

                    // Load the location picker modal
                    $('#locationPickerModal').modal()

                }},
                {title: "Launch Time", field:"launch_datetime", formatter:hyperionDateTimeFormatter, editor:hyperionDateTimeEditor},
                {title: "Launch Country", field:"launch_country_id", formatter: "lookup", formatterParams: countries, editor:"select", editorParams:{values:countries}},
                {formatter:addWarheadIcon, width:40, align:"center", headerSort:false, cellClick:function(e, cell){
                    var nowUTC = moment().utc().toISOString();
                    const id = cell.getRow().getData().id;
                    const subTable = Tabulator.prototype.findTable(".subTable" + id + "")[0];
                    newWeaponIndex = incrementNewWeaponIndex(newWeaponIndex);
                    var newWarheadData = {
                        "id": 'new',
                        "weapon": id,
                        "warhead_yield": 0,
                        "target_display_name": "Unknown Target",
                        "latitude": 0,
                        "longitude": 0,
                        "impact_datetime": nowUTC,
                    };
                    subTable.addRow(newWarheadData);
                }},
                {formatter:removeMissileIcon, width:40, align:"center", headerSort:false, cellClick:function(e, cell){
                    cell.getRow().delete();
                }},
            ],
            layout:"fitColumns",
            rowFormatter:function(row){
                // Get data
                const id = row.getData().id;

                // Delete existing subtable if it exists
                var el = row.getElement();
                var nested = el.getElementsByClassName("subTableHolder");
                for(let child of nested){
                    child.parentNode.removeChild(child);
                }

                //create and style holder elements
                var holderEl = document.createElement("div");
                var addWarheadEl = document.createElement("button");
                var tableEl = document.createElement("div");

                holderEl.style.boxSizing = "border-box";
                holderEl.style.padding = "10px 30px 10px 10px";
                holderEl.style.borderTop = "1px solid #333";
                holderEl.style.borderBottom = "1px solid #333";
                holderEl.style.background = "#ddd";
                holderEl.setAttribute('class', "subTableHolder");

                tableEl.style.border = "1px solid #333";
                tableEl.setAttribute('class', "subTable" + id + "");

                holderEl.appendChild(tableEl);

                row.getElement().appendChild(holderEl);

                var subTable = new Tabulator(tableEl, {
                   layout:"fitColumns",
                   data:row.getData().warheads,
                   columns:[
                       {title:"Warhead ID", field:"id"},
                       {title:"Weapon ID", field:"weapon", visible:false},
                       {title:"Target Name", field:"target_display_name", editor:"input"},
                       {title:"Yield", field:"warhead_yield",  editor:"number", editorParams:{min:0, max:10000, step:1}},
                       {title:"Impact Time", field:"impact_datetime", formatter:hyperionDateTimeFormatter, editor:hyperionDateTimeEditor},
                       {title:"Latitude", field:"latitude",  editor:"number", editorParams:{min:-90, max:90, step:0.000000000001}},
                       {title:"Longitude", field:"longitude",  editor:"number", editorParams:{min:-180, max:180, step:0.000000000001}},
                       {formatter:locationPickerIcon, width:20, align:"center", headerSort:false, cellClick:function(e, cell){

                            // get row information
                            thisRow = cell.getRow();
                            targetName = thisRow.getCell('target_display_name').getValue();
                            latitude = thisRow.getCell('latitude').getValue();
                            longitude = thisRow.getCell('longitude').getValue();

                            // Setup modal for this row in particular
                            $("#locationPickerModal").find('.modal-title').html("Select an impact location for " + targetName);
                            $('#locationPickerLat').val(latitude);
                            $('#locationPickerLon').val(longitude);

                            // Setup save function
                            $('#locationPickerSave').click(function() {
                                thisRow.getCell('latitude').setValue($('#locationPickerLat').val());
                                thisRow.getCell('longitude').setValue($('#locationPickerLon').val());
                                $('#locationPickerModal').modal("hide")
                            })

                            // Load the location picker modal
                            $('#locationPickerModal').modal()

                        }},
                   ]
                });

            }
        });

        //Add row on "Add Row" button click
        $("#add-weapon-button").click(function(){

            // Can't add a weapon if there are no waves to assign it to
            if (Object.keys(waves).length > 0) {
                var nowUTC = moment().utc().toISOString();
                newWeaponIndex = incrementNewWeaponIndex(newWeaponIndex);
                newWeaponData = {
                    "id": newWeaponIndex,
                    "wave": Object.keys(waves)[0],
                    "page_display_name": "Unknown Weapon",
                    "latitude": 0,
                    "longitude": 0,
                    "launch_datetime": nowUTC,
                    "launch_country_id": Object.keys(countries)[0],
                    warheads:[]
                };
                table.addRow(newWeaponData);
                table.redraw();
            } else {
                alert('Please add a wave first!')
            }

        });

        //Add save table function
        $("#save-table-button").click(function(){

            //Initialize Empty Return Data
            var returnData = [];

            rows = table.getRows();

            ajaxPromises = [];

            rows.forEach(function(row) {

                // Get Weapon Data
                weaponData = JSON.parse(JSON.stringify(row.getData()));

                // Clear out warhead data as it doesnt update in the subtable

                // Find the subtable
                const subTable = Tabulator.prototype.findTable(".subTable" + weaponData.id + "")[0];

                // Load the data into warheads as tabulator doesnt update the warhead data with changes to subtable
                // Copy needed because we'll delete some data out of the table for rest purposes
                weaponData.warheads = JSON.parse(JSON.stringify(subTable.getData()));

                // ID fixes
                if (weaponData['id'].toString().includes('new')) {
                    delete weaponData['id'];
                };
                $.each(weaponData['warheads'], function (index, warheadData){
                    delete warheadData['weapon']; // This is determined by the nesting
                    if (warheadData['id'].toString().includes('new')) {
                        delete warheadData['id'];
                    };
                });

                // Post the data and process the return
                postURL = '/scenario/api/weapons_table/'

                // Create a temporary function
                var tempFunction = function() {
                    return new Promise((resolve, reject) => {
                        $.ajax({
                            type: 'POST',
                            url: postURL,
                            data: JSON.stringify(weaponData),
                            contentType: "application/json; charset=utf-8",
                            dataType: 'json',
                            success: function(data){
                                row.update(data);
                                table.redraw();
                                resolve(data);
                            },
                            error: function(errMsg) {
                                alert(errMsg);
                                reject(errMsg);
                            }
                        });
                    })
                }

                // Call the function and store its promise
                ajaxPromises.push(tempFunction());


            });

            // Refresh the map when all the ajax has been pushed
            $.when(...ajaxPromises).then(()=>{
                reloadWeaponCesium(scenarioID, cesiumReloadData);
            });


        });

    });

};

