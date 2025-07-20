macro_rules!  print_hello{
    () => {
        println!("Hello world")
    };
}

fn main() {
    print_hello!();
}