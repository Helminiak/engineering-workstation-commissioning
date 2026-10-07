#include <cassert>
#include <iostream>
#include <numeric>
#include <vector>
int main() {
    std::vector<int> values(10);
    std::iota(values.begin(), values.end(), 1);
    const long sum = std::accumulate(values.begin(), values.end(), 0L,
        [](long total, int value) { return total + value * value; });
    assert(sum == 385);
    std::cout << "C++ PASS: sum_squares(10)=385\n";
}
