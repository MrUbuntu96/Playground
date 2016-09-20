var visElements = {
  nodes: [],
  edges: []
}

function addProp(obj, key, val) {
  Object.defineProperty(obj, key, { value: val, enumerable: true });
}

function parseElementsfromGraphML(xmlGraph) {
  // Parse graphML file to JSON
  var x2js = new X2JS();
  var jsonGraph = x2js.xml2json(xmlGraph);

  // Nodes
  var graphNodes = jsonGraph.graphml.graph.NODE;
  for(var i=0 ; i < graphNodes.length ; i++) {
    visElements.nodes[i] = new Object();
    //addProp(visElements.nodes[i], 'data', {} );
    addProp(visElements.nodes[i], 'id', graphNodes[i]._id);
    if(graphNodes[i].data != undefined) {
      for(var j=0 ; j < graphNodes[i].data.length ; j++) {
        addProp(visElements.nodes[i], graphNodes[i].data[j]._key, graphNodes[i].data[j].__text);
      }
    }
  }

  // Edges
  var graphEdges = jsonGraph.graphml.graph.EDGE;
  for(var i=0 ; i < graphEdges.length ; i++) {
    visElements.edges[i] = new Object();
    //addProp(visElements.edges[i], 'data', {});
    addProp(visElements.edges[i], 'id', graphEdges[i]._id);
    addProp(visElements.edges[i], 'from', graphEdges[i]._from);
    addProp(visElements.edges[i], 'to', graphEdges[i]._to);
    if(graphEdges[i].data != undefined) {
      for(var j=0 ; j < graphEdges[i].data.length ; j++) {
        addProp(visElements.edges[i], graphEdges[i].data[j]._key, graphEdges[i].data[j].__text);
      }
    }
  }

  return visElements;
}
/*
function parseElementsfromGraphML(xmlGraph) {
  // Parse graphML file to JSON
  var x2js = new X2JS();
  var jsonGraph = x2js.xml2json(xmlGraph);

  // Nodes
  var graphNodes = jsonGraph.graphml.graph.node;
  for(var i=0 ; i < graphNodes.length ; i++) {
    visElements.nodes[i] = new Object();
    addProp(visElements.nodes[i], 'data', {} );
    addProp(visElements.nodes[i].data, 'id', graphNodes[i]._id);
    if(graphNodes[i].data != undefined) {
      for(var j=0 ; j < graphNodes[i].data.length ; j++) {
        addProp(visElements.nodes[i].data, graphNodes[i].data[j]._key, graphNodes[i].data[j].__text);
      }
    }
  }

  // Edges
  var graphEdges = jsonGraph.graphml.graph.edge;
  for(var i=0 ; i < graphEdges.length ; i++) {
    visElements.edges[i] = new Object();
    addProp(visElements.edges[i], 'data', {});
    addProp(visElements.edges[i].data, 'id', graphEdges[i]._id);
    addProp(visElements.edges[i].data, 'source', graphEdges[i]._source);
    addProp(visElements.edges[i].data, 'target', graphEdges[i]._target);
    if(graphEdges[i].data != undefined) {
      for(var j=0 ; j < graphEdges[i].data.length ; j++) {
        addProp(visElements.edges[i].data, graphEdges[i].data[j]._key, graphEdges[i].data[j].__text);
      }
    }
  }

  return visElements;
}
*/
function getRandomInt(min, max) {
  return Math.round(Math.random() * (max - min)) + min;
}


// Demo at http://jsfiddle.net/abdmob/gkxucxrj/1/
//function convertXml2JSon() {
//  $("#jsonArea").val(JSON.stringify(x2js.xml_str2json($("#xmlArea").val())));
//}
