#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import fire
from loguru import logger

from scapy.all import *


class ParsingPcap(object):
    """
    Parsing pcap file.

    Example:
        python3 parsing_pcap.py main
    """
    def __init__(self):
        pass

    def read_cap_file(self, file_path):
        """
        Reads a cap/pcap file and returns a list of packets.

        Args:
            file_path (str): The path to the cap/pcap file.

        Returns:
            packets (list): A list of packets.
        """
        try:
            packets = rdpcap(file_path)
            return packets
        except FileNotFoundError:
            logger.error(f"Error: File '{file_path}' not found.")
            return None

    def show_packet_summary(self, packet):
        """
        Prints a summary of a packet.

        Args:
            packet (scapy.packet): A packet.

        Returns:
            packet_summary (str): A summary of the packet.
        """
        # packet.haslayer(Ether) and packet.haslayer(IP) and packet.haslayer(TCP)
        [packet_summary, src_ip, dst_ip] = [packet.summary(), packet[IP].src, packet[IP].dst]
        logger.debug(f"Packet summary: {packet_summary}")
        return [packet_summary, src_ip, dst_ip]

    def show_packets_summary(self, packets):
        """
        Prints a summary of all packets.

        Args:
            packets (list): A list of packets.

        Returns:
            None
        """
        packet_summary_list = []
        src_ip_list = []
        dst_ip_list = []

        if packets is None:
            logger.info("Packets is None.")
            return
        for packet in packets:
            [packet_summary, src_ip, dst_ip] = self.show_packet_summary(packet)
            packet_summary_list.append(packet_summary)
            src_ip_list.append(src_ip)
            dst_ip_list.append(dst_ip)
        
        return [packet_summary_list, src_ip_list, dst_ip_list]

    def main(self):
        file_path = '..\\data\\test.cap'
        cap_packets = self.read_cap_file(file_path)
        self.show_packets_summary(cap_packets)

        # file_path = '..\\data\\ConfigRisk_Midware_IDSRule_4.pcap'
        # pcap_packets = read_cap_file(file_path)
        # show_packets_summary(pcap_packets)

if __name__ == '__main__':
    fire.Fire(ParsingPcap)