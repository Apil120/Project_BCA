async function copyToClipboard() {
    // Fetch the content of responses.txt from the Template directory
    const response = await fetch('static/responses.txt');
    const content = await response.text();

    // Check if the content is not empty
    if (content.trim() !== "") {
        // Create a temporary element (textarea) to display the content
        var tempTextArea = document.createElement("textarea");
        tempTextArea.value = content;

        // Append the temporary element to the document
        document.body.appendChild(tempTextArea);

        // Select the text inside the temporary element
        tempTextArea.select();
        tempTextArea.setSelectionRange(0, 99999); // For mobile devices

        // Copy the selected text to the clipboard
        document.execCommand("copy");

        // Remove the temporary element from the document
        document.body.removeChild(tempTextArea);

        // You can add additional logic or feedback here, such as showing a tooltip or changing the button text
        alert("Text copied to clipboard!");
    } else {
        // If the file is empty, you may want to provide feedback to the user
        alert("File is empty. No content to copy!");
    }
}
