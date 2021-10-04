#!/usr/bin/env python

# Processes OpenEthereum warp snapshot and collects 4-byte code prefixes of all accounts.
#
#    openethereum --chain=kovan snapshot --snapshot-threads=8 snapshot.warp
#    warp2code-prefixes.py snapshot.warp

import sys
import rlp
import snappy
import collections

prefix_map = collections.defaultdict(int)

filename = sys.argv[1]
print(f"{filename=}")

with open(filename, 'rb') as f:
	f.seek(0,2)
	size = f.tell()
	print(f"{size=}")

	f.seek(-8,2)
	manifest_end = f.tell()
	manifest_off_bytes = f.read(8)
	print(f"{manifest_off_bytes=}")

	manifest_off = int.from_bytes(manifest_off_bytes, 'little')
	print(f"{manifest_off=}")

	f.seek(manifest_off,0)
	manifest_bytes = f.read(manifest_end-manifest_off)

	manifest = rlp.decode(manifest_bytes)
	manifest_ver = int.from_bytes(manifest[0], 'big')
	block_number = int.from_bytes(manifest[4], 'big')
	block_hash = manifest[5]
	print(f"{manifest_ver=}")
	print(f"{block_number=}")
	print(f"block_hash={block_hash.hex()}")

	state_chunks = manifest[1]
	num_chunks=len(state_chunks)
	print(f"{num_chunks=}")

	for i in range(num_chunks):
		info = state_chunks[i]
		chunk_len = int.from_bytes(info[1], 'big')
		chunk_pos = int.from_bytes(info[2], 'big')
		print(f"{i}/{num_chunks}: {chunk_pos=} {chunk_len=}", end='')

		f.seek(chunk_pos)
		chunk_compressed = f.read(chunk_len)
		chunk_bytes = snappy.uncompress(chunk_compressed)

		chunk = rlp.decode(chunk_bytes)
		print(f" uncompressed_len={len(chunk_bytes)} num_accounts={len(chunk)}", flush=True)
		for entry in chunk:
			acc = entry[1]
			has_code = acc[2] == b'\x01'
			if has_code:
				code_prefix = bytes(acc[3][:4])
				prefix_map[code_prefix] += 1



for k,v in prefix_map.items():
	print(f"{k.hex()} : {v}")
