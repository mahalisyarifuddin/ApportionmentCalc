
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
                setAttribute: (attr, val) => {
                    domElements[id].attributes = domElements[id].attributes || {};
                    domElements[id].attributes[attr] = val;
                },
                matches: () => false,
                options: [ // Mock options for select
                    { value: 'auto', textContent: '' },
                    { value: 'light', textContent: '' },
                    { value: 'dark', textContent: '' }
                ],
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

// --- Test setLanguage Refactor ---
console.log('Testing setLanguage...');

// Set language to ID
app.setLanguage('id');

// Verify updates
const addBtn = document.getElementById('add');
// "add" key in id text is "+ Tambah Partai"
if (addBtn.textContent !== '+ Tambah Partai') {
    console.error(`FAILED: 'add' button text not updated. Expected '+ Tambah Partai', got '${addBtn.textContent}'`);
    process.exit(1);
}

const themeSelect = document.getElementById('theme');
if (themeSelect.options[0].textContent !== 'Tema Otomatis') {
    console.error(`FAILED: theme option not updated. Expected 'Tema Otomatis', got '${themeSelect.options[0].textContent}'`);
    process.exit(1);
}

const closeBtn = document.getElementById('close');
if (closeBtn.attributes['aria-label'] !== 'Tutup Modal') {
    console.error(`FAILED: close button aria-label not updated. Expected 'Tutup Modal', got '${closeBtn.attributes['aria-label']}'`);
    process.exit(1);
}

console.log('setLanguage verification PASSED');
