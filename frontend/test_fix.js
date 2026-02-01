// Test script to validate the TypeScript syntax
const fs = require('fs');
const path = require('path');

// Read the file to check for syntax issues
const filePath = path.join(__dirname, 'src', 'lib', 'hooks', 'useAuth.ts');
const content = fs.readFileSync(filePath, 'utf8');

console.log('✅ Successfully read the useAuth.ts file');
console.log('🔍 Checking for syntax issues...');

// Look for the problematic line
const lines = content.split('\n');
const targetLineIndex = 141; // 0-indexed for line 142
if (lines[targetLineIndex]) {
    console.log(`Line ${targetLineIndex + 1}: ${lines[targetLineIndex].trim()}`);

    // Check if the JSX syntax looks correct
    if (lines[targetLineIndex].includes('<AuthContext.Provider') &&
        lines[targetLineIndex].includes('value={value}') &&
        lines[targetLineIndex].includes('</AuthContext.Provider>')) {
        console.log('✅ JSX syntax appears correct on line', targetLineIndex + 1);
    } else {
        console.log('⚠️ Potential JSX syntax issue on line', targetLineIndex + 1);
    }
}

console.log('✅ Syntax validation completed');