use std::io::Read;
use std::net::{TcpListener, TcpStream};
use std::time::Duration;

fn main() {
    println!("Waiting for 10secs\n");
    Duration::from_secs(20);

    let listener = TcpListener::bind("127.0.0.1:8181").unwrap();

    println!("{:?}", listener);

    let mut rcvd = [0; 512];

    for stream in listener.incoming() {
        match stream {
            Ok(mut stream) => {
                println!("Client details = {:?}", stream);
                match stream.read(&mut rcvd) {
                    Ok(_) => {
                        println!("Data recieved = {:?}", rcvd);
                    }
                    Err(error) => {
                        println!("recv returned error {:?}", error);
                    }
                }
            }
            Err(error) => {
                println!("Error returned {:?}", error);
            }
        }
    }
}
