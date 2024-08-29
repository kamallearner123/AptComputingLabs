use std::mem;

#[derive(Debug)]
struct IdsEvent {
    pub sensor_id: u16,
    pub id: u32,
    pub severity: u8,
    pub timestamp: u64,
    pub data: [u8; 10],
}

#[repr(packed)]
#[derive(Debug)]
struct IdsEvent2 {
    pub sensor_id: u16,
    pub id: u32,
    pub severity: u8,
    pub timestamp: u64,
    pub data: [u8; 10],
}

fn main() {
    let event = IdsEvent {
        sensor_id: 0,
        id: 1,
        severity: 2,
        timestamp: 3,
        data: [4; 10],
    };

    println!("Size of IdsEvent: {}", mem::size_of::<IdsEvent>());
    println!("Size of IdsEvent2: {}", mem::size_of::<IdsEvent2>());
}