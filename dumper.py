import os
import logging

def dump_to_file(agent, base, size, error, directory):
    try:
        filename = f"{int(base, 16):016x}_{size}_dump.data" if isinstance(base, str) else f"{base:016x}_{size}_dump.data"
        dump = agent.read_memory(base, size)
        with open(os.path.join(directory, filename), 'wb') as f:
            f.write(dump)
        logging.info(f"Dump saved to {filename}")
        return error
    except Exception as e:
        base_addr = int(base, 16) if isinstance(base, str) else base
        logging.error(f"[!] Memory access violation at {base_addr:016x}: {e}")
        print("Oops, memory access violation!")
        return error

def splitter(agent, base, size, max_size, error, directory):
    times = size // max_size  
    remainder = size % max_size

    current_base = int(base, 16) if isinstance(base, str) else base  

    for _ in range(times):
        logging.debug(f"Save bytes: {current_base:016x} till {current_base + max_size:016x}")
        dump_to_file(agent, current_base, max_size, error, directory)
        current_base += max_size

    if remainder != 0:
        logging.debug(f"Save bytes: {current_base:016x} till {current_base + remainder:016x}")
        dump_to_file(agent, current_base, remainder, error, directory)

def merge_dumps(directory, output_file):
    with open(output_file, 'wb') as outfile:
        for filename in os.listdir(directory):
            if filename.endswith('_dump.data'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'rb') as readfile:
                    outfile.write(readfile.read())
    logging.info(f"Merged dumps saved to {output_file}")
