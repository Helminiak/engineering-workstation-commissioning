public final class SumSquares {
    public static long sumSquares(int n) {
        if (n < 0) throw new IllegalArgumentException("negative n");
        long sum = 0;
        for (int i = 1; i <= n; ++i) sum += (long) i * i;
        return sum;
    }
    public static void main(String[] args) {
        if (sumSquares(10) != 385 || sumSquares(0) != 0) throw new AssertionError("Incorrect result");
        System.out.println("Java PASS: sum_squares(10)=385");
    }
}
