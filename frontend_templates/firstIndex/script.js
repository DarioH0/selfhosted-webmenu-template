function showContainer2() {
    fetch('/api/v1/failed_imports')
        .then(response => response.json())
        .then(data => {
            var titleElement = document.querySelector('.container1 h1');
            var subtitleElement = document.querySelector('.container1 .subtitle');
            document.querySelector('.btn1').style.display = 'none'

            if (data.length > 0) {
                titleElement.innerText = 'some modules are missing';
                subtitleElement.innerText = 'the app can\'t work without the necessary modules!\nrestart the script after you\'ve installed them:';
                
                var moduleList = document.createElement('ul');
                moduleList.id = 'moduleList';

                data.forEach(module => {
                    var listItem = document.createElement('li');
                    listItem.innerText = module;
                    moduleList.appendChild(listItem);
                });

                // Replace existing moduleList or append if it doesn't exist
                var existingModuleList = document.getElementById('moduleList');
                if (existingModuleList) {
                    existingModuleList.replaceWith(moduleList);
                } else {
                    subtitleElement.parentNode.appendChild(moduleList);
                }
            } else {
                // If no failed imports, display a placeholder message
                titleElement.innerText = 'this is a placeholder scene.';
                subtitleElement.innerText = 'you can refresh to visit the webmenu';

                var existingModuleList = document.getElementById('moduleList');
                if (existingModuleList) {
                    existingModuleList.remove();
                }
            }
        })
        .catch(error => console.error('Error:', error));
}

