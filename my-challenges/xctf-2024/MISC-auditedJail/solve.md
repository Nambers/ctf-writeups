# AuditedJail
## Description
NO way to escape ❓Closed, but something SNEAKY...
## Resources
jail.py
## Solves count
1 (unsure)
# Step
0. 根据 <https://github.com/python/cpython/issues/91153> 这个已知的 python UAF + 已知 python 偏移量 <https://github.com/Nambers/python-audit_hook_head_finder> 可以移除 python auditHook 达到成功执行 `os.system("cat /flag")` 的题解.
1. 找到 <https://github.com/python/cpython/issues/91153> 或者 <https://maplebacon.org/2024/02/dicectf2024-irs/>
2. 拿到 UAF 代码, 详细工作原理在 <https://maplebacon.org/2024/02/dicectf2024-irs/> 有
3. 通过 `B = auditHookHandler(0)` 可以拿到一个有一个 closure 也就是捕获变量的方法, 然后可以根据这个方法构造 UAF 中的 `__index__` 方法和从 `repr`/`str` 从拿到地址的方法
4. 通过 `B.__code__ = B.__code__.replace(...)` 构造出 `lambda func: int(str(func).split("0x")[-1].split(f"{62:c}")[0], 16)`
5. 通过 `type("A", (object,),{"__index__": auditHookHandler(0) }` 构造一个类, 里面有 `__index__` 方法, 该方法有一个捕获变量
6. 通过 `A.__index__.__code__ = A.__index__.__code__.replace(...)` 构造出完整 UAF exploit
7. <https://maplebacon.org/2024/02/dicectf2024-irs/> 里有提到或研究 py 代码可以得出 audit hook 在栈上然后通过一些特定偏移量可以抹除
8. exp 里用了 `os.system.__init__` 作为基地址, 然后我在 <https://github.com/Nambers/python-audit_hook_head_finder>(ctf 期间 private 了) 里用 C 脚本(或者本地 ctypes)可以拿到偏移量, 不过要确保和服务器一样是 python 3.12.3 不然偏移量会不对
9. 把偏移量后的地址抹除, 然后继续让程序运行就会打印出 flag

---

0. According to "well-known" Python UAF from <https://github.com/python/cpython/issues/91153> and known offsets <https://github.com/Nambers/python-audit_hook_head_finder>, we are able to smash the audit hook.
1. Find blogs like <https://github.com/python/cpython/issues/91153> or <https://maplebacon.org/2024/02/dicectf2024-irs/> on internet.
2. Get the UAF exploit codes. There are some detail explanations in <https://maplebacon.org/2024/02/dicectf2024-irs/>.
3. Notice that we can obtain a function with one cell in closure by `B = auditHookHandler(0)`.
4. Construct our helper function(`lambda func: int(str(func).split("0x")[-1].split(f"{62:c}")[0], 16)`) by `B.__code__ = B.__code__.replace(...)`.
5. Then build a class by using `type("A", (object,),{"__index__": auditHookHandler(0) }`.
6. Using `A.__index__.__code__ = A.__index__.__code__.replace(...)` to finish the UAF exploit
7. Using some ways to get the offsets, e.g. <https://github.com/Nambers/python-audit_hook_head_finder>.
8. Using UAF to smash the hook.