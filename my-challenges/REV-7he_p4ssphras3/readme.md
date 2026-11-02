## 标题

7he p4ssphras3

### 作者

Eritque Arcus

### 方向

Reverse

### 知识点

- 自定义硬件侧信道
- SystemVerilog 电路
- VCD波形分析
- TEA加密算法

### 难度

高级

### 内容

某用户在自定义MIPS64架构硬件上运行了一个加密算法来加密助记词(passphrase) 规则如下:
  完整形式: `xxxx_xxxx_xxxx_xxxx` 其中x为小写字母, 每一段是一个有效的英文单词
根据之前的情报该用户泄漏了前半部分密钥内容, 助记词中的第一个单词, 和完整助记词的 MD5 = `a23a6bff24f1db095015b55fbc0c8418`, 但是我们无法获取结果密文.
通过一些手段我们魔法连接了一些跳线进 SoC 的某些信号线, 通过分析这些信号线的波形我们能否还原出助记词?

最终的flag格式为 `flag{xxxx_xxxx_xxxx_xxxx}`. 应该考虑使用 `rockyou`

### 提示

- 这个短小的加密算法源码是什么, 助记词在明文中以什么格式加密
- 加法器的每一位进位信息结合 TEA 算法能带来哪些帮助

### FLAG

- flag{flag_love_play_pass}

### 是否可共享

否

### 备注

选手最终得到的是flag{}之间的字符串，提交需加上flag{}
