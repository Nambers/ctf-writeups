#include <stdint.h>

void exception_handler();

__attribute__((unused, section(".bootinfo")))
const uint64_t exception_handler_addr = (uint64_t)(void *)&exception_handler;

static char *const stdout_mmio = (char *)(0x20000010);
static const uint64_t stdout_buffer_size = 8;

__asm__(".section .text\n"
        "li $sp, _stack_top\n"
        "li $gp, __global_pointer$\n"
        "li $ra, 0x0d00\n" // placeholder
        "li $t9, __start\n"
        "jr $t9\n");

void puts_(const char *str) {
    while (str[0]) {
        uint64_t i = 0;
        char buf[8];
        for (; str[i] != '\0' && i < stdout_buffer_size - 1; ++i) {
            buf[i] = str[i];
        }
        buf[i] = '\0';
        str += i;
        *(uint64_t *)stdout_mmio = *(uint64_t *)buf;
    }
}

char *bar(const char *str) {
    static char result[32];
    int pos = 0;

    // "uiuctf{"
    for (int i = 0; i < 7; i++) {
        result[pos++] = str[i];
    }

    // str = "uiuctf{this_is_not_flag}"
    //                ^7   ^12 ^15 ^19

    char base_chars[8];
    base_chars[0] = str[7];  // 't'
    base_chars[1] = str[8];  // 'h'
    base_chars[2] = str[9];  // 'i'
    base_chars[3] = str[10]; // 's'
    base_chars[4] = str[12]; // 'i'
    base_chars[5] = str[13]; // 's'
    base_chars[6] = str[15]; // 'n'
    base_chars[7] = str[16]; // 'o'

    result[pos++] = 0x74 ^ 0x68 ^ 0x53;     // 'O'
    result[pos++] = str[9] + str[10] - 0x66;  // 'v'
    result[pos++] = str[15] ^ str[16] ^ 0x4E; // 'O'
    result[pos++] = str[11];                  // '_'

    result[pos++] = base_chars[4] - 3; // 'f'
    result[pos++] = base_chars[5] - 7; // 'l'
    result[pos++] = 0x34;              // '4'
    result[pos++] = base_chars[4] - 2; // 'g'
    result[pos++] = str[14];           // '_'

    result[pos++] = base_chars[6] - 61; // '1'
    result[pos++] = base_chars[7] + 4;  // 's'
    result[pos++] = str[18];            // '_'

    result[pos++] = str[7];  // 't'
    result[pos++] = str[8];  // 'h'
    result[pos++] = str[9];  // 'i'
    result[pos++] = str[10]; // 's'

    result[pos++] = str[23]; // '}'
    result[pos++] = 0x0A;    // '\n'
    result[pos] = 0;

    // puts_(result);
    return result;
}

char *rev_bar(const char *str) {
    // inp=uiuctf{OvO_fl4g_1s_this}
    // ret=uiuctf{flag_is_not_this}
    char result[32];
    int pos = 0;

    // Copy "uiuctf{"
    for (int i = 0; i < 7; i++) {
        result[pos++] = str[i];
    }

    // Reverse the operations to get original base_chars
    char base_chars[8];

    // From the end part of transformed string (positions 19,20,21,22)
    base_chars[0] = str[19]; // 't'
    base_chars[1] = str[20]; // 'h'
    base_chars[2] = str[21]; // 'i'
    base_chars[3] = str[22]; // 's'

    // Reconstruct original string: "flag_is_not_this}"
    result[pos++] = str[11];               // 'f'
    result[pos++] = str[12];               // 'l'
    result[pos++] = str[13] + ('a' - '4'); // '4' → 'a'
    result[pos++] = str[14];               // 'g'
    result[pos++] = str[10];               // '_'
    result[pos++] = str[11] + 3;           // 'i'
    result[pos++] = str[12] + 7;           // 's'
    result[pos++] = str[15];               // '_'
    result[pos++] = str[16] + 61;          // 'n'
    result[pos++] = str[17] - 4;           // 'o'
    result[pos++] = base_chars[0];         // 't'
    result[pos++] = str[18];               // '_'
    result[pos++] = base_chars[0];         // 't'
    result[pos++] = base_chars[1];         // 'h'
    result[pos++] = base_chars[2];         // 'i'
    result[pos++] = base_chars[3];         // 's'
    result[pos++] = str[23];               // '}'
    result[pos] = 0;
    puts_(result);
}

void __start() {
    // *(uint64_t *)(0x20000000) = *(uint64_t *)(0x20000000) + 102; // should be
    // >= 12
    char *flag = bar("uiuctf{this_is_not_flag}");
    char backup_flag[32];
    for (int i = 0; i < 32; i++) {
        backup_flag[i] = flag[i];
    }
    rev_bar(backup_flag);
    // puts_("HALT\n");
    __asm__("syscall 0x0d00\n");
    while (1)
        ; // prevent exit
}

void foo() {
    // hand-written to avoid override context
    __asm__("exception_handler:\n"
            "mfc0 $k0, $13, 0\n"
            "li $k1, 0b1111100\n"
            "andi $k0, $k0, 0b1111100\n" // get cause bits
            "beqz $k0, _int\n"           // if no exception, jump to _int
            "mfc0 $k0, $8, 1\n"          // get status reg
            "srl $k0, $k0, 6\n"          // shift right to get cause code
            "bne $k0, 0x0d00, _NOT_HALT\n");
    // print HALT\n
    puts_("HALT\n");
    __asm__("_NOT_HALT: _int: eret\n");
    while (1)
        ;
}