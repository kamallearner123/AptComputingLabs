use mini_redis::{client, Result};

#[tokio::main]
async fn main() -> Result<()>{
    println!("Hello, world!");
    let mut c = client::connect("127.0.0.1:6379").await?;

    c.set("Name", "Kamal".into()).await?;

    let msg = c.get("Name").await?;

    println!("Name = {:?}", msg);
    Ok(())
}
