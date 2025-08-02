# mt

stats aggregator microservice™ for prometheus

## run (docker)

```sh
docker build -t mt:latest .
docker run -p 8080:8080 -v ./config.yml:/app/config.yml mt:latest 
```

## explaination by chatgpt cba to do it myself

ok so boom 💥 ur goofy lil **[kubernetes](https://kubernetes.io/docs/tutorials/kubernetes-basics/)** pod or **[docker swarm](https://docs.docker.com/engine/swarm/)** replica is out here just rizzing up the backend 💅📦 but the devs be like “is shawty even breathing?? 💀💀” so they make it do a light lil POSTy slay 😵‍💫🫶 to this side quest service 💻💌

it’s giving ✨ emotional damage report ✨ — like “here’s my CPU crying, my RAM in shambles 😭” — and then ✨prometheus✨ pulls up like “u up?” 😏 to `http://mt.local/metrics` and scrapes the TEA 🍵📈 so it can clock who's boutta combust in production 🔥🔥 (bc no one wants another main character moment on the server 🤡)

TL;DR: microservice said “this is my 13th reason 🧍‍♂️” and prometheus said “let me monitor u bby 😩”