

G =
{
    "graphml": {
        "_xmlns": "http://graphml.graphdrawing.org/xmlns",
        "_xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "_xsi:schemaLocation": "http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.1/graphml.xsd",
        "graph": {
            "_edgedefault": "directed",
            "_id": "G",
            "edge": [
                {
                    "_id": "7",
                    "_source": "1",
                    "_target": "2",
                    "data": [
                        {
                            "__text": "knows",
                            "_key": "labelE"
                        },
                        {
                            "__text": "0.5",
                            "_key": "weight"
                        }
                    ]
                },
                {
                    "_id": "8",
                    "_source": "1",
                    "_target": "4",
                    "data": [
                        {
                            "__text": "knows",
                            "_key": "labelE"
                        },
                        {
                            "__text": "1.0",
                            "_key": "weight"
                        }
                    ]
                },
                {
                    "_id": "9",
                    "_source": "1",
                    "_target": "3",
                    "data": [
                        {
                            "__text": "created",
                            "_key": "labelE"
                        },
                        {
                            "__text": "0.4",
                            "_key": "weight"
                        }
                    ]
                },
                {
                    "_id": "10",
                    "_source": "4",
                    "_target": "5",
                    "data": [
                        {
                            "__text": "created",
                            "_key": "labelE"
                        },
                        {
                            "__text": "1.0",
                            "_key": "weight"
                        }
                    ]
                },
                {
                    "_id": "11",
                    "_source": "4",
                    "_target": "3",
                    "data": [
                        {
                            "__text": "created",
                            "_key": "labelE"
                        },
                        {
                            "__text": "0.4",
                            "_key": "weight"
                        }
                    ]
                },
                {
                    "_id": "12",
                    "_source": "6",
                    "_target": "3",
                    "data": [
                        {
                            "__text": "created",
                            "_key": "labelE"
                        },
                        {
                            "__text": "0.2",
                            "_key": "weight"
                        }
                    ]
                }
            ],
            "node": [
                {
                    "_id": "1",
                    "data": [
                        {
                            "__text": "person",
                            "_key": "labelV"
                        },
                        {
                            "__text": "marko",
                            "_key": "name"
                        },
                        {
                            "__text": "29",
                            "_key": "age"
                        }
                    ]
                },
                {
                    "_id": "2",
                    "data": [
                        {
                            "__text": "person",
                            "_key": "labelV"
                        },
                        {
                            "__text": "vadas",
                            "_key": "name"
                        },
                        {
                            "__text": "27",
                            "_key": "age"
                        }
                    ]
                },
                {
                    "_id": "3",
                    "data": [
                        {
                            "__text": "software",
                            "_key": "labelV"
                        },
                        {
                            "__text": "lop",
                            "_key": "name"
                        },
                        {
                            "__text": "java",
                            "_key": "lang"
                        }
                    ]
                },
                {
                    "_id": "4",
                    "data": [
                        {
                            "__text": "person",
                            "_key": "labelV"
                        },
                        {
                            "__text": "josh",
                            "_key": "name"
                        },
                        {
                            "__text": "32",
                            "_key": "age"
                        }
                    ]
                },
                {
                    "_id": "5",
                    "data": [
                        {
                            "__text": "software",
                            "_key": "labelV"
                        },
                        {
                            "__text": "ripple",
                            "_key": "name"
                        },
                        {
                            "__text": "java",
                            "_key": "lang"
                        }
                    ]
                },
                {
                    "_id": "6",
                    "data": [
                        {
                            "__text": "person",
                            "_key": "labelV"
                        },
                        {
                            "__text": "peter",
                            "_key": "name"
                        },
                        {
                            "__text": "35",
                            "_key": "age"
                        }
                    ]
                }
            ]
        },
        "key": [
            {
                "_attr.name": "labelV",
                "_attr.type": "string",
                "_for": "node",
                "_id": "labelV"
            },
            {
                "_attr.name": "name",
                "_attr.type": "string",
                "_for": "node",
                "_id": "name"
            },
            {
                "_attr.name": "lang",
                "_attr.type": "string",
                "_for": "node",
                "_id": "lang"
            },
            {
                "_attr.name": "age",
                "_attr.type": "int",
                "_for": "node",
                "_id": "age"
            },
            {
                "_attr.name": "labelE",
                "_attr.type": "string",
                "_for": "edge",
                "_id": "labelE"
            },
            {
                "_attr.name": "weight",
                "_attr.type": "double",
                "_for": "edge",
                "_id": "weight"
            }
        ]
    }
};

/*
elements: {
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
}
*/
