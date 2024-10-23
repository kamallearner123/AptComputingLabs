use std::net::TcpListener;

pub struct Server {
    addr: String,
}

impl Server {
    pub new (addr:String) -> Self {
        Server { addr }
    }

    pub fn run(&self) {
        println!("Listening on {}", self.addr);
        
        let listenet = TcpListener::bind(&self.add).unwrap();
    
    }
}