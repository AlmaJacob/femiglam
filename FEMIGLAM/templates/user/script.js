document.getElementById("contactForm").addEventListener("submit", function (e) {
    e.preventDefault();
  
    // Collect form data
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;
  
    // Mock backend communication
    const responseBox = document.getElementById("response");
    responseBox.classList.remove("hidden");
  
    // Simulate sending data to the admin
    setTimeout(() => {
      responseBox.textContent = `Thank you, ${name}! Your message has been sent successfully.`;
      responseBox.style.color = "green";
      
      // Optionally reset the form
      document.getElementById("contactForm").reset();
    }, 1000);
  });
  