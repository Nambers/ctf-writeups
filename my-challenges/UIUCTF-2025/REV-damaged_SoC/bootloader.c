// should run in SOC
#include <stdint.h>

void exception_handler();

__attribute__((section(".bootinfo"))) const struct {
    void *exception_handler_addr;
    char verification_sign[];
} bootinfo = {
    &exception_handler,
    "\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd"
    "\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd"
    "\xef\xbf\xbd"}; // uiuctf{U_Uctf_m1psl0ver#0d00_abcdefghi}

static char *const stdout_mmio = (char *)(0x20000010);
static const char alphabet[] =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

__asm__(".section .text\n"
        "li $sp, _stack_top\n"
        "li $gp, __global_pointer$\n"
        "li $ra, 0x0d00\n" // placeholder
        "li $t9, __start\n"
        "jr $t9\n");

void puts_(const char *str);

void putchar_(const char c) { *stdout_mmio = c; }

// NOTE: there will be a bunch of nops in here, because a unknown pipeline
// forwarding issue in the design I didn't find out yet
void __start() {
    puts_("Bootloading\n");
    puts_("Starting verification:");
    // setup timer for print progress
    *(uint32_t *)(0x20000000) =
        *(uint32_t *)(0x20000000) + 450; // should be >= 12
    // start

    int flag = 0;
    char *key = (char *)bootinfo.verification_sign;
    // 4 * 8 = 32, + 6 to the end
    flag = (((char *)(((uint64_t *)key) + 4))[6]) - '}';
    __asm__("nop\nsyscall 36"); // skip fake end
    puts_("\nIncorrect key\nHALT\n");
    __asm__("jr $ra\n");

    __asm__("nop\n");
    if (flag != 0) {
        // flag len should be
        // 39! -_-
        // __asm__("check1:");
        __asm__("syscall %0" ::"i"(0x8f4 - 0x218 - 4));
        // idk why but I can't use
        // __asm__("syscall %0"::"i"(&&END - &&CUR));
        // to calculate it dynamically
        __asm__("jr $ra");
    }

    // verify
    flag = (((key[0] == 'u') + (key[1] == 'i') + (key[2] == 'u') +
             (key[3] == 'c') + (key[4] == 't') + (key[5] == 'f') +
             (key[6] == '{')) == 7)
           << 1;

    // ending
    int tmp = 1;
    for (int i = 0; i < 9; i++) {
        tmp &= key[39 - 1 - 8 + i - 1] == alphabet[i];
    }
    flag = (flag | tmp) << 1;

    __asm__("syscall 16\njr $ra\nsyscall 0x100\njr $ra");

    // U_Uctf
    tmp = key[13] == '_';
    for (int i = 0; i < 6; i++) {
        if (i == 0 || i == 2)
            tmp &= key[i] == key[i + 7] + 32;
        else if (i == 1)
            tmp &= '_' == key[i + 7];
        else
            tmp &= key[i] == key[i + 7];
    }
    flag = flag | tmp;

    __asm__("syscall %0" ::"i"(0x584 - 0x508 - 4));
    // fake checker
    char flagPart[] = {118, 113, 123, 117, 118, 124, 113, 119};
    for (int i = 0; i < 8; i++) {
        flag &= key[14 + 1 + i] == flagPart[i] - 0x10;
    }
    // __asm__("check2:");
    if (flag != 0b111)
        __asm__("syscall %0\nnop" ::"i"(0x8f4 - 0x5a4 - 4));

    // key[14:] = m1 psl0ver# 0d00
    flag = key[14] == 'm' && key[15] == '1' && key[28] == '_' &&
           (key[23] + key[24] == 0x53);
    uint64_t chunk = ((uint64_t *)key)[2];  // psl0ver#, 0x23726576306c7370
    uint32_t chunk2 = ((uint32_t *)key)[6]; // 0d00, 0x30306430
    uint64_t verify_state = 0x1337C0DE12345678;
    uint32_t verify_state2 = 0x3eadbe3f;

    verify_state ^= chunk;
    // if (verify_state == 0x3045a5a822582508)
    //     putchar_('A');
    verify_state2 ^= chunk2;
    // if (verify_state2 == 0xe9dda0f)
    //     putchar_('B');

    uint8_t tmp0 = (verify_state >> 56) & 0xff;
    verify_state = (verify_state << 8);
    verify_state |= tmp0;
    // if (verify_state == 0x45a5a82258250830)
    //     putchar_('C');
    uint8_t tmp1 = (verify_state2 >> 28) & 0xf;
    verify_state2 = (verify_state2 << 4);
    verify_state2 |= tmp1;
    // somehow I cannot just do this
    // otherwise GCC will generate a single ror(SRL) instruction instead of
    // rotate... it will result to 0xFFFFFFFE verify_state2 |= ((verify_state2
    // >> 28) & 0xF);

    // if (verify_state2 == 0xe9dda0f0)
    //     putchar_('D');

    verify_state += 0x0123456789ABCDEF;
    // if (verify_state == 0x46c8ed89e1d0d61f)
    //     putchar_('E');
    verify_state2 += 0x87654321;
    // if (verify_state2 == 0x7142e411)
    //     putchar_('F');

    uint32_t temp = verify_state2;
    verify_state ^= (uint64_t)temp << 32;
    // if (verify_state == 0x378a0998e1d0d61f)
    //     putchar_('G');
    verify_state2 ^= (uint32_t)(verify_state & 0xFFFFFFFF);
    // if (verify_state2 == 0x9092320e)
    //     putchar_('H');

    verify_state ^= 0xFEDCBA9876543210;
    verify_state2 ^= 0x13579BDF;

    uint64_t expected_final = 0xc956b3009784e40f;
    uint32_t expected_final2 = 0x83c5a9d1;

    flag &=
        (verify_state == expected_final) && (verify_state2 == expected_final2);

    if (flag) {
        *(uint32_t *)(0x20000000) = 0;
        puts_("\n===verification passed!===\n");
    } else {
        // __asm__("check3:");
        __asm__("syscall %0\nnop" ::"i"(0x8f4 - 0x824 - 4));
    }

    __asm__("syscall 0x0d00\n");
    while (1)
        ;
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
        *(uint64_t *)stdout_mmio = *(uint64_t *)buf;
    }
    __asm__("jr $ra\nnop");

    __asm__("END:");
    // end
    // disable timer
    *(uint32_t *)(0x20000000) = 0;
    puts_("\nIncorrect key\n");
    __asm__("syscall 0x0d00\n");
    while (1)
        ;
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
            "bne $k0, 0x0d00, _NOT_HALT\n"
            "nop\n");
    // print HALT\n
    __asm__("addiu $sp, $sp, -6\n"
            "lw $t1, 11(%0)\n"
            "li $t2, 0x1b222c24\n"
            "sub $t1, $t1, $t2\n"
            "sw $t1, 0($sp)\n"
            "li $t1, '\\n'\n"
            "sb $t1, 4($sp)\n"
            "li $t1, 0\n"
            "sb $t1, 5($sp)\n"
            "move $a0, $sp\n"
            "jal %1\n"
            "nop\n"
            "_DL: j _DL\n" // infinite loop
            ::"r"(alphabet),
            "r"(puts_));
    __asm__("_NOT_HALT:\n"
            "mfc0 $k1, $14, 0\n"
            "add $k1, $k1, $k0\n"
            "mtc0 $k1, $14, 0\n" // need at least 2 nops bc eret resolved in ID
                                 // stage, but mtc0 in mem stage
            "nop\n"
            "nop\n"
            "eret\n"
            "nop\n");
    __asm__("_int:\n"
            "li $k0, 0x20000004\n" // acknowledge the interrupt
            "li $k1, 1\n"
            "sb $k1, 0($k0)\n"
            "li $k0, 0x20000010\n" // puts "."
            "li $k1, 0x2e\n"
            "sw $k1, 0($k0)\n"
            "li $k0, 0x20000000\n"  // timer MMIO
            "lw $k1, 0($k0)\n"      // read current
            "addiu $k1, $k1, 200\n" // increment by 200
            "sw $k1, 0($k0)\n"      // write back
            "nop\n"
            "eret\n"
            "nop\n");
    while (1)
        ;
}
