fn main() {
    let mut a:String = String::from("Kamal");
    println!("{:?}", a);
    loop {
        // sleep for 1 second
        std::thread::sleep(std::time::Duration::from_secs(1));
        println!("waiting");
    }
}
