fn sum_squares(n: u64) -> u64 {
    (1..=n).map(|x| x * x).sum()
}
fn main() {
    assert_eq!(sum_squares(10), 385);
    println!("Rust PASS: sum_squares(10)=385");
}
#[test]
fn empty_sum() {
    assert_eq!(sum_squares(0), 0);
}
