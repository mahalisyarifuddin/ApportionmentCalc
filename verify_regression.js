
const fs = require('fs');

// Mock DOM
const domElements = {};
const document = {
    getElementById: (id) => {
        if (!domElements[id]) {
            domElements[id] = {
                value: '',
                textContent: '',
                classList: {
                    toggle: () => {},
                    contains: () => false,
                    add: () => {},
                    remove: () => {}
                },
                disabled: false,
                children: [],
                lastElementChild: null,
                innerHTML: '',
                focus: () => {},
                setAttribute: () => {},
                matches: () => false,
                options: [],
                click: () => {}
            };
        }
        return domElements[id];
    },
    documentElement: { lang: 'en', className: '' },
    createElement: () => ({ click: () => {} }),
    onkeydown: null
};
const navigator = { language: 'en' };
const window = {
    confirm: () => true,
    URL: { createObjectURL: () => '' },
    Blob: class {},
    FileReader: class {
        readAsText() {}
    }
};

global.document = document;
global.navigator = navigator;
global.window = window;
global.confirm = window.confirm;
global.URL = window.URL;
global.Blob = window.Blob;
global.FileReader = window.FileReader;

// Extract JS from HTML
const html = fs.readFileSync('ApportionmentCalc.html', 'utf8');
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];

// Run the code
const modifiedJs = js.replace('new ApportionmentCalc();', 'global.appInstance = new ApportionmentCalc();');
eval(modifiedJs);

const app = global.appInstance;

// Setup inputs
document.getElementById('seats').value = '10';
document.getElementById('threshold').value = '4';

// Run 1: Normal calculation
console.log('--- Run 1 ---');
app.calculate();
const apple = app.data.results.find(p => p.name === 'Apple Party');
console.log('Apple Party Seats:', apple.hareSeats);
if (apple.hareSeats === 0) {
    console.error('Apple Party should have seats in Run 1');
    process.exit(1);
}

// Modify votes to make Apple Party fail threshold
// Total votes 55500. Threshold 4% = 2220.
// Apple has 25000.
// Let's set Apple votes to 100.
console.log('--- Modifying votes ---');
const appleParty = app.parties.find(p => p.name === 'Apple Party');
appleParty.votes = 100;

// Run 2: Apple Party fails threshold
console.log('--- Run 2 ---');
app.calculate();
const apple2 = app.data.results.find(p => p.name === 'Apple Party');
const total2 = app.data.total;
const thresholdVotes2 = app.data.thresholdVotes;
console.log(`Total: ${total2}, ThresholdVotes: ${thresholdVotes2}`);
console.log(`Apple Votes: ${apple2.votes}`);
console.log(`Apple Passed: ${apple2.passed}`);
console.log(`Apple Hare Seats: ${apple2.hareSeats}`);

// Check for regression
if (!apple2.passed && apple2.hareSeats > 0) {
    console.error('REGRESSION: Apple Party failed threshold but has seats!');
    console.error('Stale state detected.');
    process.exit(1);
}

if (apple2.hareSeats === 0) {
    console.log('Verification PASSED: No stale state.');
}
