#[derive(Debug)]
struct FriendNode {
    name: String,
    age: i32,
    friends: Vec<FriendNode>,
}

fn main() {
    let david = FriendNode {
                        age: 25,                         
                        name: "David".to_string(),
                        friends: Vec::new()};

    let john = FriendNode {
                        friends: Vec::new(),
                        name: "John".to_string(),
                        .. david}; // Copy david to john
    println!("john details: {:?}", john);

    let peter = john; 
    println!("peter details: {:?}", peter);
    // No ERROR :)
    println!("david details: {:?}", david);
}



