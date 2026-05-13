#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Unknown");
MODULE_DESCRIPTION("Kernel module loaded for RootWatch baseline detection test");
MODULE_VERSION("1.0");

static int __init rootwatch_test_init(void)
{
    return 0;
}

static void __exit rootwatch_test_exit(void)
{
}

module_init(rootwatch_test_init);
module_exit(rootwatch_test_exit);
