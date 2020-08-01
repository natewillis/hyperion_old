/*!
 * Scenario Weapon Cesium Display Template
 * Nate Willis
 * Delta Solutions
 * Date: 2020-07-31
 */

// Load Data Function
var reloadWeaponCesium = function(scenarioID, cesiumReloadData) {

    // Load Sources
    cesiumReloadData['weapon'].entities.removeAll();
    cesiumReloadData['weapon'].load(
        '/scenario/api/weapons_gis/?wave__scenario='+scenarioID.toString(),
        {
            markerSymbol: 'rocket'
        }
    );
    cesiumReloadData['warhead'].entities.removeAll();
    cesiumReloadData['warhead'].load(
        '/scenario/api/warheads_gis/?weapon__wave__scenario='+scenarioID.toString(),
        {
            markerSymbol: 'star'
        }
    );

};


// Main Load Table Function
var loadWeaponCesium = function(grid, scenarioID) {

    // Dynamically initialize cesium by adding the gridstack widget div and then initializing the cesium viewer
    grid.addWidget('<div><div class="grid-stack-item-content" id="cesiumContainer"></div></div>', {width: 6, height:9});

    // Initialize Viewer
    var viewer = new Cesium.Viewer("cesiumContainer",{
        timeline: false,
        animation: false
    });

    // Create Sources
    var weaponSource = new Cesium.GeoJsonDataSource("weapons");
    viewer.dataSources.add(weaponSource);
    var warheadSource = new Cesium.GeoJsonDataSource("warheads");
    viewer.dataSources.add(warheadSource);

    // Return Data
    cesiumReloadData = {
        'weapon': weaponSource,
        'warhead': warheadSource
    }

    // Load Data
    reloadWeaponCesium(scenarioID, cesiumReloadData);

    // Return
    return cesiumReloadData;

};

