# Homework Help
## Description
I wrote a program to solve my math homework so I could find flags. Unfortunatly my program sucks at math and just makes me do it. It does find flags though.
## Resource
homework_help - executable
# Steps
At first I try to use Angr solve the input to let this print `Thanks, I\'ll help you check the flag`. But it is not necessary, the input obviously is 3. Then, I notice that the real core function is `__stack_chk_fail`. It is not the system one! I was fooled by this name lol.  
Therefore, I build an Angr script to find the proper input of this func.

# Solution
Angr script:
```python
import angr
import sys
import claripy

def is_successful(state):
    global flag
    print(state.posix.dumps(1))
    return b'Well Done' in state.posix.dumps(1)

def should_abort(state):
    print(state.posix.dumps(1))
    return b'Nope' in state.posix.dumps(1)

project = angr.Project("F:/Downloads/homework_help", auto_load_libs = False)
print(project.loader.find_symbol("__stack_chk_fail").rebased_addr)
state = project.factory.blank_state(addr=project.loader.find_symbol("__stack_chk_fail").rebased_addr)
flag = state.solver.BVS('FLAG', 32 * 8)
# FLAG addr
print(project.loader.find_symbol("FLAG").rebased_addr)
state.memory.store(project.loader.find_symbol("FLAG").rebased_addr, flag)
simulation = project.factory.simulation_manager(state)
simulation.one_active.options.add(angr.options.LAZY_SOLVES)
simulation.explore(find=[is_successful, 0x004013f5] , avoid=[should_abort, 0x401414])

for deadended in simulation.deadended:
    print("Valid memory access triggered by %s" % repr(deadended.posix.dumps(0)))

for errored in simulation.errored:
    print("%s caused by %s" % (errored.error, repr(errored.state.posix.dumps(0))))

if simulation.found:
    for s in simulation.found:
        print("input:", s.posix.dumps(0))
        print("output:", s.posix.dumps(1))
        print(s.solver.eval(flag, cast_to=bytes).decode())
else:
    raise Exception('Could not find the solution')
``` 