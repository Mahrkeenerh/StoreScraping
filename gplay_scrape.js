fs = require('fs');
let gplay = require('google-play-scraper');


let devs = [];
let app_ids = [];
let apps = [];


async function timed(func) {
    let start = new Date().getTime();

    await func();

    let end = new Date().getTime();

    console.log('Time: ' + (end - start) / 1000 + 's');
}


async function getGeneralApps() {
    let categories = Object.values(gplay.category);
    let collections = Object.values(gplay.collection);

    let responses = [];

    for (let category of categories) {
        for (let collection of collections) {
            let response = gplay.list({
                category: category,
                collection: collection,
                num: 1000
            });

            responses.push(response);
        }
    }

    let results = await Promise.allSettled(responses);

    for (let result of results) {
        if (result.status === 'fulfilled') {
            for (let app of result.value) {
                let app_id = app.appId;
                let dev = app.developer;

                if (!app_ids.includes(app_id)) {
                    app_ids.push(app_id);
                }
                if (!devs.includes(dev)) {
                    devs.push(dev);
                }
            }
        }
    }
}


async function getDeveloperApps() {
    let solved_devs = 0;

    for (let i = 0; i < devs.length; i += 250) {
        let dev_group = devs.slice(i, i + 250);
        let dev_responses = [];

        for (let dev of dev_group) {
            let response = gplay.developer({
                devId: dev,
                num: 1000
            });

            dev_responses.push(response);
        }

        let dev_results = await Promise.allSettled(dev_responses);

        for (let result of dev_results) {
            if (result.status === 'fulfilled') {
                for (let app of result.value) {
                    let app_id = app.appId;

                    if (!app_ids.includes(app_id)) {
                        app_ids.push(app_id);
                    }
                }
            }
        }

        solved_devs += dev_group.length;
        console.log('Solved ' + solved_devs + ' devs. ' + 'Unique apps: ' + app_ids.length);
    }
}


async function getSpecificApps() {
    let solved_apps = 0;

    for (let i = 0; i < app_ids.length; i += 10000) {
        apps = [];

        for (let j = i; j < i + 10000; j += 250) {
            let app_group = app_ids.slice(j, j + 250);
            let app_responses = [];

            for (let app_id of app_group) {
                let response = gplay.app({
                    appId: app_id
                });

                app_responses.push(response);
            }

            let app_results = await Promise.allSettled(app_responses);

            for (let result of app_results) {
                if (result.status === 'fulfilled') {
                    apps.push(result.value);
                }
            }

            solved_apps += app_group.length;
            console.log('Solved ' + solved_apps + ' apps. ' + 'Apps: ' + apps.length);
        }

        fs.writeFile('gplay/apps_' + i / 10000 + '.json', JSON.stringify(apps, null, 4), function (err) {
            if (err) throw err;
            console.log('Saved ' + i / 10000);
        });
    }
}


async function main() {
    await timed(getGeneralApps);

    console.log('Unique apps: ' + app_ids.length);
    console.log('Unique devs: ' + devs.length);

    await timed(getDeveloperApps);

    console.log('Unique apps: ' + app_ids.length);

    await timed(getSpecificApps);
}

(async () => {
    await main();
})();
