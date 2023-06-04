#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
#include <functional>
#include <iomanip>
#include <sstream>
#include <iterator>
#include <cstring>
#include <openssl/md5.h>
#include <openssl/sha.h>

constexpr int SIZE = 3e5;
constexpr char VERIFY_KEY[] = "46e1b8845b40bc9d977b8932580ae44c";

int get_sequence(const std::vector<int>& A, const std::vector<int>& B, int n, int m) {
    // std::vector<int> ans(n + m - 1, 0);
    long long sum = 0;

    for (int x = 0; x < n; ++x) {
        for (int y = 0; y < m; ++y) {
            // ans[x + y] += A[x] * B[y];
            sum += A[x] * B[y];
        }
    }

    return sum;
}

std::string calculate_md5(const std::string& input) {
    unsigned char md[MD5_DIGEST_LENGTH];
    MD5(reinterpret_cast<const unsigned char*>(input.c_str()), input.size(), md);

    std::stringstream ss;
    ss << std::hex << std::setfill('0');
    for (int i = 0; i < MD5_DIGEST_LENGTH; ++i) {
        ss << std::setw(2) << static_cast<unsigned>(md[i]);
    }

    return ss.str();
}

std::string calculate_sha256(const std::string& input) {
    unsigned char sha256_hash[SHA256_DIGEST_LENGTH];
    SHA256(reinterpret_cast<const unsigned char*>(input.c_str()), input.size(), sha256_hash);

    std::stringstream ss;
    ss << std::hex << std::setfill('0');
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        ss << std::setw(2) << static_cast<unsigned>(sha256_hash[i]);
    }

    return ss.str();
}

int main() {
    std::vector<int> A(SIZE, 0);
    std::vector<int> B(SIZE, 0);

    std::ifstream document1("Document 1.txt");
    if (!document1) {
        std::cerr << "Failed to open Document 1.txt" << std::endl;
        return 1;
    }

    std::string line;
    int idx = 0;
    while (std::getline(document1, line)) {
        A[idx++] = std::stoi(line);
    }

    std::ifstream document2("Document 2.txt");
    if (!document2) {
        std::cerr << "Failed to open Document 2.txt" << std::endl;
        return 1;
    }

    idx = 0;
    while (std::getline(document2, line)) {
        B[idx++] = std::stoi(line);
    }

    std::cout << "Start" << std::endl;
    int sequence = get_sequence(A, B, SIZE, SIZE);
    int val = sequence;
    std::cout << "End" << std::endl;

    std::string val_md5 = calculate_md5(std::to_string(val));
    if (val_md5 != VERIFY_KEY) {
        std::cout << "Wrong solution." << std::endl;
        return 1;
    }

    std::cout << std::to_string(val) << std::endl;

    std::string key = calculate_sha256(std::to_string(val));
    std::string flag = "ctf{";
    for (char ch : key) {
        if (std::isalnum(ch)) {
            flag.push_back(ch);
        }
    }
    flag += "}";
    std::cout << flag << std::endl;

    return 0;
}
