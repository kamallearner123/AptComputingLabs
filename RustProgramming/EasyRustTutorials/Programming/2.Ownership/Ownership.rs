fn get_len(msg: &String) -> usize {
    msg.len()
}

fn main() {

    let message = String::from("Hello friends!!!");
    println!("Msg = {}", message);

    let rm: &String = &message; //rm : Readonly
    println!("message = {}, rm = {}", message, rm);

    println!("Len = {}", get_len(rm));

    println!("index 0 = {:?}", message.chars().nth(15));
}