
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
// We replace the last line to expose the instance
const modifiedJs = js.replace('new ApportionmentCalc();', 'global.appInstance = new ApportionmentCalc();');
eval(modifiedJs);

const app = global.appInstance;

// Setup inputs
document.getElementById('seats').value = '10';
document.getElementById('threshold').value = '4';

// Initial state
console.log('Initial parties:', app.parties.length);

// Run calculation
app.calculate();

// Check results
const data = app.data;
console.log('Total votes:', data.total);
console.log('Seats:', data.seats);
console.log('Threshold:', data.threshold);

// Capture full results for comparison
const resultsBefore = JSON.stringify(data, null, 2);
fs.writeFileSync('results_before.json', resultsBefore);

console.log('Results saved to results_before.json');
