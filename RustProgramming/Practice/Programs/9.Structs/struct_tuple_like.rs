
#[derive(Debug)]
struct Buinds(usize, usize);

fn main() {
    let mut b = Buinds(1, 2);
    let Buinds(x, y) = b;
    println!("x: {}, y: {}", x, y);
    println!("b: {:?}", b);
    println!("b.0: {}, b.1: {}", b.0, b.1);

    b.0 = 100;
    b.1 = 100;
    println!("b: {:?}", b);
}