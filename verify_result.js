
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

// Run calculation
app.calculate();

// Get results
const data = app.data;

// Load expected results
const expected = JSON.parse(fs.readFileSync('results_before.json', 'utf8'));

// Compare
let errors = 0;
if (data.total !== expected.total) {
    console.error(`Total mismatch: ${data.total} vs ${expected.total}`);
    errors++;
}

if (data.results.length !== expected.results.length) {
    console.error(`Results length mismatch`);
    errors++;
} else {
    data.results.forEach((r, i) => {
        const e = expected.results[i];
        if (r.id !== e.id || r.name !== e.name || r.votes !== e.votes) {
             console.error(`Row ${i} basics mismatch`);
             errors++;
        }
        if (r.hareSeats !== e.hareSeats) {
             console.error(`Row ${i} hareSeats mismatch: ${r.hareSeats} vs ${e.hareSeats}`);
             errors++;
        }
        if (r.sainteLagueSeats !== e.sainteLagueSeats) {
             console.error(`Row ${i} slSeats mismatch: ${r.sainteLagueSeats} vs ${e.sainteLagueSeats}`);
             errors++;
        }
        if (r.passed !== e.passed) {
             console.error(`Row ${i} passed mismatch`);
             errors++;
        }
    });
}

// Compare steps
if (data.steps.length !== expected.steps.length) {
    console.error(`Steps length mismatch`);
    errors++;
} else {
    // Check first and last step
    const checkStep = (idx) => {
        const s = data.steps[idx];
        const es = expected.steps[idx];
        if (s.winner !== es.winner || s.winnerQuotient !== es.winnerQuotient) {
             console.error(`Step ${idx} mismatch`);
             errors++;
        }
        // Check deep equality of quotients
        if (JSON.stringify(s.quotients) !== JSON.stringify(es.quotients)) {
             console.error(`Step ${idx} quotients mismatch`);
             // console.log('Got:', JSON.stringify(s.quotients));
             // console.log('Exp:', JSON.stringify(es.quotients));
             errors++;
        }
    };
    if (data.steps.length > 0) {
        checkStep(0);
        checkStep(data.steps.length - 1);
    }
}

if (errors === 0) {
    console.log('Verification PASSED: Results are identical.');
} else {
    console.error(`Verification FAILED with ${errors} errors.`);
    process.exit(1);
}
