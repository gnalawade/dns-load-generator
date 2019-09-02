#!/usr/bin/env python3

import argparse
import random
import socket
import struct
import sys

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"ERROR: {message}\n\n")
        self.print_help()
        sys.exit(2)

class DNSQueryGenerator:
    def __init__(self, count, destinations, record, type, verbose):
        self.count = count
        self.destinations = destinations
        self.record = record
        self.type = type
        self.verbose = verbose

    def build_packet(self, record):
        types = {
            "a": 1, "cname": 5, "mx": 15, "ns": 2, "ptr": 12, "soa": 6,
            "srv": 33, "txt": 16
            }
        packet = struct.pack(">H", random.randrange(1,65535))  # Query Ids
        packet += struct.pack(">H", 256) # Flags
        packet += struct.pack(">H", 1) # Questions
        packet += struct.pack(">H", 0) # Answers
        packet += struct.pack(">H", 0) # Authorities
        packet += struct.pack(">H", 0) # Additional
        split_record = record.split(".")
        for part in split_record:
            packet += struct.pack("B", len(part))
            for byte in (part):
                packet += struct.pack("c", bytes(byte, "utf-8"))
        packet += struct.pack("B", 0) # End of String
        packet += struct.pack(">H", types[self.type]) # Query Type
        packet += struct.pack(">H", 1) # Query Class
        return packet

    def send_queries(self, work_queue):
        count = 0
        skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        skt.bind(("",5000))
        for dest in self.destinations:
            for item in work_queue:
                skt.sendto(bytes(item), (str(dest), 53))
                count += 1
        if self.verbose:
            sys.stdout.write(
                f"\rSent {int(count/len(self.destinations))} queries for "
                f"{self.type.upper()} records of"
                f" {self.record} to {len(self.destinations)} destinations. "
                f"Total of {count} queries sent.\n"
                )
        else:
            sys.stdout.write(f"\rSent {count} queries.\n")

    def queue_handler(self):
        """
        Builds a worker queue with the record and counts specified
        then sends it to be processed.
        """
        work_queue = []
        query_count = 0

        while query_count < self.count:
            work_queue.append(self.build_packet(self.record))
            query_count += 1

        self.send_queries(work_queue)

def main():
    parser = MyParser()
    parser.add_argument("-c", "--count", default="10", metavar="10", type=int,
        help="Set how many queries will be generated. "
             "Default: 10"
        )
    parser.add_argument("-d", "--destinations", metavar="192.0.2.1", nargs="+",
        required=True, type=str,
        help="Set DNS server(s) to query. Accepts multiple entries "
             "separated by space."
        )
    parser.add_argument("-r", "--record", metavar="example.com",
        required=True, type=str,
        help="Set name of the record to query."
        )
    parser.add_argument("-t", "--type",
        choices=["a", "cname", "mx", "ns", "ptr", "soa", "srv", "txt"],
        default="a", type=str,
        help="Set type record to send query DNS servers for. "
             "Default: A Record"
        )
    parser.add_argument("-v", "--verbose", action="store_true",
        help="Provide more detailed output."
        )
    args = parser.parse_args()

    DNSQueryGenerator(
        count=args.count, destinations=args.destinations, record=args.record,
            type=args.type, verbose=args.verbose
        ).queue_handler()


if __name__ == "__main__":
    main()
