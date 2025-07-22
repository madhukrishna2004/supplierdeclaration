function onEdit(e) {
  if (!e) return;

  const sheet = e.source.getActiveSheet();
  const range = e.range;
  const column = range.getColumn();
  const row = range.getRow();
  const value = e.value;

  // Trigger the upload dialog when "Yes" is selected in column E
  if (column === 5 && row >= 6 && value === "Yes") {
    const html = HtmlService.createHtmlOutput(`
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(to bottom, #f9f9f9, #e3e3e3);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
          }
          .container {
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.15);
            max-width: 400px;
            text-align: center;
          }
          h3 {
            font-size: 20px;
            margin-bottom: 20px;
            color: #333;
          }
          input[type="file"] {
            display: block;
            margin: 15px auto 20px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
            background: #fafafa;
            cursor: pointer;
            width: 100%;
          }
          button {
            padding: 10px 25px;
            font-size: 16px;
            background: linear-gradient(45deg, #4CAF50, #66BB6A);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
          }
          button:hover {
            background: linear-gradient(45deg, #43A047, #57CA62);
          }
          .spinner {
            display: none;
            margin-top: 20px;
          }
          .spinner div {
            width: 20px;
            height: 20px;
            margin: 3px;
            background: linear-gradient(45deg,rgb(95, 209, 173),rgb(124, 234, 199));
            border-radius: 50%;
            display: inline-block;
            animation: bounce 1.4s infinite ease-in-out both;
          }
          .spinner div:nth-child(2) {
            animation-delay: -0.7s;
          }
          @keyframes bounce {
            0%, 100% {
              transform: scale(0);
            }
            50% {
              transform: scale(1);
            }
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h3>Upload File</h3>
          <input type="file" id="fileInput" accept=".pdf,.docx,.xlsx">
          <button onclick="uploadFile()">Upload</button>
          <div class="spinner" id="spinner">
            <div></div>
            <div></div>
          </div>
        </div>
        <script>
          function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            if (!file) {
              alert("Please select a file.");
              return;
            }
            document.getElementById('spinner').style.display = 'block';
            const reader = new FileReader();
            reader.onload = function(event) {
              const fileData = {
                name: file.name,
                type: file.type,
                content: event.target.result
              };
              google.script.run.withSuccessHandler(() => {
                google.script.host.close();
              }).handleFileUpload(fileData, ${row});
            };
            reader.readAsDataURL(file);
          }
        </script>
      </body>
      </html>
    `).setWidth(450).setHeight(400);

    SpreadsheetApp.getUi().showModalDialog(html, 'Upload Supporting File');
  }
}

function handleFileUpload(fileData, row) {
  const folderId = '1gVPKB4rFHb6PXTe3vOXLdzxv5C4m6U4s'; // Replace with your Google Drive folder ID
  const folder = DriveApp.getFolderById(folderId);

  try {
    // Decode file content from Base64
    const content = fileData.content.split(',')[1];
    const blob = Utilities.newBlob(Utilities.base64Decode(content), fileData.type, fileData.name);

    // Upload the file to Drive
    const uploadedFile = folder.createFile(blob);

    // Get the uploaded file's URL
    const fileUrl = uploadedFile.getUrl();

    // Save the chip in column J
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const chipCell = sheet.getRange(row, 10); // Column J is the 10th column

    // Set the chip-style text with clickable link
    chipCell.setRichTextValue(
      SpreadsheetApp.newRichTextValue()
        .setText('📎 Open File')
        .setLinkUrl(fileUrl)
        .build()
    );

    // Log the upload details
    logUpload(row, fileData.name, fileUrl);

    // Send an email notification
    sendEmailNotification(fileData.name, fileUrl);
  } catch (error) {
    SpreadsheetApp.getUi().alert('File upload failed: ' + error.message);
  }
}
   
function logUpload(row, fileName, fileUrl) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Upload Logs");
  if (!sheet) {
    const logSheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet("Upload Logs");
    logSheet.appendRow(["Timestamp", "Row", "File Name", "File URL"]);
  }
  const logSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Upload Logs");
  logSheet.appendRow([new Date(), `Row ${row}`, fileName, fileUrl]);
}

function sendEmailNotification(fileName, fileUrl) {
  const recipient = 'krishnamadhurama@gmail.com'; // Replace with your email address
  const subject = 'New File Uploaded';
  const body = `
    A new file has been uploaded:
    - File Name: ${fileName}
    - File URL: ${fileUrl}
  `;

  GmailApp.sendEmail(recipient, subject, body);
}
