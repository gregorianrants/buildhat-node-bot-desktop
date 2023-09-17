const zmq = require("zeromq");

let publishers = [];

let nextPort = 5000;

function getPublisher(topic) {
  let filtered = publishers.filter((publisher) => publisher.topic === topic);
  console.log(filtered);
  if (filtered.length == 0) {
    return false;
  }
  if (filtered.length == 1) {
    return filtered[0];
  }
  throw new Error("you can not have more than one publisher on a topic");
}

function createPublisher({ topic, address }) {
  nextPort += 1;
  let publisher = {
    type: "publisher",
    topic: topic,
    address: address,
    port: nextPort,
    fullAddress: `${address}:${nextPort}`,
  };
  publishers.push(publisher);
  return publisher;
}

function handlePublish(msg) {
  const { topic, address } = msg;
  let publisher = createPublisher(msg);
  return { status: "success", data: publisher };
}

function handleSubscription({ topic }) {
  let publisher = getPublisher(topic);
  if (publisher) {
    console.log(publisher);
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
    console.log("msg is", msg);
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
