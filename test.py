#!/usr/bin/python
#
from __future__ import print_function
from bcc import BPF
import ctypes as ct
import socket
import struct

bpf_text = """
#include <uapi/linux/ptrace.h>
#include <uapi/linux/ip.h>
#include <uapi/linux/tcp.h>
#include <uapi/linux/if_ether.h>
#include <linux/skbuff.h>
#include <linux/netdevice.h>
#include <bcc/proto.h>

BPF_PERF_OUTPUT(tx_events);

struct event_t {
  u32 pid;
  u64 timestamp;

  unsigned char	eth_src[ETH_ALEN];
  unsigned char	eth_dst[ETH_ALEN];
  u32 ip_src;
  u32 ip_dst;
  u16 port_src;
  u16 port_dst;

  char comm[TASK_COMM_LEN];

  int  device_ifindex;
  char device_name[IFNAMSIZ];
};

int kprobe__dev_hard_start_xmit(
        struct pt_regs* ctx, struct sk_buff* skb, struct net_device* dev)
{
  struct sk_buff buf;
  struct ethhdr eth_hdr;
  struct iphdr ip_hdr;
  struct tcphdr tcp_hdr;
  bpf_probe_read(&buf, sizeof(buf), skb);
  bpf_probe_read(&eth_hdr, sizeof(eth_hdr), skb_mac_header(&buf));
  bpf_probe_read(&ip_hdr, sizeof(ip_hdr), skb_network_header(&buf));
  bpf_probe_read(&tcp_hdr, sizeof(tcp_hdr), skb_transport_header(&buf));

  struct event_t event = {};
  event.pid = bpf_get_current_pid_tgid();
  event.timestamp = bpf_ktime_get_ns();

  memcpy(event.eth_src, eth_hdr.h_source, sizeof(event.eth_src));
  memcpy(event.eth_dst, eth_hdr.h_dest, sizeof(event.eth_dst));

  bpf_get_current_comm(&event.comm, sizeof(event.comm));
  event.ip_src = ip_hdr.saddr;
  event.ip_dst = ip_hdr.daddr;
  event.port_src = ntohs(tcp_hdr.source);
  event.port_dst = ntohs(tcp_hdr.dest);

  event.device_ifindex = dev->ifindex;
  bpf_probe_read(&event.device_name, sizeof(event.device_name), dev->name);

  tx_events.perf_submit(ctx, &event, sizeof(event));

  return 0;
};

"""

b = BPF(text=bpf_text)

TASK_COMM_LEN = 16    # linux/sched.h
ETH_ALEN = 6 # upapi/linux/if_ether.h
IFNAMSIZ = 16 # uapi/linux/if.h
class Event(ct.Structure):
    _fields_ = [("pid", ct.c_ulong),
                ("timestamp", ct.c_ulonglong),
                ("eth_src", ct.c_ubyte * ETH_ALEN),
                ("eth_dst", ct.c_ubyte * ETH_ALEN),
                ("ip_src", ct.c_uint),
                ("ip_dst", ct.c_uint),
                ("port_src", ct.c_ushort),
                ("port_dst", ct.c_ushort),
                ("comm", ct.c_char * TASK_COMM_LEN),
                ("device_ifindex", ct.c_int),
                ("device_name", ct.c_char * IFNAMSIZ),
                ]

def inet_ntoa(addr):
	dq = ''
	for i in range(0, 4):
		dq = dq + str(addr & 0xff)
		if (i != 3):
			dq = dq + '.'
		addr = addr >> 8
	return dq

def addrToString(ip, port):
    return "%s:%d" % (inet_ntoa(ip), port)

def ethAddrToString(ethAddr):
    return ':'.join('%02x' % b for b in ethAddr)

start = 0

def print_event(cpu, data, size):
    global start
    event = ct.cast(data, ct.POINTER(Event)).contents
    if start == 0:
            start = event.timestamp
    time_s = (float(event.timestamp - start)) / 1000000000
    print("%7.4f %17s (%d)   %s (%d)    %s %s -> %s %s" % (
            time_s, event.comm, event.pid,
            event.device_name, event.device_ifindex,
            ethAddrToString(event.eth_src),
            addrToString(event.ip_src, event.port_src),
            ethAddrToString(event.eth_dst),
            addrToString(event.ip_dst, event.port_dst),
    ))

# loop with callback to print_event
b["tx_events"].open_perf_buffer(print_event)
while 1:
    b.kprobe_poll()

