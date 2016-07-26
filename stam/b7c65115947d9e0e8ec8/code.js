var cyElements = {
  nodes: [],
  edges: [],
}

function newVal(v) {
  return { value: v, enumerable: true }
}

function parseElementsfromGraphML() {
  // Nodes
  var G_nodes = TinkerGraph.graphml.graph.node;
  for(var i=0 ; i < G_nodes.length ; i++) {
    cyElements.nodes[i] = new Object();
    Object.defineProperty(cyElements.nodes[i], 'data', newVal({}) );
    Object.defineProperty(cyElements.nodes[i].data, 'id', newVal(G_nodes[i]._id));
    for(var j=0 ; j < G_nodes[i].data.length ; j++) {
      Object.defineProperty(
        cyElements.nodes[i].data,
        G_nodes[i].data[j]._key,
        newVal(G_nodes[i].data[j].__text));
    }
  }

  // Edges
  var G_edges = TinkerGraph.graphml.graph.edge;
  for(var i=0 ; i < G_edges.length ; i++) {
    cyElements.edges[i] = new Object();
    Object.defineProperty(cyElements.edges[i], 'data', newVal({}) );
    Object.defineProperty(cyElements.edges[i].data, 'id', newVal(G_edges[i]._id));
    Object.defineProperty(cyElements.edges[i].data, 'source', newVal(G_edges[i]._source));
    Object.defineProperty(cyElements.edges[i].data, 'target', newVal(G_edges[i]._target));
    for(var j=0 ; j < G_edges[i].data.length ; j++) {
      Object.defineProperty(
        cyElements.edges[i].data,
        G_edges[i].data[j]._key,
        newVal(G_edges[i].data[j].__text));
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

function stylizeElements() {
  for(var i=0 ; i < cyElements.nodes.length ; i++) {
    Object.defineProperty(cyElements.nodes[i].data, 'faveColor', newVal(faveColor[getRandomInt(0,3)]));
    Object.defineProperty(cyElements.nodes[i].data, 'faveShape', newVal(faveShape[getRandomInt(0,3)]));
    Object.defineProperty(cyElements.nodes[i].data, 'weight', newVal(getRandomInt(45,70)));
  }
  for(var i=0 ; i < cyElements.edges.length ; i++) {
    Object.defineProperty(cyElements.edges[i].data, 'faveColor', newVal(faveColor[getRandomInt(0,3)]));
    Object.defineProperty(cyElements.edges[i].data, 'strength', newVal(getRandomInt(60,100)));
    if(getRandomInt(0,1)==1)
      Object.defineProperty(cyElements.edges[i].data, 'classes', newVal('questionable'));
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
  /*  elements: {
      nodes: [
        { data: { id: 'j', name: 'Jerry', weight: 65, faveColor: '#6FB1FC', faveShape: 'triangle' } },
        { data: { id: 'e', name: 'Elaine', weight: 45, faveColor: '#EDA1ED', faveShape: 'ellipse' } },
        { data: { id: 'k', name: 'Kramer', weight: 75, faveColor: '#86B342', faveShape: 'octagon' } },
        { data: { id: 'g', name: 'George', weight: 70, faveColor: '#F5A45D', faveShape: 'rectangle' } }
      ],
      edges: [
        { data: { source: 'j', target: 'e', faveColor: '#6FB1FC', strength: 90 } },
        { data: { source: 'j', target: 'k', faveColor: '#6FB1FC', strength: 70 } },
        { data: { source: 'j', target: 'g', faveColor: '#6FB1FC', strength: 80 } },

        { data: { source: 'e', target: 'j', faveColor: '#EDA1ED', strength: 95 } },
        { data: { source: 'e', target: 'k', faveColor: '#EDA1ED', strength: 60 }, classes: 'questionable' },

        { data: { source: 'k', target: 'j', faveColor: '#86B342', strength: 100 } },
        { data: { source: 'k', target: 'e', faveColor: '#86B342', strength: 100 } },
        { data: { source: 'k', target: 'g', faveColor: '#86B342', strength: 100 } },

        { data: { source: 'g', target: 'j', faveColor: '#F5A45D', strength: 90 } }
      ]
    },*/

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
function startGraph() {
  parseElementsfromGraphML();
  stylizeElements();
  console.log(JSON.stringify(cyElements));
  startCY();
}

$(function() { // on dom ready
  $.get( "tinker-modern-graphml.xml", function( data ) {
    console.log(data);
    startGraph();
  });
}); // on dom ready
