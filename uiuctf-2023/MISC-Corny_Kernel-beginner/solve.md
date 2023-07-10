# Corny Kernel
## Attachment
pwnymodule.c
```c
// SPDX-License-Identifier: GPL-2.0-only

#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt

#include <linux/module.h>
#include <linux/init.h>
#include <linux/kernel.h>

extern const char *flag1, *flag2;

static int __init pwny_init(void)
{
	pr_alert("%s\n", flag1);
	return 0;
}

static void __exit pwny_exit(void)
{
	pr_info("%s\n", flag2);
}

module_init(pwny_init);
module_exit(pwny_exit);

MODULE_AUTHOR("Nitya");
MODULE_DESCRIPTION("UIUCTF23");
MODULE_LICENSE("GPL");
MODULE_VERSION("0.1");
```
## Solution
1. Because this linux module will print out the flag at `__init` and `__exit`, we just need to load and unload it.
2. Then, because in `__init` it is `pr_alert`, which will not log out to stdout, we need to use `dmesg` to see the log.  
```bash
gzip -d pwny
insmod -d pwny
rmmod pwny
demsg
```
log:
```
[   43.189896] pwnymodule: uiuctf{m4ster_
[   55.502591] pwnymodule: k3rNE1_haCk3r}
```