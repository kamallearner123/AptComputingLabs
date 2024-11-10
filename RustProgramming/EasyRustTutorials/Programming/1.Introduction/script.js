// async function runCode() {
//     const code = document.getElementById('codeEditor').value;
//     const outputDiv = document.getElementById('output');
  
//     outputDiv.textContent = "Running...";
  
//     const response = await fetch('https://play.rust-lang.org/execute', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({
//         channel: "stable",
//         edition: "2021",
//         crateType: "bin",
//         mode: "debug",
//         tests: false,
//         code: code
//       })
//     });
  
//     const result = await response.json();
  
//     if (result.success) {
//       outputDiv.textContent = result.stdout || "No output";
//     } else {
//       outputDiv.textContent = result.stderr || "An error occurred";
//     }
//   }
  

  // Initialize CodeMirror with Rust mode
const editor = CodeMirror(document.getElementById("codeEditor"), {
    mode: "rust",
    theme: "monokai",
    lineNumbers: true,
    value: `fn main() {
    let x = String::from("Hello, Rust!");
    println!("{}", x);
  }`
  });
  
  async function runCode() {
    const code = editor.getValue();
    const outputDiv = document.getElementById('output');
    
    outputDiv.textContent = "Running...";
  
    const response = await fetch('https://play.rust-lang.org/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        channel: "stable",
        edition: "2021",
        crateType: "bin",
        mode: "debug",
        tests: false,
        code: code
      })
    });
  
    const result = await response.json();
  
    if (result.success) {
      outputDiv.textContent = result.stdout || "No output";
    } else {
      outputDiv.textContent = result.stderr || "An error occurred";
    }
  }
  