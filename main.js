/*jshint esversion: 8 */
const puppeteer = require("puppeteer");
const fs = require('fs');

const InitializeBrowser = async (_) => {
    const browser = await puppeteer.launch({
        // headless: false,
        devtools: false,
    });
    const page = await browser.newPage();

    return page;
};

const navigateToPublishersPage = async (page) => {
    await page.goto("http://paineira.usp.br/festadolivro/");
};

const getPublishersLinks = async (page) => await page.$$eval("a.bwg-a", (links) =>
    links.map((link) => link.getAttribute("href"))
);

const getDriverLink = async (page) => await page.$$eval("div > p > a", (links) => {
    for (link of links) {
        let url = link.getAttribute("href")
        if (url.includes('drive.google')) return url;
    }
}
);

const run_scrapping = async _ => {
    const page = await InitializeBrowser();

    await navigateToPublishersPage(page);

    const links = await getPublishersLinks(page);
    const wrongs = [];

    for (let i = 0; i < links.length; i++) {
        try {
            await page.goto(links[i]);
            page.waitForNavigation({ waitUntil: 'networkidle0' });
            let title = await page.$eval('header > h1.entry-title', el => el.textContent);

            let DriverLink = await getDriverLink(page);
            links[i] = [links[i], title, DriverLink]

            console.log(DriverLink);
            if (DriverLink == undefined)
                wrongs.push(links[i][0]);

            await page.goto(DriverLink);
            page.waitForNavigation({ waitUntil: 'networkidle0' });

        } catch (e) {
            wrongs.push(links[i]);
        }
    }

    fs.writeFile("temp2.txt", JSON.stringify([...links, 'Errados', ...wrongs]), (err) => {
        if (err) console.log(err);
        console.log("Successfully Written to File.");
    });
    console.log(wrongs);
    console.log(links.length);
};

run_scrapping();