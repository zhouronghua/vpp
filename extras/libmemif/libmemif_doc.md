Shared Memory Packet Interface (memif) Library    {#libmemif_doc}
==============================================

## Introduction

Shared memory packet interface (memif) provides high performance packet transmit and receive between user application and Vector Packet Processing (VPP) or multiple user applications. Using libmemif, user application can create shared memory interface in master or slave mode and connect to VPP or another application using libmemif. Once the connection is established, user application can receive or transmit packets using libmemif API.

![Architecture](docs/architecture.png)

## Features

- [x] Slave mode
  - [x] Connect to VPP over memif
  - [x] ICMP responder example app
- [x] Transmit/receive packets
- [x] Interrupt mode support
- [x] File descriptor event polling in libmemif (optional)
  - [x] Simplify file descriptor event polling (one handler for control and interrupt channel)
- [x] Multiple connections
- [x] Multiple queues
  - [x] Multi-thread support
- [x] Master mode
	- [ ] Multiple regions (TODO)
- [ ] Performance testing (TODO)

## Quickstart

This setup will run libmemif ICMP responder example app in container. Install [docker](https://docs.docker.com/engine/installation) engine.
Useful link: [Docker documentation](https://docs.docker.com/get-started).

Pull image:
```
# docker pull ligato/libmemif-sample-service
```

Now you should be able to see ligato/libmemif-sample-service image on your local machine (IMAGE ID in this README may be outdated):
```
# docker images
REPOSITORY                       TAG                 IMAGE ID            CREATED              SIZE
ligato/libmemif-sample-service   latest              32ecc2f9d013        About a minute ago   468MB
...
```

Run container:
```
# docker run -it --rm --name icmp-responder --hostname icmp-responder --privileged -v "/run/vpp/:/run/vpp/" ligato/libmemif-sample-service
```
Example application will start in debug mode. Output should look like this:
```
ICMP_Responder:add_epoll_fd:233: fd 0 added to epoll
ICMP_Responder:add_epoll_fd:233: fd 5 added to epoll
LIBMEMIF EXAMPLE APP: ICMP_Responder (debug)
==============================
libmemif version: 2.0 (debug)
memif version: 512
commands:
	help - prints this help
	exit - exit app
	conn <index> <mode> [<interrupt-desc>] - create memif. index is also used as interface id, mode 0 = slave 1 = master, interrupt-desc none = default 0 = if ring is full wait 1 = handle only ARP requests
	del  <index> - delete memif
	show - show connection details
	ip-set <index> <ip-addr> - set interface ip address
	rx-mode <index> <qid> <polling|interrupt> - set queue rx mode
	sh-count - print counters
	cl-count - clear counters
	send <index> <tx> <ip> <mac> - send icmp
```

Continue with @ref libmemif_example_setup which contains instructions on how to set up connection between icmpr-epoll example app and VPP-memif.

#### Next steps

- @subpage libmemif_build_doc
- @subpage libmemif_examples_doc
- @subpage libmemif_example_setup_doc
- @subpage libmemif_gettingstarted_doc
- @subpage libmemif_devperftest_doc
