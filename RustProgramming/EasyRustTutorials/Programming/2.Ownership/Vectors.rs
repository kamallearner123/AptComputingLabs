#[derive(Debug)]
enum MyOption<T1, T2> {
    None,
    Some1(T1),
    Some2(T2)
}


fn return_val(a:&mut [i32], index: usize) -> MyOption<i32, f32> {
    a[0] = a[0]*2;
    if index>=a.len() {
        println!("Out of range");
        MyOption::None
    } else {
        MyOption::Some1(a[index])
    }
}


fn main() {
    // let v1 = vec![1,2,3];
    // let rv1 = &v1;
    // println!("v1[3] = {}", rv1[3]);

    let mut a: [i32; 3] = [1,2,3];
    let mut ra: &mut [i32] = &mut a;
    let rra: &mut &mut [i32] = &mut ra; //ERROR/OK
    println!("ra[3] = {:?}", return_val(ra,3));
    println!("rra = {:?}", rra); //Non-Lexical analysis//
}