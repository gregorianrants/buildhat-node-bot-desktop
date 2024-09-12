const zmq = require("zeromq");

let publishers = [];

let nextPort = 5000;

function getPublisher({subscribe_to_node,subscribe_to_topic }) {
  //providing a node to subscribe to is optional, if subscribe_to_node = any
  //all publishers should return true in the filter function
  let nodeFilter = (publisher)=> (
    subscribe_to_node==='any' ? true : subscribe_to_node ===publisher.node
  )

  let filterFunction =(publisher) => (publisher.topic === subscribe_to_topic  &&
    nodeFilter(publisher) )
  
  
  let filtered = publishers.filter(filterFunction);
  //console.log(filtered);
  if (filtered.length == 0) {
    return false;
  }
  if (filtered.length == 1) {
    return filtered[0];
  }
  throw new Error("you can not have more than one publisher on a topic");
}

function createPublisher({node, topic, address }) {
  nextPort += 1;
  let publisher = {
    type: "publisher",
    node: node,
    topic: topic,
    address: address,
    port: nextPort,
    fullAddress: `${address}:${nextPort}`,
  };
  publishers.push(publisher);
  console.log('publisher registered:',publisher)
  return publisher;
}

function handlePublish(msg) {
  const { topic, address } = msg;
  let publisher = createPublisher(msg);
  return { status: "success", data: publisher };
}

function handleSubscription({ subscribe_to_node,subscribe_to_topic }) {
  let publisher = getPublisher( {subscribe_to_node,subscribe_to_topic });
  if (publisher) {
    console.log('node: ', subscribe_to_node, ', topic: ' , subscribe_to_topic, ', subscribing to publisher: ',publisher)
    return { result: "success", data: { type: "subscription", ...publisher } };
  }
  return { result: "not_ready" };
}

async function run() {
  const sock = new zmq.Reply();

  await sock.bind("tcp://*:3000");

  for await (let [msg] of sock) {
    let result;
    msg = JSON.parse(msg);
    //console.log("msg is", msg);
    let { register_as, topic } = msg;
    if (register_as === "publisher") {
      result = handlePublish(msg);
    }
    if (register_as === "subscriber") {
      result = handleSubscription(msg);
    }
    await sock.send(JSON.stringify(result));
  }
}

run();
