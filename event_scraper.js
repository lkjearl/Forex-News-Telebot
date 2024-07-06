const puppeteer = require('puppeteer');
const fs = require('fs');

async function scrapeUpcomingEvents() {
  const browser = await puppeteer.launch({
    headless: "new",
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-extensions',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--incognito', // Enable incognito mode
    ],
  });
  const page = await browser.newPage();

  await page.setUserAgent(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
  );

  try {
    await page.goto('https://www.forexfactory.com/calendar?day=today');

    const eventData = await page.evaluate(() => {
      const events = [];
      const rows = document.querySelectorAll('table.calendar__table tbody tr[data-event-id]');
      let previousTiming = ''; // Variable to store the timing of the previous event
      let prevPrevTiming = ''; // Variable to store the timing of the previous previous event

      rows.forEach((row) => {
        const impactCell = row.querySelector('.calendar__impact span');
        const timeCell = row.querySelector('.calendar__time');
        const currencyCell = row.querySelector('.calendar__currency');
        const eventCell = row.querySelector('.calendar__event');

        const impact = impactCell ? impactCell.getAttribute('title') : '';
        let time = timeCell ? timeCell.textContent : '';

        // Use the timing of the previous event if it's available
        if (!time && previousTiming) {
          time = previousTiming;
        } else if (!time && prevPrevTiming) {
          time = prevPrevTiming;
        }

        // Update the previousTiming variable with the timing of the current event
        prevPrevTiming = previousTiming;
        previousTiming = time;

        const currency = currencyCell ? currencyCell.textContent : '';
        const event = eventCell ? eventCell.textContent : '';

        if (impact === 'High Impact Expected' || impact === 'Medium Impact Expected') {
          events.push({ impact, time, currency, event });
        }
      });

      return events;
    });

    fs.writeFileSync('upcoming_events.txt', JSON.stringify(eventData, null, 2));
    console.log('Upcoming events scraped successfully.');

  } catch (error) {
    console.error('An error occurred during scraping:', error);
  } finally {
    await browser.close();
  }
}

if (require.main === module) {
  scrapeUpcomingEvents();
}
