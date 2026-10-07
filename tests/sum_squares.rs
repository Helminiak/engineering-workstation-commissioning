fn main() {
    let result: u64 = (1..=10).map(|x| x*x).sum();
    assert_eq!(result, 385);
    println!("Rust PASS: sum_squares(10)=385");
}
#[test]
fn empty_sum() {
    assert_eq!((1..=0u64).map(|x| x*x).sum::<u64>(), 0);
}
