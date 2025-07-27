function onOpen(e) {
  SpreadsheetApp.getUi().createMenu("My Custom Menu")
    .addItem("Ask for Authorization", "askForAuthorization")
    .addToUi();
}

function askForAuthorization() {
  const html = HtmlService.createHtmlOutput(`
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {
          font-family: Arial, sans-serif;
          text-align: center;
          padding: 20px;
        }
        h3 {
          color: #333;
        }
        p {
          color: #666;
        }
        .loading {
          width: 50px;
          height: 50px;
          border: 5px solid #ccc;
          border-top-color: #4CAF50;
          bordeoqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqr-radius: 50%;
          animation: spin 1s linear infinite;
          margin: 20px auto;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        button {
          padding: 10px 20px;
          font-size: 14px;
          background: #4CAF50;
          color: white;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          transition: 0.3s;
        }
        button:hover {
          background: #43A047;
        }
      </style>
    </head>
    <body>
      <h3>🔒 Authorization Required</h3>
      <p>Please authorize this script to run properly.</p>
      <div class="loading"></div>
      <button onclick="google.script.host.close()">OK</button>
    </body>
    </html>
  `).setWidth(350).setHeight(250);
  
  // ✅ Only show the UI if user interaction allows it
  try {
    SpreadsheetApp.getUi().showModalDialog(html, "Permission Required");
  } catch (error) {
    Logger.log("⚠ UI cannot be displayed in this context.");
  }
}

function sendGuidanceEmail() {
  try {
    var userEmail = Session.getActiveUser().getEmail();
    if (!userEmail) {
      Logger.log("⚠ No active user detected.");
      return;
    }

    var subject = "TradeSphere Global - Google Sheets Authentication Guide";
    var body = "Dear User,\n\nYou need to authorize the script...\n\n";

    // ✅ Use Drive API with OAuth to access files properly
    var file = getDriveFileByName("Google_Sheets_Auth_Guide.pdf");
    if (file) {
      GmailApp.sendEmail(userEmail, subject, body, { attachments: [file.getBlob()] });
      Logger.log("✅ Email sent to: " + userEmail);
    } else {
      Logger.log("⚠ File not found: Google_Sheets_Auth_Guide.pdf");
    }
  } catch (error) {
    Logger.log("❌ Error: " + error.toString());
  }
}

// ✅ Function to access Drive file securely
function getDriveFileByName(fileName) {
  var files = DriveApp.getFilesByName(fileName);
  return files.hasNext() ? files.next() : null;
}

/**
 * Step 1: Create an API endpoint to check if the script is running.
 */
function doGet(e) {
    return ContentService.createTextOutput("API is running.");
}

/**
 * Step 2: Get the OAuth token of the signed-in user.
 * This ensures the script runs with the user's identity.
 */
function getOAuthToken() {
    return ScriptApp.getOAuthToken();
}

/**
 * Step 3: Retrieve the active user's email.
 * Ensures that the script is running under the user's identity.
 */
function getUserEmail() {
    return Session.getActiveUser().getEmail();
}

// ✅ Ensures the onEdit trigger exists
function createTrigger() {
  var triggers = ScriptApp.getProjectTriggers();

  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === "onEdit") {
      Logger.log("✅ Trigger already exists.");
      return;
    }
  }

  // ✅ Create a new onEdit trigger
  ScriptApp.newTrigger("onEdit")
    .forSpreadsheet(SpreadsheetApp.getActiveSpreadsheet())
    .onEdit()
    .create();

  Logger.log("🚀 Trigger Created Successfully!");
}

//
function onEdit(e) {
  if (!e) return;

  const sheet = e.source.getActiveSheet();
  const range = e.range;
  const column = range.getColumn();
  const row = range.getRow();
  const value = e.value;

  if (column === 5 && row >= 6 && value === "Yes") {
    const consentCell = sheet.getRange(6, 11).getValue(); // Check K6

    if (!consentCell) {
      showSupplierConsentDialog();
      sheet.getRange(row, 5).setValue(""); // Reset "Yes" selection
      return;
    }

    // ✅ If Supplier Consent exists, allow file uploads
    showFileUploadDialog(row);
  }
}

// ✅ Function to Show Supplier Consent Upload Dialog
function showSupplierConsentDialog() {
  const html = HtmlService.createHtmlOutput(`
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {
          font-family: 'Arial', sans-serif;
          background: #121212;
          color: white;
          margin: 0;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
        }
        .container {
          background: #1e1e1e;
          padding: 20px;
          border-radius: 12px;
          box-shadow: 0px 4px 15px rgba(0, 255, 255, 0.15);
          text-align: center;
        }
        .loader {
          display: none;
          width: 40px;
          height: 40px;
          border: 5px solid rgba(255, 255, 255, 0.1);
          border-top-color: cyan;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin: 20px auto;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        .success {
          display: none;
          color: cyan;
          font-weight: bold;
          margin-top: 15px;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h3>Upload Supplier Consent</h3>
        <input type="file" id="fileInput" accept=".pdf,.docx,.xlsx">
        <button onclick="uploadConsent()">Upload</button>
        <div class="loader" id="loader"></div>
        <div class="success" id="successMsg">✅ Supplier Consent Uploaded...Continue to upload Attach Files!</div>
      </div>
      <script>
        function uploadConsent() {
          const fileInput = document.getElementById('fileInput');
          const file = fileInput.files[0];
          const loader = document.getElementById('loader');
          const successMsg = document.getElementById('successMsg');

          if (!file) {
            alert("Please select a file.");
            return;
          }

          loader.style.display = "block"; // Show loader

          const reader = new FileReader();
          reader.onload = function(event) {
            const fileData = {
              name: file.name,
              type: file.type,
              content: event.target.result
            };

            google.script.run.withSuccessHandler(() => {
              loader.style.display = "none"; // Hide loader
              successMsg.style.display = "block"; // Show success

              setTimeout(() => {
                google.script.host.close(); // ✅ Close modal
              }, 1500);
            }).handleSupplierConsentUpload(fileData);
          };

          reader.readAsDataURL(file);
        }
      </script>
    </body>
    </html>
  `).setWidth(450).setHeight(400);

  SpreadsheetApp.getUi().showModalDialog(html, 'Upload Supplier Consent');
}

function showFileUploadDialog(row) {
  const html = HtmlService.createHtmlOutput(`
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {
          font-family: 'Arial', sans-serif;
          background: linear-gradient(to bottom, #121212, #1e1e1e);
          color: white;
          text-align: center;
          margin: 0;
          padding: 20px;
        }
        .container {
          background: #1e1e1e;
          padding: 20px;
          border-radius: 12px;
          box-shadow: 0px 4px 15px rgba(0, 255, 255, 0.2);
        }
        input[type="file"] {
          display: block;
          margin: 15px auto;
          padding: 10px;
          border: none;
          background: #2a2a2a;
          color: white;
          border-radius: 8px;
          cursor: pointer;
        }
        button {
          padding: 10px 20px;
          background: linear-gradient(45deg, #4CAF50, #66BB6A);
          color: white;
          border: none;
          cursor: pointer;
          border-radius: 8px;
          transition: all 0.3s;
        }
        button:hover { background: linear-gradient(45deg, #43A047, #57CA62); }
        .loader {
          display: none;
          margin: 20px auto;
          width: 40px;
          height: 40px;
          border: 5px solid rgba(255, 255, 255, 0.1);
          border-top-color: cyan;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .success { display: none; color: cyan; font-weight: bold; margin-top: 15px; }
      </style>
    </head>
    <body>
      <div class="container">
        <h3>Upload File</h3>
        <input type="file" id="fileInput" accept=".pdf,.docx,.xlsx">
        <button onclick="uploadFile()">Upload</button>
        <div class="loader" id="loader"></div>
        <p class="success" id="successMsg">✅ Upload Successful!</p>
      </div>

      <script>
        function uploadFile() {
          const fileInput = document.getElementById('fileInput');
          const file = fileInput.files[0];
          const loader = document.getElementById('loader');
          const successMsg = document.getElementById('successMsg');

          if (!file) {
            alert("Please select a file.");
            return;
          }

          loader.style.display = "block"; 

          const reader = new FileReader();
          reader.onload = function(event) {
            const fileData = {
              name: file.name,
              type: file.type,
              content: event.target.result
            };

            google.script.run.withSuccessHandler((fileUrl) => {
              loader.style.display = "none"; 
              successMsg.style.display = "block"; 

              setTimeout(() => google.script.host.close(), 1500);
            }).uploadFileToDrive(fileData, ${row});
          };

          reader.readAsDataURL(file);
        }
      </script>
    </body>
    </html>
  `).setWidth(400).setHeight(350);

  SpreadsheetApp.getUi().showModalDialog(html, 'Upload File');
}

  
function uploadFileToDrive(fileData, rowNum) {
  if (!fileData || !fileData.content) return "No file data received.";

  try {
    // ✅ Define Google Drive Folder ID (Change to your folder ID)
    const folderId = "14BLdtpwodH-p75biqvDNXYRVvm-TIUojyoi0V1r-LOXeI74boE-Tta1ZhklbG0WhSckAMnIa";
    const folder = DriveApp.getFolderById(folderId);

    // ✅ Convert Base64 file to Blob
    const blob = Utilities.newBlob(Utilities.base64Decode(fileData.content.split(",")[1]), fileData.type, fileData.name);
    const file = folder.createFile(blob); 
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);

    // ✅ Get File ID & Generate Drive File Chip
    const fileId = file.getId();
    const driveFile = DriveApp.getFileById(fileId);
    const driveUrl = file.getUrl();

    // ✅ Store as Drive File Chip in Column J (10th column)
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const cell = sheet.getRange(rowNum, 10);

    const richText = SpreadsheetApp.newRichTextValue()
      .setText(driveFile.getName()) // Display file name
      .setLinkUrl(driveUrl) // Set as clickable link
      .build();

    cell.setRichTextValue(richText);

    // ✅ Force UI Update
    SpreadsheetApp.flush();

    return driveUrl; // Returning URL for further processing (if needed)
  } catch (error) {
    Logger.log("Error Uploading File: " + error.message);
    return "Error uploading file.";
  }
}



function showFileLink(row) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const fileUrl = sheet.getRange(row, 11).getValue();

  if (!fileUrl) {
    SpreadsheetApp.getUi().alert("❌ No file uploaded yet.");
  } else {
    const html = HtmlService.createHtmlOutput(`
      <html><body>
        <h3>Uploaded File</h3>
        <a href="${fileUrl}" target="_blank">📂 View / Download</a>
      </body></html>
    `);
    SpreadsheetApp.getUi().showModalDialog(html, 'View Uploaded File');
  }
}

// ✅ Function to Upload File to Google Drive & Store Link in Column K6
function handleFileUpload(fileData) {
  try {
    const folder = DriveApp.getFolderById("14BLdtpwodH-p75biqvDNXYRVvm-TIUojyoi0V1r-LOXeI74boE-Tta1ZhklbG0WhSckAMnIa"); // Replace with your Google Drive folder ID
    const blob = Utilities.newBlob(Utilities.base64Decode(fileData.content.split(",")[1]), fileData.type, fileData.name);
    const file = folder.createFile(blob);
    
    const fileUrl = file.getUrl();
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    sheet.getRange("K6").setValue(fileUrl); // Store in K6

    return fileUrl;
  } catch (error) {
    Logger.log("Error uploading file: " + error.message);
    return null;
  }
}

// ✅ Function to Check if File Exists in K6 & Prompt Upload if Missing
function checkAndAskForSupplierConsent() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const existingFileUrl = sheet.getRange("K6").getValue();

  if (!existingFileUrl) {
    const ui = SpreadsheetApp.getUi();
    const response = ui.alert(
      "Upload Supplier Consent First",
      "You must upload the Supplier Consent file before proceeding.",
      ui.ButtonSet.OK
    );

    if (response === ui.Button.OK) {
      showFileUploadDialog();
    }
  }
}

// ✅ Function to View or Download File from Column K6
function viewUploadedFile() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const fileUrl = sheet.getRange("K6").getValue();

  if (fileUrl) {
    const html = HtmlService.createHtmlOutput(`
      <script>
        window.open("${fileUrl}", "_blank");
        google.script.host.close();
      </script>
    `);
    SpreadsheetApp.getUi().showModalDialog(html, "View File");
  } else {
    SpreadsheetApp.getUi().alert("No file found in Column K6.");
  }
}

function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const loader = document.getElementById('loader');
  const successMsg = document.getElementById('successMsg');

  if (!file) {
    alert("Please select a file.");
    return;
  }

  loader.style.display = "block"; // Show loader

  const reader = new FileReader();
  reader.onload = function(event) {
    const fileData = {
      name: file.name,
      type: file.type,
      content: event.target.result
    };

    google.script.run.withSuccessHandler(() => {
      loader.style.display = "none"; // Hide loader
      successMsg.style.display = "block"; // Show success

      setTimeout(() => {
        google.script.host.close(); // ✅ Close modal
      }, 1500);
    }).handleFileUpload(fileData, window.rowNum);
  };

  reader.readAsDataURL(file);
}

function saveFileToDrive(fileData) {
  try {
    const folderId = "14BLdtpwodH-p75biqvDNXYRVvm-TIUojyoi0V1r-LOXeI74boE-Tta1ZhklbG0WhSckAMnIa"; // Update folder ID
    const folder = DriveApp.getFolderById(folderId);
    if (!folder) {
      Logger.log("⚠ Folder not found!");
      return null;
    }
    
    const blob = Utilities.newBlob(
      Utilities.base64Decode(fileData.content.split(",")[1]),
      fileData.type,
      fileData.name
    );
    const file = folder.createFile(blob);
    return file.getUrl();
  } catch (error) {
    Logger.log("❌ Error uploading file: " + error.toString());
    return null;
  }
}

function handleSupplierConsentUpload(fileData) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const folder = getOrCreateFolder("Supplier Consents"); // 🔹 Store files in a folder
  const blob = Utilities.newBlob(Utilities.base64Decode(fileData.content.split(',')[1]), fileData.type, fileData.name);
  const file = folder.createFile(blob);

const fileLink = file.getUrl(); // 🔹 Generate file link
sheet.getRange(6, 11).setFormula('=HYPERLINK("' + fileLink + '", "View Consent")'); // 🔹 Store as a clickable link
}

function handleFileUpload(fileData, row) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const folder = getOrCreateFolder("Uploaded Documents"); // 🔹 Store in another folder
  const blob = Utilities.newBlob(Utilities.base64Decode(fileData.content.split(',')[1]), fileData.type, fileData.name);
  const file = folder.createFile(blob);

  const fileLink = file.getUrl(); // 🔹 Generate file link
sheet.getRange(row, 10).setFormula('=HYPERLINK("' + fileLink + '", "View File")');
 // 🔹 Store as a clickable link
}

// ✅ Function to Create/Get a Specific Google Drive Folder
function getOrCreateFolder(folderName) {
  const folders = DriveApp.getFoldersByName(folderName);
  return folders.hasNext() ? folders.next() : DriveApp.createFolder(folderName);
}

function uploadConsent() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const loader = document.getElementById('loader');
  const successMsg = document.getElementById('successMsg');

  if (!file) {
    alert("Please select a file.");
    return;
  }

  loader.style.display = "block"; // Show loader

  const reader = new FileReader();
  reader.onload = function(event) {
    const fileData = {
      name: file.name,
      type: file.type,
      content: event.target.result
    };

    google.script.run.withSuccessHandler(() => {
      loader.style.display = "none"; // Hide loader
      successMsg.style.display = "block"; // Show success

      setTimeout(() => {
        google.script.host.close(); // ✅ Close modal
      }, 1500);
    }).handleSupplierConsentUpload(fileData);
  };

  reader.readAsDataURL(file);
}



// ✅ Sends Email Notification After File Upload
function sendEmailNotification(fileName, fileUrl) {
  const recipient = 'krishnamadhurama@gmail.com'; // ✅ Replace with your email
  const subject = 'New File Uploaded';
  const body = `A new file has been uploaded:\n\n- File Name: ${fileName}\n- File URL: ${fileUrl}`;

  GmailApp.sendEmail(recipient, subject, body);
}
