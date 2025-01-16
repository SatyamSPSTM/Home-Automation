function addDevice() {
    var deviceInput = document.getElementById('deviceInput');
    var deviceName = deviceInput.value.trim();
  
    if (deviceName === '') {
      alert('Please enter a device name.');
      return;
    }
  
    var deviceList = document.getElementById('deviceList');
    var listItem = document.createElement('li');
    listItem.textContent = deviceName;
  
    var removeButton = document.createElement('button');
    removeButton.textContent = 'Remove';
    removeButton.onclick = function() {
      listItem.remove();
    };
  
    listItem.appendChild(removeButton);
    xc.appendChild(listItem);
  
    deviceInput.value = ''; // Clear input field after adding device
  }
  