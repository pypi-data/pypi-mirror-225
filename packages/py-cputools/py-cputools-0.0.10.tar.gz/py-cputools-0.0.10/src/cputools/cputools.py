#!/usr/bin/python3

import os, re, sys, copy, logging
from typing import List

logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)
cpuinfo = '/proc/cpuinfo'
cputopology = '/sys/devices/system/cpu'

def getcpulist(value: str) -> List[int]:
    """
    Convert a cpuset string such as 1-3,7,9 to the list as [1,2,3,7,9]

    Parameters
    ----------
    value: int
        The cpuset string, in the form like 1-3,7,9

    Returns
    -------
    List[int]
        cpu list converted from the string format
    """

    siblingslist = []
    for item in value.split(','):
        if '-' in item:
           subvalue = item.split('-')
           siblingslist.extend(range(int(subvalue[0]), int(subvalue[1]) + 1))
        else:
           siblingslist.extend([int(item)])
    return siblingslist

def siblings(cputopology: str, cpudir: str, siblingsfile:str) -> List[int]:
    """
    Get a cpu list based the cpu topology, cpu name and sibling list file

    Parameters
    ----------
    cputopology: str
        CPU topology base directory, for instance, /sys/devices/system/cpu
    cpudir: str
        cpu sub directory name under the base directory, such as cpu10
    siblingsfile: str
        sibling file name, such as  thread_siblings_list or core_siblings_list

    Returns
    -------
    List[int]
        cpu list converted from the string format
    """
    # Known core_siblings_list / thread_siblings_list  formats:
    ## 0
    ## 0-3
    ## 0,4,8,12
    ## 0-7,64-71
    value = open('/'.join([cputopology, cpudir, 'topology', siblingsfile])).read().rstrip('\n')
    return getcpulist(value)


class CpuInfo:
    """
    A class to represent the cpu topology information

    Attributes
    ----------
    topology: dict
        dict key: for example "cpu10"
        dict value: dict with keys: "physical_package_id", "core_siblings_list", "thread_siblings_list"
    info: dict
        key-value pair from /proc/cpuinfo
        key: processor ID
        value: dict, key-value pair from each processor section
    allthreads: set
        all cpu threads on the system

    Methods
    -------
    has(cpu: int)
        True if the specified cpu belongs to the cpu threads on the system
    threads()
        get the total number of the cpu threads
    cores()
        get the total number of the cores
    sockets()
        get the total number of sockets
    threadsibling(thread: int)
        get a thread's sibling list, exclude the input thread
    """

    def __init__(self):
        self.info = {}
        self.p = {}
        for line in open(cpuinfo):
            if line.strip() == '':
                self.p = {}
                continue
            key, value = map(str.strip, line.split(':', 1))
            if key == 'processor':
                self.info[value] = self.p
            else:
                self.p[key] = value

        self.topology = {}
        try:
            r = re.compile('^cpu[0-9]+')
            cpudirs = [f for f in os.listdir(cputopology) if r.match(f)]
            for cpudir in cpudirs:
                # skip the offline cpus
                try:
                    online = open('/'.join([cputopology, cpudir, 'online'])).read().rstrip('\n')
                    if online == '0':
                        continue
                except:
                    continue
                self.t = {}
                self.topology[cpudir] = self.t
                self.t['physical_package_id'] = open('/'.join([cputopology, cpudir, '/topology/physical_package_id'])).read().rstrip('\n')
                self.t['core_siblings_list'] = siblings(cputopology, cpudir, 'core_siblings_list')
                self.t['thread_siblings_list'] = siblings(cputopology, cpudir, 'thread_siblings_list')

        except:
            # Cleaning the topology due to error.
            # /proc/cpuinfo will be used instead.
            logger.error("can't access /sys. Use /proc/cpuinfo")
            self.topology = {}

        self.allthreads = set()
        if self.topology:
            for p in self.topology.values():
                self.allthreads = self.allthreads.union(p['thread_siblings_list'])

    def has(self, i: int) -> bool:
        """
        Check if the system contains the input CPU

        Parameters
        ----------
        i: int
            The CPU number

        Returns
        -------
        bool
            True if the system contains the input CPU
        """

        return i in self.allthreads

    def threads(self) -> int:
        """
        Get the total CPU threads
        
        Returns
        -------
        int
            number of CPU threads
        """

        if self.topology:
            return len(set(sum([p.get('thread_siblings_list', '0') for p in self.topology.values()], [])))
        else:
            return int(self.info.itervalues().next()['siblings']) * self.sockets()

    def cores(self) -> int:
        """
        Get the total cores
        
        Returns
        -------
        int
            number of cores
        """

        if self.topology:
            allcores = sum([p.get('core_siblings_list', '0') for p in self.topology.values()], [])
            virtcores = sum([p.get('thread_siblings_list', '0')[1:]  for p in self.topology.values()], [])
            return len(set([item for item in allcores if item not in virtcores]))
        else:
            return int(self.info.itervalues().next()['cpu cores']) * self.sockets()

    def sockets(self) -> int:
        """
        Get the total CPU sockets
        
        Returns
        -------
        int
            number of sockets
        """

        if self.topology:
            return len(set([p.get('physical_package_id', '0') for p in self.topology.values()]))
        else:
            return len(set([p.get('physical id', '0') for p in self.info.values()]))

    def threadsibling(self, thread: int) -> List[int]:
        """
        Get the total CPU sockets

        Parameters
        ----------
        thread: int
            input thread to get its siblings from

        Returns
        -------
        List[int]
            list of CPU threads of the input thread
        """

        cpu = "cpu" + str(thread)
        siblings = copy.deepcopy(self.topology[cpu]['thread_siblings_list'])
        siblings.remove(thread)
        return siblings


class CpuResource:
    """
    A class used to represent the cpu resource
    
    Attributes
    ----------
    available: list[int]
        a list of integers representing the CPUs
    cpuinfo: CpuInfo
        an object of CpuInfo representing CPU topology information
    
    Methods
    -------
    print_spaced_cpustr()
        prints out the CPUs seperated by space
    allocateone()
        allocate one CPU from the available list
    allocate_whole_core()
        allocate one CPU, and remove its sibling from available list
    get_free_siblings(num: int)
        get a list of CPUs, but do not update the available list
    get_free_siblings_mask(num: int)
        use get_free_siblings to get a list of CPUs and returns a cpu mask string
    allocate_siblings(num: int)
        allocate a list of CPUs that are siblings
    remove(l: List[int])
        remove a list of CPUs from the available list
    allocate_from_range(low: int, high: int)
        allocate one CPU from a range
    allocate(num: int)
        allocate a specified number of CPUs
    """

    def __init__(self, data: str, nosibling: bool=False, available: str=""):
        """
        Parameters
        ----------
        data: str
            data content read from /proc/self/status
        nosibling: bool, optional
            True means filtering out sibling threads
        available: str, optional
            use this cpuset string to set the avaialble CPU list
        """

        self.cpuinfo = CpuInfo()

        # if caller specify available already, use it and done
        if available != "":
            self.available = getcpulist(available)
            return
    
        try:
            cpustr = re.search(r'Cpus_allowed_list:\s*([0-9\-\,]+)', data).group(1)
        except (IOError, ValueError, IndexError) as e:
            logger.critical("Exception occurred", exc_info=True)
            raise
        self.original = getcpulist(cpustr)
        self.available = copy.deepcopy(self.original)

        # remove cpu that does not belong to cpuinfo
        for c in self.original:
            if not self.cpuinfo.has(c):
                self.available.remove(c)
        if not nosibling:
            return
        for c in self.available:
            siblings = self.cpuinfo.threadsibling(c)
            for s in siblings:
                if s in self.available:
                    self.available.remove(s)

    def print_spaced_cpustr(self):
        """
        Print a space seperated cpuset string

        The purpose of the output is primarily for shell script to consume
        """

        print(' '.join([str(cpu) for cpu in self.available]))

    def _cpus_to_hex(self, cpus: List[int]) -> str:
        """
        Convert a cpu list to a hex string
        
        Parameters
        ----------
        cpus: List[int]
            A list of CPUs

        Returns
        -------
        str
            A hex string
        """

        cpu_list = [int(i in cpus) for i in range(max(cpus)+1)]
        # Revere the list, then create the binary number.
        cpu_list.reverse()
        cpu_binary = 0
        for digit in cpu_list:
            cpu_binary = 2 * cpu_binary + digit
        
        return hex(cpu_binary)

    def allocateone(self) -> int:
        """
        Allocate one CPU from the available list, use low order cpu from the availble list

        Returns
        -------
        int
            A CPU number that represents the allocated CPU
        """

        try:
            cpu= self.available.pop(0)
        except IndexError:
            sys.exit("failed to allocate cpu")
        return cpu

    def allocate_whole_core(self) -> int:
        """
        Allocate one CPU, and remove its sibling from available list

        Returns
        -------
        int
            A CPU number that represents the allocated core
        """

        cpu = self.allocateone()
        siblings = self.cpuinfo.threadsibling(cpu)
        for s in siblings:
            if s in self.available:
                self.available.remove(s)
        return cpu

    def get_free_siblings(self, num: int) -> List[int]:
        """
        Get a specified number of sibling threads, but not remove them from the availble list

        Parameters
        ----------
        num: int
            The number of siblings

        Returns
        -------
        List[int]
            The list of the sibling threads
        """

        original_pool = copy.deepcopy(self.available)
        cpus = self.allocate_siblings(num)
        self.available = original_pool
        return cpus

    def get_free_siblings_mask(self, num: int) -> str:
        """
        Get a hex mask string for the list returned by get_free_siblings

        Parameters
        ----------
        num: int
            The number of siblings

        Returns
        -------
        str
            The hex mask string for the sibling threads
        """

        cpus = self.get_free_siblings(num)
        return self._cpus_to_hex(cpus)

    def allocate_siblings(self, num: int) -> List[int]:
        """
        Allocate a specified number of CPU threads
        
        Parameters
        num: int
            The number of siblings

        Returns
        -------
        List[int]
            The list of the allocated sibling threads
        """

        cpus = []
        while (num > 0):
            cpu = self.allocateone()
            cpus.append(cpu)
            num -= 1
            if (num == 0):
                break
            siblings = self.cpuinfo.threadsibling(cpu)
            for s in siblings:
                if s in self.available:
                    self.available.remove(s)
                    cpus.append(s)
                    num -= 1
        return cpus

    def allocate_siblings_mask(self, num: int) -> str:
        """
        Allocate cpu siblings and return a corresponding hex mask string

        Parameters
        ----------
        num: int
            The number of siblings

        Returns
        -------
        str
            The hex mask string for the allocated sibling threads
        """

        cpus = self.allocate_siblings(num)
        return self._cpus_to_hex(cpus)

    def remove(self, l: List[int]):
        """
        Remove the specified list of CPUs from the available list

        Parameters
        ----------
        l: List[int]
            A cpu list to remove
        """

        self.available.remove(l)

    def allocate_from_range(self, low: int, high: int) -> int:
        """
        Allocate one CPU from a range

        Parameters
        ----------
        low: int
            The low end of the range
        high: int
            The high end of the range

        Returns
        -------
        int
            The allocated CPU number
        """

        p = None
        for i in self.available:
            if i<=high and i>=low:
                p = i
                break
        if p is not None:
            self.available.remove(p)
        return p

    def allocate(self, num: int) -> List[int]:
        """
        Allocate a specified number of CPUs from the available list

        Parameters
        ----------
        num: int
            The number of CPUs

        Returns
        -------
        List[int]
            The allocated CPUs
        """

        cpus = []
        for i in range(num):
            cpus.append(self.allocateone())
        return cpus

class CpuSet():
    """
    A class used to represent the cpuset
    
    Attributes
    ----------
    cpuset_str: str
        A comma seperated string, such as 0-5,34,46-48
    cpuset_list: list[int]
        A ordered list to keep track of the current cpuset

    Methods
    -------
    cpuset_str()
        return a cputset string, such as 0-5,34,46-48
    substract(cpuset_str: str)
        remove CPUs included in the cpuset_str from the current cpuset
    """

    def __init__(self, cpuset_str: str):
        """
        Parameters
        ----------
        cpuset_str: str
            a cputset string, such as 0-5,34,46-48
        """

        self.cpuset_list = []
        ranges = cpuset_str.split(',')
        for r in ranges:
            boundaries = r.split('-')
            if len(boundaries) == 1:
                # no '-' found
                elem = boundaries[0]
                self.cpuset_list.append(int(elem))
            elif len(boundaries) == 2:
                # '-' found
                start = int(boundaries[0])
                end = int(boundaries[1])
                for n in range(start, end+1):
                    self.cpuset_list.append(n)
        self.cpuset_list.sort()
    
    def cpuset_str(self) -> str:
        """
        Return a string representing the cpuset, for example, 2-3,4-8,20

        Returns
        -------
        str
            A string representing the current cpuset
        """

        if len(self.cpuset_list) == 0:
            return ""
        ranges = [[self.cpuset_list[0], self.cpuset_list[0]]]
        for i in range(1, len(self.cpuset_list)):
            lastRange = ranges[-1]
            if self.cpuset_list[i] == lastRange[1]+1:
                lastRange[1] = self.cpuset_list[i]
                continue
            ranges.append([self.cpuset_list[i], self.cpuset_list[i]])
        output_str = ""
        for r in ranges:
            if r[0] == r[1]:
                output_str = "%s,%d" % (output_str, r[0])
            else:
                output_str = "%s,%d-%d" %(output_str, r[0], r[1])
        return output_str.lstrip(',')

    def substract(self, cpuset_str: str):
        """
        Remove the specified CPUs from the current cpuset

        Parameters
        ----------
        cpuset_str: str
            The CPUs to be removed from the current cpuset
        """

        sub_cpuset = CpuSet(cpuset_str)
        for cpu in sub_cpuset.cpuset_list:
            self.cpuset_list.remove(cpu)


def main():
    from argparse import ArgumentParser

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