const zmq = require("zeromq")
const { EventEmitter } = require('events')



class Subscriber extends EventEmitter {
    constructor(topic, node = 'any') {
        super()
        this.socket = new zmq.Subscriber
        this.publisherAddress = null
        this.topic = topic
        this.node = node
    }

    async init() {
        await this.register()
        this.connect()
    }

    async register() {
        const socket = new zmq.Request
        socket.connect("tcp://192.168.178.47:3000")

        let action = {
            "action": "register",
            "register_as": "subscriber",
            "subscribe_to_node": this.node,
            "subscribe_to_topic": this.topic
        }

        let success = false

        while (!success) {
            await socket.send(JSON.stringify(action))
            let result = await socket.receive()
            console.log(result.toString())
            result = JSON.parse(result.toString())
            if (result.result === 'success') {
                console.log('success')
                this.publisherAddress = result.data.fullAddress
                success = true
            }
        }
    }

    async connect() {
        this.socket.connect(this.publisherAddress)
        this.socket.subscribe("")
        for await (const [msg] of this.socket) {
            this.emit('message', msg.toString())
        }

    }
}

async function main() {
    listner = new Subscriber('odometry', 'Robot')
    await listner.init()
    listner.on('message', (data) => {
        console.log(data)
    })
}

main()