const { chromium } = require('playwright');

(async () => {
  // Launch the browser
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const searchQuery = process.argv[2] ? process.argv[2] : 'Default Search Query';

  // Navigate to a website
  await page.goto('https://google.com');

  await page.fill('textarea[name="q"]', searchQuery);
  await page.press('textarea[name="q"]','Enter');

  await page.waitForSelector('div.byrV5b');

  /// Collect all divs with the class 'byrV5b' and extract URLs from their content
  const urls = await page.$$eval('div.byrV5b', divs => {
    // Define a regular expression to match URLs
    const urlRegex = /https?:\/\/[^\s]+/g;

    return divs.flatMap(div => {
      // Use the regular expression to find all URLs in the inner HTML of the div
      const urls = div.innerHTML.match(urlRegex) || [];
      return urls.filter(
        url => !url.includes('<span') && 
        !url.includes('</cite>') && 
        !url.includes('/svg'))
        .map(url => url.replace(/["']+$/, ''));
    });
  });

  console.log(JSON.stringify(urls, null, 2));


  // Wait for the search results page to load;

  // Close the browser
  await browser.close();
})();
