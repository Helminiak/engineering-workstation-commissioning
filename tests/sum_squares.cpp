#include <cassert>
#include <iostream>
int main() {
    long sum = 0;
    for (int i = 1; i <= 10; ++i) sum += i * i;
    assert(sum == 385);
    std::cout << "C++ PASS: sum_squares(10)=385\n";
}
