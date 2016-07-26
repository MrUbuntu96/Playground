require.config({
  paths: {
    "jquery": "lib",
    "underscore": "lib",
    "cytoscape": "lib",
    "cytoscape-graphml", "lib"
  }
});

if ( typeof define === "function" && define.amd && define.amd.jQuery ) {
  define( "jquery", [], function () { return jQuery; } );
}

require(['lib/modules/stam'], function(stam) {
  stam.showName("David");
});
