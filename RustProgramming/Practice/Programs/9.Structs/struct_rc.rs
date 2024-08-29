#[derive(Debug)]
struct FriendNode {
    name: String,
    age: i32,
    friends: Vec<FriendNode>,
}

fn main() {
    let david = FriendNode {
                        age: 25,                         
                        name: "Kamal".to_string(),
                        friends: Vec::new()};

    let john = FriendNode {
                        friends: Vec::new(),
                        name: "John".to_string(),
                        .. david}; // Copy david to john
    println!("john details: {:?}", john);

    let peter = john; // Clone david to peter
    println!("peter details: {:?}", peter);
    // error[E0382]: borrow of partially moved value: `david`
    println!("david details: {:?}", david);
}




