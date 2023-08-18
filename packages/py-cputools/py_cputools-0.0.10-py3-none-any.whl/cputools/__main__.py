def main():
    from argparse import ArgumentParser
    from cputools.cputools import CpuResource

    # Parse args
    parser = ArgumentParser(description='Gets CPU info')
    parser.add_argument('--remove-siblings', action='store_true', help='Remove the sibling threads from the active cpuset')
    args = parser.parse_args()
    if args.remove_siblings:
        status_content = open('/proc/self/status').read().rstrip('\n')
        cpursc = CpuResource(status_content, True)
        cpursc.print_spaced_cpustr()

if __name__ == '__main__':
    main()
