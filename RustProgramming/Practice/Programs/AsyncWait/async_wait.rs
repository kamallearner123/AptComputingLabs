use std::time::Duration;
use tokio::time::sleep;

async fn do_something() {
    println!("Doing something...");
    sleep(Duration::from_secs(2)).await;
    println!("Done!");
}

#[tokio::main]
async fn main() {
    println!("Start");
    do_something().await;
    println!("End");
}

