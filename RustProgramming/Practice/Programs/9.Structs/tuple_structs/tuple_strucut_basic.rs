use std::mem;

#[derive(Debug)]
struct Color(u8, u8, u8);
impl Color {
    fn new(r: u8, g: u8, b: u8) -> Color {
        Color(r, g, b)
    }

    fn print_color (&self) {
        println!("Color values: {}, {}, {}", self.0, self.1, self.2);
    }
}

fn main() {
    let black = Color(0, 0, 0);
    let mut white = Color(255, 255, 255);

    println!("Black color values: {}", black.0);
    white.0 = 0;
    white.print_color();

    println!("Size of Color: {}", mem::size_of::<Color>());

}

