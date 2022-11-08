fs = require('fs');

var gplay = require('google-play-scraper');
var store = require('app-store-scraper');

var g_apps = [], a_apps = [];

function saveApps(filename, apps) {
    fs.writeFile(filename, JSON.stringify(apps, null, 4), function(err) {
        if (err) {
            return console.log(err);
        }

        console.log(filename + ' saved.');
    });
}

function getGoogleApps() {
    var start = new Date().getTime();

    var categories = Object.values(gplay.category);
    var collections = Object.values(gplay.collection);

    var responses = [];

    categories.forEach(function(category) {
        collections.forEach(function(collection) {
            var response = gplay.list({
                category: category,
                collection: collection,
                num: 1000
            });
    
            responses.push(response);
        });
    });
    
    Promise.allSettled(responses).then(function(results) {    
        results.forEach(function(result) {
            if (result.status === 'fulfilled') {
                result.value.forEach(function(app) {
                    g_apps.push(app);
                });
            }
        });

        var end = new Date().getTime();

        console.log('Found ' + g_apps.length + ' apps.');
        console.log('Time: ' + (end - start) / 1000 + 's');

        saveApps('data/gplay_apps.json', g_apps);
    });
}

function getAppleApps() {
    var start = new Date().getTime();

    var categories = Object.values(store.category);
    var collections = Object.values(store.collection);

    var responses = [];

    categories.forEach(function(category) {
        collections.forEach(function(collection) {
            var response = store.list({
                category: category,
                collection: collection,
                num: 200
            });
    
            responses.push(response);
        });
    });

    Promise.allSettled(responses).then(function(results) {    
        results.forEach(function(result) {
            if (result.status === 'fulfilled') {
                result.value.forEach(function(app) {
                    a_apps.push(app);
                });
            }
        });

        var end = new Date().getTime();

        console.log('Found ' + a_apps.length + ' apps.');
        console.log('Time: ' + (end - start) / 1000 + 's');

        saveApps('data/apple_apps.json', a_apps);
    });
}

getGoogleApps();
getAppleApps();
