Kafka Playground
================

This repo serves as a very simple "playground" in which you can experiment with a local Kafka broker: publishing and consuming messages.

*Note that I'm currently working on fixing a recursive production bug. Just be careful that the block of messages will send infinitely in current-state.*

## Base Structure

It uses Kafka (obviously), Zookeeper for Kafka coordination, python for both the production and consumption of messages, and Kafdrop for an easy-to-use UI.
Everything is self-contained in Docker.

### First Time Use

- From the root, run: 
```bash
docker-compose up --build
```

*Note that after your initialization you can drop the* `--build` *extension.*

- Open `http://localhost:9000` to see all the topics, explore partitions, and view the messages in real-time.
