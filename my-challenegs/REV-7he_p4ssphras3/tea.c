#include <stdint.h>

void exception_handler();

__attribute__((unused, section(".bootinfo")))
const uint64_t exception_handler_addr = (uint64_t)(void *)&exception_handler;
const char flag[] = "XXXXflagXXXXloveXXXXplayXXXXpass";
const uint32_t tea_key[4] = {0xf0f0f0f0, 0x0f0f0f0f, 0x0fedcba9, 0x87654321};

__asm__(".section .text\n"
        "li $sp, _stack_top\n"
        "li $gp, __global_pointer$\n"
        "li $ra, 0x0d00\n" // placeholder
        "li $t9, __start\n"
        "jr $t9\n");

inline void put_char(char c) {
    *(char *)0x20000010 = c;
}
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

void code(uint32_t *v, uint32_t *k) {
    uint32_t v0 = v[0], v1 = v[1], delta = 0x9e3779b9,
             n = 32, // Invariant: Number of bits remaining
        sum = 0, tmp = 0;

    while (n--) {
        __asm__("T1: nop");
        sum += delta;
        __asm__("T2: nop");
        // tmp = v1 + sum;
        // tmp = v0 + sum;
        v0 += ((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]);
        // tmp = ((v1 << 4) + k[0]);
        __asm__("T3: nop;");
        // tmp ^= (v1 + sum);
        // __asm__("xor %0, %1, %2" : "=r"(tmp) : "r"(tmp), "r"(v1 + sum));
        // __asm__("add %0, %1, %2" : "=r"(tmp) : "r"(v1), "r"(sum));
        // tmp ^= ((v1 << 4) + k[0]);
        __asm__("T4: nop");
        // tmp ^= ((v1 >> 5) + k[1]);
        // v0 += tmp;
        v1 += ((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]);
        // to avoid lsa
        // tmp = (v0 << 4) + k[2];
        __asm__("T5: nop;");
        // tmp ^= (v0 + sum);
        // __asm__("xor %0, %1, %2" : "=r"(tmp) : "r"(tmp), "r"(v0 + sum));
        // tmp ^= ((v0 >> 5) + k[3]);
        // v1 += tmp;
        __asm__("END:");
    }
    v[0] = v0;
    v[1] = v1;
}

void __start() {
    // encrypt the flag using TEA and output the ciphertext to stdout
    uint32_t v[2] = {0, 0};
    puts_("Ciphertext: ");
    for (int i = 0; i < 32; i += 8) {
        puts_("\n<REDEACTED>");
        v[0] = *(uint32_t *)(flag + i);
        v[1] = *(uint32_t *)(flag + i + 4);
        code(v, (uint32_t *)tea_key);
        // puts_hex(v[0]);
        // puts_hex(v[1]);
    }
    put_char('\n');
    puts_("HALT\n");
    while (1)
        ;
}

void exception_handler() {
    while (1)
        ;
}