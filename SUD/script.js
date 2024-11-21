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
  await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle' }), // Wait for navigation to finish
    page.press('textarea[name="q"]', 'Enter'), // Trigger the search
  ]);

  try {
    // Navigate to a website

    // Wait for the elements to be available in the DOM
    await page.waitForSelector('.VwiC3b.yXK7lf.lVm3ye.r025kc.hJNv6b, div.byrV5b', { state: 'attached' });

    // Use Promise.all to execute both extractions concurrently
    const [extractedTexts, urls] = await Promise.all([
      // Extract text from span elements within divs with the specified class
      page.$$eval('.VwiC3b.yXK7lf.lVm3ye.r025kc.hJNv6b span', spans =>
        spans.map(span => span.textContent.trim())
      ),
      // Collect all divs with the class 'byrV5b' and extract URLs from their content
      page.$$eval('div.byrV5b', divs => {
        const urlRegex = /https?:\/\/[^\s]+/g;
        return divs.flatMap(div => {
          const urls = div.innerHTML.match(urlRegex) || [];
          return urls.filter(url => !url.includes('<span') && !url.includes('</cite>') && !url.includes('/svg'))
            .map(url => url.replace(/["']+$/, ''));
        });
      })
    ]);

    // Filter function to remove unwanted text patterns
    function filterText(text) {
      const patternsToRemove = [
        /\b\d+ hours ago\b/, // Matches '4 hours ago'
        /\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}\b/, // Matches any date in the format 'Mar 8, 2024'
        /Appeared in the.*edition as .*/, // Matches long descriptive texts
        /\b\d+ hour ago\b/ // Matches 'some hours ago.'
      ];
      for (const pattern of patternsToRemove) {
        text = text.replace(pattern, '');
      }
      return text.trim(); // Trim to remove any leading/trailing whitespace left after replacements
    }

    // Interleave the results and filter them
    const interleavedFilteredResults = [];
    const maxLength = Math.max(extractedTexts.length, urls.length);
    for (let i = 0; i < maxLength; i++) {
      if (i < urls.length) interleavedFilteredResults.push(`URL ${i + 1}: ${urls[i]}`);
      if (i < extractedTexts.length) interleavedFilteredResults.push(`Text ${i + 1}: ${filterText(extractedTexts[i])}`);
    }

    console.log(JSON.stringify(interleavedFilteredResults, null, 2));

  } catch (error) {
    console.error('An error occurred:', error.message);
  } finally {
    // Close the browser
    await browser.close();
  }
})();
