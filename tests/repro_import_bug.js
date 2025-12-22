const puppeteer = require('puppeteer');
const { expect } = require('chai');
const path = require('path');
const fs = require('fs');

describe('ApportionmentCalc Import Bug', function () {
  this.timeout(30000);

  let browser;
  let page;
  const tempCsvPath = path.resolve(__dirname, 'temp_test.csv');

  before(async () => {
    browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
    page = await browser.newPage();
    const filePath = path.resolve(__dirname, '../ApportionmentCalc.html');
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });
  });

  after(async () => {
    await browser.close();
    if (fs.existsSync(tempCsvPath)) {
      fs.unlinkSync(tempCsvPath);
    }
  });

  it('should not map Name and Votes to the same column if a column header matches both keywords', async () => {
    // Create a CSV where one header matches both "Party" and "Votes"
    // e.g., "Party Votes"
    // And another column that is just "ID" or something.
    // If logic is flawed, it might pick "Party Votes" for both Name and Votes.

    // We want "Party Name" and "Number of Votes".
    // "Party Name" matches "party".
    // "Number of Votes" matches "vote".
    // This should work fine.

    // But consider: "Party Votes" and "Something Else"
    // "Party Votes" matches 'party' and 'vote'.
    // Logic:
    // name: findIndex(... 'party' ...) -> 0
    // votes: findIndex(... 'vote' ...) -> 0

    // So both map to column 0.

    const csvContent = 'Party Votes,ID\nParty A 100,1\nParty B 200,2';
    fs.writeFileSync(tempCsvPath, csvContent);

    // Upload the file
    const fileInput = await page.$('#file');
    await fileInput.uploadFile(tempCsvPath);

    // Wait for parties to update
    // We expect 2 parties.
    // If it maps both to col 0:
    // Row 1: "Party A 100". Name="Party A 100", Votes=100.
    // Row 2: "Party B 200". Name="Party B 200", Votes=200.

    // This actually effectively works, but it's weird.

    // What if the column content is NOT numbers?
    // "Party Name, Comments"
    // "Party A, Great party"
    // "Party B, Bad party"

    // "Party Name" matches 'party'.
    // If we have "Party Votes" as header for the name column?
    // csvContent: "Party Votes,Real Votes\nParty A,100\nParty B,200"

    // Header 0: "Party Votes". Matches 'party' -> name=0. Matches 'vote' -> votes=0.
    // Header 1: "Real Votes". Matches 'vote' -> votes=1 (findIndex finds first match?)

    // findIndex finds the FIRST match.
    // So votes will also be 0.

    // So it reads name from Col 0 ("Party A")
    // And votes from Col 0 ("Party A") -> parseInt("Party A") -> NaN -> 0.

    // So parties will have 0 votes.
    // But the file HAS a "Real Votes" column.

    const badCsvContent = 'Party Votes,Real Votes\nParty A,100\nParty B,200';
    fs.writeFileSync(tempCsvPath, badCsvContent);

    await fileInput.uploadFile(tempCsvPath);

    // Check parties in the list
    const votes = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('.party-row input[type="number"]')).map(el => el.value);
    });

    console.log('Votes:', votes);

    // If bug exists, votes will be ['0', '0'].
    // If fixed, votes should be ['100', '200'].

    expect(votes).to.deep.equal(['100', '200']);
  });
});
