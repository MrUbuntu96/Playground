var cyElements = {
  nodes: [],
  edges: [],
}

function addProp(obj, key, val) {
  Object.defineProperty(obj, key, { value: val, enumerable: true });
}

function parseElementsfromGraphML(xmlGraph) {
  // Parse graphML file to JSON
  var x2js = new X2JS();
  var jsonGraph = x2js.xml2json(xmlGraph);

  // Nodes
  var graphNodes = jsonGraph.graphml.graph.node;
  for(var i=0 ; i < graphNodes.length ; i++) {
    cyElements.nodes[i] = new Object();
    addProp(cyElements.nodes[i], 'data', {} );
    addProp(cyElements.nodes[i].data, 'id', graphNodes[i]._id);
    for(var j=0 ; j < graphNodes[i].data.length ; j++) {
      addProp(cyElements.nodes[i].data, graphNodes[i].data[j]._key, graphNodes[i].data[j].__text);
    }
  }

  // Edges
  var graphEdges = jsonGraph.graphml.graph.edge;
  for(var i=0 ; i < graphEdges.length ; i++) {
    cyElements.edges[i] = new Object();
    addProp(cyElements.edges[i], 'data', {});
    addProp(cyElements.edges[i].data, 'id', graphEdges[i]._id);
    addProp(cyElements.edges[i].data, 'source', graphEdges[i]._source);
    addProp(cyElements.edges[i].data, 'target', graphEdges[i]._target);
    for(var j=0 ; j < graphEdges[i].data.length ; j++) {
      addProp(cyElements.edges[i].data, graphEdges[i].data[j]._key, graphEdges[i].data[j].__text);
    }
  }
}


var faveColor = ['#6FB1FC', '#EDA1ED', '#86B342', '#F5A45D'];
var faveShape = ['triangle', 'ellipse', 'octagon', 'rectangle'];
// weight 45-70
// strength 60-100


function getRandomInt(min, max) {
  return Math.round(Math.random() * (max - min)) + min;
}

function enrichElements() {
  for(var i=0 ; i < cyElements.nodes.length ; i++) {
    addProp(cyElements.nodes[i].data, 'faveColor', faveColor[getRandomInt(0,3)]);
    addProp(cyElements.nodes[i].data, 'faveShape', faveShape[getRandomInt(0,3)]);
    addProp(cyElements.nodes[i].data, 'weight', getRandomInt(45,70));
  }
  for(var i=0 ; i < cyElements.edges.length ; i++) {
    addProp(cyElements.edges[i].data, 'faveColor', faveColor[getRandomInt(0,3)]);
    addProp(cyElements.edges[i].data, 'strength', getRandomInt(60,100));
    if(getRandomInt(1,4)>=3)
      addProp(cyElements.edges[i].data, 'classes', 'questionable');
  }
}

function startCY() {

  $('#cy').cytoscape({
    layout: {
      name: 'cose',
      padding: 10
    },

    style: cytoscape.stylesheet()
      .selector('node')
        .css({
          'shape': 'data(faveShape)',
          'width': 'mapData(weight, 40, 80, 20, 60)',
          'content': 'data(name)',
          'text-valign': 'center',
          'text-outline-width': 2,
          'text-outline-color': 'data(faveColor)',
          'background-color': 'data(faveColor)',
          'color': '#fff'
        })
      .selector(':selected')
        .css({
          'border-width': 3,
          'border-color': '#333'
        })
      .selector('edge')
        .css({
          'curve-style': 'bezier',
          'opacity': 0.666,
          'width': 'mapData(strength, 70, 100, 2, 6)',
          'target-arrow-shape': 'triangle',
          'source-arrow-shape': 'circle',
          'line-color': 'data(faveColor)',
          'source-arrow-color': 'data(faveColor)',
          'target-arrow-color': 'data(faveColor)',
          'label': 'data(label)',
          //'edge-text-rotation': 'autorotate',
          'text-valign': 'top',
          'text-halign': 'right',
          'text-background-color': 'white',
          'text-background-shape': 'rectangle',
          'text-background-opacity': 1,
          'font-size': '10%',
          'color': 'red'
        })
      .selector('edge.questionable')
        .css({
          'line-style': 'dotted',
          'target-arrow-shape': 'diamond'
        })
      .selector('.faded')
        .css({
          'opacity': 0.25,
          'text-opacity': 0
        }),

      elements: cyElements,

    ready: function(){
      window.cy = this;
      // giddy up
    }
  });
}
// Demo at http://jsfiddle.net/abdmob/gkxucxrj/1/
//function convertXml2JSon() {
//  $("#jsonArea").val(JSON.stringify(x2js.xml_str2json($("#xmlArea").val())));
//}
function importGraph(xmlGraphData) {
  parseElementsfromGraphML(xmlGraphData);
  enrichElements();
  //console.log(JSON.stringify(cyElements));
  startCY();
}

$(function() { // on dom ready
  $.get( "tinker-modern-graphml.xml", function(xmlGraphData) {
    //console.log(xmlGraphData);
    importGraph(xmlGraphData);
  });
}); // on dom ready
