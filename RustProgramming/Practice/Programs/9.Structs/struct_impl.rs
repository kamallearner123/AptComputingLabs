#[derive(Debug)]
struct IdsEvent {
    id: u32,
    event: String,
}

impl IdsEvent {
    fn new(id: u32, event: &str) -> IdsEvent {
        if event.len() == 0 {
            return IdsEvent {
                id: id,
                event: "No Event".to_string(),
            };
        } else {
            return IdsEvent {
                id: id,
                event: event.to_string(),
            };
        }
    }

    fn get_id(&self) -> u32 {
        self.id
    }  

    fn default() -> IdsEvent {
        IdsEvent {
            id: 0,
            event: "No Event".to_string(),
        }
    }
}

fn main() {
    let mut ids_event1 = IdsEvent::new(100, "");
    println!("ids_event1: {:?}", ids_event1);
    println!("ids_event1 id: {}", ids_event1.get_id());
}

