#!/usr/bin/env python3

import re
import csv

#fnDis = input()
fnDis = "hello.dis"


syscallTable = {}
callGraph = {}

def RecursiveTrace(functionName, callGraph = callGraph, callPath = []):
    if functionName not in callGraph.keys():
        print(f"Error: function not in call graph (not implemented): {functionName}")
        return
    #print(f"tracing {functionName}: {callGraph[functionName]}")
    if functionName not in callPath:
        callPath.append(functionName)
    else:
        return

    if len(callGraph[functionName]['syscall']) > 0:
        for syscall in callGraph[functionName]['syscall']:
            print("->".join(callPath) + "-->sys_" + syscall)
    if len(callGraph[functionName]['callee']) > 0:
        for callee in callGraph[functionName]['callee']:
            RecursiveTrace(callee, callGraph, callPath)






with open("SyscallTableX64.csv", 'r', encoding='utf-8-sig') as csvf:
    csvReader = csv.DictReader(csvf)
    for row in csvReader:
        #print(f"rows: {rows}")
        key = row['NR']
        #print(f"key: {key}")
        syscallTable[key] = row['syscall name']

#print(syscallTable['1'])
#input()


with open(fnDis, "r") as fDis:
    curFunc = ""
    curEax = ""
    syscall = "0f 05"
    lineNo = 0
    for line in fDis:
        lineNo += 1
        # Update current function context
        #if re.match(r"^[^0-9].*():\n", line) != None:
        res = re.match(r"^[0-9a-z]* <([^+]*)>:\n", line)
        if  res != None:
            #print(f"find func at line {lineNo}: {line}")
            # strip the \n and : of the function name
            #curFunc = line[:-2].replace("()", "")
            curFunc = res.group(1)
            #print(f"find func at line {lineNo}: {curFunc}")

            callGraph[curFunc] = {'syscall': set(), 'callee': set(), 'traced': False}
        # Update call graph
        elif re.match(r".*callq.*", line) != None:
            res = re.match(r".*callq.*<(.*)>", line)
            # callq 000000 <function_name>
            # TODO:callq  *%rsi
            # TODO: .plt+0x00
            # TODO: callq  *0x2b7e6d(%rip)        # 6d7178 <__morecore> (refer to dyn lib?)
            # TODO: callq  0 <__libc_resp>
            if res != None:
                callee = res.group(1)
                # TODO: plt table
                if re.match(r"\.plt+0x[0-9a-f]*.*", callee) != None:
                    print(f"plt table calle tracing not implemented")
                else:
                    callGraph[curFunc]['callee'].add(callee)
                #print(f"function {curFunc} calls {callee}")
            else:
                #print(f"callee function unrecognizable (not implemented): {line}")
                pass




        # Update EAX
        else:
            # Here, there is possibilities that:
            # mov $0x00, %eax
            # mov $0x00, %rax
            # xor %eax, %eax
            res = re.match(r".*mov    (.*),\%[re]?ax$$", line)
            if res != None:
                #print(f"find eax update at line {lineNo} in func {curFunc}: eax:{res.group(1)}")
                latest_eax_message = f"find eax update at line {lineNo} in func {curFunc}: eax:{res.group(1)}"
                curEax = res.group(1)
            elif re.match(r".*xor.*ax,.*ax", line) != None:
                curEax = '$0x00'

            # Locate syscall instruction
            # TODO: other syscall instructions like int80 sysenter?
            elif re.match(r".*:\t0f 05.*syscall $", line) != None:
                # Turn '$0x00' string to decimal syscall number
                res = re.match(r"\$0x(.*)", curEax)
                if res == None:
                    #print(f"not a deterministic syscall")
                    curSyscall = "not a detemined syscall"
                else:
                    syscallNo = int(res.group(1), 16)
                    #print(f"syscall number {syscallNo} syscall name {syscallTable[str(syscallNo)]}")
                    curSyscall = syscallTable[str(syscallNo)]
                #print(f"function {curFunc} on line {lineNo} calls syscall: {curSyscall}") # + latest_eax_message)
                callGraph[curFunc]['syscall'].add(curSyscall)
                #print(callGraph[curFunc])
#print(callGraph)

print("Showing the call graph for main:")

RecursiveTrace("main", callGraph)



