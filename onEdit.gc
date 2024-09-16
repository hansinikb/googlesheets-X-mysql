function onEdit(e) {
  Logger.log("onEdit triggered");

  if (!e) {
    Logger.log("No event object.");
    return;
  }

  var sheet = e.source.getActiveSheet();   // Get the active sheet
  var row = e.range.getRow();              // Get the row number of the edited cell
  var lastColumn = sheet.getLastColumn();  // Get the last column number of the sheet
  var range = sheet.getRange(row, 1, 1, lastColumn);  // Get the entire row (from the first column to the last)
  var values = range.getValues();  // Get the values of the entire row

  // Log the values to verify what's being sent
  Logger.log("Edited row values: " + JSON.stringify(values));

  // Create a JSON object with the row number and the entire row's values
  var payload = {
    "row": row,
    "values": values  // Send the entire row of values
  };

  // Check if the entire row is empty (i.e., if the user added a new row without content yet)
  var rowEmpty = true;
  for (var i = 0; i < values[0].length; i++) {
    if (values[0][i] !== "") {
      rowEmpty = false;
      break;
    }
  }

  // If the row is not empty, send the data to the Flask server
  if (!rowEmpty) {
    sendToDatabase(payload);
  }
}

// Function to send data to the Flask server
function sendToDatabase(payload) {
  var options = {
    'method' : 'post',
    'contentType': 'application/json',  // Set Content-Type to JSON
    'payload' : JSON.stringify(payload)  // Convert the payload to a JSON string
  };

  // Send the request to your Flask server
  try {
    var response = UrlFetchApp.fetch('https://d933-2401-4900-1cb9-8539-24c4-146a-a7b0-f433.ngrok-free.app/update-database', options);
    Logger.log("Response from server: " + response.getContentText());
  } catch (err) {
    Logger.log("Error occurred: " + err.toString());
  }
}
