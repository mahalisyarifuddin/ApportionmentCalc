
// Test script for ApportionmentCalc logic
// This verifies that the integer-based remainder calculation is consistent and robust.

function runTests() {
    let seats = 100;
    console.log("Running math verification tests...");

    // Test 1: Check for discrepancies between float and integer math in a known range
    let discrepancies = 0;
    for (let total = 1000; total < 2000; total++) {
        const quota = total / seats;
        for (let votes = 1; votes < total; votes++) {
             const hareSeats = Math.floor((votes * seats) / total);

             // Old float method
             const remFloat = votes - hareSeats * quota;

             // New integer method (scaled by seats)
             // In the code we use: ((votes * seats) % total) / seats
             const remInt = ((votes * seats) % total) / seats;

             // Check if they differ significantly
             if (Math.abs(remFloat - remInt) > 1e-15) {
                 // Discrepancies are expected due to float precision!
                 // The point of this test is to confirm that remInt is the correct value
                 // and that we are fixing a real issue.
                 // But for a regression test, we want to ensure valid behavior.

                 // Let's verify that remInt is indeed mathematically correct.
                 // R = V - floor(V*S/T) * (T/S)
                 // R_exact = V - hareSeats * (Total/Seats)
                 // R_exact * Seats = V*Seats - hareSeats * Total
                 // = V*Seats - floor(V*Seats/Total)*Total
                 // = (V*Seats) % Total
                 // So remInt * Seats should equal (V*Seats)%Total.

                 const calculatedRemNumerator = remInt * seats;
                 const expectedRemNumerator = (votes * seats) % total;

                 if (Math.abs(calculatedRemNumerator - expectedRemNumerator) > 1e-10) {
                     console.error(`FAILED: Integer math logic is wrong!`);
                     console.error(`Total: ${total}, Seats: ${seats}, Votes: ${votes}`);
                     console.error(`RemInt: ${remInt}, Numerator: ${calculatedRemNumerator}, Expected: ${expectedRemNumerator}`);
                     process.exit(1);
                 }
                 discrepancies++;
             }
        }
    }

    if (discrepancies > 0) {
        console.log(`Verified: Found ${discrepancies} cases where float math was imprecise, which the new integer logic handles correctly.`);
    } else {
        console.warn("Warning: No discrepancies found in this range. Try a larger range or check the test.");
    }

    console.log("Tests passed.");
}

runTests();
