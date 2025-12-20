#include <stdint.h>

void exception_handler();

__attribute__((unused, section(".bootinfo")))
const uint64_t exception_handler_addr = (uint64_t)(void *)&exception_handler;

__asm__(".section .text\n"
        "li $sp, _stack_top\n"
        "li $gp, __global_pointer$\n"
        "li $ra, 0x0d00\n" // placeholder
        "li $t9, __start\n"
        "jr $t9\n");

inline void put_char(char c) { *(char *)0x20000010 = c; }
void puts_(const char *str) {
    while (*str != '\0') {
        uint64_t i = 0;
        char buf[8];
        for (; str[i] != '\0' && i < 8 - 1; ++i) {
            buf[i] = str[i];
        }
        buf[i] = '\0';
        str += i;
        *(uint64_t *)0x20000010 = *(uint64_t *)buf;
    }
}

void puts_hex(uint32_t v) {
    char hex[] = "0123456789abcdef";
    for (int i = 0; i < 8; i++) {
        *(char *)0x20000010 = hex[(v >> (28 - 4 * i)) & 0xf];
    }
}
// void puts_hex(uint64_t v) {
//     char hex[] = "0123456789abcdef";
//     for (int i = 0; i < 16; i++) {
//         *(char *)0x20000010 = hex[(v >> (28 - 4 * i)) & 0xf];
//     }
// }

// "flag{sysc4ll_AT_check!}"
uint16_t flag[] = {
    // part1 "flag{s" ^ key1
    0x666c ^ 0x752c, 0x6167 ^ 0x752c, 0x7b73 ^ 0x752c,
    // part2 "ysc4ll" ^ key2
    0x7973 ^ 0x1836, 0x6334 ^ 0x1836, 0x6c6c ^ 0x1836,
    // part3 "_AT_ch" ^ key3
    0x5f41 ^ 0x963e, 0x545f ^ 0x963e, 0x6368 ^ 0x963e,
    // part4 "eck!}\x00" ^ key4
    0x6563 ^ 0xf49a, 0x6b21 ^ 0xf49a, 0x7d00 ^ 0xf49a};

void __start() {
    // generate bunch of things
    // part1 "flag{s": generate XOR before
    // add to get XOR key
    uint16_t key;
    __asm__("li $at, 0x752c\n");
    // __asm__("li $at, 0x0d00\n");
    __asm__("syscall 0x0d00\n");
    __asm__("move %0, $at\n" : "=r"(key));
    for (int i = 0; i < 3; i++) {
        __asm__("nop"); // avoid DINS
        flag[i] ^= key;
    }
    // add $at to checklist
    // continue finish XOR

    // part2: ysc4ll
    __asm__("li $at, 0x1836\n");
    // __asm__("li $at, 0xcafeb\n");
    __asm__("syscall 0xcafeb\n");
    __asm__("move %0, $at\n" : "=r"(key));
    for (int i = 3; i < 6; i++) {
        __asm__("nop");
        flag[i] ^= key;
    }

    // part3: _AT_ch
    __asm__("li $at, 0x963e\n");
    // __asm__("li $at, 2\n");
    __asm__("break 2\n");
    __asm__("move %0, $at\n" : "=r"(key));
    for (int i = 6; i < 9; i++) {
        __asm__("nop");
        flag[i] ^= key;
    }

    // part4: eck!}\x00
    __asm__("li $at, 0xf49a\n");
    // __asm__("li $at, 0xcb\n");
    __asm__("break 0xcb\n");
    __asm__("move %0, $at\n" : "=r"(key));
    for (int i = 9; i < 12; i++) {
        __asm__("nop");
        flag[i] ^= key;
    }

    uint64_t buf = *(uint64_t *)0x20000018;
    puts_hex((uint32_t)buf);
    if (buf == 0xf49a963e1836752c) {
        // backdoor
        puts_(":) flag=\n");
        for (int i = 0; i < 24; i++) {
            put_char(*((char *)&flag[i] + 1));
            put_char(*((char *)&flag[i] + 0));
        }
    }

    put_char('\n');
    puts_("HALT\n");
    while (1)
        ;
}

void foo() {
    // hand-written to avoid override context
    __asm__("exception_handler:\n"
            "mfc0 $k0, $8, 1\n" // get status reg
            "srl $k1, $k0, 6\n" // shift right to get cause code
            // store to magic addr
            "li $k1, 0x20000018\n"
            "sw $at, 0($k1)\n"
            "eret\n");
    while (1)
        ;
}