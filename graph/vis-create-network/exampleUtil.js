function getScaleFreeNetwork(nodeCount) {
  var nodes = [];
  var edges = [];
  var connectionCount = [];
  var work = [];

  function createEdge(from, to) {
    edges.push({
      from: from,
      to: to
    });
    connectionCount[from]++;
    connectionCount[to]++;
    if(connectionCount[from] > 6) nodes[from].value = 2;
    if(connectionCount[to] > 6)   nodes[to].value = 3;
    console.log(from, to);
  }
  function rand(from, to) {
    return Math.floor(Math.random() * (to-from+1)) + from;
  }

  // Init the nodes
  for (var i = 0; i < nodeCount; i++) {
    nodes.push({
      id: i,
      label: String(i),
      value: 1
    });
    connectionCount[i] = 0;
    work[i] = i;
  }

  for (var self = 0; self < nodeCount ; self++) {
    var degree = Math.min(rand(1,3) +  (rand(1,10) == 1) * 7, nodeCount-1) - connectionCount[self];
    var a = work.slice(); // copy array
    a.splice(self, 1);   //
    a = a.shuffle();
    console.log('node =',self, ' - ', a)
    for(i = 0 ; i < degree ; i++)
      createEdge(self, a[i])
  }


  return {nodes:nodes, edges:edges};
}

Array.prototype.shuffle = function() {
    var input = this;

    for (var i = input.length-1; i >=0; i--) {

        var randomIndex = Math.floor(Math.random()*(i+1));
        var itemAtIndex = input[randomIndex];

        input[randomIndex] = input[i];
        input[i] = itemAtIndex;
    }
    return input;
}













var randomSeed = 764; // Math.round(Math.random()*1000);
function seededRandom() {
  var x = Math.sin(randomSeed++) * 10000;
  return x - Math.floor(x);
}


function getScaleFreeNetworkSeeded(nodeCount, seed) {
  if (seed) {
    randomSeed = Number(seed);
  }
  var nodes = [];
  var edges = [];
  var connectionCount = [];
  var edgesId = 0;


  // randomly create some nodes and edges
  for (var i = 0; i < nodeCount; i++) {
    nodes.push({
      id: i,
      label: String(i)
    });

    connectionCount[i] = 0;

    // create edges in a scale-free-network way
    if (i == 1) {
      var from = i;
      var to = 0;
      edges.push({
        id: edgesId++,
        from: from,
        to: to
      });
      connectionCount[from]++;
      connectionCount[to]++;
    }
    else if (i > 1) {
      var conn = edges.length * 2;
      var rand = Math.floor(seededRandom() * conn);
      var cum = 0;
      var j = 0;
      while (j < connectionCount.length && cum < rand) {
        cum += connectionCount[j];
        j++;
      }


      var from = i;
      var to = j;
      edges.push({
        id: edgesId++,
        from: from,
        to: to
      });
      connectionCount[from]++;
      connectionCount[to]++;
    }
  }

  return {nodes:nodes, edges:edges};
}

function loadJSON(path, success, error) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        success(JSON.parse(xhr.responseText));
      }
      else {
        error(xhr);
      }
    }
  };
  xhr.open('GET', path, true);
  xhr.send();
}
